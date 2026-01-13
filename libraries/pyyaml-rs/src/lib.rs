use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3::exceptions::{PyValueError, PyTypeError};
use serde_yaml;
use serde::Deserialize;

/// Convert serde_yaml::Value to Python object
fn yaml_to_python(py: Python, value: serde_yaml::Value) -> PyResult<PyObject> {
    match value {
        serde_yaml::Value::Null => Ok(py.None()),
        serde_yaml::Value::Bool(b) => Ok(b.to_object(py)),
        serde_yaml::Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(i.to_object(py))
            } else if let Some(f) = n.as_f64() {
                Ok(f.to_object(py))
            } else {
                Ok(py.None())
            }
        }
        serde_yaml::Value::String(s) => Ok(s.to_object(py)),
        serde_yaml::Value::Sequence(seq) => {
            let py_list = PyList::empty(py);
            for item in seq {
                py_list.append(yaml_to_python(py, item)?)?;
            }
            Ok(py_list.to_object(py))
        }
        serde_yaml::Value::Mapping(map) => {
            let py_dict = PyDict::new(py);
            for (k, v) in map {
                let py_key = yaml_to_python(py, k)?;
                let py_value = yaml_to_python(py, v)?;
                py_dict.set_item(py_key, py_value)?;
            }
            Ok(py_dict.to_object(py))
        }
        serde_yaml::Value::Tagged(tagged) => {
            // Handle tagged values by just returning the value
            yaml_to_python(py, tagged.value)
        }
    }
}

/// Convert Python object to serde_yaml::Value
fn python_to_yaml(py: Python, obj: &PyAny) -> PyResult<serde_yaml::Value> {
    if obj.is_none() {
        Ok(serde_yaml::Value::Null)
    } else if let Ok(b) = obj.extract::<bool>() {
        Ok(serde_yaml::Value::Bool(b))
    } else if let Ok(i) = obj.extract::<i64>() {
        Ok(serde_yaml::Value::Number(i.into()))
    } else if let Ok(f) = obj.extract::<f64>() {
        Ok(serde_yaml::Value::Number(f.into()))
    } else if let Ok(s) = obj.extract::<String>() {
        Ok(serde_yaml::Value::String(s))
    } else if let Ok(list) = obj.downcast::<PyList>() {
        let mut seq = Vec::new();
        for item in list.iter() {
            seq.push(python_to_yaml(py, item)?);
        }
        Ok(serde_yaml::Value::Sequence(seq))
    } else if let Ok(dict) = obj.downcast::<PyDict>() {
        let mut map = serde_yaml::Mapping::new();
        for (k, v) in dict.iter() {
            let key = python_to_yaml(py, k)?;
            let value = python_to_yaml(py, v)?;
            map.insert(key, value);
        }
        Ok(serde_yaml::Value::Mapping(map))
    } else {
        Err(PyTypeError::new_err(format!(
            "Cannot convert Python type {} to YAML",
            obj.get_type().name()?
        )))
    }
}

/// Parse YAML string and return Python object
#[pyfunction]
fn safe_load(py: Python, s: &str) -> PyResult<PyObject> {
    let value: serde_yaml::Value = serde_yaml::from_str(s)
        .map_err(|e| PyValueError::new_err(format!("YAML parse error: {}", e)))?;

    yaml_to_python(py, value)
}

/// Parse YAML string (alias for safe_load)
#[pyfunction]
fn load(py: Python, s: &str) -> PyResult<PyObject> {
    safe_load(py, s)
}

/// Parse multiple YAML documents from string
#[pyfunction]
fn safe_load_all(py: Python, s: &str) -> PyResult<PyObject> {
    let deserializer = serde_yaml::Deserializer::from_str(s);
    let py_list = PyList::empty(py);

    for doc in deserializer {
        let value = serde_yaml::Value::deserialize(doc)
            .map_err(|e| PyValueError::new_err(format!("YAML parse error: {}", e)))?;
        py_list.append(yaml_to_python(py, value)?)?;
    }

    Ok(py_list.to_object(py))
}

/// Parse multiple YAML documents (alias for safe_load_all)
#[pyfunction]
fn load_all(py: Python, s: &str) -> PyResult<PyObject> {
    safe_load_all(py, s)
}

/// Serialize Python object to YAML string
#[pyfunction]
fn safe_dump(py: Python, obj: &PyAny) -> PyResult<String> {
    let yaml_value = python_to_yaml(py, obj)?;

    serde_yaml::to_string(&yaml_value)
        .map_err(|e| PyValueError::new_err(format!("YAML serialization error: {}", e)))
}

/// Serialize Python object to YAML string (alias for safe_dump)
#[pyfunction]
fn dump(py: Python, obj: &PyAny) -> PyResult<String> {
    safe_dump(py, obj)
}

/// Serialize multiple Python objects to YAML string
#[pyfunction]
fn safe_dump_all(py: Python, documents: &PyList) -> PyResult<String> {
    let mut result = String::new();

    for doc in documents.iter() {
        let yaml_value = python_to_yaml(py, doc)?;
        let yaml_str = serde_yaml::to_string(&yaml_value)
            .map_err(|e| PyValueError::new_err(format!("YAML serialization error: {}", e)))?;

        if !result.is_empty() {
            result.push_str("---\n");
        }
        result.push_str(&yaml_str);
    }

    Ok(result)
}

/// Serialize multiple Python objects (alias for safe_dump_all)
#[pyfunction]
fn dump_all(py: Python, documents: &PyList) -> PyResult<String> {
    safe_dump_all(py, documents)
}

#[pymodule]
fn pyyaml_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(safe_load, m)?)?;
    m.add_function(wrap_pyfunction!(load, m)?)?;
    m.add_function(wrap_pyfunction!(safe_load_all, m)?)?;
    m.add_function(wrap_pyfunction!(load_all, m)?)?;
    m.add_function(wrap_pyfunction!(safe_dump, m)?)?;
    m.add_function(wrap_pyfunction!(dump, m)?)?;
    m.add_function(wrap_pyfunction!(safe_dump_all, m)?)?;
    m.add_function(wrap_pyfunction!(dump_all, m)?)?;
    Ok(())
}
