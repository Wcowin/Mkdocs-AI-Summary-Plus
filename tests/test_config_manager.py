"""Tests for the ConfigManager class."""

import os
import unittest
from unittest.mock import patch, Mock

from mkdocs_ai_summary.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager."""

    def setUp(self):
        """Set up test fixtures."""
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
        self.manager = ConfigManager(self.config)

    def test_initialization(self):
        """Test ConfigManager initialization."""
        self.assertEqual(self.manager.config, self.config)
        self.assertIsInstance(self.manager.is_ci, bool)
        self.assertIsInstance(self.manager.ci_name, (str, type(None)))

    @patch.dict(os.environ, {'CI': 'true'})
    def test_detect_ci_environment_github(self):
        """Test CI environment detection for GitHub Actions."""
        with patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'}):
            manager = ConfigManager(self.config)
            self.assertTrue(manager.is_ci)
            self.assertEqual(manager.ci_name, 'GitHub Actions')

    @patch.dict(os.environ, {'CI': 'true', 'GITLAB_CI': 'true'})
    def test_detect_ci_environment_gitlab(self):
        """Test CI environment detection for GitLab CI."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.is_ci)
        self.assertEqual(manager.ci_name, 'GitLab CI')

    @patch.dict(os.environ, {'CI': 'true', 'TRAVIS': 'true'})
    def test_detect_ci_environment_travis(self):
        """Test CI environment detection for Travis CI."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.is_ci)
        self.assertEqual(manager.ci_name, 'Travis CI')

    @patch.dict(os.environ, {'CIRCLECI': 'true'})
    def test_detect_ci_environment_circle(self):
        """Test CI environment detection for CircleCI."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.is_ci)
        self.assertEqual(manager.ci_name, 'CircleCI')

    @patch.dict(os.environ, {'JENKINS_URL': 'http://jenkins.example.com'})
    def test_detect_ci_environment_jenkins(self):
        """Test CI environment detection for Jenkins."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.is_ci)
        self.assertEqual(manager.ci_name, 'Jenkins')

    @patch.dict(os.environ, {}, clear=True)
    def test_detect_local_environment(self):
        """Test local environment detection."""
        manager = ConfigManager(self.config)
        self.assertFalse(manager.is_ci)
        self.assertIsNone(manager.ci_name)

    def test_should_run_plugin_local_enabled(self):
        """Test should_run_plugin in local environment when enabled."""
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager(self.config)
            self.assertTrue(manager.should_run_plugin())

    def test_should_run_plugin_local_disabled(self):
        """Test should_run_plugin in local environment when disabled."""
        config = self.config.copy()
        config['local_enabled'] = False
        
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager(config)
            self.assertFalse(manager.should_run_plugin())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_should_run_plugin_ci_enabled(self):
        """Test should_run_plugin in CI environment when enabled."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.should_run_plugin())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_should_run_plugin_ci_disabled(self):
        """Test should_run_plugin in CI environment when disabled."""
        config = self.config.copy()
        config['ci_enabled'] = False
        
        manager = ConfigManager(config)
        self.assertFalse(manager.should_run_plugin())

    def test_should_generate_new_summary_local(self):
        """Test should_generate_new_summary in local environment."""
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager(self.config)
            self.assertTrue(manager.should_generate_new_summary())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_should_generate_new_summary_ci_cache_only_false(self):
        """Test should_generate_new_summary in CI when cache_only is False."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.should_generate_new_summary())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_should_generate_new_summary_ci_cache_only_true(self):
        """Test should_generate_new_summary in CI when cache_only is True."""
        config = self.config.copy()
        config['ci_cache_only'] = True
        
        manager = ConfigManager(config)
        self.assertFalse(manager.should_generate_new_summary())

    def test_log_environment_status_local(self):
        """Test log_environment_status in local environment."""
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager(self.config)
            
            # Should not raise an exception
            try:
                manager.log_environment_status()
            except Exception as e:
                self.fail(f"log_environment_status raised an exception: {e}")

    @patch.dict(os.environ, {'CI': 'true', 'GITHUB_ACTIONS': 'true'})
    def test_log_environment_status_ci(self):
        """Test log_environment_status in CI environment."""
        manager = ConfigManager(self.config)
        
        # Should not raise an exception
        try:
            manager.log_environment_status()
        except Exception as e:
            self.fail(f"log_environment_status raised an exception: {e}")

    def test_is_fallback_summary_enabled_local(self):
        """Test is_fallback_summary_enabled in local environment."""
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager(self.config)
            # Fallback summary is not used in local environment
            self.assertFalse(manager.is_fallback_summary_enabled())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_is_fallback_summary_enabled_ci_true(self):
        """Test is_fallback_summary_enabled in CI when enabled."""
        manager = ConfigManager(self.config)
        self.assertTrue(manager.is_fallback_summary_enabled())

    @patch.dict(os.environ, {'CI': 'true'})
    def test_is_fallback_summary_enabled_ci_false(self):
        """Test is_fallback_summary_enabled in CI when disabled."""
        config = self.config.copy()
        config['ci_fallback_summary'] = False
        
        manager = ConfigManager(config)
        self.assertFalse(manager.is_fallback_summary_enabled())

    def test_get_config_value(self):
        """Test getting configuration values."""
        self.assertEqual(self.manager.config['ai_service'], 'deepseek')
        self.assertEqual(self.manager.config['summary_language'], 'zh')
        self.assertTrue(self.manager.config['cache_enabled'])

    def test_config_validation(self):
        """Test configuration validation."""
        # Test with valid config
        valid_config = self.config.copy()
        manager = ConfigManager(valid_config)
        self.assertIsNotNone(manager)
        
        # Test with missing required fields
        invalid_config = {}
        try:
            ConfigManager(invalid_config)
        except (KeyError, ValueError):
            # Expected to fail with missing configuration
            pass
        else:
            self.fail("ConfigManager should validate required configuration")


if __name__ == '__main__':
    unittest.main()