use cpython::{PyObject, Python};
use log::{debug, error};
use mio::net::{TcpListener, TcpStream};
use mio::{Events, Interest, Poll, Token};
use nix::fcntl::{fcntl, FcntlArg, FdFlag, OFlag};
use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};
use std::collections::HashMap;
use std::error;
use std::io::{self, Read};
use std::os::unix::io::AsRawFd;
use std::time::Duration;

use crate::globals::WSGIGlobals;
use crate::request::WSGIRequest;
use crate::workerpool::WorkerPool;
use crate::workers::{write_blocking_worker, write_non_blocking_worker};

pub const SERVER: Token = Token(0);
const READBUFSIZE: usize = 16384;
const POLL_TIMEOUT: u64 = 100;

type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

/// unset FD_CLOEXEC so we can pass
/// it to a worker without connection reset
#[inline]
fn unset_cloexec(connection: TcpStream) -> Result<TcpStream> {
    let flags = fcntl(connection.as_raw_fd(), FcntlArg::F_GETFD)?;
    let mut new_flags = FdFlag::from_bits(flags).expect("Could not set flags");
    new_flags.remove(FdFlag::FD_CLOEXEC);
    fcntl(connection.as_raw_fd(), FcntlArg::F_SETFD(new_flags))?;
    Ok(connection)
}

/// set a file descriptor into blocking mode
pub trait SetBlocking {
    fn set_blocking(&mut self) -> Result<()>;
}

impl SetBlocking for TcpStream {
    #[inline]
    fn set_blocking(&mut self) -> Result<()> {
        let flags = fcntl(self.as_raw_fd(), FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not set flags");
        new_flags.remove(OFlag::O_NONBLOCK);
        fcntl(self.as_raw_fd(), FcntlArg::F_SETFL(new_flags))?;
        Ok(())
    }
}

fn next(current: &mut Token) -> Token {
    let next = current.0;
    current.0 += 1;
    Token(next)
}

pub fn would_block(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::WouldBlock
}

pub struct Server {
    poll: Poll,
    events: Events,
    listener: TcpListener,
    workers: WorkerPool,
    connections: HashMap<Token, TcpStream>,
    current_token: Token,
    max_number_headers: usize,
}

impl<'g> Server {
    pub fn new(
        application: PyObject,
        globals: &WSGIGlobals<'g>,
        num_workers: usize,
        write_blocking: bool,
        max_number_headers: usize,
        py: Python,
    ) -> io::Result<Server> {
        let addr = globals.server_info;
        let workers = WorkerPool::new(
            globals.server_info,
            globals.script_name.to_string(),
            application,
            if write_blocking {
                write_blocking_worker
            } else {
                write_non_blocking_worker
            },
            num_workers,
            py,
        );
        let mut listener = TcpListener::bind(addr)?;
        let poll = Poll::new()?;
        poll.registry()
            .register(&mut listener, SERVER, Interest::READABLE)?;

        Ok(Server {
            poll,
            events: Events::with_capacity(1024),
            listener,
            workers,
            connections: HashMap::new(),
            current_token: Token(SERVER.0 + 1),
            max_number_headers,
        })
    }

    /// Returns a new WSGIRequest if reading is successful.
    fn handle_read_event(&self, connection: &mut impl Read) -> io::Result<WSGIRequest> {
        let mut connection_closed = false;
        let mut req = WSGIRequest::new(self.max_number_headers);
        // We can (maybe) read from the connection.
        loop {
            let mut buf = [0; READBUFSIZE];
            match connection.read(&mut buf) {
                Ok(0) => {
                    // Reading 0 bytes means the other side has closed the
                    // connection or is done writing, then so are we.
                    debug!("Reading 0 bytes, consider reading done");
                    req.parse_headers();
                    connection_closed = true;
                    break;
                }
                Ok(n) => req.append(&buf[..n]),
                // Would block "errors" are the OS's way of saying that the
                // connection is not actually ready to perform this I/O operation.
                Err(ref err) if would_block(err) => {
                    if req.parse_headers() {
                        break;
                    }
                }
                // Other errors we'll consider fatal.
                Err(err) => return Err(err),
            }
        }

        if connection_closed & !req.complete {
            debug!("Connection closed");
            Err(io::Error::new(io::ErrorKind::Other, "Incomplete request"))
        } else {
            Ok(req)
        }
    }

