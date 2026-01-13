#![allow(non_local_definitions)]

use pyo3::prelude::*;

/// Escape HTML special characters in a string
#[pyfunction]
fn escape(py: Python<'_>, s: &PyAny) -> PyResult<PyObject> {
    // Handle None
    if s.is_none() {
        return Ok(s.into());
    }
    
    // Handle Markup instances (already safe)
    if let Ok(markup) = s.extract::<PyRef<Markup>>() {
        return Ok(markup.value.clone().into_py(py));
    }
    
    // Convert to string
    let text = if let Ok(string) = s.extract::<String>() {
        string
    } else {
        s.str()?.to_str()?.to_string()
    };
    
    // Fast path: no escaping needed
    if !text.chars().any(|c| matches!(c, '&' | '<' | '>' | '"' | '\'')) {
        return Ok(Markup::new(text).into_py(py));
    }
    
    // Escape characters
    let mut result = String::with_capacity(text.len() + text.len() / 4);
    for c in text.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            '\'' => result.push_str("&#x27;"),
            _ => result.push(c),
        }
    }
    
    Ok(Markup::new(result).into_py(py))
}

/// Escape HTML, returning empty string for None instead of None
#[pyfunction]
fn escape_silent(py: Python<'_>, s: &PyAny) -> PyResult<PyObject> {
    if s.is_none() {
        return Ok(Markup::new(String::new()).into_py(py));
    }
    escape(py, s)
}

/// Convert value to unicode string, handling None
#[pyfunction]
fn soft_unicode(s: &PyAny) -> PyResult<String> {
    if s.is_none() {
        return Ok(String::new());
    }
    
    if let Ok(string) = s.extract::<String>() {
        Ok(string)
    } else {
        Ok(s.str()?.to_str()?.to_string())
    }
}

/// Convert value to string, handling Markup instances
#[pyfunction]
fn soft_str(s: &PyAny) -> PyResult<String> {
    if let Ok(markup) = s.extract::<PyRef<Markup>>() {
        return Ok(markup.value.clone());
    }
    soft_unicode(s)
}

/// Markup - A string that is ready to be safely inserted into HTML/XML
#[pyclass]
#[derive(Clone)]
struct Markup {
    value: String,
}

#[pymethods]
impl Markup {
    #[new]
    fn new(value: String) -> Self {
        Markup { value }
    }
    
    fn __str__(&self) -> String {
        self.value.clone()
    }
    
    fn __repr__(&self) -> String {
        format!("Markup('{}')", self.value)
    }
    
    fn __len__(&self) -> usize {
        self.value.len()
    }
    
    fn __add__(&self, other: &PyAny) -> PyResult<Markup> {
        let other_str = if let Ok(markup) = other.extract::<PyRef<Markup>>() {
            markup.value.clone()
        } else if let Ok(s) = other.extract::<String>() {
            // Escape raw strings when concatenating
            escape_string(&s)
        } else {
            escape_string(&other.str()?.to_str()?.to_string())
        };
        
        Ok(Markup::new(format!("{}{}", self.value, other_str)))
    }
    
    fn __radd__(&self, other: &PyAny) -> PyResult<Markup> {
        let other_str = if let Ok(markup) = other.extract::<PyRef<Markup>>() {
            markup.value.clone()
        } else if let Ok(s) = other.extract::<String>() {
            escape_string(&s)
        } else {
            escape_string(&other.str()?.to_str()?.to_string())
        };
        
        Ok(Markup::new(format!("{}{}", other_str, self.value)))
    }
    
    fn __mul__(&self, count: usize) -> Markup {
        Markup::new(self.value.repeat(count))
    }
    
    fn __rmul__(&self, count: usize) -> Markup {
        self.__mul__(count)
    }
    
    fn __mod__(&self, args: &PyAny) -> PyResult<Markup> {
        // Simple string formatting - would need more sophistication for full compatibility
        let formatted = format!("{}", args);
        Ok(Markup::new(self.value.replace("%s", &formatted)))
    }
    
    fn __html__(&self) -> String {
        self.value.clone()
    }
    
    /// Join an iterable of strings, escaping them
    fn join(&self, _py: Python<'_>, seq: &PyAny) -> PyResult<Markup> {
        let iter = seq.iter()?;
        let mut parts = Vec::new();
        
        for item in iter {
            let item = item?;
            let s = if let Ok(markup) = item.extract::<PyRef<Markup>>() {
                markup.value.clone()
            } else if let Ok(s) = item.extract::<String>() {
                escape_string(&s)
            } else {
                escape_string(&item.str()?.to_str()?.to_string())
            };
            parts.push(s);
        }
        
        Ok(Markup::new(parts.join(&self.value)))
    }
    
