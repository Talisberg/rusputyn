use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use serde_json::Value;
use jsonschema::JSONSchema;

/// Convert Python object to serde_json::Value
fn python_to_json(py: Python, obj: &PyAny) -> PyResult<Value> {
    let json_str = py.import("json")?.call_method1("dumps", (obj,))?;
    let json_str: String = json_str.extract()?;

    serde_json::from_str(&json_str)
        .map_err(|e| PyValueError::new_err(format!("JSON conversion error: {}", e)))
}

/// Validate JSON data against a schema
///
/// Raises ValidationError if validation fails
#[pyfunction]
fn validate(py: Python, instance: &PyAny, schema: &PyAny) -> PyResult<()> {
    // Convert Python objects to JSON
    let instance_json = python_to_json(py, instance)?;
    let schema_json = python_to_json(py, schema)?;

    // Compile schema
    let compiled = JSONSchema::compile(&schema_json)
        .map_err(|e| PyValueError::new_err(format!("Schema compilation error: {}", e)))?;

    // Validate - collect errors immediately to avoid lifetime issues
    let validation_result = compiled.validate(&instance_json);
    if validation_result.is_ok() {
        return Ok(());
    }

    let error_messages: Vec<String> = validation_result
        .unwrap_err()
        .map(|e| e.to_string())
        .collect();

    Err(PyValueError::new_err(format!(
        "Validation error: {}",
        error_messages.join(", ")
    )))
}

/// Check if instance is valid against schema
///
/// Returns True if valid, False otherwise
#[pyfunction]
fn is_valid(py: Python, instance: &PyAny, schema: &PyAny) -> PyResult<bool> {
    // Convert Python objects to JSON
    let instance_json = python_to_json(py, instance)?;
    let schema_json = python_to_json(py, schema)?;

    // Compile schema
    let compiled = JSONSchema::compile(&schema_json)
        .map_err(|_| PyValueError::new_err("Schema compilation error"))?;

    // Check validity
    Ok(compiled.is_valid(&instance_json))
}

/// Validator class that can be reused for multiple validations
#[pyclass]
struct Validator {
    schema: JSONSchema,
}

#[pymethods]
impl Validator {
    #[new]
    fn new(py: Python, schema: &PyAny) -> PyResult<Self> {
        let schema_json = python_to_json(py, schema)?;
        let compiled = JSONSchema::compile(&schema_json)
            .map_err(|e| PyValueError::new_err(format!("Schema compilation error: {}", e)))?;

        Ok(Validator { schema: compiled })
    }

    /// Validate an instance against the schema
    fn validate(&self, py: Python, instance: &PyAny) -> PyResult<()> {
        let instance_json = python_to_json(py, instance)?;

        let validation_result = self.schema.validate(&instance_json);
        if validation_result.is_ok() {
            return Ok(());
        }

        let error_messages: Vec<String> = validation_result
            .unwrap_err()
            .map(|e| e.to_string())
            .collect();

        Err(PyValueError::new_err(format!(
            "Validation error: {}",
            error_messages.join(", ")
        )))
    }

    /// Check if instance is valid
    fn is_valid(&self, py: Python, instance: &PyAny) -> PyResult<bool> {
        let instance_json = python_to_json(py, instance)?;
        Ok(self.schema.is_valid(&instance_json))
    }
}

#[pymodule]
fn jsonschema_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate, m)?)?;
    m.add_function(wrap_pyfunction!(is_valid, m)?)?;
    m.add_class::<Validator>()?;
    Ok(())
}
