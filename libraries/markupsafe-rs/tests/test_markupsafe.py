"""
Test suite for markupsafe-rs

Verifies API compatibility with original markupsafe.
"""

import pytest

try:
    from markupsafe_rs import escape, escape_silent, soft_unicode, soft_str, Markup
    HAS_RS = True
except ImportError:
    HAS_RS = False
    pytestmark = pytest.mark.skip("markupsafe-rs not available")


class TestEscape:
    """Test escape function."""
    
    def test_escape_empty(self):
        assert str(escape("")) == ""
    
    def test_escape_no_special_chars(self):
        assert str(escape("Hello World")) == "Hello World"
    
    def test_escape_ampersand(self):
        assert str(escape("a & b")) == "a &amp; b"
    
    def test_escape_less_than(self):
        assert str(escape("a < b")) == "a &lt; b"
    
    def test_escape_greater_than(self):
        assert str(escape("a > b")) == "a &gt; b"
    
    def test_escape_quotes(self):
        assert str(escape('"hello"')) == "&quot;hello&quot;"
        assert str(escape("'hello'")) == "&#x27;hello&#x27;"
    
    def test_escape_all_special(self):
        text = '<script>alert("XSS & \'attack\'")</script>'
        expected = '&lt;script&gt;alert(&quot;XSS &amp; &#x27;attack&#x27;&quot;)&lt;/script&gt;'
        assert str(escape(text)) == expected
    
    def test_escape_unicode(self):
        assert str(escape("中文 <test>")) == "中文 &lt;test&gt;"
        assert str(escape("🚀 & 🎯")) == "🚀 &amp; 🎯"
    
    def test_escape_already_markup(self):
        m = Markup("<b>test</b>")
        result = escape(m)
        assert str(result) == "<b>test</b>"
    
    def test_escape_none(self):
        result = escape(None)
        assert result is None


class TestEscapeSilent:
    """Test escape_silent function."""
    
    def test_escape_silent_none(self):
        result = escape_silent(None)
        assert str(result) == ""
    
    def test_escape_silent_empty(self):
        assert str(escape_silent("")) == ""
    
    def test_escape_silent_text(self):
        assert str(escape_silent("<test>")) == "&lt;test&gt;"


class TestSoftUnicode:
    """Test soft_unicode function."""
    
    def test_soft_unicode_none(self):
        assert soft_unicode(None) == ""
    
    def test_soft_unicode_string(self):
        assert soft_unicode("test") == "test"
    
    def test_soft_unicode_unicode(self):
        assert soft_unicode("中文") == "中文"
    
    def test_soft_unicode_number(self):
        assert soft_unicode(42) == "42"


