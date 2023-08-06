use cpython::{
    NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyResult, PyTuple, Python, PythonObject,
    ToPyObject,
};
use httparse::{self};
use log::{debug, error};
use std::net::SocketAddr;
use std::sync::Arc;
use urlencoding::decode;

use crate::globals::WSGIGlobals;
use crate::response::WSGIResponse;

// https://tools.ietf.org/html/rfc7230#section-3.2
// Each header field consists of a case-insensitive field name ...
pub const CONTENT_LENGTH_HEADER: &str = "content-length";
const CONTENT_TYPE_HEADER: &str = "content-type";
const CONTENT_TYPE: &str = "CONTENT_TYPE";
const REQUEST_METHOD: &str = "REQUEST_METHOD";
const PATH_INFO: &str = "PATH_INFO";
const QUERY_STRING: &str = "QUERY_STRING";
const SERVER_PROTOCOL: &str = "SERVER_PROTOCOL";

pub struct WSGIRequest {
    pub data: Vec<u8>,
    pub body: Vec<u8>,
    pub complete: bool,
    pub content_length: usize,
    pub http_headers: Vec<(String, String)>,
    pub peer_addr: Option<SocketAddr>,
    pub response: Arc<Option<WSGIResponse>>,
    num_headers: usize,
}

impl WSGIRequest {
    pub fn new(num_headers: usize) -> WSGIRequest {
        WSGIRequest {
            data: Vec::new(),
            body: Vec::new(),
            complete: false,
            content_length: 0,
            http_headers: Vec::new(),
            peer_addr: None,
            response: Arc::new(None),
            num_headers,
        }
    }

    #[inline]
    pub fn append(&mut self, data: &[u8]) {
        self.data.append(&mut data.to_vec());
    }

    pub fn parse_headers(&mut self) -> bool {
        let mut headers = vec![httparse::EMPTY_HEADER; self.num_headers];
        let mut req = httparse::Request::new(&mut headers);
        if let Ok(res) = req.parse(&self.data) {
            if let httparse::Status::Complete(size) = res {
                self.complete = true;
                let length = self.data.len();
                self.content_length = length - size;
                let mut parse_error = false;
                for header in req.headers.iter() {
                    match header.name.to_lowercase().as_str() {
                        CONTENT_LENGTH_HEADER => {
                            if let Ok(val) = std::str::from_utf8(header.value) {
                                if let Ok(parsedval) = val.parse() {
                                    self.content_length = parsedval;
                                }
                            }
                        }
                        &_ => {
                            let key = if header.name.to_lowercase().as_str() == CONTENT_TYPE_HEADER
                            {
                                CONTENT_TYPE.to_string()
                            } else {
                                let mut key = "HTTP_".to_string();
                                key.push_str(&header.name.to_ascii_uppercase().replace("-", "_"));
                                key
                            };
                            match String::from_utf8(header.value.to_vec()) {
                                Ok(val) => self.http_headers.push((key, val)),
                                Err(e) => {
                                    error!("{:?} encountered for value: {:?}", e, header.value);
                                    parse_error = true;
                                }
                            }
                        }
                    }
                }
                if self.content_length > 0 {
                    if self.content_length > length - size {
                        self.complete = false;
                    } else {
                        self.body
                            .extend_from_slice(&self.data[size..size + self.content_length]);
                    }
                }
                if let Some(method) = req.method {
                    self.http_headers
                        .push((REQUEST_METHOD.to_string(), method.to_string()));
                }
                if let Some(path) = req.path {
                    match decode(path) {
                        Ok(decoded) => {
                            let parts: Vec<&str> = decoded.split('?').collect();
                            self.http_headers
                                .push((PATH_INFO.to_string(), parts[0].to_string()));
                            if parts.len() > 1 {
                                self.http_headers
                                    .push((QUERY_STRING.to_string(), parts[1].to_string()));
                            } else {
                                self.http_headers
                                    .push((QUERY_STRING.to_string(), "".to_string()));
                            }
                        }
                        Err(e) => {
                            error!("Could not urldecode path info: {:?}", e);
                            parse_error = true;
                        }
                    }
                }
                if let Some(version) = req.version {
                    if version > 1 {
                        error!("Unsupported version: {:?}", version);
                        parse_error = true;
                    } else {
                        let protocol = format!("HTTP/1.{}", version);
                        self.http_headers
                            .push((SERVER_PROTOCOL.to_string(), protocol));
                    }
                }
                return !parse_error;
            }
        }
        false
    }

