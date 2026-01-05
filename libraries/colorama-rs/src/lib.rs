use pyo3::prelude::*;

// ANSI escape code constants
const CSI: &str = "\x1b[";
const OSC: &str = "\x1b]";
const BEL: &str = "\x07";

// Fore colors
const FORE_BLACK: &str = "\x1b[30m";
const FORE_RED: &str = "\x1b[31m";
const FORE_GREEN: &str = "\x1b[32m";
const FORE_YELLOW: &str = "\x1b[33m";
const FORE_BLUE: &str = "\x1b[34m";
const FORE_MAGENTA: &str = "\x1b[35m";
const FORE_CYAN: &str = "\x1b[36m";
const FORE_WHITE: &str = "\x1b[37m";
const FORE_RESET: &str = "\x1b[39m";

// Light fore colors
const FORE_LIGHTBLACK_EX: &str = "\x1b[90m";
const FORE_LIGHTRED_EX: &str = "\x1b[91m";
const FORE_LIGHTGREEN_EX: &str = "\x1b[92m";
const FORE_LIGHTYELLOW_EX: &str = "\x1b[93m";
const FORE_LIGHTBLUE_EX: &str = "\x1b[94m";
const FORE_LIGHTMAGENTA_EX: &str = "\x1b[95m";
const FORE_LIGHTCYAN_EX: &str = "\x1b[96m";
const FORE_LIGHTWHITE_EX: &str = "\x1b[97m";

// Back colors
const BACK_BLACK: &str = "\x1b[40m";
const BACK_RED: &str = "\x1b[41m";
const BACK_GREEN: &str = "\x1b[42m";
const BACK_YELLOW: &str = "\x1b[43m";
const BACK_BLUE: &str = "\x1b[44m";
const BACK_MAGENTA: &str = "\x1b[45m";
const BACK_CYAN: &str = "\x1b[46m";
const BACK_WHITE: &str = "\x1b[47m";
const BACK_RESET: &str = "\x1b[49m";

// Light back colors
const BACK_LIGHTBLACK_EX: &str = "\x1b[100m";
const BACK_LIGHTRED_EX: &str = "\x1b[101m";
const BACK_LIGHTGREEN_EX: &str = "\x1b[102m";
const BACK_LIGHTYELLOW_EX: &str = "\x1b[103m";
const BACK_LIGHTBLUE_EX: &str = "\x1b[104m";
const BACK_LIGHTMAGENTA_EX: &str = "\x1b[105m";
const BACK_LIGHTCYAN_EX: &str = "\x1b[106m";
const BACK_LIGHTWHITE_EX: &str = "\x1b[107m";

// Style
const STYLE_DIM: &str = "\x1b[2m";
const STYLE_NORMAL: &str = "\x1b[22m";
const STYLE_BRIGHT: &str = "\x1b[1m";
const STYLE_RESET_ALL: &str = "\x1b[0m";

/// Fore color codes module
#[pyclass(frozen)]
#[derive(Clone)]
pub struct Fore;

#[pymethods]
impl Fore {
    #[classattr]
    const BLACK: &'static str = FORE_BLACK;
    #[classattr]
    const RED: &'static str = FORE_RED;
    #[classattr]
    const GREEN: &'static str = FORE_GREEN;
    #[classattr]
    const YELLOW: &'static str = FORE_YELLOW;
    #[classattr]
    const BLUE: &'static str = FORE_BLUE;
    #[classattr]
    const MAGENTA: &'static str = FORE_MAGENTA;
    #[classattr]
    const CYAN: &'static str = FORE_CYAN;
    #[classattr]
    const WHITE: &'static str = FORE_WHITE;
    #[classattr]
    const RESET: &'static str = FORE_RESET;
    #[classattr]
    const LIGHTBLACK_EX: &'static str = FORE_LIGHTBLACK_EX;
    #[classattr]
    const LIGHTRED_EX: &'static str = FORE_LIGHTRED_EX;
    #[classattr]
    const LIGHTGREEN_EX: &'static str = FORE_LIGHTGREEN_EX;
    #[classattr]
    const LIGHTYELLOW_EX: &'static str = FORE_LIGHTYELLOW_EX;
    #[classattr]
    const LIGHTBLUE_EX: &'static str = FORE_LIGHTBLUE_EX;
    #[classattr]
    const LIGHTMAGENTA_EX: &'static str = FORE_LIGHTMAGENTA_EX;
    #[classattr]
    const LIGHTCYAN_EX: &'static str = FORE_LIGHTCYAN_EX;
    #[classattr]
    const LIGHTWHITE_EX: &'static str = FORE_LIGHTWHITE_EX;
}

