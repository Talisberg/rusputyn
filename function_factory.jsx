import React, { useState } from 'react';

const TEMPLATES = {
  pyfunction_simple: {
    name: "Simple PyFunction",
    template: `/// {description}
/// humanize.{fn_name}({example_input}) -> "{example_output}"
#[pyfunction]
fn {fn_name}(value: {input_type}) -> {output_type} {{
    {body}
}}`,
    fields: ['fn_name', 'description', 'example_input', 'example_output', 'input_type', 'output_type', 'body']
  },
  
  pyfunction_with_options: {
    name: "PyFunction with Options",
    template: `/// {description}
/// humanize.{fn_name}({example_input}) -> "{example_output}"
#[pyfunction]
#[pyo3(signature = (value, {option_params}))]
fn {fn_name}(value: {input_type}, {rust_params}) -> {output_type} {{
    {body}
}}`,
    fields: ['fn_name', 'description', 'example_input', 'example_output', 'input_type', 'output_type', 'option_params', 'rust_params', 'body']
  },

  format_parser: {
    name: "Format String Parser (reusable block)",
    template: `// Parse format string for precision
let precision = if fmt.contains('.') {{
    fmt.chars()
        .skip_while(|c| *c != '.')
        .skip(1)
        .take_while(|c| c.is_ascii_digit())
        .collect::<String>()
        .parse::<usize>()
        .unwrap_or({default_precision})
}} else {{
    {default_precision}
}};`,
    fields: ['default_precision']
  },

  suffix_lookup: {
    name: "Suffix Lookup Table",
    template: `const {const_name}: &[&str] = &[{suffixes}];`,
    fields: ['const_name', 'suffixes']
  },

  threshold_match: {
    name: "Threshold Match Block",
    template: `let (divisor, suffix): (f64, &str) = {thresholds}
    else {{
        return {fallback};
    }};`,
    fields: ['thresholds', 'fallback']
  },

  benchmark_case: {
    name: "Benchmark Test Case",
    template: `# {fn_name} benchmark
py = benchmark("{fn_name}", lambda: humanize.{fn_name}({test_value}))
rs = benchmark("{fn_name}", lambda: humanize_rs.{fn_name}({test_value}))
print_comparison(py, rs)

py_result = humanize.{fn_name}({test_value})
rs_result = humanize_rs.{fn_name}({test_value})
print(f"  Python output: {{py_result}}")
print(f"  Rust output:   {{rs_result}}")
print(f"  Match: {{'✓' if py_result == rs_result else '✗'}}")`,
    fields: ['fn_name', 'test_value']
  },

  module_registration: {
    name: "Module Function Registration",
    template: `m.add_function(wrap_pyfunction!({fn_name}, m)?)?;`,
    fields: ['fn_name']
  }
};

const PRESETS = {
  intcomma: {
    template: 'pyfunction_with_options',
    values: {
      fn_name: 'intcomma',
      description: 'Format a number with comma separators',
      example_input: '1000000',
      example_output: '1,000,000',
      input_type: 'i64',
      output_type: 'String',
      option_params: 'ndigits=None',
      rust_params: 'ndigits: Option<i32>',
      body: `match ndigits {
        Some(n) if n > 0 => {
            let factor = 10_f64.powi(n);
            let rounded = (value as f64 / factor).round() * factor;
            (rounded as i64).to_formatted_string(&Locale::en)
        }
        _ => value.to_formatted_string(&Locale::en),
    }`
    }
  },
  ordinal: {
    template: 'pyfunction_simple',
    values: {
      fn_name: 'ordinal',
      description: 'Convert a number to its ordinal form',
      example_input: '3',
      example_output: '3rd',
      input_type: 'i64',
      output_type: 'String',
      body: `let suffix = match (value % 10, value % 100) {
        (1, 11) => "th",
        (2, 12) => "th",
        (3, 13) => "th",
        (1, _) => "st",
        (2, _) => "nd",
        (3, _) => "rd",
        _ => "th",
    };
    format!("{}{}", value.to_formatted_string(&Locale::en), suffix)`
    }
  },
  naturalsize: {
    template: 'pyfunction_with_options',
    values: {
      fn_name: 'naturalsize',
      description: 'Convert a file size to human readable form',
      example_input: '1048576',
      example_output: '1.0 MB',
      input_type: 'i64',
      output_type: 'String',
      option_params: 'binary=false, gnu=false, format_str=None',
      rust_params: 'binary: bool, gnu: bool, format_str: Option<&str>',
      body: '// See full implementation'
    }
  }
};