    pub fn wsgi_environ(&self, globals: &WSGIGlobals, py: Python) -> PyResult<PyDict> {
        let io = &globals.io_module;
        let sys = &globals.sys_module;
        let environ = PyDict::new(py);
        for (k, v) in self.http_headers.iter() {
            environ.set_item(py, k, v)?;
        }
        environ.set_item(py, "SERVER_NAME", format!("{}", globals.server_info.ip()))?;
        environ.set_item(py, "SERVER_PORT", format!("{}", globals.server_info.port()))?;
        // XXX the following item needs to be set properly
        environ.set_item(py, "SCRIPT_NAME", "")?;
        environ.set_item(
            py,
            "REMOTE_ADDR",
            match self.peer_addr {
                None => "".to_string(),
                Some(addr) => format!("{}", addr.ip()),
            },
        )?;
        let input = io.call(py, "BytesIO", NoArgs, None)?;
        let bodylen = self.body.len();
        if bodylen > 0 {
            environ.set_item(py, "CONTENT_LENGTH", bodylen)?;
            input.call_method(
                py,
                "write",
                PyTuple::new(
                    py,
                    &[PyBytes::new(py, &self.body[..]).as_object().clone_ref(py)],
                ),
                None,
            )?;
            input.call_method(
                py,
                "seek",
                PyTuple::new(py, &[(0 as i32).to_py_object(py).as_object().clone_ref(py)]),
                None,
            )?;
        }
        environ.set_item(py, "wsgi.input", input)?;
        environ.set_item(py, "wsgi.errors", sys.get(py, "stderr")?)?;
        environ.set_item(py, "wsgi.version", (1, 0))?;
        environ.set_item(py, "wsgi.multithread", false)?;
        environ.set_item(py, "wsgi.multiprocess", true)?;
        environ.set_item(py, "wsgi.run_once", false)?;
        environ.set_item(py, "wsgi.url_scheme", "http")?;
        if let Some(wsgi) = &globals.wsgi_module {
            debug!("Setting FileWrapper in environ");
            environ.set_item(py, "wsgi.file_wrapper", wsgi.get(py, "FileWrapper")?)?;
        }
        Ok(environ)
    }

    #[inline]
    pub fn get_response(&mut self) -> Option<&mut WSGIResponse> {
        if let Some(opt) = Arc::get_mut(&mut self.response) {
            if let Some(resp) = opt {
                return Some(resp);
            }
        }
        None
    }
}

#[cfg(test)]
mod tests {
    use cpython::{NoArgs, ObjectProtocol, PyBytes, PyClone, PyString, Python, PythonObject};
    use log::debug;
    use std::net::SocketAddr;
    use std::sync::Arc;

    use crate::globals::WSGIGlobals;
    use crate::request::WSGIRequest;
    use crate::response::WSGIResponse;

    macro_rules! assert_header {
        ($got:ident, $py:ident, $key:literal, $value:expr) => {
            assert!(
                $got.get_item($py, $key)
                    .unwrap()
                    .extract::<PyString>($py)
                    .unwrap()
                    .to_string($py)
                    .unwrap()
                    == $value
            );
        };
    }

