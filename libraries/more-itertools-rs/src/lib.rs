use pyo3::prelude::*;
use pyo3::types::{PyIterator, PyList, PyTuple};
use pyo3::exceptions::PyValueError;
use std::collections::{HashSet, HashMap};

/// Break iterable into lists of length n
#[pyfunction]
#[pyo3(signature = (iterable, n, strict=false))]
fn chunked(py: Python, iterable: &PyAny, n: usize, strict: bool) -> PyResult<PyObject> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be at least one"));
    }

    let iter = PyIterator::from_object(iterable)?;
    let mut result = Vec::new();
    let mut current_chunk = Vec::new();

    for item in iter {
        let item = item?;
        current_chunk.push(item);

        if current_chunk.len() == n {
            result.push(PyList::new(py, &current_chunk).to_object(py));
            current_chunk.clear();
        }
    }

    // Handle last incomplete chunk
    if !current_chunk.is_empty() {
        if strict {
            return Err(PyValueError::new_err(
                "iterator is not divisible by n"
            ));
        }
        result.push(PyList::new(py, &current_chunk).to_object(py));
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Break iterable into tuples of length n
#[pyfunction]
#[pyo3(signature = (iterable, n, strict=false))]
fn batched(py: Python, iterable: &PyAny, n: usize, strict: bool) -> PyResult<PyObject> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be at least one"));
    }

    let iter = PyIterator::from_object(iterable)?;
    let mut result = Vec::new();
    let mut current_batch = Vec::new();

    for item in iter {
        let item = item?;
        current_batch.push(item);

        if current_batch.len() == n {
            result.push(PyTuple::new(py, &current_batch).to_object(py));
            current_batch.clear();
        }
    }

    // Handle last incomplete batch
    if !current_batch.is_empty() {
        if strict {
            return Err(PyValueError::new_err(
                "iterator is not divisible by n"
            ));
        }
        result.push(PyTuple::new(py, &current_batch).to_object(py));
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Flatten one level of nesting
#[pyfunction]
fn flatten(py: Python, listOfLists: &PyAny) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(listOfLists)?;
    let mut result = Vec::new();

    for item in iter {
        let item = item?;
        let inner_iter = PyIterator::from_object(item)?;
        for inner_item in inner_iter {
            result.push(inner_item?);
        }
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Return first item of iterable or default
#[pyfunction]
#[pyo3(signature = (iterable, default=None))]
fn first(py: Python, iterable: &PyAny, default: Option<PyObject>) -> PyResult<PyObject> {
    let mut iter = PyIterator::from_object(iterable)?;

    match iter.next() {
        Some(Ok(item)) => Ok(item.to_object(py)),
        Some(Err(e)) => Err(e),
        None => match default {
            Some(d) => Ok(d),
            None => Err(PyValueError::new_err("first() of empty sequence")),
        }
    }
}

/// Return last item of iterable or default
#[pyfunction]
#[pyo3(signature = (iterable, default=None))]
fn last(py: Python, iterable: &PyAny, default: Option<PyObject>) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(iterable)?;
    let mut last_item = None;

    for item in iter {
        last_item = Some(item?);
    }

    match last_item {
        Some(item) => Ok(item.to_object(py)),
        None => match default {
            Some(d) => Ok(d),
            None => Err(PyValueError::new_err("last() of empty sequence")),
        }
    }
}

/// Return first n items as a list
#[pyfunction]
fn take(py: Python, n: usize, iterable: &PyAny) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(iterable)?;
    let mut result = Vec::new();

    for (i, item) in iter.enumerate() {
        if i >= n {
            break;
        }
        result.push(item?);
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Yield distinct elements preserving order
#[pyfunction]
fn unique_everseen(py: Python, iterable: &PyAny) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(iterable)?;
    let mut seen = HashSet::new();
    let mut result = Vec::new();

    for item in iter {
        let item = item?;
        let hash = item.hash()?;

        if seen.insert(hash) {
            result.push(item);
        }
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Split iterable into two based on predicate
#[pyfunction]
fn partition(py: Python, pred: &PyAny, iterable: &PyAny) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(iterable)?;
    let mut false_items = Vec::new();
    let mut true_items = Vec::new();

    for item in iter {
        let item = item?;
        let item_obj = item.to_object(py);
        let result: bool = pred.call1((item_obj.clone_ref(py),))?.extract()?;

        if result {
            true_items.push(item_obj);
        } else {
            false_items.push(item_obj);
        }
    }

    let false_list = PyList::new(py, false_items).to_object(py);
    let true_list = PyList::new(py, true_items).to_object(py);

    Ok(PyTuple::new(py, &[false_list, true_list]).to_object(py))
}

/// Create sliding window over sequence
#[pyfunction]
#[pyo3(signature = (seq, n, fillvalue=None, step=1))]
fn windowed(py: Python, seq: &PyAny, n: usize, fillvalue: Option<PyObject>, step: usize) -> PyResult<PyObject> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be at least one"));
    }
    if step == 0 {
        return Err(PyValueError::new_err("step must be at least one"));
    }

    let items: Vec<PyObject> = PyIterator::from_object(seq)?
        .map(|item| item.map(|i| i.to_object(py)))
        .collect::<PyResult<Vec<_>>>()?;

    if items.is_empty() {
        return Ok(PyList::empty(py).to_object(py));
    }

    let mut result = Vec::new();
    let mut i = 0;

    while i + n <= items.len() || (i < items.len() && fillvalue.is_some()) {
        let mut window = Vec::new();

        for j in 0..n {
            if i + j < items.len() {
                window.push(items[i + j].clone_ref(py));
            } else if let Some(ref fv) = fillvalue {
                window.push(fv.clone_ref(py));
            }
        }

        result.push(PyTuple::new(py, &window).to_object(py));
        i += step;

        if i + n > items.len() && fillvalue.is_none() {
            break;
        }
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Check if all elements are unique
#[pyfunction]
fn all_unique(iterable: &PyAny) -> PyResult<bool> {
    let iter = PyIterator::from_object(iterable)?;
    let mut seen = HashSet::new();

    for item in iter {
        let item = item?;
        let hash = item.hash()?;

        if !seen.insert(hash) {
            return Ok(false);
        }
    }

    Ok(true)
}

/// Interleave multiple iterables
#[pyfunction]
fn interleave(py: Python, iterables: &PyTuple) -> PyResult<PyObject> {
    let mut iters: Vec<_> = iterables
        .iter()
        .map(|it| PyIterator::from_object(it))
        .collect::<PyResult<Vec<_>>>()?;

    if iters.is_empty() {
        return Ok(PyList::empty(py).to_object(py));
    }

    let mut result = Vec::new();
    let mut any_active = true;

    while any_active {
        any_active = false;

        for iter in &mut iters {
            if let Some(item) = iter.next() {
                result.push(item?);
                any_active = true;
            }
        }
    }

    Ok(PyList::new(py, result).to_object(py))
}

/// Count occurrences of each element
#[pyfunction]
fn count_items(py: Python, iterable: &PyAny) -> PyResult<PyObject> {
    let iter = PyIterator::from_object(iterable)?;
    let mut counts: HashMap<isize, usize> = HashMap::new();

    for item in iter {
        let item = item?;
        let hash = item.hash()?;
        *counts.entry(hash).or_insert(0) += 1;
    }

    let dict = pyo3::types::PyDict::new(py);

    // Reconstruct items for display (simplified - using hash as key)
    for (hash, count) in counts {
        dict.set_item(hash, count)?;
    }

    Ok(dict.to_object(py))
}

/// Check if iterable is sorted
#[pyfunction]
#[pyo3(signature = (iterable, reverse=false))]
fn is_sorted(iterable: &PyAny, reverse: bool) -> PyResult<bool> {
    let mut iter = PyIterator::from_object(iterable)?;

    let mut prev = match iter.next() {
        Some(Ok(item)) => item,
        Some(Err(e)) => return Err(e),
        None => return Ok(true), // Empty iterable is sorted
    };

    for item in iter {
        let item = item?;
        let cmp = if reverse {
            prev.lt(item)?
        } else {
            prev.gt(item)?
        };

        if cmp {
            return Ok(false);
        }
        prev = item;
    }

    Ok(true)
}

/// Python module definition
#[pymodule]
fn more_itertools_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(chunked, m)?)?;
    m.add_function(wrap_pyfunction!(batched, m)?)?;
    m.add_function(wrap_pyfunction!(flatten, m)?)?;
    m.add_function(wrap_pyfunction!(first, m)?)?;
    m.add_function(wrap_pyfunction!(last, m)?)?;
    m.add_function(wrap_pyfunction!(take, m)?)?;
    m.add_function(wrap_pyfunction!(unique_everseen, m)?)?;
    m.add_function(wrap_pyfunction!(partition, m)?)?;
    m.add_function(wrap_pyfunction!(windowed, m)?)?;
    m.add_function(wrap_pyfunction!(all_unique, m)?)?;
    m.add_function(wrap_pyfunction!(interleave, m)?)?;
    m.add_function(wrap_pyfunction!(count_items, m)?)?;
    m.add_function(wrap_pyfunction!(is_sorted, m)?)?;

    m.add("__version__", "0.1.0")?;

    Ok(())
}