export default function FunctionFactory() {
  const [selectedTemplate, setSelectedTemplate] = useState('pyfunction_simple');
  const [fieldValues, setFieldValues] = useState({});
  const [output, setOutput] = useState('');
  const [copied, setCopied] = useState(false);

  const template = TEMPLATES[selectedTemplate];

  const handleFieldChange = (field, value) => {
    const newValues = { ...fieldValues, [field]: value };
    setFieldValues(newValues);
    generateOutput(newValues);
  };

  const generateOutput = (values) => {
    let result = template.template;
    template.fields.forEach(field => {
      const regex = new RegExp(`\\{${field}\\}`, 'g');
      result = result.replace(regex, values[field] || `<${field}>`);
    });
    setOutput(result);
  };

  const loadPreset = (presetName) => {
    const preset = PRESETS[presetName];
    setSelectedTemplate(preset.template);
    setFieldValues(preset.values);
    
    // Generate output with preset values
    let result = TEMPLATES[preset.template].template;
    TEMPLATES[preset.template].fields.forEach(field => {
      const regex = new RegExp(`\\{${field}\\}`, 'g');
      result = result.replace(regex, preset.values[field] || `<${field}>`);
    });
    setOutput(result);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleTemplateChange = (newTemplate) => {
    setSelectedTemplate(newTemplate);
    setFieldValues({});
    setOutput(TEMPLATES[newTemplate].template);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-2 text-orange-400">🦀 Rust Function Factory</h1>
        <p className="text-gray-400 mb-6">Generate consistent PyO3 function blocks for humanize-rs</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Controls */}
          <div className="space-y-4">
            {/* Template Selector */}
            <div className="bg-gray-800 rounded-lg p-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">Template</label>
              <select
                value={selectedTemplate}
                onChange={(e) => handleTemplateChange(e.target.value)}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              >
                {Object.entries(TEMPLATES).map(([key, val]) => (
                  <option key={key} value={key}>{val.name}</option>
                ))}
              </select>
            </div>

            {/* Presets */}
            <div className="bg-gray-800 rounded-lg p-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">Quick Presets</label>
              <div className="flex flex-wrap gap-2">
                {Object.keys(PRESETS).map(preset => (
                  <button
                    key={preset}
                    onClick={() => loadPreset(preset)}
                    className="px-3 py-1 bg-orange-600 hover:bg-orange-500 rounded text-sm font-mono"
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>

            {/* Field Inputs */}
            <div className="bg-gray-800 rounded-lg p-4 space-y-3">
              <label className="block text-sm font-medium text-gray-300 mb-2">Fields</label>
              {template.fields.map(field => (
                <div key={field}>
                  <label className="block text-xs text-gray-400 mb-1 font-mono">{field}</label>
                  {field === 'body' || field === 'thresholds' ? (
                    <textarea
                      value={fieldValues[field] || ''}
                      onChange={(e) => handleFieldChange(field, e.target.value)}
                      className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm h-32"
                      placeholder={`Enter ${field}...`}
                    />
                  ) : (
                    <input
                      type="text"
                      value={fieldValues[field] || ''}
                      onChange={(e) => handleFieldChange(field, e.target.value)}
                      className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm"
                      placeholder={`Enter ${field}...`}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Right Panel - Output */}
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex justify-between items-center mb-3">
              <label className="text-sm font-medium text-gray-300">Generated Code</label>
              <button
                onClick={copyToClipboard}
                className={`px-3 py-1 rounded text-sm ${
                  copied ? 'bg-green-600' : 'bg-blue-600 hover:bg-blue-500'
                }`}
              >
                {copied ? '✓ Copied!' : 'Copy'}
              </button>
            </div>
            <pre className="bg-gray-950 rounded p-4 overflow-auto text-sm font-mono text-green-400 h-96 whitespace-pre-wrap">
              {output || template.template}
            </pre>
          </div>
        </div>

        {/* Common Patterns Reference */}
        <div className="mt-6 bg-gray-800 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-orange-400 mb-3">Common Patterns</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-gray-900 rounded p-3">
              <h3 className="text-gray-300 font-medium mb-2">Format Parsing</h3>
              <code className="text-xs text-gray-400 block">
                Extract precision from "%.1f" style format strings
              </code>
            </div>
            <div className="bg-gray-900 rounded p-3">
              <h3 className="text-gray-300 font-medium mb-2">Threshold Matching</h3>
              <code className="text-xs text-gray-400 block">
                if value &gt;= X then divisor/suffix else...
              </code>
            </div>
            <div className="bg-gray-900 rounded p-3">
              <h3 className="text-gray-300 font-medium mb-2">Locale Formatting</h3>
              <code className="text-xs text-gray-400 block">
                value.to_formatted_string(&Locale::en)
              </code>
            </div>
          </div>
        </div>

        {/* Functions Checklist */}
        <div className="mt-6 bg-gray-800 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-orange-400 mb-3">humanize API Coverage</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm font-mono">
            {[
              { name: 'intcomma', done: true },
              { name: 'ordinal', done: true },
              { name: 'intword', done: true },
              { name: 'naturalsize', done: true },
              { name: 'fractional', done: true },
              { name: 'apnumber', done: true },
              { name: 'scientific', done: true },
              { name: 'naturaltime', done: false },
              { name: 'naturaldate', done: false },
              { name: 'naturalday', done: false },
              { name: 'naturaldelta', done: false },
              { name: 'precisedelta', done: false },
            ].map(fn => (
              <div 
                key={fn.name}
                className={`px-2 py-1 rounded ${fn.done ? 'bg-green-900 text-green-300' : 'bg-gray-700 text-gray-400'}`}
              >
                {fn.done ? '✓' : '○'} {fn.name}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
