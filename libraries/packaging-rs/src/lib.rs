use once_cell::sync::Lazy;
use pyo3::prelude::*;
use regex::Regex;
use std::cmp::Ordering;

// PEP 440 version regex
static VERSION_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(?ix)
        ^
        v?
        (?:
            (?P<epoch>[0-9]+)!
        )?
        (?P<release>[0-9]+(?:\.[0-9]+)*)
        (?:
            [-_\.]?
            (?P<pre>
                (?:a|alpha|b|beta|c|rc|pre|preview)
                [-_\.]?
                (?P<pre_num>[0-9]+)?
            )
        )?
        (?:
            (?:-(?P<post_num1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?:post|rev|r)
                [-_\.]?
                (?P<post_num2>[0-9]+)?
            )
        )?
        (?:
            [-_\.]?
            (?:dev)
            [-_\.]?
            (?P<dev_num>[0-9]+)?
        )?
        (?:
            \+
            (?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*)
        )?
        $
    ").unwrap()
});

/// Parsed version components
#[derive(Clone, Debug, PartialEq, Eq)]
struct VersionParts {
    epoch: u32,
    release: Vec<u32>,
    pre: Option<(String, u32)>,
    post: Option<u32>,
    dev: Option<u32>,
    local: Option<String>,
}

impl PartialOrd for VersionParts {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for VersionParts {
    fn cmp(&self, other: &Self) -> Ordering {
        // Compare epoch first
        match self.epoch.cmp(&other.epoch) {
            Ordering::Equal => {}
            ord => return ord,
        }
        
        // Compare release segments
        let max_len = self.release.len().max(other.release.len());
        for i in 0..max_len {
            let a = self.release.get(i).copied().unwrap_or(0);
            let b = other.release.get(i).copied().unwrap_or(0);
            match a.cmp(&b) {
                Ordering::Equal => {}
                ord => return ord,
            }
        }
        
        // Pre-release (dev < pre < no-pre < post)
        match (&self.dev, &self.pre, &self.post, &other.dev, &other.pre, &other.post) {
            // Both have dev
            (Some(a), None, None, Some(b), None, None) => return a.cmp(b),
            // Self has dev, other doesn't
            (Some(_), _, _, None, _, _) => return Ordering::Less,
            // Other has dev, self doesn't
            (None, _, _, Some(_), _, _) => return Ordering::Greater,
            _ => {}
        }
        
        // Pre-release comparison
        match (&self.pre, &other.pre) {
            (Some((a_type, a_num)), Some((b_type, b_num))) => {
                let a_ord = pre_type_order(a_type);
                let b_ord = pre_type_order(b_type);
                match a_ord.cmp(&b_ord) {
                    Ordering::Equal => match a_num.cmp(b_num) {
                        Ordering::Equal => {}
                        ord => return ord,
                    },
                    ord => return ord,
                }
            }
            (Some(_), None) => return Ordering::Less,
            (None, Some(_)) => return Ordering::Greater,
            (None, None) => {}
        }
        
        // Post-release comparison
        match (&self.post, &other.post) {
            (Some(a), Some(b)) => match a.cmp(b) {
                Ordering::Equal => {}
                ord => return ord,
            },
            (Some(_), None) => return Ordering::Greater,
            (None, Some(_)) => return Ordering::Less,
            (None, None) => {}
        }
        
        Ordering::Equal
    }
}

fn pre_type_order(pre_type: &str) -> u32 {
    match pre_type.to_lowercase().as_str() {
        "a" | "alpha" => 0,
        "b" | "beta" => 1,
        "c" | "rc" | "pre" | "preview" => 2,
        _ => 3,
    }
}

fn parse_version_parts(version: &str) -> Option<VersionParts> {
    let caps = VERSION_REGEX.captures(version)?;
    
    let epoch = caps.name("epoch")
        .map(|m| m.as_str().parse().unwrap_or(0))
        .unwrap_or(0);
    
    let release: Vec<u32> = caps.name("release")?
        .as_str()
        .split('.')
        .filter_map(|s| s.parse().ok())
        .collect();
    
    let pre = caps.name("pre").map(|m| {
        let pre_str = m.as_str().to_lowercase();
        let pre_type = if pre_str.starts_with("a") || pre_str.starts_with("alpha") {
            "a".to_string()
        } else if pre_str.starts_with("b") || pre_str.starts_with("beta") {
            "b".to_string()
        } else {
            "rc".to_string()
        };
        let pre_num = caps.name("pre_num")
            .map(|m| m.as_str().parse().unwrap_or(0))
            .unwrap_or(0);
        (pre_type, pre_num)
    });
    
    let post = caps.name("post_num1")
        .or_else(|| caps.name("post_num2"))
        .map(|m| m.as_str().parse().unwrap_or(0));
    
    let dev = caps.name("dev_num")
        .map(|m| m.as_str().parse().unwrap_or(0));
    
    let local = caps.name("local")
        .map(|m| m.as_str().to_string());
    
    Some(VersionParts {
        epoch,
        release,
        pre,
        post,
        dev,
        local,
    })
}

/// Python Version class
#[pyclass]
#[derive(Clone)]
pub struct Version {
    original: String,
    parts: VersionParts,
}

#[pymethods]
impl Version {
    #[new]
    fn new(version: &str) -> PyResult<Self> {
        let parts = parse_version_parts(version)
            .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(
                format!("Invalid version: {}", version)
            ))?;
        
