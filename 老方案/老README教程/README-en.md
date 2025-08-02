# MkDocs AI Summary 

![alt text](logo-2.png)

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-Hooks-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>

<p align="center">
    <a href="README.md">中文</a> | <a href="README-en.md">English</a>
</p>

🚀 **Supercharge Your MkDocs Documentation with AI!**   
This project provides powerful MkDocs hooks that add AI-driven summary generation and intelligent reading statistics to your technical documentation and blogs.

![Preview 1](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)
![Preview 2](https://s1.imagehub.cc/images/2025/06/03/526b59b6a2e478f2ffa1629320e3e2ce.png)

🌐 **Live Demo**: https://wcowin.work/mkdocs-ai-hooks/

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📦 Quick Installation](#-quick-installation)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Guide](#-usage-guide)
- [🎨 Display Examples](#-display-examples)
- [⚙️ Advanced Configuration](#️-advanced-configuration)
- [🌍 Multi-Language Support](#-multi-language-support)
- [📊 Performance Optimization](#-performance-optimization)
- [🤝 Contributing Guide](#-contributing-guide)

---

## ✨ Features

### 🤖 AI Smart Summary
- **Multi-AI Service Integration**: Support for DeepSeek, OpenAI, Claude, Gemini and other mainstream AI services
- **Automatic Summary Generation**: Generate high-quality 80-120 word intelligent summaries
- **Multi-Language Support**: Support for Chinese, English, and bilingual summary generation
- **Intelligent Content Cleaning**: Automatically filter YAML frontmatter, HTML tags, code blocks and other formatting elements
- **Fallback Summary Mechanism**: Provides keyword-based local summaries when AI services are unavailable
- **Intelligent Caching System**: 7-day intelligent expiration, avoiding duplicate API calls
- **Flexible Configuration**: Support precise control at both folder and page levels

### 📊 Intelligent Reading Statistics (Optional)
- **Accurate Character Counting**: Specially optimized for Chinese and English content recognition
- **Smart Code Detection**: Recognizes 30+ programming languages and command-line code
- **Reading Time Estimation**: Intelligent calculation based on language characteristics (Chinese: 400 chars/min, English: 200 words/min)
- **Beautiful Information Display**: Uses MkDocs Material theme styled info boxes

### 🚀 Smart Features
- **Environment Adaptive**: Automatically recognizes CI/local environment, locally or deployment both configurable enable/disable
- **Automatic Language Recognition**: Supports 30+ programming and markup languages
- **Content Type Detection**: Distinguishes between code, configuration, command-line and other content types
- **LRU Cache Optimization**: Improves processing performance (Todo)
- **Comprehensive Error Handling**: Exception handling and logging (Todo)

---

## 📦 Quick Installation

### Method 1: Direct Download (Recommended)

**Step 1**: Download Files
- Download the latest version from [Releases page](https://github.com/Wcowin/mkdocs-ai-hooks/releases)
- Or directly download `ai_summary.py` file

**Step 2**: Create Directory and Place Files
```bash
# Execute in your MkDocs project root directory
mkdir -p docs/overrides/hooks/
mv ai_summary.py docs/overrides/hooks/
```

**Step 3**: Configure MkDocs Theme and Override Path
```yaml
# Add to mkdocs.yml
theme:
  name: material
  custom_dir: docs/overrides  # Required configuration!!!
  features:
    - content.code.copy
    - content.code.select
```

### Method 2: Git Clone
```bash
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks 
pip install -r requirements.txt
```

### Dependencies Installation
```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Basic Configuration

**Step 1**: Configure Hooks
Make sure ai_summary.py is placed in the docs/overrides/hooks directory, then:
```yaml
# Add to mkdocs.yml
hooks:
  - docs/overrides/hooks/ai_summary.py      # AI summary hook
```

**Step 2**: Local Configuration
Create a `.env` file in the root directory to store API keys (remember to add to `.gitignore`):
```bash
# .env file content
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

```bash
# .gitignore file content
# Environment variable files (sensitive information)
.env
.env.local
.env.*.local
*.key

# MkDocs build output directory
site/

# AI summary cache directory (project root) - needs to be committed
!.ai_cache/
```

Check the directory tree structure here:
```
$ tree -a
Project Name
├── .github
│   ├── .DS_Store
│   └── workflows
│       └── ci.yml
├── docs
│   └── index.md
|   └── overrides
│       └── hooks
│           └── ai_summary.py
├── .env
├── .gitignore
├── README.md
└── mkdocs.yml
```

### 2. Configure AI Service

**Choose AI Service Provider**:
- 🌟 **DeepSeek** (Recommended): High cost-performance ratio, excellent Chinese performance
- 🔥 **OpenAI**: Powerful features, wide support
- ⚡ **Claude**: Clear logic, excellent text understanding
- 🧠 **Gemini**: Google's product, multi-language support

**Get API Keys**:
- [DeepSeek](https://platform.deepseek.com/usage) - Register to get API key
- [ChatAnywhere](https://github.com/chatanywhere/GPT_API_free) - Free OpenAI quota

**Store the obtained API keys in the `.env` file created in the previous step!!!**

### 3. Set Parameters

Configure directories that need AI summaries in `ai_summary.py`:
```python
# 📂 Folders to enable AI summaries
self.enabled_folders = [
    'blog/',      # Blog articles
    # Add more folders...
]
```

### 4. Local Run and Test

```bash
mkdocs serve  # Local preview
```

### 5. Deployment Configuration

```yaml
# ci.yml
name: ci 
on:
  push:
    branches:
      - master 
      - main
  # Prevent access to secrets from fork repositories
  pull_request:
    types: [closed]
    branches: [main, master]
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
            includes
            requirements.txt
            .ai_cache
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - name: Set cache ID
        run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV 
      - uses: actions/cache@v3
        with:
          key: mkdocs-material-${{ github.run_number }}
          path: .cache
          restore-keys: |
            mkdocs-material-
      - run: pip install mkdocs-git-revision-date-localized-plugin
      - run: pip install mkdocs-git-authors-plugin
      - run: pip install mkdocs-git-committers-plugin-2
      - run: pip install markdown-callouts
      - run: pip install mkdocs-rss-plugin
      - run: pip install requests>=2.25.0
      - run: pip install python-dateutil>=2.8.0
      - run: pip install cachetools>=4.2.0
      - run: pip install python-dotenv>=0.19.0
      - run: pip install pymdown-extensions
      - run: pip install mkdocs-material 
      - run: pip install --upgrade --force-reinstall mkdocs-material
      - name: Deploy with AI Summary
        env:
          # AI summary switch control
          AI_SUMMARY_CI_ENABLED: 'true'           # Enable AI summary in CI deployment environment (true=generate AI summaries for articles in CI)
          AI_SUMMARY_CI_ONLY_CACHE: 'true'       # CI deployment does not generate new summaries (true=use local deployment summary cache, no repeated API calls)
          AI_SUMMARY_CI_FALLBACK: 'true'          # Enable fallback summary in CI deployment (true=generate offline basic summary when API fails)
          # AI_SUMMARY_LOCAL_ENABLED: 'false'       # Disable AI summary in local deployment environment (true=generate summaries during local development) (no need to manage this line)
          # AI_SUMMARY_CACHE_ENABLED: 'true'        # Enable cache function locally (true=cache summaries to avoid repeated generation) (no need to manage this line)
          # API key configuration
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: mkdocs gh-deploy --force
      
      # Auto-commit newly generated AI cache files
      - name: Auto-commit AI cache (if any new files)
        run: |
          if [ -d ".ai_cache" ] && [ "$(ls -A .ai_cache 2>/dev/null)" ]; then
            git config --local user.email "action@github.com"
            git config --local user.name "GitHub Action"
            git add .ai_cache/
            if ! git diff --cached --quiet; then
              git commit -m "🤖 Auto-update AI summary cache [skip ci]"
              git push
              echo "✅ Auto-committed new AI cache files"
            else
              echo "ℹ️ No new cache files to commit"
            fi
          else
            echo "ℹ️ No cache directory found or cache is empty"
          fi
```

```python
# Configuration in ai_summary.py
# AI summary local environment configuration
self.ci_config = {
    # CI deployment environment switch (no need to manage, only effective when set in ci.yml)
    'enabled_in_ci': os.getenv('AI_SUMMARY_CI_ENABLED', 'true').lower() == 'true',
    
    # Local deployment environment switch (true=enable AI summary during local development)
    'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'true').lower() == 'true',
    
    # CI deployment cache-only mode (no need to manage, only effective when set in ci.yml)
    'ci_only_cache': os.getenv('AI_SUMMARY_CI_ONLY_CACHE', 'false').lower() == 'true',
    
    # Local deployment cache function switch (true=enable cache to avoid repeated generation, false=always generate new summaries)
    'cache_enabled': os.getenv('AI_SUMMARY_CACHE_ENABLED', 'true').lower() == 'true',
    
    # CI deployment fallback summary switch (no need to manage, only effective when set in ci.yml)
    'ci_fallback_enabled': os.getenv('AI_SUMMARY_CI_FALLBACK', 'true').lower() == 'true',
}
```

**Several Operation Modes**:
1. **Completely Disabled**: No summary generation in both local and CI deployment
2. **CI Deployment Only**: Disabled locally, generate new summaries in CI deployment
3. **Cache Mode**: Summaries already generated locally, CI deployment uses cache (**Recommended. The above configuration has default CI deployment cache mode, you can choose combinations yourself**)
4. **Fully Enabled**: Both local and CI deployment run (more API consumption)

### 6. GitHub Secrets Configuration

**Step 1**: Set Repository Secrets
1. Go to GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** to add:
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
![GitHub Secrets Configuration](https://s1.imagehub.cc/images/2025/06/04/b5fd63d839bb6443c8560a5f690d2c41.png)

---

Then deploy to GitHub Pages or other platforms.

**If there are errors, you can ask ChatGPT or ask questions in Issues.**

## 📖 Usage Guide

### AI Summary Control

#### Method 1: Page-Level Control (Recommended)
In the YAML meta at the top of Markdown files:

**Enable AI Summary**:
```yaml
---
title: Article Title
ai_summary: true   # Enable AI summary
---
```

**Disable AI Summary**:
```yaml
---
title: Article Title
ai_summary: false  # Disable AI summary
description: Custom summary content  # Optional manual summary
---
```

#### Method 2: Folder-Level Control
```python
# Configure in ai_summary.py
# 📂 Customizable folder configuration
self.enabled_folders = [
    'blog/',      # blog folder
    'index.md',     
    # 'develop/',   # develop folder
    # 'posts/',     # posts folder
    # 'trip/',     # trip folder
    # 'about/',     # about folder
]

# 📋 Excluded files and folders
self.exclude_patterns = [
    '404.md', 'tag.md', 'tags.md',
]

# 📋 Excluded specific files
self.exclude_files = [
    'blog/index.md',
]
```

---

## 🎨 Display Examples

### AI Summary Display
**Live Preview**:
![AI Summary Display](https://s1.imagehub.cc/images/2025/06/04/152205c10ef1bfd7658b383a3e5e6e9f.png)

### 💰 Cost Information
- **Single Request**: Approximately $0.005-0.008 USD (medium to large documents)
- **Monthly Estimate**: About $1-5 USD for regular blogs
- **Free Quota**: Most AI service providers offer free credits for new users

---

## ⚙️ Advanced Configuration

### Custom AI Services

#### Method 1: Using Configuration Functions (Recommended)
```python
# Create hooks_config.py in the same directory as mkdocs.yml
from docs.overrides.hooks.ai_summary import configure_ai_summary, add_ai_service, add_openai_service

# Add OpenAI-compatible service
add_openai_service(
    'my_deepseek',
    'https://api.deepseek.com/v1/chat/completions',
    'deepseek-chat',
    'your-deepseek-key'
)

# Add locally deployed model
add_openai_service(
    'local_llm',
    'http://localhost:8000/v1/chat/completions',
    'local-model',
    'dummy-key',
    temperature=0.7
)

# Add completely custom service
add_ai_service('custom_service', {
    'url': 'https://api.custom.com/v1/chat/completions',
    'model': 'custom-model',
    'api_key': 'your-custom-key',
    'format': 'openai',  # or 'claude', 'gemini', 'custom'
    'max_tokens': 200,
    'temperature': 0.3,
    'headers': {'Custom-Header': 'value'}
})

# Configure basic settings and service priority
configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='en',
    service_priority=['my_deepseek', 'local_llm', 'custom_service', 'openai']
)
```

#### Method 2: Configuration from Environment Variables
```python
# Create hooks_config.py in the same directory as mkdocs.yml
from docs.overrides.hooks.ai_summary import add_service_from_env, configure_ai_summary

# Auto-configure from environment variables
add_service_from_env('my_service', 'MYAPI')

configure_ai_summary(
    enabled_folders=['blog/'],
    service_priority=['my_service', 'openai']
)
```

```bash
# Add to .env file
MYAPI_URL=https://api.myservice.com/v1/chat/completions
MYAPI_MODEL=my-model
MYAPI_API_KEY=your-api-key
MYAPI_MAX_TOKENS=150
MYAPI_TEMPERATURE=0.3
MYAPI_FORMAT=openai
```

#### Method 3: Direct Configuration in configure_ai_summary
```python
# Create hooks_config.py in the same directory as mkdocs.yml
from docs.overrides.hooks.ai_summary import configure_ai_summary

configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='en',
    custom_services={
        'my_openai': {
            'url': 'https://api.openai.com/v1/chat/completions',
            'model': 'gpt-4',
            'api_key': 'your-openai-key',
            'format': 'openai'
        },
        'local_llm': {
            'url': 'http://localhost:8000/v1/chat/completions',
            'model': 'local-model',
            'api_key': 'dummy',
            'format': 'openai',
            'temperature': 0.7
        }
    },
    service_priority=['my_openai', 'local_llm', 'deepseek']
)
```

### Supported API Formats

#### OpenAI-Compatible Format
```python
{
    'url': 'https://api.openai.com/v1/chat/completions',
    'model': 'gpt-4',
    'api_key': 'your-key',
    'format': 'openai'
}
```

#### Claude Format
```python
{
    'url': 'https://api.anthropic.com/v1/messages',
    'model': 'claude-3-haiku-20240307',
    'api_key': 'your-key',
    'format': 'claude'
}
```

#### Gemini Format
```python
{
    'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
    'model': 'gemini-pro',
    'api_key': 'your-key',
    'format': 'gemini'
}
```

#### Fully Custom Format
```python
def custom_payload_builder(content, title, config):
    return {
        "prompt": f"Please summarize: {content}",
        "max_length": 120
    }

def custom_response_parser(response_data):
    return response_data.get('summary', '')

{
    'url': 'https://api.custom.com/summarize',
    'api_key': 'your-key',
    'format': 'custom',
    'custom_payload_builder': custom_payload_builder,
    'custom_response_parser': custom_response_parser
}
```

### Common Custom Configuration Examples

#### 1. Using Azure OpenAI
```python
add_ai_service('azure_openai', {
    'url': 'https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2023-12-01-preview',
    'model': 'gpt-4',
    'api_key': 'your-azure-key',
    'format': 'openai',
    'headers': {'api-key': 'your-azure-key'}  # Azure uses api-key header
})
```

#### 2. Using Ollama Local Model
```python
add_openai_service(
    'ollama',
    'http://localhost:11434/v1/chat/completions',
    'llama2',
    'dummy-key'  # Ollama doesn't need real key
)
```

#### 3. Using Alibaba Qwen
```python
add_openai_service(
    'qwen',
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    'qwen-turbo',
    'your-dashscope-key'
)
```

#### 4. Using Zhipu AI
```python
add_openai_service(
    'zhipu',
    'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    'glm-4',
    'your-zhipu-key'
)
```

### Service Management Functions

```python
from docs.overrides.hooks.ai_summary import list_ai_services, set_service_priority

# List all available services
list_ai_services()

# Dynamically adjust service priority
set_service_priority('my_custom_service', 'openai', 'deepseek')
```

### Configuration File Organization

It's recommended to create `hooks_config.py` in the project root to manage all custom configurations:

```python
# hooks_config.py
from docs.overrides.hooks.ai_summary import *

# Custom service configuration
add_openai_service('my_gpt4', 'https://api.openai.com/v1/chat/completions', 'gpt-4', os.getenv('OPENAI_API_KEY'))
add_service_from_env('aliyun_qwen', 'QWEN')

# Basic configuration
configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='en',
    service_priority=['my_gpt4', 'aliyun_qwen', 'deepseek'],
    cache_enabled=True
)
```

Then include it in `mkdocs.yml`:

```yaml
hooks:
  - docs/overrides/hooks/ai_summary.py
  - hooks_config.py  # Include custom configuration
```

---

## 🌍 Multi-Language Support

### Language Configuration
```python
# Set in ai_summary.py
self.summary_language = 'en'    # English summaries
# self.summary_language = 'zh'  # Chinese summaries
# self.summary_language = 'both' # Bilingual summaries
```

### Supported Languages
- **Fully Supported**: Chinese, English
- **Partially Supported**: Japanese, Korean, French, German

---

## 📊 Performance Optimization

### Implemented Optimizations
- **LRU Caching**: Function-level caching improves performance
- **Precompiled Regex**: Faster text processing
- **Smart Filtering**: Reduces unnecessary API calls
- **Content Hashing**: Intelligent caching based on content changes

### Performance Recommendations
- Use `ci_only_cache: true` to only use cache in CI environment
- Set `enabled_folders` appropriately to avoid processing unnecessary files
- Regularly clean expired cache files

---

## 🤝 Contributing Guide

### How to Contribute
1. **Fork** this repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Create **Pull Request**

### Development Environment
```bash
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks
pip install -r requirements.txt
```

---

## 📝 Changelog

### [v1.3.0] (2025-06-04) - Latest Version

#### Core Improvements

- **Unified Cache Architecture**
- **Cache path unified to project root directory .ai_cache**
- **Local and CI environments use the same cache strategy**
- **Enhanced CI/CD support**, **Support CI cache-only mode, significantly reducing deployment time**
- **Smart recognition of 15+ deployment platforms (GitHub Actions, GitLab CI, etc.)**
- **Configurable fallback summary mechanism**

### [v1.2.0] (2025-06-03)

#### ✨ Major New Features
- **Multi-AI Service Support**: Integration of DeepSeek, OpenAI, Gemini, Claude
- **Environment Adaptive**: Automatic recognition of CI/local environment
- **Intelligent Caching System**: Content hash caching, 7-day automatic expiration
- **Security Configuration**: GitHub Secrets integration, secure API key management

#### 🔧 Technical Improvements
- **Unified API Interface**: Automatic adaptation to different AI service formats
- **Enhanced Error Handling**: Comprehensive exception handling mechanisms
- **Performance Optimization**: LRU caching and regex precompilation

### [v1.0.0] (2025-06-01) - Initial Version
- 🤖 **AI smart summary functionality**
- 📖 **Reading time statistics functionality**
- 💾 **Basic caching system**
- 🎯 **Basic configuration options**

---

## 🐛 Issue Reporting

Encountered a problem? Please report it in [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues).

**When reporting, please include**:
- MkDocs version
- Python version
- Complete error messages
- Reproduction steps
- Configuration files (remove sensitive information)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Thanks to the following projects and services:
- [MkDocs](https://www.mkdocs.org/) - Excellent static site generator
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Beautiful theme
- [DeepSeek](https://deepseek.com/) - High cost-performance AI API service
- All contributors and users

---

## 🔗 Contact Author

<div align="center">

### Telegram
<a href="https://t.me/wecowin" target="_blank">
<img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Telegram" style="border-radius: 10px;" width="300px">
</a>

### WeChat
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="300px">

</div>

---

## ⭐ Project Statistics

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

## ☕ Support the Project

<div align="center">

<a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
<img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 300px; border-radius: 15px;">
</a>

**If this project helps you, please give it a ⭐ Star!**

</div>

---

<div align="center">

📝 *Making MkDocs documentation smarter*

**[⬆ Back to Top](#mkdocs-ai-hooks)**

</div>