/// Back color codes module
#[pyclass(frozen)]
#[derive(Clone)]
pub struct Back;

#[pymethods]
impl Back {
    #[classattr]
    const BLACK: &'static str = BACK_BLACK;
    #[classattr]
    const RED: &'static str = BACK_RED;
    #[classattr]
    const GREEN: &'static str = BACK_GREEN;
    #[classattr]
    const YELLOW: &'static str = BACK_YELLOW;
    #[classattr]
    const BLUE: &'static str = BACK_BLUE;
    #[classattr]
    const MAGENTA: &'static str = BACK_MAGENTA;
    #[classattr]
    const CYAN: &'static str = BACK_CYAN;
    #[classattr]
    const WHITE: &'static str = BACK_WHITE;
    #[classattr]
    const RESET: &'static str = BACK_RESET;
    #[classattr]
    const LIGHTBLACK_EX: &'static str = BACK_LIGHTBLACK_EX;
    #[classattr]
    const LIGHTRED_EX: &'static str = BACK_LIGHTRED_EX;
    #[classattr]
    const LIGHTGREEN_EX: &'static str = BACK_LIGHTGREEN_EX;
    #[classattr]
    const LIGHTYELLOW_EX: &'static str = BACK_LIGHTYELLOW_EX;
    #[classattr]
    const LIGHTBLUE_EX: &'static str = BACK_LIGHTBLUE_EX;
    #[classattr]
    const LIGHTMAGENTA_EX: &'static str = BACK_LIGHTMAGENTA_EX;
    #[classattr]
    const LIGHTCYAN_EX: &'static str = BACK_LIGHTCYAN_EX;
    #[classattr]
    const LIGHTWHITE_EX: &'static str = BACK_LIGHTWHITE_EX;
}

/// Style codes module
#[pyclass(frozen)]
#[derive(Clone)]
pub struct Style;

#[pymethods]
impl Style {
    #[classattr]
    const DIM: &'static str = STYLE_DIM;
    #[classattr]
    const NORMAL: &'static str = STYLE_NORMAL;
    #[classattr]
    const BRIGHT: &'static str = STYLE_BRIGHT;
    #[classattr]
    const RESET_ALL: &'static str = STYLE_RESET_ALL;
}

/// Cursor positioning
#[pyclass(frozen)]
#[derive(Clone)]
pub struct Cursor;

#[pymethods]
impl Cursor {
    /// Move cursor up n lines
    #[staticmethod]
    fn UP(n: Option<u32>) -> String {
        format!("{}{}A", CSI, n.unwrap_or(1))
    }
    
    /// Move cursor down n lines
    #[staticmethod]
    fn DOWN(n: Option<u32>) -> String {
        format!("{}{}B", CSI, n.unwrap_or(1))
    }
    
    /// Move cursor forward n columns
    #[staticmethod]
    fn FORWARD(n: Option<u32>) -> String {
        format!("{}{}C", CSI, n.unwrap_or(1))
    }
    
    /// Move cursor back n columns
    #[staticmethod]
    fn BACK(n: Option<u32>) -> String {
        format!("{}{}D", CSI, n.unwrap_or(1))
    }
    
    /// Move cursor to position (x, y)
    #[staticmethod]
    fn POS(x: Option<u32>, y: Option<u32>) -> String {
        format!("{}{};{}H", CSI, y.unwrap_or(1), x.unwrap_or(1))
    }
}

/// ANSI code generation functions
#[pyfunction]
fn code_to_chars(code: u32) -> String {
    format!("{}{}m", CSI, code)
}

#[pyfunction]
fn set_title(title: &str) -> String {
    format!("{}2;{}{}", OSC, title, BEL)
}

