use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyString};
use pyo3::exceptions::PyValueError;
use std::io::Read;

/// Convert TOML value to Python object
fn toml_value_to_py(py: Python<'_>, value: &toml::Value) -> PyResult<PyObject> {
    match value {
        toml::Value::String(s) => Ok(s.clone().into_py(py)),
        toml::Value::Integer(i) => Ok(i.into_py(py)),
        toml::Value::Float(f) => Ok(f.into_py(py)),
        toml::Value::Boolean(b) => Ok(b.into_py(py)),
        toml::Value::Datetime(dt) => {
            // Convert TOML datetime to Python datetime
            let dt_str = dt.to_string();
            
            // Import datetime module
            let datetime = py.import("datetime")?;
            
            // Parse different datetime formats
            if dt_str.contains('T') || dt_str.contains(' ') {
                // Full datetime with optional time
                if dt_str.contains('+') || dt_str.ends_with('Z') {
                    // With timezone
                    datetime.call_method1("fromisoformat", (dt_str.replace('Z', "+00:00"),))?.extract()
                } else {
                    // Without timezone (local)
                    let date_str = if dt_str.contains(' ') {
                        dt_str.replace(' ', "T")
                    } else {
                        dt_str
                    };
                    datetime.call_method1("fromisoformat", (date_str,))?.extract()
                }
            } else if dt_str.contains(':') {
                // Time only
                let time_cls = datetime.getattr("time")?;
                let parts: Vec<&str> = dt_str.split(':').collect();
                if parts.len() >= 2 {
                    let hour: u32 = parts[0].parse().unwrap_or(0);
                    let minute: u32 = parts[1].parse().unwrap_or(0);
                    let second: u32 = if parts.len() > 2 {
                        parts[2].split('.').next().unwrap_or("0").parse().unwrap_or(0)
                    } else {
                        0
                    };
                    time_cls.call1((hour, minute, second))?.extract()
                } else {
                    Ok(dt_str.into_py(py))
                }
            } else {
                // Date only
                let date_cls = datetime.getattr("date")?;
                date_cls.call_method1("fromisoformat", (dt_str,))?.extract()
            }
        }
        toml::Value::Array(arr) => {
            let list = PyList::empty(py);
            for item in arr {
                list.append(toml_value_to_py(py, item)?)?;
            }
            Ok(list.into())
        }
        toml::Value::Table(table) => {
            let dict = PyDict::new(py);
            for (key, value) in table {
                dict.set_item(key, toml_value_to_py(py, value)?)?;
            }
            Ok(dict.into())
        }
    }
}

/// Parse a TOML string and return a Python dict
/// 
/// Args:
///     s (str): TOML string to parse
///
/// Returns:
///     dict: Parsed TOML data as Python dictionary
///
/// Raises:
///     TOMLDecodeError: If the TOML is invalid
#[pyfunction]
fn loads(py: Python<'_>, s: &str) -> PyResult<PyObject> {
    // Parse TOML
    let value: toml::Value = s.parse().map_err(|e| {
        PyValueError::new_err(format!("TOML parse error: {}", e))
    })?;
    
    // Convert to Python dict
    toml_value_to_py(py, &value)
}

/// Load and parse TOML from a binary file object
///
/// Args:
///     fp: A binary file object (must have .read() method)
///
/// Returns:
///     dict: Parsed TOML data as Python dictionary
///
/// Raises:
///     TOMLDecodeError: If the TOML is invalid
#[pyfunction]
fn load(py: Python<'_>, fp: &PyAny) -> PyResult<PyObject> {
    // Read from file object
    let content = if let Ok(read_method) = fp.getattr("read") {
        let bytes = read_method.call0()?;
        
        // Convert bytes to string
        if let Ok(byte_str) = bytes.extract::<&[u8]>() {
            String::from_utf8(byte_str.to_vec()).map_err(|e| {
                PyValueError::new_err(format!("UTF-8 decode error: {}", e))
            })?
        } else if let Ok(s) = bytes.extract::<String>() {
            s
        } else {
            return Err(PyValueError::new_err("Could not read from file object"));
        }
    } else {
        return Err(PyValueError::new_err("File object must have read() method"));
    };
    
    // Parse and return
    loads(py, &content)
}

/// tomli-rs: High-performance TOML parser for Python
///
/// A drop-in replacement for Python's tomli module, implemented in Rust
/// for significantly faster parsing of TOML configuration files.
///
/// Functions:
///     loads(s: str) -> dict: Parse a TOML string
///     load(fp: BinaryIO) -> dict: Load and parse TOML from a file
///
/// Example:
///     ```python
///     import tomli_rs
///
///     # Parse from string
///     config = tomli_rs.loads('[server]\\nport = 8080')
///
///     # Parse from file
///     with open('config.toml', 'rb') as f:
///         config = tomli_rs.load(f)
///     ```
#[pymodule]
fn tomli_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(loads, m)?)?;
    m.add_function(wrap_pyfunction!(load, m)?)?;
    
    // Add version
    m.add("__version__", "0.1.0")?;
    
    // Create TOMLDecodeError exception class (alias to ValueError for compatibility)
    let decode_error = _py.get_type::<PyValueError>();
    m.add("TOMLDecodeError", decode_error)?;
    
    Ok(())
}
