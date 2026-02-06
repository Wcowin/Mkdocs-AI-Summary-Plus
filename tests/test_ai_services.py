"""Tests for AI services module"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from mkdocs_ai_summary.ai_services import AIServiceManager


class TestAIServiceManager:
    """Test cases for AIServiceManager"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = {
            'ai_service': 'glm',
            'model': 'glm-4-flash',
            'max_tokens': 300,
            'temperature': 0.3,
            'summary_language': 'zh'
        }
        self.manager = AIServiceManager(self.config)
    
    def test_initialization(self):
        """Test AIServiceManager initialization"""
        assert self.manager.config == self.config
        assert self.manager.service == 'glm'
        assert self.manager.model == 'glm-4-flash'
        assert self.manager.max_tokens == 300
        assert self.manager.temperature == 0.3
        assert self.manager.language == 'zh'
    
    def test_build_prompt_chinese(self):
        """Test prompt building for Chinese language"""
        content = "这是一个测试文档"
        prompt = self.manager._build_prompt(content)
        
        assert isinstance(prompt, str)
        assert "中文" in prompt or "摘要" in prompt
        assert content in prompt
    
    def test_build_prompt_english(self):
        """Test prompt building for English language"""
        self.manager.language = 'en'
        content = "This is a test document"
        prompt = self.manager._build_prompt(content)
        
        assert isinstance(prompt, str)
        assert "summary" in prompt.lower() or "summarize" in prompt.lower()
        assert content in prompt
    
    @patch('os.getenv')
    def test_get_api_key_glm(self, mock_getenv):
        """Test API key retrieval for GLM service"""
        mock_getenv.return_value = "test_glm_key"
        
        api_key = self.manager._get_api_key('glm')
        
        mock_getenv.assert_called_with('GLM_API_KEY')
        assert api_key == "test_glm_key"
    
    @patch('os.getenv')
    def test_get_api_key_openai(self, mock_getenv):
        """Test API key retrieval for OpenAI service"""
        mock_getenv.return_value = "test_openai_key"
        
        api_key = self.manager._get_api_key('openai')
        
        mock_getenv.assert_called_with('OPENAI_API_KEY')
        assert api_key == "test_openai_key"
    
    @patch('os.getenv')
    def test_get_api_key_deepseek(self, mock_getenv):
        """Test API key retrieval for DeepSeek service"""
        mock_getenv.return_value = "test_deepseek_key"
        
        api_key = self.manager._get_api_key('deepseek')
        
        mock_getenv.assert_called_with('DEEPSEEK_API_KEY')
        assert api_key == "test_deepseek_key"
    
    @patch('os.getenv')
    def test_get_api_key_gemini(self, mock_getenv):
        """Test API key retrieval for Gemini service"""
        mock_getenv.return_value = "test_gemini_key"
        
        api_key = self.manager._get_api_key('gemini')
        
        mock_getenv.assert_called_with('GEMINI_API_KEY')
        assert api_key == "test_gemini_key"
    
    @patch('os.getenv')
    def test_get_api_key_missing(self, mock_getenv):
        """Test API key retrieval when key is missing"""
        mock_getenv.return_value = None
        
        api_key = self.manager._get_api_key('glm')
        
        assert api_key is None
    
    @patch('requests.post')
    @patch('os.getenv')
    def test_call_openai_compatible_success(self, mock_getenv, mock_post):
        """Test successful OpenAI compatible API call"""
        mock_getenv.return_value = "test_api_key"
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Generated summary'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        content = "Test content"
        result = self.manager._call_openai_compatible('glm', content)
        
        assert result == 'Generated summary'
        mock_post.assert_called_once()
    
    @patch('requests.post')
    @patch('os.getenv')
    def test_call_openai_compatible_api_error(self, mock_getenv, mock_post):
        """Test OpenAI compatible API call with API error"""
        mock_getenv.return_value = "test_api_key"
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        content = "Test content"
        result = self.manager._call_openai_compatible('glm', content)
        
        assert result is None
    
    @patch('requests.post')
    @patch('os.getenv')
    def test_call_openai_compatible_network_error(self, mock_getenv, mock_post):
        """Test OpenAI compatible API call with network error"""
        mock_getenv.return_value = "test_api_key"
        
        # Mock network error
        mock_post.side_effect = requests.RequestException("Network error")
        
        content = "Test content"
        result = self.manager._call_openai_compatible('glm', content)
        
        assert result is None
    
    @patch('requests.post')
    @patch('os.getenv')
    def test_call_gemini_success(self, mock_getenv, mock_post):
        """Test successful Gemini API call"""
        mock_getenv.return_value = "test_api_key"
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Generated summary'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response
        
        content = "Test content"
        result = self.manager._call_gemini(content)
        
        assert result == 'Generated summary'
        mock_post.assert_called_once()
    
    @patch('requests.post')
    @patch('os.getenv')
    def test_call_gemini_api_error(self, mock_getenv, mock_post):
        """Test Gemini API call with API error"""
        mock_getenv.return_value = "test_api_key"
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        content = "Test content"
        result = self.manager._call_gemini(content)
        
        assert result is None
    
    @patch.object(AIServiceManager, '_call_openai_compatible')
    @patch('os.getenv')
    def test_generate_summary_success(self, mock_getenv, mock_call_openai):
        """Test successful summary generation"""
        mock_getenv.return_value = "test_api_key"
        mock_call_openai.return_value = "Generated summary"
        
        content = "Test content"
        result = self.manager.generate_summary(content)
        
        assert result == "Generated summary"
        mock_call_openai.assert_called_once_with('glm', content)
    
    @patch.object(AIServiceManager, '_call_openai_compatible')
    @patch('os.getenv')
    def test_generate_summary_no_api_key(self, mock_getenv, mock_call_openai):
        """Test summary generation without API key"""
        mock_getenv.return_value = None
        
        content = "Test content"
        result = self.manager.generate_summary(content)
        
        assert result is None
        mock_call_openai.assert_not_called()
    
    @patch.object(AIServiceManager, '_call_openai_compatible')
    @patch.object(AIServiceManager, '_get_api_key')
    def test_generate_summary_with_fallback(self, mock_get_api_key, mock_call_openai):
        """Test summary generation with service fallback"""
        # First service fails (no API key), second succeeds
        mock_get_api_key.side_effect = [None, "backup_key"]
        mock_call_openai.return_value = "Fallback summary"
        
        # Configure fallback services
        self.manager.config['fallback_services'] = ['openai']
        
        content = "Test content"
        result = self.manager.generate_summary(content)
        
        # Should try fallback service
        assert mock_get_api_key.call_count >= 1
    
    def test_get_service_config_glm(self):
        """Test service configuration for GLM"""
        config = self.manager._get_service_config('glm')
        
        assert 'url' in config
        assert 'headers' in config
        assert 'data' in config
        assert config['url'] == 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    
    def test_get_service_config_openai(self):
        """Test service configuration for OpenAI"""
        config = self.manager._get_service_config('openai')
        
        assert 'url' in config
        assert 'headers' in config
        assert 'data' in config
        assert config['url'] == 'https://api.openai.com/v1/chat/completions'
    
    def test_get_service_config_deepseek(self):
        """Test service configuration for DeepSeek"""
        config = self.manager._get_service_config('deepseek')
        
        assert 'url' in config
        assert 'headers' in config
        assert 'data' in config
        assert config['url'] == 'https://api.deepseek.com/chat/completions'
    
    def test_get_service_config_unknown(self):
        """Test service configuration for unknown service"""
        config = self.manager._get_service_config('unknown')
        
        assert config is None