    pub fn poll_once(&mut self) -> Result<()> {
        match self
            .poll
            .poll(&mut self.events, Some(Duration::from_millis(POLL_TIMEOUT)))
        {
            Ok(_) => {
                for event in self.events.iter() {
                    match event.token() {
                        SERVER => {
                            while let Ok((mut connection, _addr)) = self.listener.accept() {
                                let token = next(&mut self.current_token);
                                debug!("current token: {:?}", token);

                                self.poll.registry().register(
                                    &mut connection,
                                    token,
                                    Interest::READABLE,
                                )?;

                                self.connections.insert(token, connection);
                            }
                        }
                        token if event.is_readable() => {
                            // (maybe) received an event for a TCP connection.
                            if let Some(mut connection) = self.connections.remove(&token) {
                                match self.handle_read_event(&mut connection) {
                                    Ok(mut req) => {
                                        if let Ok(addr) = connection.peer_addr() {
                                            req.peer_addr = Some(addr);
                                        }
                                        self.workers.execute(
                                            token,
                                            req,
                                            Some(unset_cloexec(connection)?),
                                        )?;
                                    }
                                    Err(e) => {
                                        error!("Could not handle read event: {:?}", e);
                                    }
                                }
                            }
                        }
                        _ => (),
                    }
                }
            }
            Err(e) => return Err(Box::new(e)),
        }
        Ok(())
    }

    pub fn serve(&mut self) -> Result<()> {
        let py_thread_state = unsafe { PyEval_SaveThread() };
        loop {
            if let Err(e) = self.poll_once() {
                error!("Error processing poll events: {:?}", e);
                self.workers.join()?;
                break;
            }
        }
        unsafe { PyEval_RestoreThread(py_thread_state) };
        Ok(())
    }
}

#[cfg(test)]
mod tests {

    use cpython::{PyClone, PyDict, Python, PythonObject};
    use env_logger;
    use log::debug;
    use mio::net::{self, TcpListener};
    use mio::Token;
    use nix::fcntl::{fcntl, FcntlArg, FdFlag};
    use std::io::{self, Read, Write};
    use std::net::{SocketAddr, TcpStream};
    use std::ops::Range;
    use std::os::unix::io::AsRawFd;
    use std::thread;
    use std::time::Duration;

    use crate::globals::WSGIGlobals;
    use crate::server::{next, unset_cloexec, would_block, Server};

    struct StreamMock {
        pub data: Vec<u8>,
        block_pos: usize,
        raise: bool,
        pos: usize,
        error: Option<io::ErrorKind>,
    }

    impl StreamMock {
        pub fn new(data: Vec<u8>, block_before_complete: bool, raise: bool) -> StreamMock {
            let block_pos = if block_before_complete {
                10
            } else {
                data.len()
            };
            StreamMock {
                data,
                block_pos,
                raise,
                pos: 0,
                error: None,
            }
        }

        pub fn read_slice(&mut self, range: Range<usize>, buf: &mut [u8]) -> usize {
            self.pos = range.start;
            let start = range.start;
            let num_bytes = range.end - self.pos;
            for idx in range {
                let offset = idx - start;
                match self.data.get(idx) {
                    Some(d) => {
                        buf[offset] = *d;
                        self.pos = self.pos + 1;
                    }
                    None => return offset,
                }
            }
            num_bytes
        }
    }

