use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::path::PathBuf;

mod config;
mod generator;
use crate::config::ProjectConfig;

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

/// Main function to generate a project from the static branch
#[pyfunction]
fn generate_project_from_static_branch(config_dict: &Bound<'_, PyDict>) -> PyResult<bool> {
    // Convert the Python dictionary to a Rust ProjectConfig struct
    let project_name: String = if let Some(value) = config_dict.get_item("project_name")? {
        value.extract()?
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "project_name is required",
        ));
    };

    let destination: String = if let Some(value) = config_dict.get_item("destination")? {
        value.extract()?
    } else {
        ".".to_string()
    };

    let destination_path = PathBuf::from(destination);

    // Extract other configuration options with defaults or Optionals
    let author_name: String = if let Some(value) = config_dict.get_item("author_name")? {
        value.extract()?
    } else {
        "Test User".to_string()
    };

    let author_email: String = if let Some(value) = config_dict.get_item("author_email")? {
        value.extract()?
    } else {
        "test@example.com".to_string()
    };

    let db_name: Option<String> = if let Some(value) = config_dict.get_item("db_name")? {
        Some(value.extract()?)
    } else {
        Some(project_name.to_lowercase().replace('-', "_"))
    };

    let db_owner_admin: Option<String> =
        if let Some(value) = config_dict.get_item("db_owner_admin")? {
            Some(value.extract()?)
        } else {
            Some(format!(
                "{}_owner",
                project_name.to_lowercase().replace('-', "_")
            ))
        };

    let db_owner_pword: Option<String> =
        if let Some(value) = config_dict.get_item("db_owner_pword")? {
            Some(value.extract()?)
        } else {
            Some("password".to_string())
        };

    let include_server: bool = if let Some(value) = config_dict.get_item("include_server")? {
        value.extract()?
    } else {
        true
    };

    let include_frontend: bool = if let Some(value) = config_dict.get_item("include_frontend")? {
        value.extract()?
    } else {
        true
    };

    let include_tauri_desktop: bool =
        if let Some(value) = config_dict.get_item("include_tauri_desktop")? {
            value.extract()?
        } else {
            true
        };

    let app_identifier: String = if let Some(value) = config_dict.get_item("app_identifier")? {
        value.extract()?
    } else {
        format!(
            "com.example.{}",
            project_name.to_lowercase().replace('-', "")
        )
    };

    let deno_package_name: String =
        if let Some(value) = config_dict.get_item("deno_package_name")? {
            value.extract()?
        } else {
            "@test/gwa-project".to_string()
        };

    // Create the ProjectConfig struct
    let project_config = ProjectConfig {
        project_name: project_name.clone(),
        author_name,
        author_email,
        app_identifier,
        db_name,
        db_owner_admin,
        db_owner_pword,
        include_server,
        include_frontend,
        include_tauri_desktop,
        deno_package_name,
    };

    // Generate the project using the existing generator
    match generator::generate_project(&project_config, &destination_path) {
        Ok(_) => Ok(true),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
            "Failed to generate project: {}",
            e
        ))),
    }
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(generate_project_from_static_branch, m)?)?;
    Ok(())
}