        Ok(Version {
            original: version.to_string(),
            parts,
        })
    }
    
    fn __str__(&self) -> String {
        self.original.clone()
    }
    
    fn __repr__(&self) -> String {
        format!("<Version('{}')>", self.original)
    }
    
    fn __hash__(&self) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        self.original.hash(&mut hasher);
        hasher.finish()
    }
    
    fn __eq__(&self, other: &Version) -> bool {
        self.parts == other.parts
    }
    
    fn __lt__(&self, other: &Version) -> bool {
        self.parts < other.parts
    }
    
    fn __le__(&self, other: &Version) -> bool {
        self.parts <= other.parts
    }
    
    fn __gt__(&self, other: &Version) -> bool {
        self.parts > other.parts
    }
    
    fn __ge__(&self, other: &Version) -> bool {
        self.parts >= other.parts
    }
    
    #[getter]
    fn epoch(&self) -> u32 {
        self.parts.epoch
    }
    
    #[getter]
    fn release(&self) -> Vec<u32> {
        self.parts.release.clone()
    }
    
    #[getter]
    fn major(&self) -> u32 {
        self.parts.release.first().copied().unwrap_or(0)
    }
    
    #[getter]
    fn minor(&self) -> u32 {
        self.parts.release.get(1).copied().unwrap_or(0)
    }
    
    #[getter]
    fn micro(&self) -> u32 {
        self.parts.release.get(2).copied().unwrap_or(0)
    }
    
    #[getter]
    fn pre(&self) -> Option<(String, u32)> {
        self.parts.pre.clone()
    }
    
    #[getter]
    fn post(&self) -> Option<u32> {
        self.parts.post
    }
    
    #[getter]
    fn dev(&self) -> Option<u32> {
        self.parts.dev
    }
    
    #[getter]
    fn local(&self) -> Option<String> {
        self.parts.local.clone()
    }
    
    #[getter]
    fn is_prerelease(&self) -> bool {
        self.parts.pre.is_some() || self.parts.dev.is_some()
    }
    
    #[getter]
    fn is_postrelease(&self) -> bool {
        self.parts.post.is_some()
    }
    
    #[getter]
    fn is_devrelease(&self) -> bool {
        self.parts.dev.is_some()
    }
    
    #[getter]
    fn public(&self) -> String {
        let mut result = String::new();
        
        if self.parts.epoch > 0 {
            result.push_str(&format!("{}!", self.parts.epoch));
        }
        
        result.push_str(&self.parts.release.iter()
            .map(|n| n.to_string())
            .collect::<Vec<_>>()
            .join("."));
        
        if let Some((pre_type, pre_num)) = &self.parts.pre {
            result.push_str(&format!("{}{}", pre_type, pre_num));
        }
        
        if let Some(post) = self.parts.post {
            result.push_str(&format!(".post{}", post));
        }
        
        if let Some(dev) = self.parts.dev {
            result.push_str(&format!(".dev{}", dev));
        }
        
        result
    }
    
    #[getter]
    fn base_version(&self) -> String {
        let mut result = String::new();
        
        if self.parts.epoch > 0 {
            result.push_str(&format!("{}!", self.parts.epoch));
        }
        
        result.push_str(&self.parts.release.iter()
            .map(|n| n.to_string())
            .collect::<Vec<_>>()
            .join("."));
        
        result
    }
}

/// Parse a version string
#[pyfunction]
fn parse(version: &str) -> PyResult<Version> {
    Version::new(version)
}

/// Check if a version string is valid
#[pyfunction]
fn is_valid_version(version: &str) -> bool {
    parse_version_parts(version).is_some()
}

/// Canonicalize a version string
#[pyfunction]
fn canonicalize_version(version: &str) -> PyResult<String> {
    let v = Version::new(version)?;
    Ok(v.public())
}

/// Python module
#[pymodule]
fn packaging_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Version>()?;
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(is_valid_version, m)?)?;
    m.add_function(wrap_pyfunction!(canonicalize_version, m)?)?;
    Ok(())
}
