#[macro_use]
extern crate cpython;

use cpython::{PyResult, Python};

py_module_initializer!(august, initlibaugust, PyInit_august, |py, m| {
    m.add(
        py,
        "__doc__",
        "A library for converting HTML to plain text.",
    )?;
    m.add(
        py,
        "convert",
        py_fn!(py, convert(input: &str, width: Option<usize> = Some(79))),
    )?;
    m.add(
        py,
        "convert_unstyled",
        py_fn!(
            py,
            convert_unstyled(input: &str, width: Option<usize> = Some(79))
        ),
    )?;
    Ok(())
});

// logic implemented as a normal rust function
fn convert(_: Python, input: &str, width: Option<usize>) -> PyResult<String> {
    Ok(august::convert(input, width.unwrap_or(79)))
}

fn convert_unstyled(_: Python, input: &str, width: Option<usize>) -> PyResult<String> {
    Ok(august::convert_unstyled(input, width.unwrap_or(79)))
}
