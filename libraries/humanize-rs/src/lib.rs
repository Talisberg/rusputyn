use pyo3::prelude::*;
use num_format::{Locale, ToFormattedString};

/// Format a number with comma separators
/// humanize.intcomma(1000000) -> "1,000,000"
#[pyfunction]
#[pyo3(signature = (value, ndigits=None))]
fn intcomma(value: i64, ndigits: Option<i32>) -> String {
    match ndigits {
        Some(n) if n > 0 => {
            let factor = 10_f64.powi(n);
            let rounded = (value as f64 / factor).round() * factor;
            (rounded as i64).to_formatted_string(&Locale::en)
        }
        _ => value.to_formatted_string(&Locale::en),
    }
}

/// Convert a number to its ordinal form
/// humanize.ordinal(3) -> "3rd"
#[pyfunction]
fn ordinal(value: i64) -> String {
    let suffix = match (value % 10, value % 100) {
        (1, 11) => "th",
        (2, 12) => "th",
        (3, 13) => "th",
        (1, _) => "st",
        (2, _) => "nd",
        (3, _) => "rd",
        _ => "th",
    };
    format!("{}{}", value, suffix)
}

/// Convert a number to its word form
/// humanize.intword(1_000_000) -> "1.0 million"
#[pyfunction]
#[pyo3(signature = (value, format_str=None))]
fn intword(value: i64, format_str: Option<&str>) -> String {
    let fmt = format_str.unwrap_or("%.1f");
    
    let (divisor, suffix): (f64, &str) = if value.abs() >= 1_000_000_000_000_000 {
        (1_000_000_000_000_000.0, "quadrillion")
    } else if value.abs() >= 1_000_000_000_000 {
        (1_000_000_000_000.0, "trillion")
    } else if value.abs() >= 1_000_000_000 {
        (1_000_000_000.0, "billion")
    } else if value.abs() >= 1_000_000 {
        (1_000_000.0, "million")
    } else {
        return value.to_formatted_string(&Locale::en);
    };
    
    let num = value as f64 / divisor;
    
    // Parse format string for precision
    let precision = if fmt.contains('.') {
        fmt.chars()
            .skip_while(|c| *c != '.')
            .skip(1)
            .take_while(|c| c.is_ascii_digit())
            .collect::<String>()
            .parse::<usize>()
            .unwrap_or(1)
    } else {
        1
    };
    
    format!("{:.prec$} {}", num, suffix, prec = precision)
}

const SUFFIXES: &[&str] = &["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
const BINARY_SUFFIXES: &[&str] = &["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];

/// Convert a file size to human readable form
/// humanize.naturalsize(1048576) -> "1.0 MB"
#[pyfunction]
#[pyo3(signature = (value, binary=false, gnu=false, format_str=None))]
fn naturalsize(value: i64, binary: bool, gnu: bool, format_str: Option<&str>) -> String {
    let fmt = format_str.unwrap_or("%.1f");
    let base: f64 = if binary { 1024.0 } else { 1000.0 };
    let suffixes = if binary { BINARY_SUFFIXES } else { SUFFIXES };
    
    let abs_value = value.abs() as f64;
    
    if abs_value < base {
        if gnu {
            return format!("{}B", value);
        }
        return format!("{} Bytes", value);
    }
    
    let mut unit_idx = 0;
    let mut size = abs_value;
    
    while size >= base && unit_idx < suffixes.len() - 1 {
        size /= base;
        unit_idx += 1;
    }
    
    if value < 0 {
        size = -size;
    }
    
    // Parse format string for precision
    let precision = if fmt.contains('.') {
        fmt.chars()
            .skip_while(|c| *c != '.')
            .skip(1)
            .take_while(|c| c.is_ascii_digit())
            .collect::<String>()
            .parse::<usize>()
            .unwrap_or(1)
    } else {
        1
    };
    
    let suffix = if gnu {
        &suffixes[unit_idx][..1] // Just the first letter for GNU style
    } else {
        suffixes[unit_idx]
    };
    
    if gnu {
        format!("{:.prec$}{}", size, suffix, prec = precision)
    } else {
        format!("{:.prec$} {}", size, suffix, prec = precision)
    }
}

/// Convert a fractional number to a string
/// humanize.fractional(0.5) -> "1/2"
#[pyfunction]
fn fractional(value: f64) -> String {
    // Common fractions to check
    let fractions = [
        (1.0 / 8.0, "⅛"),
        (1.0 / 4.0, "¼"),
        (1.0 / 3.0, "⅓"),
        (3.0 / 8.0, "⅜"),
        (1.0 / 2.0, "½"),
        (5.0 / 8.0, "⅝"),
        (2.0 / 3.0, "⅔"),
        (3.0 / 4.0, "¾"),
        (7.0 / 8.0, "⅞"),
    ];
    
    let whole = value.trunc() as i64;
    let frac = value.fract().abs();
    
    if frac < 0.0001 {
        return whole.to_string();
    }
    
    // Find closest fraction
    let mut closest = "";
    let mut min_diff = f64::MAX;
    
    for (f, s) in fractions.iter() {
        let diff = (frac - f).abs();
        if diff < min_diff {
            min_diff = diff;
            closest = s;
        }
    }
    
    if min_diff > 0.05 {
        // No close match, return decimal
        return format!("{:.2}", value);
    }
    
    if whole == 0 {
        closest.to_string()
    } else {
        format!("{}{}", whole, closest)
    }
}

/// Convert a boolean to "yes" or "no"
#[pyfunction]
fn apnumber(value: i64) -> String {
    match value {
        1 => "one".to_string(),
        2 => "two".to_string(),
        3 => "three".to_string(),
        4 => "four".to_string(),
        5 => "five".to_string(),
        6 => "six".to_string(),
        7 => "seven".to_string(),
        8 => "eight".to_string(),
        9 => "nine".to_string(),
        _ => value.to_formatted_string(&Locale::en),
    }
}

/// Convert scientific notation to decimal
#[pyfunction]
fn scientific(value: f64, precision: Option<usize>) -> String {
    let prec = precision.unwrap_or(2);
    format!("{:.prec$e}", value, prec = prec)
        .replace("e", " x 10^")
        .replace("x 10^0", "")
        .replace("x 10^+", "x 10^")
}

/// A Python module implemented in Rust
#[pymodule]
fn humanize_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(intcomma, m)?)?;
    m.add_function(wrap_pyfunction!(ordinal, m)?)?;
    m.add_function(wrap_pyfunction!(intword, m)?)?;
    m.add_function(wrap_pyfunction!(naturalsize, m)?)?;
    m.add_function(wrap_pyfunction!(fractional, m)?)?;
    m.add_function(wrap_pyfunction!(apnumber, m)?)?;
    m.add_function(wrap_pyfunction!(scientific, m)?)?;
    Ok(())
}
