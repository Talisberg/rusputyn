use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyList};
use encoding_rs::Encoding;

/// Encoding detection result
#[pyclass]
#[derive(Clone)]
pub struct CharsetMatch {
    #[pyo3(get)]
    encoding: String,
    #[pyo3(get)]
    confidence: f64,
    #[pyo3(get)]
    language: String,
    decoded: String,
    raw: Vec<u8>,
}

#[pymethods]
impl CharsetMatch {
    fn __str__(&self) -> String {
        self.decoded.clone()
    }
    
    fn __repr__(&self) -> String {
        format!("<CharsetMatch '{}' confidence={:.2}>", self.encoding, self.confidence)
    }
    
    fn output(&self) -> &str {
        &self.decoded
    }
    
    fn raw_bytes<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new_bound(py, &self.raw)
    }
}

/// Encoding detection results collection
#[pyclass]
#[derive(Clone)]
pub struct CharsetMatches {
    matches: Vec<CharsetMatch>,
}

#[pymethods]
impl CharsetMatches {
    fn __len__(&self) -> usize {
        self.matches.len()
    }
    
    fn __bool__(&self) -> bool {
        !self.matches.is_empty()
    }
    
    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<CharsetMatchesIter>> {
        let iter = CharsetMatchesIter {
            inner: slf.matches.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }
    
    fn best(&self) -> Option<CharsetMatch> {
        self.matches.first().cloned()
    }
    
    fn first(&self) -> Option<CharsetMatch> {
        self.best()
    }
}

#[pyclass]
pub struct CharsetMatchesIter {
    inner: std::vec::IntoIter<CharsetMatch>,
}

#[pymethods]
impl CharsetMatchesIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    
    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<CharsetMatch> {
        slf.inner.next()
    }
}

// Encodings to try with their labels
fn get_encodings() -> Vec<(&'static Encoding, &'static str)> {
    vec![
        (encoding_rs::UTF_8, "utf-8"),
        (encoding_rs::WINDOWS_1252, "windows-1252"),
        (encoding_rs::WINDOWS_1251, "windows-1251"),
        (encoding_rs::WINDOWS_1250, "windows-1250"),
        (encoding_rs::WINDOWS_1253, "windows-1253"),
        (encoding_rs::WINDOWS_1254, "windows-1254"),
        (encoding_rs::WINDOWS_1255, "windows-1255"),
        (encoding_rs::WINDOWS_1256, "windows-1256"),
        (encoding_rs::WINDOWS_1257, "windows-1257"),
        (encoding_rs::WINDOWS_1258, "windows-1258"),
        (encoding_rs::ISO_8859_2, "iso-8859-2"),
        (encoding_rs::ISO_8859_3, "iso-8859-3"),
        (encoding_rs::ISO_8859_4, "iso-8859-4"),
        (encoding_rs::ISO_8859_5, "iso-8859-5"),
        (encoding_rs::ISO_8859_6, "iso-8859-6"),
        (encoding_rs::ISO_8859_7, "iso-8859-7"),
        (encoding_rs::ISO_8859_8, "iso-8859-8"),
        (encoding_rs::SHIFT_JIS, "shift_jis"),
        (encoding_rs::EUC_JP, "euc-jp"),
        (encoding_rs::ISO_2022_JP, "iso-2022-jp"),
        (encoding_rs::GB18030, "gb18030"),
        (encoding_rs::GBK, "gbk"),
        (encoding_rs::BIG5, "big5"),
        (encoding_rs::EUC_KR, "euc-kr"),
        (encoding_rs::KOI8_R, "koi8-r"),
        (encoding_rs::KOI8_U, "koi8-u"),
        (encoding_rs::UTF_16LE, "utf-16-le"),
        (encoding_rs::UTF_16BE, "utf-16-be"),
    ]
}

fn calculate_confidence(bytes: &[u8], decoded: &str, had_errors: bool) -> f64 {
    if had_errors {
        return 0.0;
    }
    
    let mut score = 1.0;
    
    let ratio = decoded.len() as f64 / bytes.len().max(1) as f64;
    if ratio < 0.5 || ratio > 2.0 {
        score *= 0.8;
    }
    
    let replacement_count = decoded.chars().filter(|&c| c == '\u{FFFD}').count();
    if replacement_count > 0 {
        score *= 0.5_f64.powi(replacement_count.min(10) as i32);
    }
    
    let printable = decoded.chars().filter(|c| c.is_ascii_graphic() || c.is_ascii_whitespace()).count();
    let printable_ratio = printable as f64 / decoded.len().max(1) as f64;
    score *= 0.5 + 0.5 * printable_ratio;
    
    if decoded.contains(' ') {
        score *= 1.1;
    }
    if decoded.contains('\n') {
        score *= 1.05;
    }
    
    score.min(1.0)
}

fn detect_bom(bytes: &[u8]) -> Option<(&'static str, &'static Encoding)> {
    if bytes.starts_with(&[0xEF, 0xBB, 0xBF]) {
        Some(("utf-8-sig", encoding_rs::UTF_8))
    } else if bytes.starts_with(&[0xFF, 0xFE]) {
        Some(("utf-16-le", encoding_rs::UTF_16LE))
    } else if bytes.starts_with(&[0xFE, 0xFF]) {
        Some(("utf-16-be", encoding_rs::UTF_16BE))
    } else {
        None
    }
}

fn is_valid_utf8(bytes: &[u8]) -> bool {
    std::str::from_utf8(bytes).is_ok()
}

