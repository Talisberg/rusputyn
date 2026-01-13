"""
Tests for jsonschema-rs

Verifies API compatibility with jsonschema
"""

import pytest
import jsonschema_rs

try:
    import jsonschema as jsonschema_py
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


class TestBasicValidation:
    """Test basic schema validation"""

    def test_validate_simple_object(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            }
        }
        data = {"name": "Alice", "age": 30}

        # Should not raise
        jsonschema_rs.validate(data, schema)

    def test_validate_invalid_type(self):
        schema = {"type": "string"}
        data = 123

        with pytest.raises(Exception):
            jsonschema_rs.validate(data, schema)

    def test_validate_required_properties(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }

        # Valid
        jsonschema_rs.validate({"name": "Alice"}, schema)

        # Invalid - missing required
        with pytest.raises(Exception):
            jsonschema_rs.validate({}, schema)

    def test_validate_array(self):
        schema = {
            "type": "array",
            "items": {"type": "number"}
        }

        # Valid
        jsonschema_rs.validate([1, 2, 3], schema)

        # Invalid
        with pytest.raises(Exception):
            jsonschema_rs.validate([1, "two", 3], schema)

    def test_validate_nested_object(self):
        schema = {
            "type": "object",
            "properties": {
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"}
                    }
                }
            }
        }

        data = {
            "address": {
                "street": "123 Main St",
                "city": "Springfield"
            }
        }

        jsonschema_rs.validate(data, schema)


class TestIsValid:
    """Test is_valid function"""

    def test_is_valid_true(self):
        schema = {"type": "string"}
        assert jsonschema_rs.is_valid("hello", schema) is True

    def test_is_valid_false(self):
        schema = {"type": "string"}
        assert jsonschema_rs.is_valid(123, schema) is False

    def test_is_valid_complex(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number", "minimum": 0}
            },
            "required": ["name"]
        }

        assert jsonschema_rs.is_valid({"name": "Alice", "age": 30}, schema) is True
        assert jsonschema_rs.is_valid({"age": 30}, schema) is False  # Missing required
        assert jsonschema_rs.is_valid({"name": "Bob", "age": -5}, schema) is False  # Invalid minimum


class TestValidator:
    """Test Validator class"""

    def test_validator_reuse(self):
        schema = {"type": "string"}
        validator = jsonschema_rs.Validator(schema)

        # Validate multiple instances
        validator.validate("hello")
        validator.validate("world")

        with pytest.raises(Exception):
            validator.validate(123)

    def test_validator_is_valid(self):
        schema = {"type": "number"}
        validator = jsonschema_rs.Validator(schema)

        assert validator.is_valid(42) is True
        assert validator.is_valid("42") is False

    def test_validator_complex_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "users": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string", "format": "email"}
                        },
                        "required": ["name", "email"]
                    }
                }
            }
        }

        validator = jsonschema_rs.Validator(schema)

        valid_data = {
            "users": [
                {"name": "Alice", "email": "alice@example.com"},
                {"name": "Bob", "email": "bob@example.com"}
            ]
        }

        validator.validate(valid_data)


class TestEdgeCases:
    """Test edge cases"""

    def test_empty_schema(self):
        schema = {}
        data = {"anything": "goes"}

        jsonschema_rs.validate(data, schema)
        assert jsonschema_rs.is_valid(data, schema) is True

    def test_null_value(self):
        schema = {"type": "null"}

        jsonschema_rs.validate(None, schema)
        assert jsonschema_rs.is_valid(None, schema) is True

    def test_boolean_schema(self):
        # true schema accepts everything
        assert jsonschema_rs.is_valid({"any": "data"}, True) is True

        # false schema rejects everything
        assert jsonschema_rs.is_valid({"any": "data"}, False) is False

    def test_multiple_types(self):
        schema = {"type": ["string", "number"]}

        assert jsonschema_rs.is_valid("hello", schema) is True
        assert jsonschema_rs.is_valid(42, schema) is True
        assert jsonschema_rs.is_valid(True, schema) is False


class TestConstraints:
    """Test various JSON Schema constraints"""

    def test_string_constraints(self):
        schema = {
            "type": "string",
            "minLength": 2,
            "maxLength": 10
        }

        assert jsonschema_rs.is_valid("hi", schema) is True
        assert jsonschema_rs.is_valid("hello", schema) is True
        assert jsonschema_rs.is_valid("x", schema) is False  # Too short
        assert jsonschema_rs.is_valid("this is too long", schema) is False

    def test_number_constraints(self):
        schema = {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        }

        assert jsonschema_rs.is_valid(50, schema) is True
        assert jsonschema_rs.is_valid(0, schema) is True
        assert jsonschema_rs.is_valid(100, schema) is True
        assert jsonschema_rs.is_valid(-1, schema) is False
        assert jsonschema_rs.is_valid(101, schema) is False

    def test_array_constraints(self):
        schema = {
            "type": "array",
            "minItems": 1,
            "maxItems": 3
        }

        assert jsonschema_rs.is_valid([1], schema) is True
        assert jsonschema_rs.is_valid([1, 2, 3], schema) is True
        assert jsonschema_rs.is_valid([], schema) is False
        assert jsonschema_rs.is_valid([1, 2, 3, 4], schema) is False

    def test_enum(self):
        schema = {"enum": ["red", "green", "blue"]}

        assert jsonschema_rs.is_valid("red", schema) is True
        assert jsonschema_rs.is_valid("yellow", schema) is False


@pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
class TestCompatibility:
    """Test compatibility with Python jsonschema"""

    def test_validate_compatibility(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            }
        }

        valid_data = {"name": "Alice", "age": 30}
        invalid_data = {"name": 123, "age": "thirty"}

        # Both should accept valid data
        jsonschema_py.validate(valid_data, schema)
        jsonschema_rs.validate(valid_data, schema)

        # Both should reject invalid data
        with pytest.raises(Exception):
            jsonschema_py.validate(invalid_data, schema)

        with pytest.raises(Exception):
            jsonschema_rs.validate(invalid_data, schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