class TestMarkupClass:
    """Test Markup class."""
    
    def test_markup_creation(self):
        m = Markup("<b>test</b>")
        assert str(m) == "<b>test</b>"
    
    def test_markup_repr(self):
        m = Markup("test")
        assert "Markup" in repr(m)
    
    def test_markup_len(self):
        m = Markup("hello")
        assert len(m) == 5
    
    def test_markup_add(self):
        m1 = Markup("<b>hello</b>")
        m2 = Markup("<i>world</i>")
        result = m1 + " " + m2
        assert str(result) == "<b>hello</b> <i>world</i>"
    
    def test_markup_add_escapes_string(self):
        m = Markup("<b>test</b>")
        result = m + "<script>"
        assert str(result) == "<b>test</b>&lt;script&gt;"
    
    def test_markup_radd(self):
        m = Markup("<b>world</b>")
        result = "hello " + m
        assert str(result) == "hello &lt;b&gt;world&lt;/b&gt;" or str(result) == "hello <b>world</b>"
    
    def test_markup_mul(self):
        m = Markup("x")
        result = m * 3
        assert str(result) == "xxx"
    
    def test_markup_rmul(self):
        m = Markup("x")
        result = 3 * m
        assert str(result) == "xxx"
    
    def test_markup_join(self):
        m = Markup(", ")
        items = ["a", "b", "c"]
        result = m.join(items)
        assert str(result) == "a, b, c"
    
    def test_markup_join_escapes(self):
        m = Markup(", ")
        items = ["<a>", "b", "<c>"]
        result = m.join(items)
        assert str(result) == "&lt;a&gt;, b, &lt;c&gt;"
    
    def test_markup_join_mixed(self):
        m = Markup(", ")
        items = [Markup("<b>a</b>"), "b", "<c>"]
        result = m.join(items)
        assert str(result) == "<b>a</b>, b, &lt;c&gt;"
    
    def test_markup_split(self):
        m = Markup("a, b, c")
        parts = m.split(", ")
        assert len(parts) == 3
        assert all(isinstance(p, Markup) for p in parts)
    
    def test_markup_strip(self):
        m = Markup("  hello  ")
        assert str(m.strip()) == "hello"
    
    def test_markup_lstrip(self):
        m = Markup("  hello  ")
        assert str(m.lstrip()) == "hello  "
    
    def test_markup_rstrip(self):
        m = Markup("  hello  ")
        assert str(m.rstrip()) == "  hello"
    
    def test_markup_lower(self):
        m = Markup("HELLO")
        assert str(m.lower()) == "hello"
    
    def test_markup_upper(self):
        m = Markup("hello")
        assert str(m.upper()) == "HELLO"
    
    def test_markup_replace(self):
        m = Markup("hello world")
        result = m.replace("world", "python")
        assert str(result) == "hello python"
    
    def test_markup_startswith(self):
        m = Markup("hello world")
        assert m.startswith("hello")
        assert not m.startswith("world")
    
    def test_markup_endswith(self):
        m = Markup("hello world")
        assert m.endswith("world")
        assert not m.endswith("hello")
    
    def test_markup_unescape(self):
        m = Markup("&lt;b&gt;hello&lt;/b&gt;")
        assert m.unescape() == "<b>hello</b>"
    
    def test_markup_isalnum(self):
        assert Markup("abc123").isalnum()
        assert not Markup("abc 123").isalnum()
    
    def test_markup_isalpha(self):
        assert Markup("abc").isalpha()
        assert not Markup("abc123").isalpha()
    
    def test_markup_isdigit(self):
        assert Markup("123").isdigit()
        assert not Markup("abc").isdigit()
    
    def test_markup_islower(self):
        assert Markup("hello").islower()
        assert not Markup("Hello").islower()
    
    def test_markup_isupper(self):
        assert Markup("HELLO").isupper()
        assert not Markup("Hello").isupper()
    
    def test_markup_isspace(self):
        assert Markup("   ").isspace()
        assert not Markup("hello").isspace()


class TestRealWorld:
    """Test real-world scenarios."""
    
    def test_template_rendering(self):
        """Simulate Jinja2-style template rendering."""
        data = {
            "title": "My <Page>",
            "content": "Hello & welcome",
            "author": 'John "Doe"'
        }
        
        html = f"""
        <html>
        <head><title>{escape(data['title'])}</title></head>
        <body>
        <h1>{escape(data['title'])}</h1>
        <p>{escape(data['content'])}</p>
        <footer>By {escape(data['author'])}</footer>
        </body>
        </html>
        """
        
        assert "&lt;Page&gt;" in html
        assert "&amp;" in html
        assert "&quot;" in html or "&#x27;" in html
    
    def test_form_output(self):
        """Simulate form field escaping."""
        user_input = '<script>alert("XSS")</script>'
        safe_input = escape(user_input)
        
        form_html = f'<input type="text" value="{safe_input}">'
        assert "<script>" not in form_html
        assert "&lt;script&gt;" in form_html
    
    def test_safe_html_building(self):
        """Test building safe HTML programmatically."""
        wrapper = Markup("<div class='content'>")
        content = "User input: <script>"
        closing = Markup("</div>")
        
        result = wrapper + escape(content) + closing
        assert str(result) == "<div class='content'>User input: &lt;script&gt;</div>"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
