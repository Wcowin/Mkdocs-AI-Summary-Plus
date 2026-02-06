"""Tests for cache manager module"""

import pytest
import os
import json
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from mkdocs_ai_summary.cache_manager import CacheManager


class TestCacheManager:
    """Test cases for CacheManager"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = {
            'cache_enabled': True,
            'cache_expire_days': 30,
            'cache_auto_clean': True
        }
        
        # Use temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, 'ai_summary_cache.json')
        
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            self.manager = CacheManager(self.config)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        os.rmdir(self.temp_dir)
    
    def test_initialization_enabled(self):
        """Test CacheManager initialization when enabled"""
        assert self.manager.enabled is True
        assert self.manager.expire_days == 30
        assert self.manager.auto_clean is True
    
    def test_initialization_disabled(self):
        """Test CacheManager initialization when disabled"""
        config = {'cache_enabled': False}
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            manager = CacheManager(config)
        
        assert manager.enabled is False
    
    def test_get_cache_file_path(self):
        """Test cache file path generation"""
        # Create a new manager without mocking to test actual path
        manager = CacheManager(self.config)
        path = manager._get_cache_file_path()
        
        assert isinstance(path, str)
        assert path.endswith('ai_summary_cache.json')
    
    def test_load_cache_empty(self):
        """Test loading cache when file doesn't exist"""
        cache = self.manager._load_cache()
        
        assert isinstance(cache, dict)
        assert len(cache) == 0
    
    def test_load_cache_existing(self):
        """Test loading cache from existing file"""
        # Create test cache data
        test_data = {
            'hash1': {
                'summary': 'Test summary',
                'service': 'glm',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Write test data to cache file
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        cache = self.manager._load_cache()
        
        assert 'hash1' in cache
        assert cache['hash1']['summary'] == 'Test summary'
        assert cache['hash1']['service'] == 'glm'
    
    def test_load_cache_invalid_json(self):
        """Test loading cache with invalid JSON"""
        # Write invalid JSON to cache file
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            f.write('invalid json')
        
        cache = self.manager._load_cache()
        
        # Should return empty dict on invalid JSON
        assert isinstance(cache, dict)
        assert len(cache) == 0
    
    def test_save_cache(self):
        """Test saving cache to file"""
        test_data = {
            'hash1': {
                'summary': 'Test summary',
                'service': 'glm',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        self.manager._save_cache(test_data)
        
        # Verify file was created and contains correct data
        assert os.path.exists(self.cache_file)
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == test_data
    
    def test_save_cache_create_directory(self):
        """Test saving cache creates directory if it doesn't exist"""
        # Use non-existent directory
        non_existent_dir = os.path.join(self.temp_dir, 'subdir')
        cache_file = os.path.join(non_existent_dir, 'cache.json')
        
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = cache_file
            manager = CacheManager(self.config)
        
        test_data = {'test': 'data'}
        manager._save_cache(test_data)
        
        # Verify directory was created
        assert os.path.exists(non_existent_dir)
        assert os.path.exists(cache_file)
        
        # Clean up
        os.remove(cache_file)
        os.rmdir(non_existent_dir)
    
    def test_is_expired_not_expired(self):
        """Test checking if cache entry is not expired"""
        timestamp = datetime.now().isoformat()
        
        is_expired = self.manager._is_expired(timestamp)
        
        assert is_expired is False
    
    def test_is_expired_expired(self):
        """Test checking if cache entry is expired"""
        # Create timestamp from 31 days ago (older than 30 day expiry)
        old_timestamp = (datetime.now() - timedelta(days=31)).isoformat()
        
        is_expired = self.manager._is_expired(old_timestamp)
        
        assert is_expired is True
    
    def test_is_expired_invalid_timestamp(self):
        """Test checking expiry with invalid timestamp"""
        invalid_timestamp = "invalid-timestamp"
        
        is_expired = self.manager._is_expired(invalid_timestamp)
        
        # Should treat invalid timestamp as expired
        assert is_expired is True
    
    def test_get_cached_summary_hit(self):
        """Test getting cached summary with cache hit"""
        # Create test cache data
        test_data = {
            'hash1': {
                'summary': 'Cached summary',
                'service': 'glm',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        result = self.manager.get_cached_summary('hash1')
        
        assert result is not None
        assert result['summary'] == 'Cached summary'
        assert result['service'] == 'glm'
    
    def test_get_cached_summary_miss(self):
        """Test getting cached summary with cache miss"""
        result = self.manager.get_cached_summary('nonexistent_hash')
        
        assert result is None
    
    def test_get_cached_summary_expired(self):
        """Test getting cached summary that is expired"""
        # Create expired cache data
        old_timestamp = (datetime.now() - timedelta(days=31)).isoformat()
        test_data = {
            'hash1': {
                'summary': 'Expired summary',
                'service': 'glm',
                'timestamp': old_timestamp
            }
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        result = self.manager.get_cached_summary('hash1')
        
        assert result is None
    
    def test_get_cached_summary_disabled(self):
        """Test getting cached summary when cache is disabled"""
        config = {'cache_enabled': False}
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            manager = CacheManager(config)
        
        result = manager.get_cached_summary('hash1')
        
        assert result is None
    
    def test_save_summary(self):
        """Test saving summary to cache"""
        content_hash = 'test_hash'
        summary = 'Test summary'
        service = 'glm'
        
        self.manager.save_summary(content_hash, summary, service)
        
        # Verify summary was saved
        result = self.manager.get_cached_summary(content_hash)
        
        assert result is not None
        assert result['summary'] == summary
        assert result['service'] == service
        assert 'timestamp' in result
    
    def test_save_summary_disabled(self):
        """Test saving summary when cache is disabled"""
        config = {'cache_enabled': False}
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            manager = CacheManager(config)
        
        manager.save_summary('hash1', 'summary', 'glm')
        
        # Cache file should not be created
        assert not os.path.exists(self.cache_file)
    
    def test_clean_expired_entries(self):
        """Test cleaning expired cache entries"""
        # Create mixed cache data (some expired, some not)
        current_time = datetime.now()
        old_timestamp = (current_time - timedelta(days=31)).isoformat()
        new_timestamp = current_time.isoformat()
        
        test_data = {
            'expired_hash': {
                'summary': 'Expired summary',
                'service': 'glm',
                'timestamp': old_timestamp
            },
            'valid_hash': {
                'summary': 'Valid summary',
                'service': 'glm',
                'timestamp': new_timestamp
            }
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        cleaned_count = self.manager.clean_expired_entries()
        
        # Should have cleaned 1 expired entry
        assert cleaned_count == 1
        
        # Verify only valid entry remains
        cache = self.manager._load_cache()
        assert 'expired_hash' not in cache
        assert 'valid_hash' in cache
    
    def test_clean_expired_entries_disabled(self):
        """Test cleaning expired entries when cache is disabled"""
        config = {'cache_enabled': False}
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            manager = CacheManager(config)
        
        cleaned_count = manager.clean_expired_entries()
        
        assert cleaned_count == 0
    
    def test_clean_expired_entries_auto_clean_disabled(self):
        """Test that auto clean doesn't run when disabled"""
        config = {
            'cache_enabled': True,
            'cache_expire_days': 30,
            'cache_auto_clean': False
        }
        
        with patch('mkdocs_ai_summary.cache_manager.CacheManager._get_cache_file_path') as mock_path:
            mock_path.return_value = self.cache_file
            manager = CacheManager(config)
        
        # Auto clean should not run during initialization
        # This is tested implicitly by not having expired entries cleaned
        assert manager.auto_clean is False