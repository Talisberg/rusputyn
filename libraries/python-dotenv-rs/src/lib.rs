use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::exceptions::PyIOError;
use std::fs;
use std::path::{Path, PathBuf};
use std::collections::HashMap;

/// Parse a single line from a .env file
fn parse_line(line: &str) -> Option<(String, String)> {
    let line = line.trim();

    // Skip empty lines and comments
    if line.is_empty() || line.starts_with('#') {
        return None;
    }

    // Find the first = sign
    if let Some(eq_pos) = line.find('=') {
        let key = line[..eq_pos].trim();
        let value = line[eq_pos + 1..].trim();

        // Skip invalid keys
        if key.is_empty() {
            return None;
        }

        // Handle quoted values
        let parsed_value = if (value.starts_with('"') && value.ends_with('"')) ||
                             (value.starts_with('\'') && value.ends_with('\'')) {
            // Remove quotes
            value[1..value.len()-1].to_string()
        } else {
            value.to_string()
        };

        Some((key.to_string(), parsed_value))
    } else {
        None
    }
}

/// Parse .env file content into a HashMap
fn parse_dotenv(content: &str) -> HashMap<String, String> {
    let mut env_vars = HashMap::new();

    for line in content.lines() {
        if let Some((key, value)) = parse_line(line) {
            env_vars.insert(key, value);
        }
    }

    env_vars
}

/// Load environment variables from a .env file
///
/// Args:
///     dotenv_path (str, optional): Path to .env file. If None, searches for .env in current and parent directories.
///     override (bool): Whether to override existing environment variables. Default: False
///
/// Returns:
///     bool: True if .env file was found and loaded, False otherwise
#[pyfunction]
#[pyo3(signature = (dotenv_path=None, override_vars=false))]
fn load_dotenv(py: Python<'_>, dotenv_path: Option<String>, override_vars: bool) -> PyResult<bool> {
    // Determine the path to load
    let path = if let Some(p) = dotenv_path {
        PathBuf::from(p)
    } else {
        // Search for .env file
        match find_dotenv_path() {
            Some(p) => p,
            None => return Ok(false),
        }
    };

    // Check if file exists
    if !path.exists() {
        return Ok(false);
    }

    // Read file content
    let content = fs::read_to_string(&path)
        .map_err(|e| PyIOError::new_err(format!("Failed to read .env file: {}", e)))?;

    // Parse environment variables
    let env_vars = parse_dotenv(&content);

    // Set environment variables
    let os_module = py.import("os")?;
    let environ = os_module.getattr("environ")?;

    for (key, value) in env_vars {
        // Check if we should override
        if override_vars || !environ.contains(&key)? {
            environ.set_item(key, value)?;
        }
    }

    Ok(true)
}

/// Find .env file by searching current directory and parents
///
/// Returns:
///     str or None: Path to .env file if found, None otherwise
#[pyfunction]
fn find_dotenv() -> Option<String> {
    find_dotenv_path().map(|p| p.to_string_lossy().to_string())
}

/// Internal function to find .env file path
fn find_dotenv_path() -> Option<PathBuf> {
    let current_dir = std::env::current_dir().ok()?;

    // Check current directory
    let dotenv_path = current_dir.join(".env");
    if dotenv_path.exists() {
        return Some(dotenv_path);
    }

    // Check parent directories (up to 5 levels)
    let mut search_dir = current_dir.as_path();
    for _ in 0..5 {
        if let Some(parent) = search_dir.parent() {
            let dotenv_path = parent.join(".env");
            if dotenv_path.exists() {
                return Some(dotenv_path);
            }
            search_dir = parent;
        } else {
            break;
        }
    }

    None
}

/// Parse .env file content and return as dictionary
///
/// Args:
///     content (str): Content of .env file
///
/// Returns:
///     dict: Dictionary of environment variables
#[pyfunction]
fn dotenv_values(py: Python<'_>, content: String) -> PyResult<PyObject> {
    let env_vars = parse_dotenv(&content);

    let dict = PyDict::new(py);
    for (key, value) in env_vars {
        dict.set_item(key, value)?;
    }

    Ok(dict.into())
}

/// Set a single environment variable
///
/// Args:
///     key (str): Environment variable name
///     value (str): Environment variable value
///     override (bool): Whether to override if already exists. Default: True
///
/// Returns:
///     tuple: (success, warning_message or None)
#[pyfunction]
#[pyo3(signature = (key, value, override_vars=true))]
fn set_key(py: Python<'_>, key: String, value: String, override_vars: bool) -> PyResult<(bool, Option<String>)> {
    let os_module = py.import("os")?;
    let environ = os_module.getattr("environ")?;

    // Check if key exists
    let exists = environ.contains(&key)?;

    if exists && !override_vars {
        return Ok((false, Some(format!("Key '{}' already exists", key))));
    }

    environ.set_item(key, value)?;
    Ok((true, None))
}

/// Get value of an environment variable
///
/// Args:
///     key (str): Environment variable name
///
/// Returns:
///     str or None: Value of environment variable, or None if not set
#[pyfunction]
fn get_key(py: Python<'_>, key: String) -> PyResult<Option<String>> {
    let os_module = py.import("os")?;
    let environ = os_module.getattr("environ")?;

    if let Ok(value) = environ.get_item(&key) {
        if value.is_none() {
            Ok(None)
        } else {
            Ok(Some(value.extract()?))
        }
    } else {
        Ok(None)
    }
}

/// Unset an environment variable
///
/// Args:
///     key (str): Environment variable name
///
/// Returns:
///     bool: True if variable was unset, False if it didn't exist
#[pyfunction]
fn unset_key(py: Python<'_>, key: String) -> PyResult<bool> {
    let os_module = py.import("os")?;
    let environ = os_module.getattr("environ")?;

    if environ.contains(&key)? {
        environ.del_item(&key)?;
        Ok(true)
    } else {
        Ok(false)
    }
}

/// python-dotenv-rs: High-performance .env file loader for Python
///
/// A drop-in replacement for Python's python-dotenv module, implemented in Rust
/// for significantly faster environment variable loading and parsing.
///
/// Functions:
///     load_dotenv(dotenv_path=None, override=False) -> bool
///     find_dotenv() -> str or None
///     dotenv_values(content: str) -> dict
///     set_key(key: str, value: str, override=True) -> (bool, str or None)
///     get_key(key: str) -> str or None
///     unset_key(key: str) -> bool
///
/// Example:
///     ```python
///     import dotenv_rs
///
///     # Load .env file
///     dotenv_rs.load_dotenv()
///
///     # Or specify path
///     dotenv_rs.load_dotenv('.env.production')
///     ```
#[pymodule]
fn dotenv_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_dotenv, m)?)?;
    m.add_function(wrap_pyfunction!(find_dotenv, m)?)?;
    m.add_function(wrap_pyfunction!(dotenv_values, m)?)?;
    m.add_function(wrap_pyfunction!(set_key, m)?)?;
    m.add_function(wrap_pyfunction!(get_key, m)?)?;
    m.add_function(wrap_pyfunction!(unset_key, m)?)?;

    m.add("__version__", "0.1.0")?;

    Ok(())
}