    #[test]
    fn test_get() {
        let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16);
        got.append(raw);
        got.parse_headers();
        assert!(got.http_headers.len() == 13);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                }
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_url_decode() {
        let raw = b"GET /foo%2042?bar=baz%20foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16);
        got.append(raw);
        got.parse_headers();
        assert!(got.http_headers.len() == 12);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo 42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz foo"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                }
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_error_url() {
        let raw = b"GET /foo 42?bar=baz foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16);
        got.append(raw);
        match got.parse_headers() {
            true => assert!(false),
            false => (),
        }
    }

    #[test]
    fn test_parse_body_once() {
        let raw = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2";
        let mut got = WSGIRequest::new(16);
        got.append(raw);
        got.parse_headers();
        assert!(got.complete);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(value, expected);
                }
                &_ => {}
            }
        }
        assert_eq!(&got.body[..], b"field1=value1&field2=value2");
    }

    #[test]
    fn test_parse_multiple() {
        let raw1 = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 41\r\n\r\nfield1=value1&field2=value2";
        let raw2 = b"&field3=value3";
        let mut got = WSGIRequest::new(16);
        got.append(raw1);
        got.parse_headers();
        assert!(!got.complete);
        assert!(got.content_length == 41);
        got.append(raw2);
        got.parse_headers();
        assert!(got.complete);
        assert!(got.content_length == 41);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(expected, value);
                }
                &_ => {}
            }
        }
        let expected = b"field1=value1&field2=value2&field3=value3";
        debug!("{:?}", got.body);
        assert!(got.body.iter().zip(expected.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_environ_dict() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut req = WSGIRequest::new(16);
        req.peer_addr = Some(SocketAddr::new("192.168.1.23".parse().unwrap(), 43567));
        req.append(raw);
        req.parse_headers();
        let got = req.wsgi_environ(&g, py).unwrap();
        assert_header!(got, py, "SERVER_NAME", "127.0.0.1");
        assert_header!(got, py, "SERVER_PORT", "7878");
        assert_header!(got, py, "SCRIPT_NAME", "");
        assert_header!(got, py, "REMOTE_ADDR", "192.168.1.23");
        assert_header!(got, py, "HTTP_COOKIE", "foo_language=en;");
        assert_header!(got, py, "PATH_INFO", "/foo42");
        assert_header!(got, py, "QUERY_STRING", "bar=baz");
        assert_header!(got, py, "HTTP_ACCEPT", "image/webp,*/*");
        assert_header!(
            got,
            py,
            "HTTP_ACCEPT_LANGUAGE",
            "de-DE,en-US;q=0.7,en;q=0.3"
        );
        assert_header!(got, py, "HTTP_ACCEPT_ENCODING", "gzip, deflate");
        assert_header!(got, py, "HTTP_AUTHORIZATION", "Basic YWRtaW46YWRtaW4=");
        assert_header!(got, py, "HTTP_CONNECTION", "keep-alive");
        assert_header!(got, py, "REQUEST_METHOD", "GET");
        assert_header!(got, py, "HTTP_HOST", "localhost:7878");
        assert_header!(
            got,
            py,
            "HTTP_USER_AGENT",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
        );
        assert_header!(got, py, "HTTP_DNT", "1");
        assert_header!(got, py, "SERVER_PROTOCOL", "HTTP/1.1");
    }

    #[test]
    fn test_post_simple_form() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2";
        let mut req = WSGIRequest::new(16);
        req.append(raw);
        req.parse_headers();
        let got = req.wsgi_environ(&g, py).unwrap();
        assert_header!(got, py, "CONTENT_TYPE", "application/x-www-form-urlencoded");
        let input = got
            .get_item(py, "wsgi.input")
            .unwrap()
            .as_object()
            .clone_ref(py);
        debug!("{:?}", input);
        let input = input.call_method(py, "read", NoArgs, None).unwrap();
        debug!("{:?}", input);
        assert!(input.extract::<PyBytes>(py).unwrap().data(py) == b"field1=value1&field2=value2");
    }
    #[test]
    fn test_get_response() {
        let mut req = WSGIRequest::new(16);
        match req.get_response() {
            None => (),
            _ => assert!(false),
        }
        let expected = b"Hello";
        let mut response = WSGIResponse::new();
        response.current_chunk = expected.to_vec();
        req.response = Arc::new(Some(response));
        match req.get_response() {
            Some(resp) => assert!(&resp.current_chunk == expected),
            _ => assert!(false),
        }
    }
}
