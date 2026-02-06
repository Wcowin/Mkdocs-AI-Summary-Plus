"""Tests for utility functions"""

import pytest
from unittest.mock import patch, Mock
import os

from mkdocs_ai_summary.utils import (
    get_ci_name,
    clean_markdown_content,
    validate_api_key,
    truncate_content,
    format_file_size,
    is_valid_folder_path
)


class TestGetCIName:
    """Test cases for get_ci_name function"""
    
    @patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'})
    def test_github_actions(self):
        """Test GitHub Actions detection"""
        result = get_ci_name()
        assert result == 'GitHub Actions'
    
    @patch.dict(os.environ, {'GITLAB_CI': 'true'})
    def test_gitlab_ci(self):
        """Test GitLab CI detection"""
        result = get_ci_name()
        assert result == 'GitLab CI'
    
    @patch.dict(os.environ, {'TRAVIS': 'true'})
    def test_travis_ci(self):
        """Test Travis CI detection"""
        result = get_ci_name()
        assert result == 'Travis CI'
    
    @patch.dict(os.environ, {'CIRCLECI': 'true'})
    def test_circle_ci(self):
        """Test CircleCI detection"""
        result = get_ci_name()
        assert result == 'CircleCI'
    
    @patch.dict(os.environ, {'JENKINS_URL': 'http://jenkins.example.com'})
    def test_jenkins(self):
        """Test Jenkins detection"""
        result = get_ci_name()
        assert result == 'Jenkins'
    
    @patch.dict(os.environ, {'APPVEYOR': 'True'})
    def test_appveyor(self):
        """Test AppVeyor detection"""
        result = get_ci_name()
        assert result == 'AppVeyor'
    
    @patch.dict(os.environ, {'BUILDKITE': 'true'})
    def test_buildkite(self):
        """Test Buildkite detection"""
        result = get_ci_name()
        assert result == 'Buildkite'
    
    @patch.dict(os.environ, {'DRONE': 'true'})
    def test_drone_ci(self):
        """Test Drone CI detection"""
        result = get_ci_name()
        assert result == 'Drone CI'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_no_ci_environment(self):
        """Test when not in CI environment"""
        result = get_ci_name()
        assert result is None
    
    @patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'GITLAB_CI': 'true'})
    def test_multiple_ci_environments(self):
        """Test when multiple CI environment variables are set"""
        result = get_ci_name()
        # Should return the first match (GitHub Actions has priority)
        assert result == 'GitHub Actions'


class TestCleanMarkdownContent:
    """Test cases for clean_markdown_content function"""
    
    def test_remove_headers(self):
        """Test removing markdown headers"""
        content = "# Header 1\n## Header 2\n### Header 3"
        result = clean_markdown_content(content)
        
        assert "Header 1" in result
        assert "Header 2" in result
        assert "Header 3" in result
        assert "#" not in result
    
    def test_remove_code_blocks(self):
        """Test removing code blocks"""
        content = """Text before

```python
code = "should be removed"
print(code)
```

Text after
"""
        result = clean_markdown_content(content)
        
        assert "Text before" in result
        assert "Text after" in result
        assert "code =" not in result
        assert "print(code)" not in result
        assert "python" not in result
    
    def test_remove_inline_code(self):
        """Test removing inline code"""
        content = "This is `inline code` in text."
        result = clean_markdown_content(content)
        
        assert "This is" in result
        assert "in text" in result
        assert "`" not in result
        assert "inline code" not in result
    
    def test_remove_links(self):
        """Test removing markdown links"""
        content = "Visit [Google](https://google.com) for search."
        result = clean_markdown_content(content)
        
        assert "Visit" in result
        assert "Google" in result
        assert "for search" in result
        assert "https://google.com" not in result
        assert "[" not in result
        assert "]" not in result
    
    def test_remove_images(self):
        """Test removing markdown images"""
        content = "Here is an ![alt text](image.png) image."
        result = clean_markdown_content(content)
        
        assert "Here is an" in result
        assert "image" in result
        assert "alt text" in result
        assert "image.png" not in result
        assert "![" not in result
    
    def test_remove_html_tags(self):
        """Test removing HTML tags"""
        content = "<div>Content</div> and <span style='color: red;'>styled text</span>"
        result = clean_markdown_content(content)
        
        assert "Content" in result
        assert "styled text" in result
        assert "<div>" not in result
        assert "</div>" not in result
        assert "<span" not in result
        assert "style=" not in result
    
    def test_normalize_whitespace(self):
        """Test normalizing whitespace"""
        content = "Text   with    multiple\n\n\nspaces\n\n\nand\n\nlines"
        result = clean_markdown_content(content)
        
        assert "Text with multiple" in result
        assert "spaces and lines" in result
        # Should not have excessive whitespace
        assert "   " not in result
        assert "\n\n\n" not in result
    
    def test_remove_list_markers(self):
        """Test removing list markers"""
        content = """- Item 1
- Item 2
* Item 3
+ Item 4
1. Numbered item
2. Another numbered item
"""
        result = clean_markdown_content(content)
        
        assert "Item 1" in result
        assert "Item 2" in result
        assert "Item 3" in result
        assert "Item 4" in result
        assert "Numbered item" in result
        assert "Another numbered item" in result
        assert "-" not in result
        assert "*" not in result
        assert "+" not in result
        assert "1." not in result
        assert "2." not in result
    
    def test_complex_content(self):
        """Test cleaning complex markdown content"""
        content = """# Document Title

This is a paragraph with [a link](http://example.com) and `inline code`.

## Section

```python
def function():
    return "code"
```

- List item 1
- List item 2

![Image](image.png)

<div class="note">HTML content</div>

Final paragraph.
"""
        
        result = clean_markdown_content(content)
        
        # Should keep text content
        assert "Document Title" in result
        assert "This is a paragraph" in result
        assert "a link" in result
        assert "Section" in result
        assert "List item 1" in result
        assert "List item 2" in result
        assert "Image" in result
        assert "HTML content" in result
        assert "Final paragraph" in result
        
        # Should remove formatting
        assert "#" not in result
        assert "http://example.com" not in result
        assert "`" not in result
        assert "def function" not in result
        assert "python" not in result
        assert "-" not in result
        assert "image.png" not in result
        assert "<div" not in result
        assert "class=" not in result


