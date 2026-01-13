use chrono::{Datelike, Local};
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;

// Month name mappings
static MONTHS: Lazy<HashMap<&'static str, u32>> = Lazy::new(|| {
    let mut m = HashMap::new();
    m.insert("jan", 1); m.insert("january", 1);
    m.insert("feb", 2); m.insert("february", 2);
    m.insert("mar", 3); m.insert("march", 3);
    m.insert("apr", 4); m.insert("april", 4);
    m.insert("may", 5);
    m.insert("jun", 6); m.insert("june", 6);
    m.insert("jul", 7); m.insert("july", 7);
    m.insert("aug", 8); m.insert("august", 8);
    m.insert("sep", 9); m.insert("sept", 9); m.insert("september", 9);
    m.insert("oct", 10); m.insert("october", 10);
    m.insert("nov", 11); m.insert("november", 11);
    m.insert("dec", 12); m.insert("december", 12);
    m
});

// Timezone abbreviations (common ones)
static TZOFFSETS: Lazy<HashMap<&'static str, i32>> = Lazy::new(|| {
    let mut m = HashMap::new();
    m.insert("utc", 0);
    m.insert("gmt", 0);
    m.insert("z", 0);
    m.insert("est", -5 * 3600);
    m.insert("edt", -4 * 3600);
    m.insert("cst", -6 * 3600);
    m.insert("cdt", -5 * 3600);
    m.insert("mst", -7 * 3600);
    m.insert("mdt", -6 * 3600);
    m.insert("pst", -8 * 3600);
    m.insert("pdt", -7 * 3600);
    m
});

// Pre-compiled regex patterns
static ISO_DATETIME: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(?:Z|([+-])(\d{2}):?(\d{2}))?$").unwrap()
});

static ISO_DATE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^(\d{4})-(\d{2})-(\d{2})$").unwrap()
});

static US_DATE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})$").unwrap()
});

static EU_DATE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$").unwrap()
});

static TIME_12H: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|AM|PM)").unwrap()
});

static TIME_24H: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(\d{1,2}):(\d{2})(?::(\d{2}))?(?:\.(\d+))?").unwrap()
});

static MONTH_DAY_YEAR: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(?i)([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})").unwrap()
});

static DAY_MONTH_YEAR: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(?i)(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+),?\s+(\d{4})").unwrap()
});

static TIMEZONE_OFFSET: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"([+-])(\d{2}):?(\d{2})$").unwrap()
});

fn parse_year(s: &str) -> Option<i32> {
    let year: i32 = s.parse().ok()?;
    if year < 100 {
        // Two-digit year
        if year >= 69 {
            Some(1900 + year)
        } else {
            Some(2000 + year)
        }
    } else {
        Some(year)
    }
}

fn parse_month_name(s: &str) -> Option<u32> {
    MONTHS.get(s.to_lowercase().as_str()).copied()
}

struct ParsedDateTime {
    year: i32,
    month: u32,
    day: u32,
    hour: u32,
    minute: u32,
    second: u32,
    microsecond: u32,
    tz_offset: Option<i32>, // seconds
}

impl ParsedDateTime {
    fn new() -> Self {
        let now = Local::now();
        Self {
            year: now.year(),
            month: now.month(),
            day: now.day(),
            hour: 0,
            minute: 0,
            second: 0,
            microsecond: 0,
            tz_offset: None,
        }
    }
}

