"""Tests for content processor module"""

import pytest
from unittest.mock import Mock

from mkdocs_ai_summary.content_processor import ContentProcessor


class TestContentProcessor:
    """Test cases for ContentProcessor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = {
            'enabled_folders': ['blog/', 'docs/'],
            'exclude_patterns': ['index.md'],
            'exclude_files': ['blog/index.md'],
            'summary_language': 'zh'
        }
        self.processor = ContentProcessor(self.config)
    
    def test_initialization(self):
        """Test ContentProcessor initialization"""
        assert self.processor.config == self.config
        assert self.processor.enabled_folders == ['blog/', 'docs/']
        assert self.processor.exclude_patterns == ['index.md']
        assert self.processor.exclude_files == ['blog/index.md']
        assert self.processor.language == 'zh'
    
    def test_should_generate_summary_enabled_folder(self):
        """Test should_generate_summary for enabled folder"""
        # Create mock page
        mock_page = Mock()
        mock_page.file.src_path = 'blog/test-post.md'
        mock_page.meta = {}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is True
    
    def test_should_generate_summary_disabled_folder(self):
        """Test should_generate_summary for disabled folder"""
        # Create mock page
        mock_page = Mock()
        mock_page.file.src_path = 'other/test.md'
        mock_page.meta = {}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is False
    
    def test_should_generate_summary_excluded_pattern(self):
        """Test should_generate_summary for excluded pattern"""
        # Create mock page
        mock_page = Mock()
        mock_page.file.src_path = 'blog/index.md'
        mock_page.meta = {}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is False
    
    def test_should_generate_summary_excluded_file(self):
        """Test should_generate_summary for excluded file"""
        # Create mock page
        mock_page = Mock()
        mock_page.file.src_path = 'blog/index.md'
        mock_page.meta = {}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is False
    
    def test_should_generate_summary_meta_disabled(self):
        """Test should_generate_summary when disabled in page meta"""
        # Create mock page with ai_summary disabled
        mock_page = Mock()
        mock_page.file.src_path = 'blog/test.md'
        mock_page.meta = {'ai_summary': False}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is False
    
    def test_should_generate_summary_meta_enabled(self):
        """Test should_generate_summary when explicitly enabled in page meta"""
        # Create mock page with ai_summary enabled (overrides folder rules)
        mock_page = Mock()
        mock_page.file.src_path = 'other/test.md'  # Not in enabled folders
        mock_page.meta = {'ai_summary': True}
        
        result = self.processor.should_generate_summary(mock_page)
        
        assert result is True
    
    def test_clean_content_for_ai_basic(self):
        """Test basic content cleaning for AI processing"""
        content = """# Title

This is a paragraph with some text.

## Subtitle

Another paragraph here.

```python
code_block = "should be removed"
```