class TestValidateAPIKey:
    """Test cases for validate_api_key function"""
    
    def test_valid_api_key(self):
        """Test valid API key"""
        valid_key = "sk-1234567890abcdef"
        result = validate_api_key(valid_key)
        assert result is True
    
    def test_empty_api_key(self):
        """Test empty API key"""
        result = validate_api_key("")
        assert result is False
    
    def test_none_api_key(self):
        """Test None API key"""
        result = validate_api_key(None)
        assert result is False
    
    def test_whitespace_api_key(self):
        """Test whitespace-only API key"""
        result = validate_api_key("   \n\t   ")
        assert result is False
    
    def test_short_api_key(self):
        """Test too short API key"""
        short_key = "abc"
        result = validate_api_key(short_key)
        assert result is False
    
    def test_long_valid_api_key(self):
        """Test long valid API key"""
        long_key = "sk-" + "a" * 100
        result = validate_api_key(long_key)
        assert result is True


class TestTruncateContent:
    """Test cases for truncate_content function"""
    
    def test_short_content(self):
        """Test content shorter than max length"""
        content = "Short content"
        result = truncate_content(content, 100)
        assert result == content
    
    def test_long_content(self):
        """Test content longer than max length"""
        content = "A" * 200
        result = truncate_content(content, 100)
        
        assert len(result) <= 103  # 100 + "..."
        assert result.endswith("...")
        assert result.startswith("A")
    
    def test_exact_length_content(self):
        """Test content exactly at max length"""
        content = "A" * 100
        result = truncate_content(content, 100)
        assert result == content
    
    def test_zero_max_length(self):
        """Test with zero max length"""
        content = "Some content"
        result = truncate_content(content, 0)
        assert result == "..."
    
    def test_negative_max_length(self):
        """Test with negative max length"""
        content = "Some content"
        result = truncate_content(content, -10)
        assert result == "..."
    
    def test_empty_content(self):
        """Test with empty content"""
        result = truncate_content("", 100)
        assert result == ""


class TestFormatFileSize:
    """Test cases for format_file_size function"""
    
    def test_bytes(self):
        """Test formatting bytes"""
        result = format_file_size(500)
        assert result == "500 B"
    
    def test_kilobytes(self):
        """Test formatting kilobytes"""
        result = format_file_size(1536)  # 1.5 KB
        assert result == "1.5 KB"
    
    def test_megabytes(self):
        """Test formatting megabytes"""
        result = format_file_size(2097152)  # 2 MB
        assert result == "2.0 MB"
    
    def test_gigabytes(self):
        """Test formatting gigabytes"""
        result = format_file_size(3221225472)  # 3 GB
        assert result == "3.0 GB"
    
    def test_zero_size(self):
        """Test formatting zero size"""
        result = format_file_size(0)
        assert result == "0 B"
    
    def test_exact_kb(self):
        """Test exact kilobyte size"""
        result = format_file_size(1024)
        assert result == "1.0 KB"
    
    def test_exact_mb(self):
        """Test exact megabyte size"""
        result = format_file_size(1048576)
        assert result == "1.0 MB"


class TestIsValidFolderPath:
    """Test cases for is_valid_folder_path function"""
    
    def test_valid_folder_paths(self):
        """Test valid folder paths"""
        valid_paths = [
            "blog/",
            "docs/",
            "articles/",
            "content/posts/",
            "src/pages/"
        ]
        
        for path in valid_paths:
            result = is_valid_folder_path(path)
            assert result is True, f"Path {path} should be valid"
    
    def test_invalid_folder_paths(self):
        """Test invalid folder paths"""
        invalid_paths = [
            "blog",  # Missing trailing slash
            "/blog/",  # Absolute path
            "../blog/",  # Parent directory reference
            "./blog/",  # Current directory reference
            "",  # Empty string
            "/",  # Root path
            "blog//",  # Double slash
            "blog/./",  # Current directory in path
            "blog/../",  # Parent directory in path
        ]
        
        for path in invalid_paths:
            result = is_valid_folder_path(path)
            assert result is False, f"Path {path} should be invalid"
    
    def test_none_path(self):
        """Test None path"""
        result = is_valid_folder_path(None)
        assert result is False
    
    def test_nested_valid_paths(self):
        """Test nested valid folder paths"""
        nested_paths = [
            "content/blog/",
            "src/content/posts/",
            "docs/api/reference/",
            "website/content/articles/"
        ]
        
        for path in nested_paths:
            result = is_valid_folder_path(path)
            assert result is True, f"Nested path {path} should be valid"
    
    def test_special_characters(self):
        """Test paths with special characters"""
        # Valid special characters
        valid_special = [
            "blog-posts/",
            "my_articles/",
            "content.backup/",
            "docs-v2/"
        ]
        
        for path in valid_special:
            result = is_valid_folder_path(path)
            assert result is True, f"Path with special chars {path} should be valid"
        
        # Invalid special characters
        invalid_special = [
            "blog:posts/",
            "my|articles/",
            "content<backup>/",
            "docs>v2/"
        ]
        
        for path in invalid_special:
            result = is_valid_folder_path(path)
            assert result is False, f"Path with invalid chars {path} should be invalid"