#[pyfunction]
fn clear_screen(mode: Option<u32>) -> String {
    format!("{}{}J", CSI, mode.unwrap_or(2))
}

#[pyfunction]
fn clear_line(mode: Option<u32>) -> String {
    format!("{}{}K", CSI, mode.unwrap_or(2))
}

/// Generate foreground color code for 256-color palette
#[pyfunction]
fn fore_256(color: u8) -> String {
    format!("{}38;5;{}m", CSI, color)
}

/// Generate background color code for 256-color palette
#[pyfunction]
fn back_256(color: u8) -> String {
    format!("{}48;5;{}m", CSI, color)
}

/// Generate foreground color code for RGB
#[pyfunction]
fn fore_rgb(r: u8, g: u8, b: u8) -> String {
    format!("{}38;2;{};{};{}m", CSI, r, g, b)
}

/// Generate background color code for RGB
#[pyfunction]
fn back_rgb(r: u8, g: u8, b: u8) -> String {
    format!("{}48;2;{};{};{}m", CSI, r, g, b)
}

/// Colorize a string with foreground, background, and style
#[pyfunction]
#[pyo3(signature = (text, fore=None, back=None, style=None))]
fn colorize(text: &str, fore: Option<&str>, back: Option<&str>, style: Option<&str>) -> String {
    let mut result = String::with_capacity(text.len() + 32);
    
    if let Some(s) = style {
        result.push_str(s);
    }
    if let Some(f) = fore {
        result.push_str(f);
    }
    if let Some(b) = back {
        result.push_str(b);
    }
    
    result.push_str(text);
    result.push_str(STYLE_RESET_ALL);
    
    result
}

/// Strip ANSI escape codes from a string
#[pyfunction]
fn strip_ansi(text: &str) -> String {
    let mut result = String::with_capacity(text.len());
    let mut chars = text.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c == '\x1b' {
            // Skip escape sequence
            if let Some(&next) = chars.peek() {
                if next == '[' {
                    chars.next(); // consume '['
                    // Skip until we hit a letter (end of sequence)
                    while let Some(&c) = chars.peek() {
                        chars.next();
                        if c.is_ascii_alphabetic() {
                            break;
                        }
                    }
                } else if next == ']' {
                    chars.next(); // consume ']'
                    // Skip until BEL or ST
                    while let Some(c) = chars.next() {
                        if c == '\x07' || c == '\\' {
                            break;
                        }
                    }
                }
            }
        } else {
            result.push(c);
        }
    }
    
    result
}

/// Initialize colorama (no-op on Unix, placeholder for Windows)
#[pyfunction]
#[pyo3(signature = (autoreset=false, convert=None, strip=None, wrap=true))]
fn init(autoreset: bool, convert: Option<bool>, strip: Option<bool>, wrap: bool) {
    // On Unix systems, colorama.init() is essentially a no-op
    // The actual ANSI codes work directly
    let _ = (autoreset, convert, strip, wrap);
}

/// Deinitialize colorama
#[pyfunction]
fn deinit() {
    // No-op on Unix
}

/// Reinitialize colorama
#[pyfunction]
fn reinit() {
    // No-op on Unix
}

/// A Python module implemented in Rust
#[pymodule]
fn colorama_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Fore>()?;
    m.add_class::<Back>()?;
    m.add_class::<Style>()?;
    m.add_class::<Cursor>()?;
    
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(deinit, m)?)?;
    m.add_function(wrap_pyfunction!(reinit, m)?)?;
    m.add_function(wrap_pyfunction!(code_to_chars, m)?)?;
    m.add_function(wrap_pyfunction!(set_title, m)?)?;
    m.add_function(wrap_pyfunction!(clear_screen, m)?)?;
    m.add_function(wrap_pyfunction!(clear_line, m)?)?;
    m.add_function(wrap_pyfunction!(fore_256, m)?)?;
    m.add_function(wrap_pyfunction!(back_256, m)?)?;
    m.add_function(wrap_pyfunction!(fore_rgb, m)?)?;
    m.add_function(wrap_pyfunction!(back_rgb, m)?)?;
    m.add_function(wrap_pyfunction!(colorize, m)?)?;
    m.add_function(wrap_pyfunction!(strip_ansi, m)?)?;
    
    Ok(())
}
