use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use unicode_width::UnicodeWidthStr;

/// Table format specification
#[derive(Clone)]
struct TableFormat {
    line_above: Option<Line>,
    line_below: Option<Line>,
    line_between_rows: Option<Line>,
    header_line: Option<Line>,
    padding: usize,
    with_header_hide: bool,
}

#[derive(Clone)]
struct Line {
    begin: &'static str,
    hline: &'static str,
    sep: &'static str,
    end: &'static str,
}

impl Line {
    const fn new(begin: &'static str, hline: &'static str, sep: &'static str, end: &'static str) -> Self {
        Self { begin, hline, sep, end }
    }
}

fn get_format(name: &str) -> TableFormat {
    match name {
        "plain" => TableFormat {
            line_above: None,
            line_below: None,
            line_between_rows: None,
            header_line: None,
            padding: 1,
            with_header_hide: false,
        },
        "simple" => TableFormat {
            line_above: None,
            line_below: Some(Line::new("", "-", "  ", "")),
            line_between_rows: None,
            header_line: Some(Line::new("", "-", "  ", "")),
            padding: 1,
            with_header_hide: true,
        },
        "github" | "pipe" => TableFormat {
            line_above: None,
            line_below: None,
            line_between_rows: None,
            header_line: Some(Line::new("|", "-", "|", "|")),
            padding: 1,
            with_header_hide: false,
        },
        "grid" => TableFormat {
            line_above: Some(Line::new("+", "-", "+", "+")),
            line_below: Some(Line::new("+", "-", "+", "+")),
            line_between_rows: Some(Line::new("+", "-", "+", "+")),
            header_line: Some(Line::new("+", "=", "+", "+")),
            padding: 1,
            with_header_hide: false,
        },
        "pretty" => TableFormat {
            line_above: Some(Line::new("+", "-", "+", "+")),
            line_below: Some(Line::new("+", "-", "+", "+")),
            line_between_rows: None,
            header_line: Some(Line::new("+", "-", "+", "+")),
            padding: 1,
            with_header_hide: false,
        },
        "psql" => TableFormat {
            line_above: None,
            line_below: None,
            line_between_rows: None,
            header_line: Some(Line::new("", "-", "+-", "")),
            padding: 1,
            with_header_hide: true,
        },
        "orgtbl" => TableFormat {
            line_above: None,
            line_below: None,
            line_between_rows: None,
            header_line: Some(Line::new("|", "-", "+", "|")),
            padding: 1,
            with_header_hide: false,
        },
        "rst" | "simple_outline" => TableFormat {
            line_above: Some(Line::new("", "=", "  ", "")),
            line_below: Some(Line::new("", "=", "  ", "")),
            line_between_rows: None,
            header_line: Some(Line::new("", "=", "  ", "")),
            padding: 1,
            with_header_hide: false,
        },
        "rounded_grid" => TableFormat {
            line_above: Some(Line::new("╭", "─", "┬", "╮")),
            line_below: Some(Line::new("╰", "─", "┴", "╯")),
            line_between_rows: Some(Line::new("├", "─", "┼", "┤")),
            header_line: Some(Line::new("├", "═", "╪", "┤")),
            padding: 1,
            with_header_hide: false,
        },
        "heavy_grid" => TableFormat {
            line_above: Some(Line::new("┏", "━", "┳", "┓")),
            line_below: Some(Line::new("┗", "━", "┻", "┛")),
            line_between_rows: Some(Line::new("┣", "━", "╋", "┫")),
            header_line: Some(Line::new("┣", "━", "╋", "┫")),
            padding: 1,
            with_header_hide: false,
        },
        "double_grid" => TableFormat {
            line_above: Some(Line::new("╔", "═", "╦", "╗")),
            line_below: Some(Line::new("╚", "═", "╩", "╝")),
            line_between_rows: Some(Line::new("╠", "═", "╬", "╣")),
            header_line: Some(Line::new("╠", "═", "╬", "╣")),
            padding: 1,
            with_header_hide: false,
        },
        "tsv" => TableFormat {
            line_above: None,
            line_below: None,
            line_between_rows: None,
            header_line: None,
            padding: 0,
            with_header_hide: false,
        },
        _ => TableFormat {
            line_above: None,
            line_below: Some(Line::new("", "-", "  ", "")),
            line_between_rows: None,
            header_line: Some(Line::new("", "-", "  ", "")),
            padding: 1,
            with_header_hide: true,
        },
    }
}

fn get_separator(format: &str) -> &'static str {
    match format {
        "tsv" => "\t",
        "github" | "pipe" | "orgtbl" | "rounded_grid" | "heavy_grid" | "double_grid" | "grid" | "pretty" => "|",
        _ => "  ",
    }
}

