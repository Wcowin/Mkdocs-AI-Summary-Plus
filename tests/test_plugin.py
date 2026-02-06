"""Tests for the main AISummaryPlugin class."""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

from mkdocs.config import Config
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from mkdocs_ai_summary.plugin import AISummaryPlugin


class TestAISummaryPlugin(unittest.TestCase):
    """Test cases for AISummaryPlugin."""

    def setUp(self):
        """Set up test fixtures."""
        self.plugin = AISummaryPlugin()
        self.config = {
            'ai_service': 'deepseek',
            'summary_language': 'zh',
            'cache_enabled': True,
            'cache_expire_days': 30,
            'enabled_folders': ['docs'],
            'exclude_patterns': [],
            'exclude_files': [],
            'local_enabled': True,
            'ci_enabled': True,
            'ci_cache_only': False,
            'ci_fallback_summary': True,
            'fallback_services': ['openai'],
            'max_content_length': 8000,
            'summary_length': 'medium'
        }

    def test_plugin_initialization(self):
        """Test plugin initialization."""
        self.assertIsInstance(self.plugin, AISummaryPlugin)
        self.assertIsNone(self.plugin.config_manager)
        self.assertIsNone(self.plugin.cache_manager)
        self.assertIsNone(self.plugin.ai_service_manager)
        self.assertIsNone(self.plugin.content_processor)

    @patch.dict(os.environ, {'DEEPSEEK_API_KEY': 'test_key'})
    def test_on_config(self):
        """Test on_config hook."""
        mock_config = Mock()
        mock_config.__getitem__ = Mock(side_effect=lambda key: self.config.get(key))
        mock_config.get = Mock(side_effect=lambda key, default=None: self.config.get(key, default))
        
        # Mock the managers
        with patch('mkdocs_ai_summary.plugin.ConfigManager') as mock_config_manager, \
             patch('mkdocs_ai_summary.plugin.CacheManager') as mock_cache_manager, \
             patch('mkdocs_ai_summary.plugin.AIServiceManager') as mock_ai_manager, \
             patch('mkdocs_ai_summary.plugin.ContentProcessor') as mock_content_processor:
            
            result = self.plugin.on_config(mock_config)
            
            # Verify managers were created
            mock_config_manager.assert_called_once()
            mock_cache_manager.assert_called_once()
            mock_ai_manager.assert_called_once()
            mock_content_processor.assert_called_once()
            
            # Verify config is returned
            self.assertEqual(result, mock_config)

    def test_on_config_disabled_environment(self):
        """Test on_config when plugin is disabled in current environment."""
        mock_config = Mock()
        mock_config.__getitem__ = Mock(side_effect=lambda key: self.config.get(key))
        mock_config.get = Mock(side_effect=lambda key, default=None: self.config.get(key, default))
        
        with patch('mkdocs_ai_summary.plugin.ConfigManager') as mock_config_manager:
            mock_config_manager.return_value.should_run_plugin.return_value = False
            
            result = self.plugin.on_config(mock_config)
            
            # Plugin should be disabled
            self.assertFalse(self.plugin.enabled)
            self.assertEqual(result, mock_config)

    def test_on_page_markdown_disabled(self):
        """Test on_page_markdown when plugin is disabled."""
        self.plugin.enabled = False
        
        markdown = "# Test Page\n\nSome content."
        page = Mock()
        config = Mock()
        files = Mock()
        
        result = self.plugin.on_page_markdown(markdown, page, config, files)
        
        # Should return original markdown unchanged
        self.assertEqual(result, markdown)

    def test_on_page_markdown_enabled(self):
        """Test on_page_markdown when plugin is enabled."""
        self.plugin.enabled = True
        
        # Mock managers
        self.plugin.config_manager = Mock()
        self.plugin.cache_manager = Mock()
        self.plugin.ai_service_manager = Mock()
        self.plugin.content_processor = Mock()
        
        # Mock return values
        self.plugin.content_processor.should_generate_summary.return_value = True
        self.plugin.content_processor.process_page_content.return_value = "# Test Page\n\n**AI Summary:** Test summary\n\nSome content."
        
        markdown = "# Test Page\n\nSome content."
        page = Mock()
        page.file = Mock()
        page.file.src_path = "test.md"
        page.meta = {}
        config = Mock()
        files = Mock()
        
        result = self.plugin.on_page_markdown(markdown, page, config, files)
        
        # Should return processed markdown
        self.assertIn("AI Summary", result)
        self.plugin.content_processor.should_generate_summary.assert_called_once()
        self.plugin.content_processor.process_page_content.assert_called_once()

    def test_on_page_markdown_skip_summary(self):
        """Test on_page_markdown when summary should be skipped."""
        self.plugin.enabled = True
        
        # Mock managers
        self.plugin.config_manager = Mock()
        self.plugin.cache_manager = Mock()
        self.plugin.ai_service_manager = Mock()
        self.plugin.content_processor = Mock()
        
        # Mock return values
        self.plugin.content_processor.should_generate_summary.return_value = False
        
        markdown = "# Test Page\n\nSome content."
        page = Mock()
        page.file = Mock()
        page.file.src_path = "test.md"
        page.meta = {}
        config = Mock()
        files = Mock()
        
        result = self.plugin.on_page_markdown(markdown, page, config, files)
        
        # Should return original markdown
        self.assertEqual(result, markdown)
        self.plugin.content_processor.should_generate_summary.assert_called_once()
        self.plugin.content_processor.process_page_content.assert_not_called()

    def test_on_post_build(self):
        """Test on_post_build hook."""
        self.plugin.enabled = True
        self.plugin.cache_manager = Mock()
        
        config = Mock()
        
        self.plugin.on_post_build(config)
        
        # Should call cleanup_expired_cache
        self.plugin.cache_manager.cleanup_expired_cache.assert_called_once()

    def test_on_post_build_disabled(self):
        """Test on_post_build when plugin is disabled."""
        self.plugin.enabled = False
        self.plugin.cache_manager = Mock()
        
        config = Mock()
        
        self.plugin.on_post_build(config)
        
        # Should not call cleanup
        self.plugin.cache_manager.cleanup_expired_cache.assert_not_called()

    def test_on_post_build_no_cache_manager(self):
        """Test on_post_build when cache manager is not initialized."""
        self.plugin.enabled = True
        self.plugin.cache_manager = None
        
        config = Mock()
        
        # Should not raise an exception
        try:
            self.plugin.on_post_build(config)
        except Exception as e:
            self.fail(f"on_post_build raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()