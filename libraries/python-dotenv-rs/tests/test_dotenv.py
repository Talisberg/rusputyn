"""
Tests for python-dotenv-rs

Ensures API compatibility with python-dotenv
"""

import os
import tempfile
from pathlib import Path
import pytest

try:
    import dotenv_rs as dotenv
except ImportError:
    import dotenv  # Fallback to python-dotenv


class TestDotenvBasics:
    """Test basic dotenv functionality"""

    def test_load_dotenv_from_string(self):
        """Test parsing dotenv content"""
        content = """
        KEY1=value1
        KEY2=value2
        KEY3="quoted value"
        """
        result = dotenv.dotenv_values(content)
        assert result['KEY1'] == 'value1'
        assert result['KEY2'] == 'value2'
        assert result['KEY3'] == 'quoted value'

    def test_comments_are_ignored(self):
        """Test that comments are properly ignored"""
        content = """
        # This is a comment
        KEY1=value1
        # Another comment
        KEY2=value2
        """
        result = dotenv.dotenv_values(content)
        assert len(result) == 2
        assert result['KEY1'] == 'value1'
        assert result['KEY2'] == 'value2'

    def test_empty_lines_ignored(self):
        """Test that empty lines don't cause issues"""
        content = """
        KEY1=value1

        KEY2=value2

        """
        result = dotenv.dotenv_values(content)
        assert len(result) == 2

    def test_quoted_values(self):
        """Test single and double quoted values"""
        content = '''
        SINGLE='single quoted'
        DOUBLE="double quoted"
        UNQUOTED=no quotes
        '''
        result = dotenv.dotenv_values(content)
        assert result['SINGLE'] == 'single quoted'
        assert result['DOUBLE'] == 'double quoted'
        assert result['UNQUOTED'] == 'no quotes'

    def test_whitespace_handling(self):
        """Test that whitespace is properly handled"""
        content = """
        KEY1  =  value1
        KEY2=value2
          KEY3=value3
        """
        result = dotenv.dotenv_values(content)
        assert result['KEY1'] == 'value1'
        assert result['KEY2'] == 'value2'
        assert result['KEY3'] == 'value3'


class TestDotenvFile:
    """Test loading from files"""

    def test_load_dotenv_file(self):
        """Test loading .env from file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("TEST_KEY=test_value\n")
            f.write("ANOTHER_KEY=another_value\n")
            temp_path = f.name

        try:
            # Clear any existing values
            if 'TEST_KEY' in os.environ:
                del os.environ['TEST_KEY']
            if 'ANOTHER_KEY' in os.environ:
                del os.environ['ANOTHER_KEY']

            # Load dotenv
            result = dotenv.load_dotenv(temp_path)
            assert result is True

            # Check environment variables were set
            assert os.environ.get('TEST_KEY') == 'test_value'
            assert os.environ.get('ANOTHER_KEY') == 'another_value'

        finally:
            # Cleanup
            os.unlink(temp_path)
            if 'TEST_KEY' in os.environ:
                del os.environ['TEST_KEY']
            if 'ANOTHER_KEY' in os.environ:
                del os.environ['ANOTHER_KEY']

    def test_load_dotenv_nonexistent(self):
        """Test loading from non-existent file returns False"""
        result = dotenv.load_dotenv('/nonexistent/path/.env')
        assert result is False

    def test_override_behavior(self):
        """Test that override parameter works correctly"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("OVERRIDE_TEST=from_file\n")
            temp_path = f.name

        try:
            # Set initial value
            os.environ['OVERRIDE_TEST'] = 'original'

            # Load without override (default)
            dotenv.load_dotenv(temp_path, override_vars=False)
            assert os.environ['OVERRIDE_TEST'] == 'original'

            # Load with override
            dotenv.load_dotenv(temp_path, override_vars=True)
            assert os.environ['OVERRIDE_TEST'] == 'from_file'

        finally:
            os.unlink(temp_path)
            if 'OVERRIDE_TEST' in os.environ:
                del os.environ['OVERRIDE_TEST']


class TestSetGetUnset:
    """Test set_key, get_key, unset_key functions"""

    def test_set_and_get_key(self):
        """Test setting and getting a key"""
        key = 'TEST_SET_KEY'
        value = 'test_value'

        try:
            success, warning = dotenv.set_key(key, value)
            assert success is True
            assert warning is None

            retrieved = dotenv.get_key(key)
            assert retrieved == value

        finally:
            if key in os.environ:
                del os.environ[key]

    def test_get_nonexistent_key(self):
        """Test getting a non-existent key returns None"""
        result = dotenv.get_key('NONEXISTENT_KEY_12345')
        assert result is None

    def test_unset_key(self):
        """Test unsetting a key"""
        key = 'TEST_UNSET_KEY'
        os.environ[key] = 'test_value'

        result = dotenv.unset_key(key)
        assert result is True
        assert key not in os.environ

    def test_unset_nonexistent_key(self):
        """Test unsetting a non-existent key returns False"""
        result = dotenv.unset_key('NONEXISTENT_KEY_12345')
        assert result is False

    def test_set_key_no_override(self):
        """Test set_key with override=False"""
        key = 'TEST_NO_OVERRIDE'
        os.environ[key] = 'original'

        try:
            success, warning = dotenv.set_key(key, 'new_value', override_vars=False)
            assert success is False
            assert warning is not None
            assert os.environ[key] == 'original'

        finally:
            if key in os.environ:
                del os.environ[key]


class TestRealWorldScenarios:
    """Test real-world usage patterns"""

    def test_django_style_env(self):
        """Test typical Django .env file"""
        content = """
        # Django settings
        SECRET_KEY=django-insecure-abc123
        DEBUG=True
        ALLOWED_HOSTS=localhost,127.0.0.1

        # Database
        DATABASE_URL=postgresql://user:pass@localhost:5432/db

        # Email
        EMAIL_HOST=smtp.gmail.com
        EMAIL_PORT=587
        """
        result = dotenv.dotenv_values(content)
        assert result['SECRET_KEY'] == 'django-insecure-abc123'
        assert result['DEBUG'] == 'True'
        assert result['DATABASE_URL'] == 'postgresql://user:pass@localhost:5432/db'
        assert result['EMAIL_PORT'] == '587'

    def test_node_style_env(self):
        """Test typical Node.js .env file"""
        content = """
        NODE_ENV=production
        PORT=3000
        API_KEY="sk-1234567890abcdef"
        BASE_URL='https://api.example.com'
        """
        result = dotenv.dotenv_values(content)
        assert result['NODE_ENV'] == 'production'
        assert result['PORT'] == '3000'
        assert result['API_KEY'] == 'sk-1234567890abcdef'
        assert result['BASE_URL'] == 'https://api.example.com'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
