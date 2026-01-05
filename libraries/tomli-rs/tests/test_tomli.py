"""
Test suite for tomli-rs

Verifies API compatibility with original tomli.
"""

import pytest
import io

try:
    import tomli_rs
    HAS_RS = True
except ImportError:
    HAS_RS = False
    pytestmark = pytest.mark.skip("tomli-rs not available")


class TestLoads:
    """Test loads() function."""
    
    def test_empty_string(self):
        result = tomli_rs.loads("")
        assert result == {}
    
    def test_simple_key_value(self):
        result = tomli_rs.loads('key = "value"')
        assert result == {"key": "value"}
    
    def test_integer(self):
        result = tomli_rs.loads("number = 42")
        assert result == {"number": 42}
    
    def test_float(self):
        result = tomli_rs.loads("pi = 3.14159")
        assert result["pi"] == pytest.approx(3.14159)
    
    def test_boolean(self):
        result = tomli_rs.loads("enabled = true\ndisabled = false")
        assert result == {"enabled": True, "disabled": False}
    
    def test_string(self):
        result = tomli_rs.loads('msg = "Hello, World!"')
        assert result == {"msg": "Hello, World!"}
    
    def test_multiline_string(self):
        toml = '''
msg = """
Line 1
Line 2
Line 3
"""
'''
        result = tomli_rs.loads(toml)
        assert "Line 1" in result["msg"]
        assert "Line 2" in result["msg"]
    
    def test_array(self):
        result = tomli_rs.loads("numbers = [1, 2, 3, 4, 5]")
        assert result == {"numbers": [1, 2, 3, 4, 5]}
    
    def test_mixed_array(self):
        result = tomli_rs.loads('mixed = [1, "two", 3.0, true]')
        assert result["mixed"] == [1, "two", 3.0, True]
    
    def test_nested_array(self):
        result = tomli_rs.loads("nested = [[1, 2], [3, 4]]")
        assert result == {"nested": [[1, 2], [3, 4]]}
    
    def test_table(self):
        toml = """
[server]
host = "localhost"
port = 8080
"""
        result = tomli_rs.loads(toml)
        assert result == {
            "server": {
                "host": "localhost",
                "port": 8080
            }
        }
    
    def test_nested_table(self):
        toml = """
[database.connection]
host = "localhost"
port = 5432
"""
        result = tomli_rs.loads(toml)
        assert result == {
            "database": {
                "connection": {
                    "host": "localhost",
                    "port": 5432
                }
            }
        }
    
    def test_array_of_tables(self):
        toml = """
[[servers]]
name = "alpha"
ip = "10.0.1.1"

[[servers]]
name = "beta"
ip = "10.0.1.2"
"""
        result = tomli_rs.loads(toml)
        assert len(result["servers"]) == 2
        assert result["servers"][0]["name"] == "alpha"
        assert result["servers"][1]["name"] == "beta"
    
    def test_comments(self):
        toml = """
# This is a comment
key = "value"  # Inline comment
"""
        result = tomli_rs.loads(toml)
        assert result == {"key": "value"}
    
    def test_invalid_toml(self):
        with pytest.raises(Exception):  # Should raise TOMLDecodeError
            tomli_rs.loads("invalid toml [[[")


class TestLoad:
    """Test load() function."""
    
    def test_load_from_file(self):
        toml_bytes = b'[section]\nkey = "value"'
        fp = io.BytesIO(toml_bytes)
        result = tomli_rs.load(fp)
        assert result == {"section": {"key": "value"}}
    
    def test_load_simple(self):
        toml_bytes = b'name = "test"\nversion = "1.0.0"'
        fp = io.BytesIO(toml_bytes)
        result = tomli_rs.load(fp)
        assert result == {"name": "test", "version": "1.0.0"}
    
    def test_load_complex(self):
        toml_bytes = b"""
[package]
name = "my-package"
version = "1.0.0"

[dependencies]
requests = "^2.28.0"
"""
        fp = io.BytesIO(toml_bytes)
        result = tomli_rs.load(fp)
        assert result["package"]["name"] == "my-package"
        assert "requests" in result["dependencies"]


class TestDataTypes:
    """Test various TOML data types."""
    
    def test_string_types(self):
        toml = """
basic = "Hello"
literal = 'World'
multiline = '''
Line 1
Line 2'''
"""
        result = tomli_rs.loads(toml)
        assert result["basic"] == "Hello"
        assert result["literal"] == "World"
        assert "Line 1" in result["multiline"]
    
    def test_number_types(self):
        toml = """
int_positive = 42
int_negative = -17
float_positive = 3.14
float_negative = -0.01
scientific = 5e+22
"""
        result = tomli_rs.loads(toml)
        assert result["int_positive"] == 42
        assert result["int_negative"] == -17
        assert result["float_positive"] == pytest.approx(3.14)
    
    def test_boolean_types(self):
        result = tomli_rs.loads("yes = true\nno = false")
        assert result["yes"] is True
        assert result["no"] is False
    
    def test_datetime_types(self):
        # Note: Exact datetime handling may vary
        toml = """
dt = 2024-01-15T10:30:00Z
date = 2024-01-15
time = 10:30:00
"""
        result = tomli_rs.loads(toml)
        # Just verify they parse without error
        assert "dt" in result
        assert "date" in result
        assert "time" in result


class TestRealWorld:
    """Test real-world TOML files."""
    
    def test_pyproject_toml(self):
        toml = """
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
description = "A test package"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
"""
        result = tomli_rs.loads(toml)
        assert result["project"]["name"] == "my-package"
        assert "pytest" in result["tool"]["pytest.ini_options"]["python_files"][0]
    
    def test_cargo_toml(self):
        toml = """
[package]
name = "my-rust-project"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
criterion = "0.5"
"""
        result = tomli_rs.loads(toml)
        assert result["package"]["name"] == "my-rust-project"
        assert "serde" in result["dependencies"]


class TestEdgeCases:
    """Test edge cases and corner cases."""
    
    def test_empty_table(self):
        result = tomli_rs.loads("[empty]")
        assert result == {"empty": {}}
    
    def test_empty_array(self):
        result = tomli_rs.loads("arr = []")
        assert result == {"arr": []}
    
    def test_special_characters_in_keys(self):
        toml = """
"special key!" = "value"
'another-key' = 123
"""
        result = tomli_rs.loads(toml)
        assert result["special key!"] == "value"
        assert result["another-key"] == 123
    
    def test_unicode(self):
        toml = 'msg = "Hello 世界 🌍"'
        result = tomli_rs.loads(toml)
        assert result["msg"] == "Hello 世界 🌍"
    
    def test_escaped_characters(self):
        toml = r'path = "C:\\Users\\test\\file.txt"'
        result = tomli_rs.loads(toml)
        assert "\\" in result["path"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
