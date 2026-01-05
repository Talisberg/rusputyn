use once_cell::sync::Lazy;
use pyo3::prelude::*;
use regex::Regex;
use std::net::{Ipv4Addr, Ipv6Addr};

// Pre-compiled regex patterns for performance
static EMAIL_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    ).unwrap()
});

static SLUG_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[-a-zA-Z0-9_]+$").unwrap()
});

static UUID_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$").unwrap()
});

static MD5_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[a-fA-F0-9]{32}$").unwrap()
});

static SHA1_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[a-fA-F0-9]{40}$").unwrap()
});

static SHA256_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[a-fA-F0-9]{64}$").unwrap()
});

static SHA512_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[a-fA-F0-9]{128}$").unwrap()
});

static MAC_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$").unwrap()
});

/// Validate an email address
/// validators.email("test@example.com") -> True
#[pyfunction]
fn email(value: &str) -> bool {
    if value.is_empty() || value.len() > 254 {
        return false;
    }
    EMAIL_REGEX.is_match(value)
}

static URL_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(
        r"^(https?|ftps?)://[^\s/$.?#].[^\s]*$"
    ).unwrap()
});

/// Validate a URL
/// validators.url("https://example.com") -> True
#[pyfunction]
#[pyo3(signature = (value, public=false))]
fn url(value: &str, public: bool) -> bool {
    if !URL_REGEX.is_match(value) {
        return false;
    }
    
    if public {
        // Check if it's not a private IP/localhost
        let lower = value.to_lowercase();
        if lower.contains("localhost") || 
           lower.contains("127.0.0.1") || 
           lower.contains("192.168.") || 
           lower.contains("10.0.") ||
           lower.contains("172.16.") {
            return false;
        }
    }
    true
}

/// Validate a domain name
/// validators.domain("example.com") -> True
#[pyfunction]
fn domain(value: &str) -> bool {
    if value.is_empty() || value.len() > 253 {
        return false;
    }
    
    // Check for valid characters and structure
    let parts: Vec<&str> = value.split('.').collect();
    if parts.len() < 2 {
        return false;
    }
    
    for part in &parts {
        if part.is_empty() || part.len() > 63 {
            return false;
        }
        if part.starts_with('-') || part.ends_with('-') {
            return false;
        }
        if !part.chars().all(|c| c.is_ascii_alphanumeric() || c == '-') {
            return false;
        }
    }
    
    // TLD must be alphabetic
    let tld = parts.last().unwrap();
    if !tld.chars().all(|c| c.is_ascii_alphabetic()) {
        return false;
    }
    
    true
}

/// Validate an IPv4 address
/// validators.ipv4("192.168.1.1") -> True
#[pyfunction]
fn ipv4(value: &str) -> bool {
    value.parse::<Ipv4Addr>().is_ok()
}

/// Validate an IPv6 address
/// validators.ipv6("::1") -> True
#[pyfunction]
fn ipv6(value: &str) -> bool {
    value.parse::<Ipv6Addr>().is_ok()
}

/// Validate an IP address (v4 or v6)
/// validators.ip_address("192.168.1.1") -> True
#[pyfunction]
fn ip_address(value: &str) -> bool {
    ipv4(value) || ipv6(value)
}

/// Validate a slug
/// validators.slug("my-slug-123") -> True
#[pyfunction]
fn slug(value: &str) -> bool {
    if value.is_empty() {
        return false;
    }
    SLUG_REGEX.is_match(value)
}

/// Validate a UUID
/// validators.uuid("550e8400-e29b-41d4-a716-446655440000") -> True
#[pyfunction]
fn uuid(value: &str) -> bool {
    UUID_REGEX.is_match(value)
}

/// Validate an MD5 hash
/// validators.md5("d41d8cd98f00b204e9800998ecf8427e") -> True
#[pyfunction]
fn md5(value: &str) -> bool {
    MD5_REGEX.is_match(value)
}

/// Validate a SHA1 hash
#[pyfunction]
fn sha1(value: &str) -> bool {
    SHA1_REGEX.is_match(value)
}

/// Validate a SHA256 hash
#[pyfunction]
fn sha256(value: &str) -> bool {
    SHA256_REGEX.is_match(value)
}

