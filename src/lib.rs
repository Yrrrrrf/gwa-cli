use pyo3::prelude::*;

#[pyfunction]
fn hello_from_bin() -> String {
    "Hello from gwa!".to_string()
}

// Create an init function to register the application metadata
#[pyfunction]
pub fn init() -> PyResult<()> {
    // todo: On 'dev_utils' crate, the macro must also return the value as a HashMap!
    dev_utils::app_dt!(file!(),
        "package" => ["authors", "license", "description"]
    );
    Ok(())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(init, m)?)?;
    Ok(())
}
