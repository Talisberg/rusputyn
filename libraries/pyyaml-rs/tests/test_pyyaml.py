"""
Tests for pyyaml-rs

Verifies API compatibility with PyYAML
"""

import pytest
import pyyaml_rs as yaml_rs

try:
    import yaml as yaml_py
    PYYAML_AVAILABLE = True
except ImportError:
    PYYAML_AVAILABLE = False


class TestBasicParsing:
    """Test basic YAML parsing"""

    def test_parse_null(self):
        assert yaml_rs.safe_load("null") is None
        assert yaml_rs.safe_load("~") is None
        assert yaml_rs.safe_load("") is None

    def test_parse_boolean(self):
        assert yaml_rs.safe_load("true") is True
        assert yaml_rs.safe_load("false") is False
        # Note: serde_yaml uses YAML 1.2 spec where yes/no are strings, not booleans
        # PyYAML uses YAML 1.1 spec where yes/no are booleans

    def test_parse_integer(self):
        assert yaml_rs.safe_load("42") == 42
        assert yaml_rs.safe_load("-17") == -17
        assert yaml_rs.safe_load("0") == 0

    def test_parse_float(self):
        result = yaml_rs.safe_load("3.14")
        assert isinstance(result, float)
        assert abs(result - 3.14) < 0.001

        result = yaml_rs.safe_load("-0.5")
        assert abs(result - (-0.5)) < 0.001

    def test_parse_string(self):
        assert yaml_rs.safe_load("'hello'") == "hello"
        assert yaml_rs.safe_load('"world"') == "world"
        assert yaml_rs.safe_load("plain text") == "plain text"

    def test_parse_list(self):
        yaml_str = """
- item1
- item2
- item3
"""
        result = yaml_rs.safe_load(yaml_str)
        assert result == ["item1", "item2", "item3"]

    def test_parse_dict(self):
        yaml_str = """
key1: value1
key2: value2
key3: value3
"""
        result = yaml_rs.safe_load(yaml_str)
        assert result == {"key1": "value1", "key2": "value2", "key3": "value3"}

    def test_parse_nested_structure(self):
        yaml_str = """
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
"""
        result = yaml_rs.safe_load(yaml_str)
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432
        assert result["database"]["credentials"]["username"] == "admin"

    def test_parse_list_of_dicts(self):
        yaml_str = """
- name: Alice
  age: 30
- name: Bob
  age: 25
"""
        result = yaml_rs.safe_load(yaml_str)
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["age"] == 25


class TestLoadAlias:
    """Test that load() is an alias for safe_load()"""

    def test_load_alias(self):
        yaml_str = "key: value"
        assert yaml_rs.load(yaml_str) == yaml_rs.safe_load(yaml_str)


class TestMultipleDocuments:
    """Test parsing multiple YAML documents"""

    def test_safe_load_all_simple(self):
        yaml_str = """---
doc1: value1
---
doc2: value2
---
doc3: value3
"""
        result = yaml_rs.safe_load_all(yaml_str)
        assert len(result) == 3
        assert result[0] == {"doc1": "value1"}
        assert result[1] == {"doc2": "value2"}
        assert result[2] == {"doc3": "value3"}

    def test_safe_load_all_mixed(self):
        yaml_str = """---
- item1
- item2
---
key: value
---
42
"""
        result = yaml_rs.safe_load_all(yaml_str)
        assert len(result) == 3
        assert result[0] == ["item1", "item2"]
        assert result[1] == {"key": "value"}
        assert result[2] == 42

    def test_load_all_alias(self):
        yaml_str = "---\nkey1: value1\n---\nkey2: value2"
        assert yaml_rs.load_all(yaml_str) == yaml_rs.safe_load_all(yaml_str)


