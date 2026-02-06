#!/usr/bin/env python3
"""
MkDocs AI Summary Plugin - PyPI 发布脚本

此脚本自动化 PyPI 发布流程，包括：
1. 版本检查和验证
2. 清理旧构建文件
3. 构建分发包
4. 上传到 PyPI
5. 创建 Git 标签
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional
import re
import json
import requests
from dotenv import load_dotenv

# 从 .env 加载环境变量（含 PyPI token）
load_dotenv(Path(__file__).parent / ".env")


class PyPIPublisher:
    """PyPI 发布管理器"""
    
    # 支持的环境变量：TWINE_PASSWORD（twine 标准）或 PYPI_TOKEN
    TOKEN_ENV_VARS = ("TWINE_PASSWORD", "PYPI_TOKEN")
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.setup_py = self.project_root / "setup.py"
        self.pyproject_toml = self.project_root / "pyproject.toml"
        self.package_name = "mkdocs_ai_summary_wcowin"
    
    def _get_pypi_token(self) -> Optional[str]:
        """从 .env 或环境变量获取 PyPI token（支持 TWINE_PASSWORD、PYPI_TOKEN）"""
        for env_var in self.TOKEN_ENV_VARS:
            token = os.environ.get(env_var)
            if token and token.strip():
                return token.strip()
        return None
        
    def get_current_version(self):
        """获取当前版本号"""
        try:
            # 从 setup.py 读取版本
            with open(self.setup_py, 'r', encoding='utf-8') as f:
                content = f.read()
                version_match = re.search(r"version='([^']+)'", content)
                if version_match:
                    return version_match.group(1)
            
            # 从 pyproject.toml 读取版本
            with open(self.pyproject_toml, 'r', encoding='utf-8') as f:
                content = f.read()
                version_match = re.search(r'version = "([^"]+)"', content)
                if version_match:
                    return version_match.group(1)
                    
            raise ValueError("无法找到版本号")
        except Exception as e:
            print(f"❌ 获取版本号失败: {e}")
            sys.exit(1)
    
    def check_pypi_version(self, version):
        """检查 PyPI 上是否已存在该版本"""
        try:
            url = f"https://pypi.org/pypi/{self.package_name}/json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                print("📦 这是首次发布到 PyPI")
                return False
                
            if response.status_code == 200:
                data = response.json()
                existing_versions = list(data['releases'].keys())
                
                if version in existing_versions:
                    print(f"❌ 版本 {version} 已存在于 PyPI 上")
                    print(f"现有版本: {', '.join(existing_versions[-5:])}")
                    return True
                else:
                    print(f"✅ 版本 {version} 可以发布")
                    print(f"最新版本: {existing_versions[-1] if existing_versions else 'None'}")
                    return False
            else:
                print(f"⚠️ 无法检查 PyPI 版本状态: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ 检查 PyPI 版本时出错: {e}")
            return False
    
    def clean_build_files(self):
        """清理构建文件"""
        print("🧹 清理旧的构建文件...")
        
        dirs_to_clean = [
            'build',
            'dist',
            '*.egg-info',
            '__pycache__',
            '.pytest_cache'
        ]
        
        for pattern in dirs_to_clean:
            if '*' in pattern:
                # 使用 glob 模式
                for path in self.project_root.glob(pattern):
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"  删除目录: {path.name}")
            else:
                path = self.project_root / pattern
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    print(f"  删除: {path.name}")
    
    def run_command(self, command, description):
        """运行命令并处理错误"""
        print(f"🔧 {description}...")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                print(f"  输出: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description}失败:")
            print(f"  命令: {command}")
            print(f"  错误: {e.stderr}")
            return False
    
    def build_package(self):
        """构建分发包"""
        print("📦 构建分发包...")
        
        # 构建源码分发和轮子
        if not self.run_command(f"{sys.executable} setup.py sdist bdist_wheel", "构建分发包"):
            return False
            
        # 检查构建结果
        dist_dir = self.project_root / "dist"
        if not dist_dir.exists():
            print("❌ 构建失败：dist 目录不存在")
            return False
            
        files = list(dist_dir.glob("*"))
        if not files:
            print("❌ 构建失败：没有生成分发文件")
            return False
            
        print("✅ 构建成功，生成文件:")
        for file in files:
            print(f"  - {file.name}")
            
        return True
    
    def check_package(self):
        """检查包的完整性"""
        print("🔍 检查包完整性...")
        
        # 使用 twine check 检查包
        return self.run_command(f"{sys.executable} -m twine check dist/*", "检查包完整性")
    
    def upload_to_pypi(self, test=False):
        """上传到 PyPI（token 从环境变量 TWINE_PASSWORD 或 PYPI_TOKEN 读取）"""
        token = self._get_pypi_token()
        if not token:
            print("❌ 未找到 PyPI token，请在 .env 中设置 TWINE_PASSWORD 或 PYPI_TOKEN")
            print("   示例: TWINE_PASSWORD=pypi-xxxx")
            return False

        # 确保 twine 能从环境变量读取（若用户用 PYPI_TOKEN，则设置 TWINE_PASSWORD）
        if "TWINE_PASSWORD" not in os.environ:
            os.environ["TWINE_PASSWORD"] = token
        os.environ["TWINE_USERNAME"] = "__token__"

        if test:
            print("🚀 上传到 TestPyPI...")
            command = f"{sys.executable} -m twine upload --repository testpypi dist/*"
            description = "上传到 TestPyPI"
        else:
            print("🚀 上传到 PyPI...")
            command = f"{sys.executable} -m twine upload dist/*"
            description = "上传到 PyPI"

        return self.run_command(command, description)
    
    def create_git_tag(self, version):
        """创建 Git 标签"""
        print(f"🏷️ 创建 Git 标签 v{version}...")
        
        # 检查是否有未提交的更改
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("⚠️ 检测到未提交的更改，建议先提交代码")
            return False
            
        # 创建标签
        if not self.run_command(f"git tag v{version}", f"创建标签 v{version}"):
            return False
            
        # 推送标签
        return self.run_command("git push origin --tags", "推送标签到远程仓库")
    
    def publish(self, test=False, skip_tag=True):
        """执行完整的发布流程"""
        print("🚀 开始 PyPI 发布流程")
        print("=" * 50)
        
        # 1. 获取版本号
        version = self.get_current_version()
        print(f"📋 当前版本: {version}")
        
        # 2. 检查 PyPI 版本（仅在正式发布时）
        if not test and self.check_pypi_version(version):
            print("💡 提示: 请更新版本号后重新发布")
            return False
        
        # 3. 清理构建文件
        self.clean_build_files()
        
        # 4. 构建包
        if not self.build_package():
            return False
        
        # 5. 检查包
        if not self.check_package():
            return False
        
        # 6. 上传到 PyPI
        if not self.upload_to_pypi(test=test):
            return False
        
        # 7. 创建 Git 标签（仅在正式发布时）
        if not test and not skip_tag:
            self.create_git_tag(version)
        
        print("\n" + "=" * 50)
        if test:
            print("✅ 成功发布到 TestPyPI!")
            print(f"🔗 查看: https://test.pypi.org/project/{self.package_name}/{version}/")
        else:
            print("✅ 成功发布到 PyPI!")
            print(f"🔗 查看: https://pypi.org/project/{self.package_name}/{version}/")
            print(f"📦 安装: pip install {self.package_name}=={version}")
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MkDocs AI Summary Plugin PyPI 发布工具")
    parser.add_argument(
        "--test",
        action="store_true",
        help="发布到 TestPyPI 而不是正式 PyPI"
    )
    parser.add_argument(
        "--create-tag",
        action="store_true",
        help="创建 Git 标签（默认跳过）"
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="仅清理构建文件"
    )
    
    args = parser.parse_args()
    
    publisher = PyPIPublisher()
    
    if args.clean_only:
        publisher.clean_build_files()
        print("✅ 清理完成")
        return
    
    # 检查必要工具
    required_tools = ['twine', 'wheel']
    missing_tools = []
    
    for tool in required_tools:
        if tool == 'wheel':
            # wheel 使用不同的命令格式
            result = subprocess.run(
                f"{sys.executable} -m wheel version",
                shell=True,
                capture_output=True
            )
        else:
            result = subprocess.run(
                f"{sys.executable} -m {tool} --version",
                shell=True,
                capture_output=True
            )
        if result.returncode != 0:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ 缺少必要工具: {', '.join(missing_tools)}")
        print("请运行: pip install twine wheel")
        sys.exit(1)
    
    # 执行发布
    success = publisher.publish(test=args.test, skip_tag=not args.create_tag)
    
    if not success:
        print("❌ 发布失败")
        sys.exit(1)


if __name__ == "__main__":
    main()