    /// Split the markup
    fn split(&self, sep: Option<&str>, maxsplit: Option<isize>) -> Vec<Markup> {
        let parts = if let Some(sep) = sep {
            if let Some(max) = maxsplit {
                if max < 0 {
                    self.value.split(sep).collect::<Vec<_>>()
                } else {
                    self.value.splitn(max as usize + 1, sep).collect::<Vec<_>>()
                }
            } else {
                self.value.split(sep).collect::<Vec<_>>()
            }
        } else {
            self.value.split_whitespace().collect::<Vec<_>>()
        };
        
        parts.into_iter().map(|s| Markup::new(s.to_string())).collect()
    }
    
    /// Return a copy with leading and trailing whitespace removed
    fn strip(&self) -> Markup {
        Markup::new(self.value.trim().to_string())
    }
    
    /// Return a copy with leading whitespace removed
    fn lstrip(&self) -> Markup {
        Markup::new(self.value.trim_start().to_string())
    }
    
    /// Return a copy with trailing whitespace removed
    fn rstrip(&self) -> Markup {
        Markup::new(self.value.trim_end().to_string())
    }
    
    /// Return a copy converted to lowercase
    fn lower(&self) -> Markup {
        Markup::new(self.value.to_lowercase())
    }
    
    /// Return a copy converted to uppercase
    fn upper(&self) -> Markup {
        Markup::new(self.value.to_uppercase())
    }
    
    /// Replace occurrences of old with new
    fn replace(&self, old: &str, new: &str, count: Option<usize>) -> Markup {
        let result = if let Some(n) = count {
            self.value.replacen(old, new, n)
        } else {
            self.value.replace(old, new)
        };
        Markup::new(result)
    }
    
    /// Check if markup starts with prefix
    fn startswith(&self, prefix: &str) -> bool {
        self.value.starts_with(prefix)
    }
    
    /// Check if markup ends with suffix
    fn endswith(&self, suffix: &str) -> bool {
        self.value.ends_with(suffix)
    }
    
    /// Unescape the markup (convert to plain string)
    fn unescape(&self) -> String {
        let mut result = self.value.clone();
        result = result.replace("&amp;", "&");
        result = result.replace("&lt;", "<");
        result = result.replace("&gt;", ">");
        result = result.replace("&quot;", "\"");
        result = result.replace("&#x27;", "'");
        result = result.replace("&#39;", "'");
        result
    }
    
    /// Check if all characters are alphanumeric
    fn isalnum(&self) -> bool {
        !self.value.is_empty() && self.value.chars().all(|c| c.is_alphanumeric())
    }
    
    /// Check if all characters are alphabetic
    fn isalpha(&self) -> bool {
        !self.value.is_empty() && self.value.chars().all(|c| c.is_alphabetic())
    }
    
    /// Check if all characters are digits
    fn isdigit(&self) -> bool {
        !self.value.is_empty() && self.value.chars().all(|c| c.is_ascii_digit())
    }
    
    /// Check if all characters are lowercase
    fn islower(&self) -> bool {
        let mut has_cased = false;
        for c in self.value.chars() {
            if c.is_uppercase() {
                return false;
            }
            if c.is_lowercase() {
                has_cased = true;
            }
        }
        has_cased
    }
    
    /// Check if all characters are uppercase
    fn isupper(&self) -> bool {
        let mut has_cased = false;
        for c in self.value.chars() {
            if c.is_lowercase() {
                return false;
            }
            if c.is_uppercase() {
                has_cased = true;
            }
        }
        has_cased
    }
    
    /// Check if all characters are whitespace
    fn isspace(&self) -> bool {
        !self.value.is_empty() && self.value.chars().all(|c| c.is_whitespace())
    }
}

/// Helper function to escape a string
fn escape_string(text: &str) -> String {
    if !text.chars().any(|c| matches!(c, '&' | '<' | '>' | '"' | '\'')) {
        return text.to_string();
    }
    
    let mut result = String::with_capacity(text.len() + text.len() / 4);
    for c in text.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            '\'' => result.push_str("&#x27;"),
            _ => result.push(c),
        }
    }
    result
}

#[pymodule]
fn markupsafe_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(escape, m)?)?;
    m.add_function(wrap_pyfunction!(escape_silent, m)?)?;
    m.add_function(wrap_pyfunction!(soft_unicode, m)?)?;
    m.add_function(wrap_pyfunction!(soft_str, m)?)?;
    m.add_class::<Markup>()?;
    Ok(())
}