- List item 1
- List item 2
"""
        
        cleaned = self.processor.clean_content_for_ai(content)
        
        # Should remove markdown formatting but keep text content
        assert "Title" in cleaned
        assert "This is a paragraph" in cleaned
        assert "Subtitle" in cleaned
        assert "Another paragraph" in cleaned
        assert "List item 1" in cleaned
        assert "List item 2" in cleaned
        
        # Should remove code blocks
        assert "code_block" not in cleaned
        assert "python" not in cleaned
    
    def test_clean_content_for_ai_links_and_images(self):
        """Test cleaning links and images from content"""
        content = """Here is a [link](http://example.com) and an ![image](image.png).

Another [internal link](../other.md) here.
"""
        
        cleaned = self.processor.clean_content_for_ai(content)
        
        # Should keep link text but remove URLs
        assert "link" in cleaned
        assert "internal link" in cleaned
        assert "image" in cleaned
        
        # Should remove URLs and image paths
        assert "http://example.com" not in cleaned
        assert "image.png" not in cleaned
        assert "../other.md" not in cleaned
    
    def test_clean_content_for_ai_html_tags(self):
        """Test cleaning HTML tags from content"""
        content = """<div class="container">
    <p>This is <strong>bold</strong> text.</p>
    <span style="color: red;">Red text</span>
</div>
"""
        
        cleaned = self.processor.clean_content_for_ai(content)
        
        # Should keep text content
        assert "This is" in cleaned
        assert "bold" in cleaned
        assert "text" in cleaned
        assert "Red text" in cleaned
        
        # Should remove HTML tags and attributes
        assert "<div" not in cleaned
        assert "class=" not in cleaned
        assert "<strong>" not in cleaned
        assert "style=" not in cleaned
    
    def test_clean_content_for_ai_whitespace(self):
        """Test cleaning excessive whitespace"""
        content = """Title



Paragraph with    multiple   spaces.



Another paragraph.


"""
        
        cleaned = self.processor.clean_content_for_ai(content)
        
        # Should normalize whitespace
        assert "Title" in cleaned
        assert "Paragraph with multiple spaces" in cleaned
        assert "Another paragraph" in cleaned
        
        # Should not have excessive newlines or spaces
        assert "\n\n\n" not in cleaned
        assert "    " not in cleaned
    
    def test_get_content_hash(self):
        """Test content hash generation"""
        content1 = "This is test content"
        content2 = "This is different content"
        content3 = "This is test content"  # Same as content1
        
        hash1 = self.processor.get_content_hash(content1)
        hash2 = self.processor.get_content_hash(content2)
        hash3 = self.processor.get_content_hash(content3)
        
        # Hashes should be strings
        assert isinstance(hash1, str)
        assert isinstance(hash2, str)
        assert isinstance(hash3, str)
        
        # Same content should produce same hash
        assert hash1 == hash3
        
        # Different content should produce different hash
        assert hash1 != hash2
    
    def test_format_summary_chinese(self):
        """Test summary formatting for Chinese language"""
        summary = "这是一个测试摘要"
        service = "glm"
        
        formatted = self.processor.format_summary(summary, service)
        
        assert isinstance(formatted, str)
        assert summary in formatted
        assert "摘要" in formatted or "AI" in formatted
        # Should contain some formatting (admonition or similar)
        assert "!!!" in formatted or ":::" in formatted
    
    def test_format_summary_english(self):
        """Test summary formatting for English language"""
        self.processor.language = 'en'
        summary = "This is a test summary"
        service = "openai"
        
        formatted = self.processor.format_summary(summary, service)
        
        assert isinstance(formatted, str)
        assert summary in formatted
        assert "Summary" in formatted or "AI" in formatted
        # Should contain some formatting (admonition or similar)
        assert "!!!" in formatted or ":::" in formatted
    
    def test_format_summary_different_services(self):
        """Test summary formatting for different AI services"""
        summary = "Test summary"
        
        # Test different services
        services = ['glm', 'openai', 'deepseek', 'gemini']
        
        for service in services:
            formatted = self.processor.format_summary(summary, service)
            
            assert isinstance(formatted, str)
            assert summary in formatted
            # Each service might have different styling
            assert len(formatted) > len(summary)  # Should add formatting
    
    def test_inject_summary_at_beginning(self):
        """Test injecting summary at the beginning of content"""
        original_content = """# Document Title

This is the first paragraph of the document.

## Section 1

More content here.
"""
        
        formatted_summary = "!!! info \"AI Summary\"\n    This is the summary."
        
        result = self.processor.inject_summary(original_content, formatted_summary)
        
        # Summary should be at the beginning
        assert result.startswith(formatted_summary)
        
        # Original content should follow
        assert "# Document Title" in result
        assert "This is the first paragraph" in result
        
        # Should have proper spacing
        lines = result.split('\n')
        assert len(lines) > len(original_content.split('\n'))
    
    def test_inject_summary_empty_content(self):
        """Test injecting summary into empty content"""
        original_content = ""
        formatted_summary = "!!! info \"AI Summary\"\n    This is the summary."
        
        result = self.processor.inject_summary(original_content, formatted_summary)
        
        # Should just return the formatted summary
        assert result == formatted_summary
    
    def test_inject_summary_whitespace_handling(self):
        """Test proper whitespace handling when injecting summary"""
        original_content = "\n\n# Title\n\nContent"
        formatted_summary = "Summary content"
        
        result = self.processor.inject_summary(original_content, formatted_summary)
        
        # Should handle leading whitespace properly
        assert result.startswith(formatted_summary)
        assert "# Title" in result
        assert "Content" in result
    
    def test_enabled_folders_normalization(self):
        """Test that enabled folders are properly normalized"""
        # Test with various folder formats
        config = {
            'enabled_folders': ['blog', 'docs/', 'articles'],
            'exclude_patterns': [],
            'exclude_files': [],
            'summary_language': 'en'
        }
        
        processor = ContentProcessor(config)
        
        # All folders should be normalized to end with '/'
        expected_folders = ['blog/', 'docs/', 'articles/']
        assert processor.enabled_folders == expected_folders
    
    def test_path_matching_edge_cases(self):
        """Test edge cases in path matching"""
        # Create mock page with edge case path
        mock_page = Mock()
        mock_page.meta = {}
        
        # Test root level file
        mock_page.file.src_path = 'README.md'
        result = self.processor.should_generate_summary(mock_page)
        assert result is False  # Not in enabled folders
        
        # Test nested path
        mock_page.file.src_path = 'blog/2023/post.md'
        result = self.processor.should_generate_summary(mock_page)
        assert result is True  # In blog/ folder
        
        # Test exact folder match
        mock_page.file.src_path = 'blog/post.md'
        result = self.processor.should_generate_summary(mock_page)
        assert result is True