fn visible_width(s: &str) -> usize {
    UnicodeWidthStr::width(s)
}

fn pad_cell(content: &str, width: usize, align: char) -> String {
    let content_width = visible_width(content);
    if content_width >= width {
        return content.to_string();
    }
    
    let padding = width - content_width;
    match align {
        'r' => format!("{:>width$}{}", "", content, width = padding),
        'c' => {
            let left = padding / 2;
            let right = padding - left;
            format!("{:>width$}{}{:>width2$}", "", content, "", width = left, width2 = right)
        }
        _ => format!("{}{:>width$}", content, "", width = padding), // left align default
    }
}

fn build_line(widths: &[usize], line: &Line, padding: usize) -> String {
    let mut result = String::new();
    result.push_str(line.begin);
    
    for (i, &width) in widths.iter().enumerate() {
        if i > 0 {
            result.push_str(line.sep);
        }
        let total_width = width + padding * 2;
        for _ in 0..total_width {
            result.push_str(line.hline);
        }
    }
    
    result.push_str(line.end);
    result
}

fn build_row(cells: &[String], widths: &[usize], aligns: &[char], sep: &str, padding: usize, use_borders: bool) -> String {
    let mut result = String::new();
    
    if use_borders {
        result.push_str("|");
    }
    
    for (i, (cell, &width)) in cells.iter().zip(widths.iter()).enumerate() {
        if i > 0 {
            result.push_str(sep);
        }
        
        let align = aligns.get(i).copied().unwrap_or('l');
        let padded = pad_cell(cell, width, align);
        
        for _ in 0..padding {
            result.push(' ');
        }
        result.push_str(&padded);
        for _ in 0..padding {
            result.push(' ');
        }
    }
    
    if use_borders {
        result.push_str("|");
    }
    
    result
}

