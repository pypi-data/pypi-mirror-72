use cpython::exc::{IOError, ValueError};
use cpython::{PyErr, PyObject, PyResult, Python};

use crate::filewrapper::FileWrapper;
use crate::globals::WSGIGlobals;
use crate::server::Server;
use crate::startresponse::StartResponse;

fn serve(
    py: Python,
    application: PyObject,
    addr: &str,
    num_workers: usize,
    write_blocking: bool,
    max_number_headers: usize,
) -> PyResult<PyObject> {
    let addr = match addr.parse() {
        Ok(addr) => addr,
        Err(_) => return Err(PyErr::new::<ValueError, _>(py, "Could not parse address")),
    };
    let globals = WSGIGlobals::new(addr, "", py);

    match slog_envlogger::init() {
        Ok(_) => {
            if num_workers < 1 {
                return Err(PyErr::new::<ValueError, _>(py, "Need at least 1 worker"));
            }
            match Server::new(
                application,
                &globals,
                num_workers,
                write_blocking,
                max_number_headers,
                py,
            ) {
                Ok(mut server) => match server.serve() {
                    Ok(_) => Ok(py.None()),
                    Err(_) => Err(PyErr::new::<IOError, _>(
                        py,
                        "Error encountered during event loop",
                    )),
                },
                Err(e) => Err(PyErr::new::<IOError, _>(
                    py,
                    format!("Could not create server: {:?}", e),
                )),
            }
        }
        Err(_) => Err(PyErr::new::<IOError, _>(py, "Could not setup logging")),
    }
}

py_module_initializer!(pyruvate, initpyruvate, PyInit_pyruvate, |py, m| {
    m.add(py, "__doc__", "Pyruvate WSGI server")
        .expect("Could not add documentation string");
    m.add_class::<StartResponse>(py)
        .expect("Could not add StartResponse class to module");
    m.add_class::<FileWrapper>(py)
        .expect("Could not add FileWrapper class to module");
    m.add(
        py,
        "serve",
        py_fn!(
            py,
            serve(
                application: PyObject,
                addr: &str,
                num_workers: usize = 2,
                write_blocking: bool = false,
                max_number_headers: usize = 16
            )
        ),
    )
    .expect("Could not add serve() function to module");
    Ok(())
});