/// Validate a SHA512 hash
#[pyfunction]
fn sha512(value: &str) -> bool {
    SHA512_REGEX.is_match(value)
}

/// Validate a MAC address
/// validators.mac_address("01:23:45:67:89:AB") -> True
#[pyfunction]
fn mac_address(value: &str) -> bool {
    MAC_REGEX.is_match(value)
}

/// Validate a value is between min and max
/// validators.between(5, min=1, max=10) -> True
#[pyfunction]
#[pyo3(signature = (value, min=None, max=None))]
fn between(value: f64, min: Option<f64>, max: Option<f64>) -> bool {
    if let Some(min_val) = min {
        if value < min_val {
            return false;
        }
    }
    if let Some(max_val) = max {
        if value > max_val {
            return false;
        }
    }
    true
}

/// Validate string length
/// validators.length("hello", min=1, max=10) -> True
#[pyfunction]
#[pyo3(signature = (value, min=None, max=None))]
fn length(value: &str, min: Option<usize>, max: Option<usize>) -> bool {
    let len = value.len();
    if let Some(min_val) = min {
        if len < min_val {
            return false;
        }
    }
    if let Some(max_val) = max {
        if len > max_val {
            return false;
        }
    }
    true
}

/// Validate a credit card number using Luhn algorithm
/// validators.card_number("4111111111111111") -> True
#[pyfunction]
fn card_number(value: &str) -> bool {
    // Remove spaces and dashes
    let clean: String = value.chars().filter(|c| c.is_ascii_digit()).collect();
    
    if clean.len() < 13 || clean.len() > 19 {
        return false;
    }
    
    // Luhn algorithm
    let mut sum = 0;
    let mut double = false;
    
    for c in clean.chars().rev() {
        if let Some(digit) = c.to_digit(10) {
            let mut d = digit;
            if double {
                d *= 2;
                if d > 9 {
                    d -= 9;
                }
            }
            sum += d;
            double = !double;
        } else {
            return false;
        }
    }
    
    sum % 10 == 0
}

/// Validate an IBAN
#[pyfunction]
fn iban(value: &str) -> bool {
    let clean: String = value.chars().filter(|c| !c.is_whitespace()).collect();
    
    if clean.len() < 15 || clean.len() > 34 {
        return false;
    }
    
    // Check country code (first 2 chars should be letters)
    let country: String = clean.chars().take(2).collect();
    if !country.chars().all(|c| c.is_ascii_alphabetic()) {
        return false;
    }
    
    // Check digits (chars 3-4)
    let check: String = clean.chars().skip(2).take(2).collect();
    if !check.chars().all(|c| c.is_ascii_digit()) {
        return false;
    }
    
    // Rest should be alphanumeric
    let rest: String = clean.chars().skip(4).collect();
    if !rest.chars().all(|c| c.is_ascii_alphanumeric()) {
        return false;
    }
    
    // Full IBAN validation would require mod-97 check
    // This is a simplified version
    true
}

/// A Python module implemented in Rust
#[pymodule]
fn validators_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(email, m)?)?;
    m.add_function(wrap_pyfunction!(url, m)?)?;
    m.add_function(wrap_pyfunction!(domain, m)?)?;
    m.add_function(wrap_pyfunction!(ipv4, m)?)?;
    m.add_function(wrap_pyfunction!(ipv6, m)?)?;
    m.add_function(wrap_pyfunction!(ip_address, m)?)?;
    m.add_function(wrap_pyfunction!(slug, m)?)?;
    m.add_function(wrap_pyfunction!(uuid, m)?)?;
    m.add_function(wrap_pyfunction!(md5, m)?)?;
    m.add_function(wrap_pyfunction!(sha1, m)?)?;
    m.add_function(wrap_pyfunction!(sha256, m)?)?;
    m.add_function(wrap_pyfunction!(sha512, m)?)?;
    m.add_function(wrap_pyfunction!(mac_address, m)?)?;
    m.add_function(wrap_pyfunction!(between, m)?)?;
    m.add_function(wrap_pyfunction!(length, m)?)?;
    m.add_function(wrap_pyfunction!(card_number, m)?)?;
    m.add_function(wrap_pyfunction!(iban, m)?)?;
    Ok(())
}