class TestDumping:
    """Test YAML serialization"""

    def test_dump_null(self):
        result = yaml_rs.safe_dump(None)
        assert "null" in result or "~" in result

    def test_dump_boolean(self):
        assert "true" in yaml_rs.safe_dump(True)
        assert "false" in yaml_rs.safe_dump(False)

    def test_dump_integer(self):
        result = yaml_rs.safe_dump(42)
        assert "42" in result

    def test_dump_float(self):
        result = yaml_rs.safe_dump(3.14)
        assert "3.14" in result

    def test_dump_string(self):
        result = yaml_rs.safe_dump("hello")
        assert "hello" in result

    def test_dump_list(self):
        result = yaml_rs.safe_dump(["item1", "item2", "item3"])
        # Should contain the items
        assert "item1" in result
        assert "item2" in result
        assert "item3" in result

    def test_dump_dict(self):
        result = yaml_rs.safe_dump({"key1": "value1", "key2": "value2"})
        assert "key1" in result
        assert "value1" in result
        assert "key2" in result
        assert "value2" in result

    def test_dump_nested(self):
        data = {
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }
        result = yaml_rs.safe_dump(data)
        assert "database" in result
        assert "localhost" in result
        assert "5432" in result

    def test_dump_alias(self):
        data = {"key": "value"}
        assert yaml_rs.dump(data) == yaml_rs.safe_dump(data)


class TestDumpAll:
    """Test dumping multiple documents"""

    def test_dump_all_simple(self):
        docs = [
            {"doc1": "value1"},
            {"doc2": "value2"},
            {"doc3": "value3"}
        ]
        result = yaml_rs.safe_dump_all(docs)
        assert "doc1" in result
        assert "doc2" in result
        assert "doc3" in result
        assert result.count("---") >= 2  # At least 2 document separators

    def test_dump_all_mixed(self):
        docs = [
            ["item1", "item2"],
            {"key": "value"},
            42
        ]
        result = yaml_rs.safe_dump_all(docs)
        assert "item1" in result
        assert "key" in result
        assert "42" in result

    def test_dump_all_alias(self):
        docs = [{"key1": "value1"}, {"key2": "value2"}]
        assert yaml_rs.dump_all(docs) == yaml_rs.safe_dump_all(docs)


class TestRoundTrip:
    """Test that load -> dump -> load produces same result"""

    def test_roundtrip_dict(self):
        original = {"key": "value", "number": 42, "flag": True}
        yaml_str = yaml_rs.safe_dump(original)
        loaded = yaml_rs.safe_load(yaml_str)
        assert loaded == original

    def test_roundtrip_list(self):
        original = [1, 2, 3, "four", True, None]
        yaml_str = yaml_rs.safe_dump(original)
        loaded = yaml_rs.safe_load(yaml_str)
        assert loaded == original

    def test_roundtrip_nested(self):
        original = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "active": True
        }
        yaml_str = yaml_rs.safe_dump(original)
        loaded = yaml_rs.safe_load(yaml_str)
        assert loaded == original


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_yaml(self):
        with pytest.raises(Exception):  # Should raise ValueError
            yaml_rs.safe_load("{ invalid: yaml: structure:")

    def test_invalid_yaml_multiline(self):
        invalid_yaml = """
        key: value
        invalid
        - mixed
        """
        # This might parse or might raise depending on YAML rules
        # Just verify it doesn't crash
        try:
            yaml_rs.safe_load(invalid_yaml)
        except Exception:
            pass  # Expected


@pytest.mark.skipif(not PYYAML_AVAILABLE, reason="PyYAML not installed")
class TestCompatibilityWithPyYAML:
    """Test compatibility with PyYAML"""

    def test_load_compatibility(self):
        yaml_str = """
key: value
number: 42
list:
  - item1
  - item2
"""
        py_result = yaml_py.safe_load(yaml_str)
        rs_result = yaml_rs.safe_load(yaml_str)
        assert py_result == rs_result

    def test_dump_compatibility(self):
        data = {"key": "value", "number": 42}
        py_yaml = yaml_py.safe_dump(data)
        rs_yaml = yaml_rs.safe_dump(data)

        # Both should be valid YAML that produces same data
        assert yaml_py.safe_load(py_yaml) == yaml_py.safe_load(rs_yaml)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
