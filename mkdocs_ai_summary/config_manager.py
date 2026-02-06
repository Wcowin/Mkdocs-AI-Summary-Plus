"""配置管理器模块

负责处理插件配置、环境变量和运行环境检测。
"""

import os
from typing import Dict, Any


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, plugin_config: Dict[str, Any]):
        """初始化配置管理器
        
        Args:
            plugin_config: 插件配置字典
        """
        self.config = plugin_config  # 为了兼容性保留
        self.plugin_config = plugin_config
        self.is_ci = self._detect_ci_environment()
        self.ci_name = self._get_ci_name() if self.is_ci else None
    
    def _detect_ci_environment(self) -> bool:
        """检测CI环境
        
        通过检查常见的CI环境变量来判断是否在CI环境中运行。
        
        Returns:
            bool: True表示在CI环境中，False表示在本地环境中
        """
        ci_indicators = [
            'CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS', 'GITLAB_CI',
            'JENKINS_URL', 'TRAVIS', 'CIRCLECI', 'AZURE_HTTP_USER_AGENT',
            'TEAMCITY_VERSION', 'BUILDKITE', 'CODEBUILD_BUILD_ID',
            'NETLIFY', 'VERCEL', 'CF_PAGES'
        ]
        return any(os.getenv(indicator) for indicator in ci_indicators)
    
    def _get_ci_name(self) -> str:
        """获取CI环境名称
        
        Returns:
            str: CI环境名称
        """
        if os.getenv('GITHUB_ACTIONS'):
            return 'GitHub Actions'
        elif os.getenv('GITLAB_CI'):
            return 'GitLab CI'
        elif os.getenv('JENKINS_URL'):
            return 'Jenkins'
        elif os.getenv('TRAVIS'):
            return 'Travis CI'
        elif os.getenv('CIRCLECI'):
            return 'CircleCI'
        elif os.getenv('NETLIFY'):
            return 'Netlify'
        elif os.getenv('VERCEL'):
            return 'Vercel'
        elif os.getenv('CF_PAGES'):
            return 'Cloudflare Pages'
        else:
            return 'Unknown CI'
    
    def should_run_plugin(self) -> bool:
        """判断是否应该运行插件
        
        根据环境类型和配置决定是否启用AI摘要功能。
        
        Returns:
            bool: True表示应该运行，False表示不应该运行
        """
        if self.is_ci:
            return self.plugin_config.get('ci_enabled', True)
        else:
            return self.plugin_config.get('local_enabled', False)
    
    def should_generate_new_summary(self) -> bool:
        """判断是否应该生成新摘要
        
        在CI环境中，如果设置为仅缓存模式，则不生成新摘要。
        
        Returns:
            bool: True表示可以生成新摘要，False表示不应生成
        """
        if self.is_ci and self.plugin_config.get('ci_cache_only', False):
            return False
        return True
    
    def log_environment_status(self, debug: bool = False) -> None:
        """记录环境状态日志
        
        Args:
            debug: 是否显示调试信息
        """
        if debug:
            if self.is_ci:
                ci_name = self._get_ci_name()
                if self.plugin_config.get('ci_enabled', True):
                    if self.plugin_config.get('ci_cache_only', False):
                        print(f"🚀 CI ({ci_name}) - 缓存模式")
                    else:
                        print(f"🚀 CI ({ci_name}) - AI摘要启用")
                else:
                    print(f"🚫 CI ({ci_name}) - AI摘要禁用")
            else:
                if self.plugin_config.get('local_enabled', False):
                    print("💻 本地环境 - AI摘要启用")
                else:
                    print("🚫 本地环境 - AI摘要禁用")
    
    def is_fallback_summary_enabled(self) -> bool:
        """获取备用摘要启用状态
        
        Returns:
            bool: True表示启用备用摘要，False表示不启用
        """
        if self.is_ci:
            return self.plugin_config.get('ci_fallback', True)
        return False  # 本地环境不使用备用摘要
    
    def should_run(self) -> bool:
        """判断是否应该运行插件（别名方法）
        
        这是 should_run_plugin 方法的别名，用于保持向后兼容性。
        
        Returns:
            bool: True表示应该运行，False表示不应该运行
        """
        return self.should_run_plugin()
    
    def get_fallback_enabled(self) -> bool:
        """获取备用摘要启用状态（别名方法）
        
        这是 is_fallback_summary_enabled 方法的别名，用于保持向后兼容性。
        
        Returns:
            bool: True表示启用备用摘要，False表示不启用
        """
        return self.is_fallback_summary_enabled()