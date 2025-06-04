# MkDocs AI Hooks

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-Hooks-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>

<p align="center">
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/blob/main/README.md">中文</a> | <a href="README-en.md">English</a>
</p>

🚀 **您的MkDocs文档首选智能摘要！**   
这个项目利用MkDocs hooks，为您的技术文档和博客添加AI驱动的摘要生成和智能阅读统计功能。

![预览图1](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)
![预览图2](https://s1.imagehub.cc/images/2025/06/03/526b59b6a2e478f2ffa1629320e3e2ce.png)

🌐 **在线演示**: https://wcowin.work/mkdocs-ai-hooks/

---

## 📋 目录导航

- [✨ 功能特性](#-功能特性)
- [📦 快速安装](#-快速安装)
- [🚀 快速开始](#-快速开始)
- [📖 使用指南](#-使用指南)
- [🎨 显示效果](#-显示效果)
- [⚙️ 高级配置](#️-高级配置)
- [🔐 安全配置](#-安全配置)
- [🌍 多语言支持](#-多语言支持)
- [📊 性能优化](#-性能优化)
- [🤝 贡献指南](#-贡献指南)

---

## ✨ 功能特性

### 🤖 AI智能摘要
- **多AI服务集成**: 支持DeepSeek、OpenAI、Claude、Gemini等主流AI服务
- **自动摘要生成**: 生成高质量的80-120字智能摘要
- **多语言支持**: 支持中文、英文、双语摘要生成
- **智能内容清理**: 自动过滤YAML、HTML、代码块等格式内容
- **备用摘要机制**: API失败时提供基于关键词的本地摘要
- **智能缓存系统**: 7天智能过期，避免重复API调用
- **灵活配置**: 支持文件夹级别和页面级别的精确控制

### 📊 智能阅读统计（可选）
- **精准字符统计**: 专门优化的中英文内容识别
- **智能代码检测**: 识别30+编程语言和命令行代码
- **阅读时间估算**: 基于语言特性的智能计算（中文400字/分钟，英文200词/分钟）
- **美观信息展示**: 使用MkDocs Material风格的信息框

### 🚀 智能化特性
- **环境自适应**: 自动识别CI/本地环境，智能启用/禁用
- **自动语言识别**: 支持30+编程语言和标记语言
- **内容类型检测**: 区分代码、配置、命令行等不同内容
- **LRU缓存优化**: 提升处理性能
- **完善错误处理**: 异常处理和详细日志记录

---

## 📦 快速安装

### 方法1: 直接下载（推荐）

**步骤1**: 下载文件
- 从 [Releases页面](https://github.com/Wcowin/mkdocs-ai-hooks/releases) 下载最新版本
- 或直接下载 `ai_summary.py` 和 `reading_time.py` 文件

**步骤2**: 创建目录并放置文件
```bash
# 在您的MkDocs项目根目录下执行
mkdir -p docs/overrides/hooks/
mv ai_summary.py docs/overrides/hooks/
mv reading_time.py docs/overrides/hooks/
```

**步骤3**: 配置MkDocs主题
```yaml
# 在 mkdocs.yml 中添加
theme:
  name: material
  custom_dir: docs/overrides  # 必需配置！
  features:
    - content.code.copy
    - content.code.select
```

### 方法2: Git克隆
```bash
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks 
pip install -r requirements.txt
```

### 依赖安装
```bash
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 1. 基础配置

**配置hooks**
```yaml
# 在 mkdocs.yml 中添加
hooks:
  - docs/overrides/hooks/ai_summary.py      # AI摘要hook
  - docs/overrides/hooks/reading_time.py    # 阅读时间统计hook
```

**初始化构建**
```bash
mkdocs build  # 生成缓存文件
```

### 2. 配置AI服务

**选择AI服务提供商**：
- 🌟 **DeepSeek**（推荐）：性价比高，中文表现优秀
- 🔥 **OpenAI**：功能强大，广泛支持
- ⚡ **Claude**：逻辑清晰，文本理解佳
- 🧠 **Gemini**：Google出品，多语言支持

**获取API密钥**：
- [DeepSeek](https://platform.deepseek.com/usage) - 注册获取API密钥
- [ChatAnywhere](https://github.com/chatanywhere/GPT_API_free) - 免费OpenAI额度

### 3. 设置摘要范围

在 `ai_summary.py` 中配置需要AI摘要的目录：
```python
# 📂 启用AI摘要的文件夹
self.enabled_folders = [
    'blog/',      # 博客文章
    'docs/',      # 文档页面
    'tutorials/', # 教程内容
    # 添加更多文件夹...
]
```

### 4. 运行和测试

```bash
mkdocs serve  # 本地预览
```

---

## 📖 使用指南

### AI摘要控制

#### 方法1: 页面级控制（推荐）
在Markdown文件的YAML frontmatter中：

**启用AI摘要**：
```yaml
---
title: 文章标题
ai_summary: true   # 强制启用AI摘要
---
```

**禁用AI摘要**：
```yaml
---
title: 文章标题
ai_summary: false  # 禁用AI摘要
description: 自定义摘要内容  # 可选手动摘要
---
```

#### 方法2: 文件夹级控制
```python
# 在 ai_summary.py 中配置
self.enabled_folders = ['blog/', 'docs/']  # 指定文件夹
```

### 阅读时间控制

**隐藏阅读时间**：
```yaml
---
title: 页面标题
hide_reading_time: true  # 隐藏阅读时间统计
---
```

---

## 🎨 显示效果

### AI摘要显示
```markdown
!!! info "🤖 AI智能摘要"
    本文详细介绍了MkDocs hooks的开发和使用方法，涵盖AI摘要生成、阅读时间统计等功能实现。通过DeepSeek API集成和智能缓存机制，为技术文档提供自动化的内容增强服务。

# 您的文章标题
文章内容...
```

### 阅读信息显示
```markdown
!!! info "📖 阅读信息"
    阅读时间：**3** 分钟 | 中文字符：**1247** | 有效代码行数：**45**

# 您的文章标题
文章内容...
```

**实际效果预览**：
![效果展示](https://s1.imagehub.cc/images/2025/06/03/8e4818b5b73c07d9b90a7471b1bfcbae.jpg)

### 💰 成本说明
- **单次费用**: 约0.03-0.05元（中大型文档）
- **月度预估**: 普通博客约1-5元
- **免费额度**: 多数AI服务商提供新用户免费额度

---

## ⚙️ 高级配置

### 自定义AI服务
```python
# 添加新的AI服务
self.ai_services = {
    'your_service': {
        'url': 'https://api.yourservice.com/v1/chat/completions',
        'model': 'your-model',
        'api_key': os.getenv('YOUR_API_KEY'),
        'max_tokens': 150,
        'temperature': 0.3
    }
}
```

### 自定义提示词
```python
def generate_ai_summary(self, content, page_title=""):
    prompt = f"""请为以下技术文档生成一个简洁的中文摘要（80-120字）：
    
    文章标题：{page_title}
    文章内容：{content[:2500]}
    
    要求：
    1. 突出核心技术要点
    2. 使用简洁专业的语言
    3. 长度控制在80-120字
    """
```

### 缓存配置
```python
# 修改缓存过期时间
cache_time = datetime.fromisoformat(cache_data.get('timestamp', '1970-01-01'))
if (datetime.now() - cache_time).days < 30:  # 改为30天
    return cache_data
```

### 环境配置选项（还在测试）

```python
# 🚀 CI 环境配置 - 默认只在 CI 环境中启用
self.ci_config = {
    # CI环境启用控制：从环境变量AI_SUMMARY_CI_ENABLED读取，默认为'true'
    # 控制是否在CI/CD环境（如GitHub Actions、GitLab CI等）中启用AI摘要功能
    'enabled_in_ci': os.getenv('AI_SUMMARY_CI_ENABLED', 'true').lower() == 'true',  # 默认 CI 中启用
    
    # 本地环境启用控制：从环境变量AI_SUMMARY_LOCAL_ENABLED读取，默认为'false'
    # 控制是否在本地开发环境中启用AI摘要功能，默认禁用以避免开发时产生API费用
    'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'false').lower() == 'true',  # 默认本地禁用
    
    # 下面这行是被注释的备选配置，如果启用则本地环境默认开启AI摘要
    # 'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'true').lower() == 'true',  # 默认本地启用
    
    # CI缓存策略：从环境变量AI_SUMMARY_CI_ONLY_CACHE读取，默认为'false'
    # false = CI环境中允许调用AI API生成新摘要
    # true = CI环境中仅使用已有缓存，不调用AI API（节省API费用和构建时间）
    'ci_only_cache': os.getenv('AI_SUMMARY_CI_ONLY_CACHE', 'false').lower() == 'true',  # CI 中也允许生成新摘要
    
    # CI备用摘要控制：从环境变量AI_SUMMARY_CI_FALLBACK读取，默认为'true'
    # true = 当AI服务不可用时，启用基于关键词的本地备用摘要生成
    # false = 禁用备用摘要，AI失败时不显示任何摘要
    'ci_fallback_enabled': os.getenv('AI_SUMMARY_CI_FALLBACK', 'true').lower() == 'true'
}
```

目前是推荐只改变上面这两项：
```python
    # 本地环境启用控制：从环境变量AI_SUMMARY_LOCAL_ENABLED读取，默认为'false'
    # 控制是否在本地开发环境中启用AI摘要功能，默认禁用以避免开发时产生API费用
    'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'false').lower() == 'true',  # 默认本地禁用
    
    # 下面这行是被注释的备选配置，如果启用则本地环境默认开启AI摘要
    # 'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'true').lower() == 'true',  # 默认本地启用
```


**四种运行模式**：
1. **完全禁用**: 本地和CI部署都不运行摘要生成
2. **仅CI启用**: 本地禁用，CI部署生成新摘要
3. **缓存模式**：本地已经生成过摘要，CI部署使用缓存（还在测试,后续版本推出）（推荐）
4. **完全启用**: 本地和CI部署都正常运行

---

## 🔐 安全配置

### GitHub Secrets配置（强烈推荐）

**步骤1**: 设置Repository Secrets
1. 进入GitHub仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret** 添加：
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
```

**步骤2**: 本地开发配置
创建 `.env` 文件（记得添加到 `.gitignore`）：
```bash
# .env 文件内容
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# 可选环境配置
AI_SUMMARY_LOCAL_ENABLED=false    # 本地禁用，避免产生费用
AI_SUMMARY_CI_ENABLED=true        # CI环境启用
```

**步骤3**: CI/CD工作流配置
```yaml
name: ci 
on:
  push:
    branches:
      - master 
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          sparse-checkout: |
            docs
            mkdocs.yml
            requirements.txt
            site/.ai_cache
            
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
          
      - name: Set cache ID
        run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV 
      
      - uses: actions/cache@v3
        with:
          key: mkdocs-material-${{ github.run_id }}
          path: .cache
          restore-keys: |
            mkdocs-material-
            
      # 安装 MkDocs 核心依赖
      - run: pip install mkdocs-material 
      - run: pip install --upgrade --force-reinstall mkdocs-material
      
      # 安装 MkDocs 插件
      - run: pip install mkdocs-git-revision-date-localized-plugin
      - run: pip install mkdocs-git-authors-plugin  
      - run: pip install mkdocs-git-committers-plugin-2
      - run: pip install markdown-callouts
      - run: pip install mkdocs-rss-plugin
      - run: pip install pymdown-extensions
      
      # 安装 AI Hooks 依赖
      - run: pip install requests>=2.25.0
      - run: pip install python-dateutil>=2.8.0
      - run: pip install cachetools>=4.2.0
      - run: pip install python-dotenv>=0.19.0  # 添加这行
      # 安装项目特定依赖（如果存在）
      - name: Install project dependencies
        run: |
          if [ -f requirements.txt ]; then 
            pip install -r requirements.txt
          fi
      
      # 调试信息
      - name: Debug - Check repository structure
        run: |
          echo "仓库根目录结构："
          ls -la
          echo "检查 mkdocs.yml："
          cat mkdocs.yml || echo "mkdocs.yml not found"
          echo "检查 docs 目录："
          ls -la docs/ || echo "docs directory not found"
      
      # 构建和部署
      - name: Build and Deploy
        env:
          # DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AI_SUMMARY_CI_ENABLED: "true"
          AI_SUMMARY_LOCAL_ENABLED: "false"
          AI_SUMMARY_CI_ONLY_CACHE: "false"
          AI_SUMMARY_CI_FALLBACK: "true"
        run: mkdocs gh-deploy --force
```

### 安全最佳实践
- ✅ **永远不要**将API密钥写在代码中
- ✅ 使用环境变量管理敏感信息
- ✅ 定期轮换API密钥
- ✅ 监控API使用量，设置上限
- ✅ 为不同环境使用不同密钥

---

## 🌍 多语言支持

### 语言配置
```python
# 在 ai_summary.py 中设置
self.summary_language = 'zh'    # 中文摘要
# self.summary_language = 'en'  # 英文摘要
# self.summary_language = 'both' # 双语摘要
```

### 支持的语言
- **完全支持**: 中文、英文
- **计划支持**: 日文、韩文、法文、德文

---

## 📊 性能优化

### 已实现优化
- **LRU缓存**: 函数级别缓存提升性能
- **正则预编译**: 提高文本处理速度
- **智能过滤**: 减少不必要的API调用
- **内容哈希**: 基于内容变化的智能缓存

### 性能建议
- 使用 `ci_only_cache: true` 在CI环境中仅使用缓存
- 合理设置 `enabled_folders` 避免处理不必要的文件
- 定期清理过期缓存文件

---

## 🤝 贡献指南

### 如何贡献
1. **Fork** 这个仓库
2. 创建特性分支
3. 提交更改
4. 推送分支
5. 创建 **Pull Request**

### 开发环境
```bash
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks
pip install -r requirements.txt
```

---

## 📝 更新日志

### [v1.2.0] (2025-06-03) - 最新版本

#### ✨ 主要新功能
- **多AI服务支持**: 集成DeepSeek、OpenAI、Gemini、Claude
- **环境自适应**: 自动识别CI/本地环境
- **智能缓存系统**: 内容哈希缓存，7天自动过期
- **安全配置**: GitHub Secrets集成，API密钥安全管理

#### 🔧 技术改进
- **统一API接口**: 自适配不同AI服务格式
- **错误处理增强**: 完善的异常处理机制
- **性能优化**: LRU缓存和正则预编译

### [v1.0.0] (2025-06-01) - 初始版本
- 🤖 AI智能摘要功能
- 📖 阅读时间统计功能
- 💾 基础缓存系统
- 🎯 基本配置选项

---

## 🐛 问题反馈

遇到问题？请在 [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues) 中反馈。

**反馈时请包含**：
- MkDocs版本
- Python版本
- 完整错误信息
- 复现步骤
- 配置文件（去除敏感信息）

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

感谢以下项目和服务：
- [MkDocs](https://www.mkdocs.org/) - 优秀的静态站点生成器
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - 精美的主题
- [DeepSeek](https://deepseek.com/) - 高性价比的AI API服务
- 所有贡献者和使用者

---

## 🔗 联系作者

<div align="center">

### Telegram
<a href="https://t.me/wecowin" target="_blank">
<img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Telegram" style="border-radius: 10px;" width="300px">
</a>

### 微信交流
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="300px">

</div>

---

## ⭐ 项目统计

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=Wcowin/mkdocs-ai-hooks&type=Date)](https://www.star-history.com/#Wcowin/mkdocs-ai-hooks&Date)

<a href="https://github.com/Wcowin/mkdocs-ai-hooks/stargazers">
<img src="https://img.shields.io/github/stars/Wcowin/mkdocs-ai-hooks?style=social" alt="Stars">
</a>
<a href="https://github.com/Wcowin/mkdocs-ai-hooks/network/members">
<img src="https://img.shields.io/github/forks/Wcowin/mkdocs-ai-hooks?style=social" alt="Forks">
</a>

</div>

---

## ☕ 支持项目

<div align="center">

<a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
<img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 300px; border-radius: 15px;">
</a>

**如果这个项目对您有帮助，请给它一个 ⭐ Star！**

</div>

---

<div align="center">

📝 *让MkDocs文档更加智能化和用户友好*

**[⬆ 回到顶部](#mkdocs-ai-hooks)**

</div>