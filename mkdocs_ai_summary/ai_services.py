"""AI服务管理器模块

负责管理多种AI服务的调用和降级处理。
"""

import os
import requests
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from pathlib import Path

# 改进的环境变量加载逻辑
def load_env_files():
    """从多个位置加载.env文件"""
    env_paths = [
        Path.cwd() / '.env',  # 当前工作目录
        Path.home() / '.env',  # 用户主目录
        Path(__file__).parent.parent.parent / '.env',  # 项目根目录
        Path(__file__).parent.parent / '.env',  # 上级目录
    ]
    
    loaded_files = []
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            loaded_files.append(str(env_path))
    
    # 静默加载环境变量，避免不必要的输出
    pass

# 加载环境变量
load_env_files()


class AIServiceManager:
    """AI服务管理器"""
    
    def __init__(self, default_service: str, model: str, max_tokens: int, temperature: float, 
                 fallback_services: list = None, custom_services: dict = None):
        """初始化AI服务管理器
        
        Args:
            default_service: 默认AI服务名称
            model: 模型名称
            max_tokens: 最大token数
            temperature: 温度参数
            fallback_services: 备用服务列表
            custom_services: 自定义服务配置字典
        """
        self.default_service = default_service
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # AI服务配置（内置服务）
        self.ai_services = {
            'deepseek': {
                'url': 'https://api.deepseek.com/v1/chat/completions',
                'model': 'deepseek-chat',
                'api_key': os.getenv('DEEPSEEK_API_KEY'),
                'type': 'openai_compatible'
            },
            'openai': {
                'url': 'https://api.chatanywhere.tech/v1/chat/completions',
                'model': 'gpt-3.5-turbo',
                'api_key': os.getenv('OPENAI_API_KEY'),
                'type': 'openai_compatible'
            },
            'gemini': {
                'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
                'model': 'gemini-pro',
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'type': 'gemini'
            },
            'glm': {
                'url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
                'model': 'glm-4-flash',
                'api_key': os.getenv('GLM_API_KEY'),
                'type': 'openai_compatible'
            },
            'siliconflow': {
                'url': 'https://api.siliconflow.cn/v1/chat/completions',
                'model': 'deepseek-ai/DeepSeek-V3',
                'api_key': os.getenv('SILICONFLOW_API_KEY'),
                'type': 'openai_compatible'
            }
        }
        
        # 合并自定义服务配置
        if custom_services:
            self._add_custom_services(custom_services)
        
        # 设置服务降级顺序
        if fallback_services:
            self.fallback_order = fallback_services
        else:
            # 默认降级顺序
            self.fallback_order = ['siliconflow', 'openai', 'glm', 'deepseek', 'gemini']
    
    def _add_custom_services(self, custom_services: dict):
        """添加自定义服务配置
        
        Args:
            custom_services: 自定义服务配置字典
            格式示例:
            {
                'my_service': {
                    'url': 'https://api.example.com/v1/chat/completions',
                    'model': 'my-model',
                    'api_key_env': 'MY_SERVICE_API_KEY',  # 环境变量名
                    'type': 'openai_compatible'  # 或 'gemini'
                }
            }
        """
        for service_name, config in custom_services.items():
            # 从环境变量获取 API 密钥
            api_key_env = config.get('api_key_env', f'{service_name.upper()}_API_KEY')
            api_key = os.getenv(api_key_env)
            
            # 如果直接提供了 api_key，使用提供的值
            if 'api_key' in config:
                api_key = config['api_key']
            
            self.ai_services[service_name] = {
                'url': config['url'],
                'model': config.get('model', 'default-model'),
                'api_key': api_key,
                'type': config.get('type', 'openai_compatible')
            }
            
            # 如果配置中指定了 headers，也保存下来
            if 'headers' in config:
                self.ai_services[service_name]['headers'] = config['headers']
    
    def generate_summary(self, content: str, title: str, language: str = 'zh', debug: bool = False) -> Optional[Dict[str, Any]]:
        """生成AI摘要
        
        Args:
            content: 页面内容
            title: 页面标题
            language: 摘要语言 ('zh', 'en', 'both')
            debug: 是否显示调试信息
            
        Returns:
            dict|None: 包含摘要和服务信息的字典，失败时返回None
        """
        # 首先尝试默认服务
        if debug:
            print(f"🔄 尝试默认服务: {self.default_service}")
        result = self._try_service(self.default_service, content, title, language, debug)
        if result:
            return result
        
        # 如果默认服务失败，按照 fallback_order 顺序尝试备用服务
        for service_name in self.fallback_order:
            if service_name != self.default_service:
                if debug:
                    print(f"🔄 尝试备用服务: {service_name}")
                result = self._try_service(service_name, content, title, language, debug)
                if result:
                    return result
        
        return None
    
    def _try_service(self, service_name: str, content: str, title: str, language: str = 'zh', debug: bool = False) -> Optional[Dict[str, Any]]:
        """尝试调用指定的AI服务
        
        Args:
            service_name: 服务名称
            content: 页面内容
            title: 页面标题
            language: 摘要语言
            debug: 是否显示调试信息
            
        Returns:
            dict|None: 包含摘要和服务信息的字典，失败时返回None
        """
        service_config = self.ai_services.get(service_name)
        if not service_config or not service_config.get('api_key'):
            if debug:
                print(f"⚠️ {service_name} 不可用: 缺少API密钥")
            return None
        
        try:
            # 根据服务类型选择调用方法
            service_type = service_config.get('type', 'openai_compatible')
            
            if service_type == 'gemini':
                return self._call_gemini_api(service_config, content, title, language)
            else:  # openai_compatible
                return self._call_openai_compatible_api(service_config, content, title, service_name, language)
        except Exception as e:
            # 简化错误信息输出
            error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            if debug:
                print(f"⚠️ {service_name} 失败: {error_msg}")
            return None
    
    def _call_openai_compatible_api(self, config: Dict, content: str, title: str, service_name: str, language: str = 'zh') -> Dict[str, Any]:
        """调用OpenAI兼容的API
        
        Args:
            config: 服务配置
            content: 页面内容
            title: 页面标题
            service_name: 服务名称
            language: 摘要语言
            
        Returns:
            dict: 包含摘要和服务信息的字典
        """
        # 基础 headers
        headers = {
            'Authorization': f'Bearer {config["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        # 如果配置中有自定义 headers，合并进去
        if 'headers' in config:
            headers.update(config['headers'])
        
        prompt = self._build_prompt(content, title, language)
        
        data = {
            'model': config['model'],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
        
        response = requests.post(config['url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        summary = result['choices'][0]['message']['content'].strip()
        
        return {
            'summary': summary,
            'service': service_name
        }
    
    def _call_gemini_api(self, config: Dict, content: str, title: str, language: str = 'zh') -> Dict[str, Any]:
        """调用Gemini API
        
        Args:
            config: 服务配置
            content: 页面内容
            title: 页面标题
            language: 摘要语言
            
        Returns:
            dict: 包含摘要和服务信息的字典
        """
        url = f"{config['url']}?key={config['api_key']}"
        
        headers = {'Content-Type': 'application/json'}
        
        prompt = self._build_prompt(content, title, language)
        
        data = {
            'contents': [{
                'parts': [{'text': prompt}]
            }],
            'generationConfig': {
                'maxOutputTokens': self.max_tokens,
                'temperature': self.temperature
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        summary = result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        return {
            'summary': summary,
            'service': 'gemini'
        }
    
    def _build_prompt(self, content: str, title: str, language: str = 'zh') -> str:
        """构建AI提示词
        
        Args:
            content: 页面内容
            title: 页面标题
            language: 摘要语言
            
        Returns:
            str: 构建好的提示词
        """
        if language == 'en':
            return f"""Please generate a concise summary (100-150 words) for the following document:

Title: {title}

Content:
{content[:2000]}

Requirements:
1. Answer in English
2. Highlight the core points of the document
3. Use clear and concise language
4. Do not include irrelevant information"""
        elif language == 'both':
            return f"""请为以下文档生成一个简洁的双语摘要（中文100-150字，英文100-150字）：

标题：{title}

Content:
{content[:2000]}

要求：
1. 先用中文生成摘要，然后用英文生成摘要
2. 突出文档的核心要点
3. 语言简洁明了
4. 不要包含无关信息
5. 格式：**中文摘要：**\n[中文内容]\n\n**English Summary:**\n[English content]"""
        else:  # 默认中文
            return f"""请为以下文档生成一个简洁的摘要（100-150字）：

标题：{title}

内容：
{content[:2000]}

要求：
1. 用中文回答
2. 突出文档的核心要点
3. 语言简洁明了
4. 不要包含无关信息"""
    
    def get_available_services(self) -> list:
        """获取可用的AI服务列表
        
        Returns:
            list: 有API密钥的服务名称列表
        """
        available = []
        for service_name, config in self.ai_services.items():
            if config.get('api_key'):
                available.append(service_name)
        return available
    
    def validate_service_config(self, debug: bool = False) -> bool:
        """验证服务配置
        
        Args:
            debug: 是否显示调试信息
        
        Returns:
            bool: True表示至少有一个服务可用，False表示没有可用服务
        """
        # 显示API密钥状态
        if debug:
            print("🔍 API密钥状态检查:")
            for service_name, config in self.ai_services.items():
                api_key = config.get('api_key')
                if api_key:
                    # 只显示API密钥的前几位和后几位，中间用*代替
                    if len(api_key) > 12:
                        masked_key = f"{api_key[:6]}...{api_key[-4:]}"
                    else:
                        masked_key = "***"
                    print(f"   ✅ {service_name}: {masked_key}")
                else:
                    print(f"   ❌ {service_name}: 未配置")
        
        available_services = self.get_available_services()
        if not available_services:
            print("⚠️ 没有可用的AI服务，请检查API密钥配置")
            print("💡 请确保在.env文件中设置了相应的API密钥:")
            print("   - GLM_API_KEY=your_glm_api_key")
            print("   - OPENAI_API_KEY=your_openai_api_key")
            print("   - DEEPSEEK_API_KEY=your_deepseek_api_key")
            print("   - GOOGLE_API_KEY=your_google_api_key")
            print("   - SILICONFLOW_API_KEY=your_siliconflow_api_key")
            return False
        
        if debug:
            print(f"📊 可用AI服务: {', '.join(available_services)}")
            print()  # 添加空行分隔
        
        if self.default_service not in available_services:
            if debug:
                print(f"⚠️ 默认服务 {self.default_service} 不可用，切换至 {available_services[0]}")
            self.default_service = available_services[0]
        
        return True