fn parse_datetime_str(s: &str, dayfirst: bool, _yearfirst: bool) -> Option<ParsedDateTime> {
    let s = s.trim();
    let mut result = ParsedDateTime::new();
    
    // Try ISO format first (most common)
    if let Some(caps) = ISO_DATETIME.captures(s) {
        result.year = caps.get(1)?.as_str().parse().ok()?;
        result.month = caps.get(2)?.as_str().parse().ok()?;
        result.day = caps.get(3)?.as_str().parse().ok()?;
        result.hour = caps.get(4)?.as_str().parse().ok()?;
        result.minute = caps.get(5)?.as_str().parse().ok()?;
        result.second = caps.get(6)?.as_str().parse().ok()?;
        
        if let Some(frac) = caps.get(7) {
            let frac_str = frac.as_str();
            let padded = format!("{:0<6}", &frac_str[..frac_str.len().min(6)]);
            result.microsecond = padded.parse().unwrap_or(0);
        }
        
        // Handle timezone
        if s.ends_with('Z') || s.ends_with('z') {
            result.tz_offset = Some(0);
        } else if let (Some(sign), Some(h), Some(m)) = (caps.get(8), caps.get(9), caps.get(10)) {
            let hours: i32 = h.as_str().parse().ok()?;
            let mins: i32 = m.as_str().parse().ok()?;
            let offset = hours * 3600 + mins * 60;
            result.tz_offset = Some(if sign.as_str() == "-" { -offset } else { offset });
        }
        
        return Some(result);
    }
    
    // Try ISO date only
    if let Some(caps) = ISO_DATE.captures(s) {
        result.year = caps.get(1)?.as_str().parse().ok()?;
        result.month = caps.get(2)?.as_str().parse().ok()?;
        result.day = caps.get(3)?.as_str().parse().ok()?;
        return Some(result);
    }
    
    // Try US format MM/DD/YYYY
    if let Some(caps) = US_DATE.captures(s) {
        let first: u32 = caps.get(1)?.as_str().parse().ok()?;
        let second: u32 = caps.get(2)?.as_str().parse().ok()?;
        result.year = parse_year(caps.get(3)?.as_str())?;
        
        if dayfirst {
            result.day = first;
            result.month = second;
        } else {
            result.month = first;
            result.day = second;
        }
        return Some(result);
    }
    
    // Try European format DD.MM.YYYY
    if let Some(caps) = EU_DATE.captures(s) {
        let first: u32 = caps.get(1)?.as_str().parse().ok()?;
        let second: u32 = caps.get(2)?.as_str().parse().ok()?;
        result.year = parse_year(caps.get(3)?.as_str())?;
        
        if dayfirst {
            result.day = first;
            result.month = second;
        } else {
            result.month = first;
            result.day = second;
        }
        return Some(result);
    }
    
    // Try "Month Day, Year" format
    if let Some(caps) = MONTH_DAY_YEAR.captures(s) {
        result.month = parse_month_name(caps.get(1)?.as_str())?;
        result.day = caps.get(2)?.as_str().parse().ok()?;
        result.year = caps.get(3)?.as_str().parse().ok()?;
        
        // Check for time portion
        let remaining = &s[caps.get(0)?.end()..];
        if let Some(time_caps) = TIME_12H.captures(remaining) {
            result.hour = time_caps.get(1)?.as_str().parse().ok()?;
            result.minute = time_caps.get(2)?.as_str().parse().ok()?;
            if let Some(sec) = time_caps.get(3) {
                result.second = sec.as_str().parse().ok()?;
            }
            let ampm = time_caps.get(4)?.as_str().to_lowercase();
            if ampm == "pm" && result.hour != 12 {
                result.hour += 12;
            } else if ampm == "am" && result.hour == 12 {
                result.hour = 0;
            }
        } else if let Some(time_caps) = TIME_24H.captures(remaining) {
            result.hour = time_caps.get(1)?.as_str().parse().ok()?;
            result.minute = time_caps.get(2)?.as_str().parse().ok()?;
            if let Some(sec) = time_caps.get(3) {
                result.second = sec.as_str().parse().ok()?;
            }
        }
        
        return Some(result);
    }
    
    // Try "Day Month Year" format
    if let Some(caps) = DAY_MONTH_YEAR.captures(s) {
        result.day = caps.get(1)?.as_str().parse().ok()?;
        result.month = parse_month_name(caps.get(2)?.as_str())?;
        result.year = caps.get(3)?.as_str().parse().ok()?;
        return Some(result);
    }
    
    None
}

/// Parse a datetime string into a Python datetime object
/// dateutil.parser.parse("2023-01-15 14:30:00") -> datetime(2023, 1, 15, 14, 30, 0)
#[pyfunction]
#[pyo3(signature = (timestr, parserinfo=None, dayfirst=false, yearfirst=false, fuzzy=false, fuzzy_with_tokens=false, default=None, ignoretz=false, tzinfos=None))]
fn parse(
    py: Python<'_>,
    timestr: &str,
    parserinfo: Option<&Bound<'_, PyAny>>,
    dayfirst: bool,
    yearfirst: bool,
    fuzzy: bool,
    fuzzy_with_tokens: bool,
    default: Option<&Bound<'_, PyAny>>,
    ignoretz: bool,
    tzinfos: Option<&Bound<'_, PyAny>>,
) -> PyResult<PyObject> {
    let _ = (parserinfo, fuzzy, fuzzy_with_tokens, default, ignoretz, tzinfos); // TODO: implement these

    let parsed = parse_datetime_str(timestr, dayfirst, yearfirst)
        .ok_or_else(|| pyo3::exceptions::PyValueError::new_err(
            format!("Unable to parse datetime string: {}", timestr)
        ))?;

    // Validate
    if parsed.month < 1 || parsed.month > 12 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid month"));
    }
    if parsed.day < 1 || parsed.day > 31 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid day"));
    }

    // Create Python datetime using the datetime module
    let datetime_mod = py.import_bound("datetime")?;
    let datetime_cls = datetime_mod.getattr("datetime")?;

    let dt = datetime_cls.call1((
        parsed.year,
        parsed.month,
        parsed.day,
        parsed.hour,
        parsed.minute,
        parsed.second,
        parsed.microsecond,
    ))?;

    Ok(dt.into())
}

/// Parse an ISO format datetime string (fast path)
#[pyfunction]
fn isoparse(py: Python<'_>, timestr: &str) -> PyResult<PyObject> {
    parse(py, timestr, None, false, false, false, false, None, false, None)
}

/// A Python module implemented in Rust
#[pymodule]
fn dateutil_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(isoparse, m)?)?;
    Ok(())
}