#[pyfunction]
#[pyo3(signature = (byte_str, _steps=5, _chunk_size=512, threshold=0.2, _cp_isolation=None, _cp_exclusion=None, _preemptive_behaviour=true, _explain=false, _language_threshold=0.1, _enable_fallback=true))]
fn from_bytes(
    _py: Python<'_>,
    byte_str: &Bound<'_, PyBytes>,
    _steps: usize,
    _chunk_size: usize,
    threshold: f64,
    _cp_isolation: Option<&Bound<'_, PyList>>,
    _cp_exclusion: Option<&Bound<'_, PyList>>,
    _preemptive_behaviour: bool,
    _explain: bool,
    _language_threshold: f64,
    _enable_fallback: bool,
) -> PyResult<CharsetMatches> {
    let bytes = byte_str.as_bytes();
    let mut matches = Vec::new();
    
    if bytes.is_empty() {
        return Ok(CharsetMatches { matches });
    }
    
    // Check BOM
    if let Some((name, encoding)) = detect_bom(bytes) {
        let (decoded, _, had_errors) = encoding.decode(bytes);
        if !had_errors {
            matches.push(CharsetMatch {
                encoding: name.to_string(),
                confidence: 1.0,
                language: String::new(),
                decoded: decoded.to_string(),
                raw: bytes.to_vec(),
            });
            return Ok(CharsetMatches { matches });
        }
    }
    
    // Fast path: UTF-8
    if is_valid_utf8(bytes) {
        let decoded = unsafe { std::str::from_utf8_unchecked(bytes) };
        let confidence = calculate_confidence(bytes, decoded, false);
        if confidence >= threshold {
            matches.push(CharsetMatch {
                encoding: "utf-8".to_string(),
                confidence,
                language: String::new(),
                decoded: decoded.to_string(),
                raw: bytes.to_vec(),
            });
            if confidence > 0.9 {
                return Ok(CharsetMatches { matches });
            }
        }
    }
    
    // Try other encodings
    for (encoding, name) in get_encodings() {
        if name == "utf-8" {
            continue;
        }
        
        let (decoded, _, had_errors) = encoding.decode(bytes);
        let confidence = calculate_confidence(bytes, &decoded, had_errors);
        
        if confidence >= threshold {
            matches.push(CharsetMatch {
                encoding: name.to_string(),
                confidence,
                language: String::new(),
                decoded: decoded.to_string(),
                raw: bytes.to_vec(),
            });
        }
    }
    
    matches.sort_by(|a, b| b.confidence.partial_cmp(&a.confidence).unwrap());
    
    Ok(CharsetMatches { matches })
}

#[pyfunction]
#[pyo3(signature = (path, _steps=5, _chunk_size=512, threshold=0.2, _cp_isolation=None, _cp_exclusion=None, _preemptive_behaviour=true, _explain=false, _language_threshold=0.1, _enable_fallback=true))]
fn from_path(
    py: Python<'_>,
    path: &str,
    _steps: usize,
    _chunk_size: usize,
    threshold: f64,
    _cp_isolation: Option<&Bound<'_, PyList>>,
    _cp_exclusion: Option<&Bound<'_, PyList>>,
    _preemptive_behaviour: bool,
    _explain: bool,
    _language_threshold: f64,
    _enable_fallback: bool,
) -> PyResult<CharsetMatches> {
    let bytes = std::fs::read(path)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    
    let py_bytes = PyBytes::new_bound(py, &bytes);
    from_bytes(py, &py_bytes, 5, 512, threshold, None, None, true, false, 0.1, true)
}

#[pyfunction]
fn detect(byte_str: &Bound<'_, PyBytes>) -> PyResult<Option<String>> {
    let bytes = byte_str.as_bytes();
    
    if std::str::from_utf8(bytes).is_ok() {
        return Ok(Some("utf-8".to_string()));
    }
    
    for (encoding, name) in get_encodings() {
        let (_, _, had_errors) = encoding.decode(bytes);
        if !had_errors {
            return Ok(Some(name.to_string()));
        }
    }
    
    Ok(None)
}

#[pyfunction]
fn normalize(byte_str: &Bound<'_, PyBytes>) -> PyResult<String> {
    let bytes = byte_str.as_bytes();
    
    if let Ok(s) = std::str::from_utf8(bytes) {
        return Ok(s.to_string());
    }
    
    for (encoding, _) in get_encodings() {
        let (decoded, _, had_errors) = encoding.decode(bytes);
        if !had_errors {
            return Ok(decoded.to_string());
        }
    }
    
    Ok(String::from_utf8_lossy(bytes).to_string())
}

#[pyfunction]
fn is_valid(byte_str: &Bound<'_, PyBytes>, encoding_name: &str) -> bool {
    let bytes = byte_str.as_bytes();
    
    let encoding = match Encoding::for_label(encoding_name.as_bytes()) {
        Some(enc) => enc,
        None => return false,
    };
    
    let (_, _, had_errors) = encoding.decode(bytes);
    !had_errors
}

#[pymodule]
fn charset_normalizer_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CharsetMatch>()?;
    m.add_class::<CharsetMatches>()?;
    m.add_function(wrap_pyfunction!(from_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(from_path, m)?)?;
    m.add_function(wrap_pyfunction!(detect, m)?)?;
    m.add_function(wrap_pyfunction!(normalize, m)?)?;
    m.add_function(wrap_pyfunction!(is_valid, m)?)?;
    Ok(())
}