    impl Read for StreamMock {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            match self.error {
                None => {
                    let num_bytes = self.read_slice(0..self.block_pos, buf);
                    self.error = Some(io::ErrorKind::WouldBlock);
                    Ok(num_bytes)
                }
                Some(errkind) if errkind == io::ErrorKind::WouldBlock => {
                    self.error = Some(io::ErrorKind::Other);
                    Err(io::Error::new(
                        io::ErrorKind::WouldBlock,
                        "StreamMock blocking",
                    ))
                }
                Some(errkind) if errkind == io::ErrorKind::Other => {
                    self.error = Some(io::ErrorKind::WriteZero);
                    Ok(self.read_slice(self.block_pos..buf.len(), buf))
                }
                Some(_) => {
                    if self.raise {
                        Err(io::Error::new(
                            io::ErrorKind::BrokenPipe,
                            "StreamMock raising",
                        ))
                    } else {
                        Ok(0)
                    }
                }
            }
        }
    }

    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_next() {
        let mut start = Token(0);
        for idx in 0..6 {
            let got = next(&mut start);
            assert_eq!(Token(idx), got);
            assert_eq!(start.0, idx + 1);
        }
    }

    #[test]
    fn test_handle_read_event() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:0".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let server = Server::new(py.None(), &g, 2, false, 16, py).unwrap();
        let expected = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut s = StreamMock::new(expected.to_vec(), true, false);
        // read interrupted by WouldBlock, block will occur
        // before complete parsing of request is possible
        match server.handle_read_event(&mut s) {
            Ok(mut req) => {
                debug!("Got (after WouldBlock): {:?}", &req.data[..]);
                assert!(req.data.iter().zip(expected.iter()).all(|(p, q)| p == q));
                assert!(req.parse_headers());
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
        }
        let mut s = StreamMock::new(expected.to_vec(), false, false);
        // read interrupted by WouldBlock, block will occur
        // when complete parsing of request is possible
        match server.handle_read_event(&mut s) {
            Ok(mut req) => {
                debug!("Got (after WouldBlock): {:?}", &req.data[..]);
                assert!(req.data.iter().zip(expected.iter()).all(|(p, q)| p == q));
                assert!(req.parse_headers());
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
        }
        let mut s = StreamMock::new(expected.to_vec(), true, true);
        // read until WouldBlock, block will occur
        // before complete parsing of request is possible
        // and then raise BrokenPipe
        match server.handle_read_event(&mut s) {
            Ok(_) => {
                assert!(false);
            }
            Err(e) => {
                assert!(e.kind() == io::ErrorKind::BrokenPipe);
            }
        }
    }

    #[test]
    fn test_handle_read_event_too_many_headers() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:0".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let server = Server::new(py.None(), &g, 2, false, 16, py).unwrap();
        let expected = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\nH1: 1\r\nH2: 2\r\nH3: 3\r\nH4: 4\r\nH5: 5\r\nH6: 6\r\nH7: 7\r\nH8: 8\r\nH9: 9\r\nH10: 10\r\nH11: 11\r\nH12: 12\r\n\r\n";
        let mut s = StreamMock::new(expected.to_vec(), true, false);
        // read interrupted by WouldBlock, block will occur
        // before complete parsing of request is possible
        match server.handle_read_event(&mut s) {
            Ok(_) => {
                assert!(false);
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(e.kind() == io::ErrorKind::Other);
            }
        }
    }

    #[test]
    fn test_would_block() {
        let wbe = io::Error::new(io::ErrorKind::WouldBlock, "foo");
        assert!(would_block(&wbe));
        let nwbe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!would_block(&nwbe));
    }

    #[test]
    fn test_create_blocking_server() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let si = "127.0.0.1:0".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, 2, true, 16, py) {
                    Ok(got) => {
                        assert!(got.current_token == Token(1));
                    }
                    Err(e) => {
                        debug!("Error when creating Server: {:?}", e);
                        assert!(false);
                    }
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_create_non_blocking_server() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let si = "127.0.0.1:0".parse().unwrap();
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, 2, false, 16, py) {
                    Ok(got) => {
                        assert!(got.current_token == Token(1));
                    }
                    Err(e) => {
                        debug!("Error when creating Server: {:?}", e);
                        assert!(false);
                    }
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_server_poll_once() {
        init();
        let si = "127.0.0.1:7878".parse().unwrap();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let sn = "/foo";
                let g = WSGIGlobals::new(si, sn, py);
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, 1, true, 16, py) {
                    Ok(mut got) => {
                        // accept
                        got.poll_once().unwrap();
                        // create request in separate thread
                        let t = thread::spawn(move || {
                            let mut connection =
                                TcpStream::connect_timeout(&si, Duration::from_millis(1000))
                                    .expect("Failed to connect to server");
                            let req = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\n\r\n";
                            match connection.write(req) {
                                Ok(num_bytes) => assert_eq!(num_bytes, req.len()),
                                Err(_) => assert!(false),
                            };
                        });
                        // read + propagate HTTPrequest
                        got.poll_once().unwrap();
                        t.join().unwrap();
                    }
                    Err(e) => {
                        debug!("Error when creating Server: {:?}", e);
                        assert!(false);
                    }
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_unset_cloexec() {
        let addr: SocketAddr = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(addr).unwrap();
        let before = net::TcpStream::connect(listener.local_addr().unwrap()).unwrap();
        // man 2 fcntl - file descriptor flags
        let fd_before =
            FdFlag::from_bits(fcntl(before.as_raw_fd(), FcntlArg::F_GETFD).unwrap()).unwrap();
        assert!(fd_before.contains(FdFlag::FD_CLOEXEC));
        match unset_cloexec(before) {
            Ok(after) => {
                let fd_after =
                    FdFlag::from_bits(fcntl(after.as_raw_fd(), FcntlArg::F_GETFD).unwrap())
                        .unwrap();
                assert!(!fd_after.contains(FdFlag::FD_CLOEXEC));
            }
            Err(e) => {
                debug!("Unexpected error: {:?}", e);
                assert!(false);
            }
        }
    }
}