/// Main tabulate function
/// tabulate([["a", "b"], ["c", "d"]], headers=["X", "Y"]) -> formatted table
#[pyfunction]
#[pyo3(signature = (tabular_data, headers=None, tablefmt=None, floatfmt=None, numalign=None, stralign=None, missingval=None, showindex=None, disable_numparse=None, colalign=None))]
fn tabulate(
    py: Python<'_>,
    tabular_data: &Bound<'_, PyAny>,
    headers: Option<&Bound<'_, PyAny>>,
    tablefmt: Option<&str>,
    floatfmt: Option<&str>,
    numalign: Option<&str>,
    stralign: Option<&str>,
    missingval: Option<&str>,
    showindex: Option<&Bound<'_, PyAny>>,
    disable_numparse: Option<bool>,
    colalign: Option<&Bound<'_, PyAny>>,
) -> PyResult<String> {
    let fmt_name = tablefmt.unwrap_or("simple");
    let format = get_format(fmt_name);
    let sep = get_separator(fmt_name);
    let missing = missingval.unwrap_or("");
    let float_fmt = floatfmt.unwrap_or(".6g");
    let num_align = numalign.unwrap_or("right");
    let str_align = stralign.unwrap_or("left");
    let _disable_num = disable_numparse.unwrap_or(false);
    
    let use_borders = matches!(fmt_name, "github" | "pipe" | "orgtbl" | "rounded_grid" | "heavy_grid" | "double_grid" | "grid" | "pretty");
    
    // Parse headers
    let header_row: Vec<String> = if let Some(h) = headers {
        if let Ok(list) = h.downcast::<PyList>() {
            list.iter()
                .map(|item| item.str().map(|s| s.to_string()).unwrap_or_default())
                .collect()
        } else if let Ok(s) = h.extract::<String>() {
            if s == "firstrow" || s == "keys" {
                vec![] // Will handle specially
            } else {
                vec![]
            }
        } else {
            vec![]
        }
    } else {
        vec![]
    };
    
    // Parse data rows
    let mut rows: Vec<Vec<String>> = Vec::new();
    
    // Handle list of lists
    if let Ok(list) = tabular_data.downcast::<PyList>() {
        for item in list.iter() {
            if let Ok(row_list) = item.downcast::<PyList>() {
                let row: Vec<String> = row_list
                    .iter()
                    .map(|cell| {
                        if cell.is_none() {
                            missing.to_string()
                        } else if let Ok(f) = cell.extract::<f64>() {
                            // Format float
                            if float_fmt == ".6g" {
                                format!("{:.6}", f).trim_end_matches('0').trim_end_matches('.').to_string()
                            } else {
                                format!("{}", f)
                            }
                        } else {
                            cell.str().map(|s| s.to_string()).unwrap_or_default()
                        }
                    })
                    .collect();
                rows.push(row);
            } else if let Ok(tuple) = item.extract::<Vec<PyObject>>() {
                let row: Vec<String> = tuple
                    .iter()
                    .map(|cell| {
                        cell.bind(py).str().map(|s| s.to_string()).unwrap_or_default()
                    })
                    .collect();
                rows.push(row);
            }
        }
    }
    // Handle list of dicts
    else if let Ok(list) = tabular_data.downcast::<PyList>() {
        if let Some(first) = list.get_item(0).ok() {
            if let Ok(_dict) = first.downcast::<PyDict>() {
                // Extract keys as headers, values as rows
                for item in list.iter() {
                    if let Ok(dict) = item.downcast::<PyDict>() {
                        let row: Vec<String> = dict
                            .values()
                            .iter()
                            .map(|v| v.str().map(|s| s.to_string()).unwrap_or_default())
                            .collect();
                        rows.push(row);
                    }
                }
            }
        }
    }
    
    if rows.is_empty() {
        return Ok(String::new());
    }
    
    // Calculate column count
    let num_cols = rows.iter().map(|r| r.len()).max().unwrap_or(0);
    let num_cols = num_cols.max(header_row.len());
    
    // Normalize rows to same length
    for row in &mut rows {
        while row.len() < num_cols {
            row.push(missing.to_string());
        }
    }
    
    // Parse column alignments
    let mut aligns: Vec<char> = vec!['l'; num_cols];
    
    if let Some(ca) = colalign {
        if let Ok(list) = ca.downcast::<PyList>() {
            for (i, item) in list.iter().enumerate() {
                if i < num_cols {
                    if let Ok(s) = item.extract::<String>() {
                        aligns[i] = match s.as_str() {
                            "right" => 'r',
                            "center" => 'c',
                            _ => 'l',
                        };
                    }
                }
            }
        }
    } else {
        // Auto-detect: numbers right, strings left
        for (i, _) in (0..num_cols).enumerate() {
            let is_numeric = rows.iter().all(|row| {
                row.get(i)
                    .map(|s| s.parse::<f64>().is_ok() || s.is_empty())
                    .unwrap_or(true)
            });
            if is_numeric && num_align == "right" {
                aligns[i] = 'r';
            } else if !is_numeric && str_align == "left" {
                aligns[i] = 'l';
            }
        }
    }
    
    // Calculate column widths
    let mut widths: Vec<usize> = vec![0; num_cols];
    
    // Consider headers
    for (i, h) in header_row.iter().enumerate() {
        if i < num_cols {
            widths[i] = widths[i].max(visible_width(h));
        }
    }
    
    // Consider data
    for row in &rows {
        for (i, cell) in row.iter().enumerate() {
            if i < num_cols {
                widths[i] = widths[i].max(visible_width(cell));
            }
        }
    }
    
    // Build output
    let mut output = Vec::new();
    
    // Top line
    if let Some(ref line) = format.line_above {
        output.push(build_line(&widths, line, format.padding));
    }
    
    // Header
    let has_header = !header_row.is_empty();
    if has_header {
        let mut padded_headers = header_row.clone();
        while padded_headers.len() < num_cols {
            padded_headers.push(String::new());
        }
        output.push(build_row(&padded_headers, &widths, &aligns, sep, format.padding, use_borders));
        
        // Header separator
        if let Some(ref line) = format.header_line {
            output.push(build_line(&widths, line, format.padding));
        }
    }
    
    // Data rows
    for (i, row) in rows.iter().enumerate() {
        output.push(build_row(row, &widths, &aligns, sep, format.padding, use_borders));
        
        // Row separator (not after last row)
        if i < rows.len() - 1 {
            if let Some(ref line) = format.line_between_rows {
                output.push(build_line(&widths, line, format.padding));
            }
        }
    }
    
    // Bottom line
    if let Some(ref line) = format.line_below {
        if !format.with_header_hide || !has_header {
            // For simple format, only show bottom line if no header
        }
        output.push(build_line(&widths, line, format.padding));
    }
    
    Ok(output.join("\n"))
}

/// Get list of available table formats
#[pyfunction]
fn tabulate_formats() -> Vec<&'static str> {
    vec![
        "plain",
        "simple", 
        "github",
        "grid",
        "pipe",
        "orgtbl",
        "rst",
        "psql",
        "pretty",
        "rounded_grid",
        "heavy_grid",
        "double_grid",
        "tsv",
    ]
}

/// A Python module implemented in Rust
#[pymodule]
fn tabulate_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tabulate, m)?)?;
    m.add_function(wrap_pyfunction!(tabulate_formats, m)?)?;
    Ok(())
}
