# MkDocs AI Hooks

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-Hooks-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>

<p align="center">
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/blob/main/README.md">中文</a> | <a href="https://github.com/Wcowin/mkdocs-ai-hooks/blob/main/README-en.md">English</a>
</p>

🚀 **Supercharge Your MkDocs Documentation with AI!**   
This project provides powerful MkDocs hooks that add AI-driven summary generation and intelligent reading statistics to your technical documentation and blogs.

![Preview 1](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)
![Preview 2](https://s1.imagehub.cc/images/2025/06/03/526b59b6a2e478f2ffa1629320e3e2ce.png)

**Live Demo**: https://wcowin.work/Mkdocs-Wcowin/blog/Mkdocs/mkfirst/

## ✨ Features

### 🤖 AI Smart Summary
- **Automatic Article Summaries**: Generate high-quality 80-120 word summaries using multiple AI services
- **Multi-AI Service Support**: Integrated support for DeepSeek, OpenAI, Claude, and Gemini
- **Multi-Language Support**: Support for Chinese, English, and bilingual summaries
- **Intelligent Content Cleaning**: Automatically filter YAML frontmatter, HTML tags, code blocks, and other formatting elements
- **Fallback Summary Mechanism**: Provides keyword-based local summaries when AI services are unavailable
- **Efficient Caching System**: Avoid duplicate API calls with intelligent 7-day cache expiration
- **Flexible Configuration**: Support precise control at both folder and page levels

### 📊 Intelligent Reading Statistics (Optional)
- **Accurate Character Counting**: Specially optimized for Chinese content recognition
- **Smart Code Detection**: Recognizes 30+ programming languages and command-line code
- **Reading Time Estimation**: Based on reading habits (Chinese: 400 chars/min, English: 200 words/min)
- **Beautiful Information Display**: Uses MkDocs Material theme styled info boxes

### 🚀 Smart Features
- **Automatic Language Recognition**: Supports 30+ programming and markup languages
- **Content Type Detection**: Distinguishes between code, configuration, command-line, and other content types
- **Performance Optimization**: LRU cache improves processing speed
- **Comprehensive Error Handling**: Robust exception handling and detailed logging

## 📦 Installation

### Method 1: Direct Download (Recommended)
Download from the [releases page](https://github.com/Wcowin/mkdocs-ai-hooks/releases) and place the files in your MkDocs project:

Or download the Python files from the hooks directory:
- `ai_summary.py`: AI summary generator
- `reading_time.py`: Reading time statistics

```bash
# Create directory structure
mkdir -p docs/overrides/hooks/

# Place downloaded files
mv ai_summary.py docs/overrides/hooks/
mv reading_time.py docs/overrides/hooks/
```

![Installation Location](https://s1.imagehub.cc/images/2025/06/03/8b1c7485da460dfd6f61c15cde89b5e5.png)

Add `custom_dir` under theme in `mkdocs.yml`:
```yaml
# Optional: Material theme configuration
theme:
  name: material
  custom_dir: docs/overrides  # Required! Must have this!
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

## 🚀 Quick Start

### 1. Configure MkDocs
First, run `mkdocs build` once to generate cache files:
```bash
mkdocs build 
```

Add hooks in `mkdocs.yml` and configure the theme:
```yaml
hooks:
  - docs/overrides/hooks/ai_summary.py      # AI summary hook
  - docs/overrides/hooks/reading_time.py    # Reading time statistics hook

# Theme configuration (required for custom styling)
theme:
  name: material
  custom_dir: docs/overrides  # Required! Must have this!!
  features:
    - content.code.copy
    - content.code.select
```

### 2. Configure AI Summary Directories
Edit the `ai_summary.py` file to specify which folders should have AI summaries:

```python
# 📂 Customize folder configuration
self.enabled_folders = [
    'blog/',      # Blog articles
    'develop/',   # Development docs
    'tutorials/', # Tutorial content
    # Add more folders as needed
]

# 📋 Excluded files and folders
self.exclude_patterns = [
    'waline.md', 'link.md', '404.md', 'tag.md', 'tags.md',
    '/about/', '/search/', '/sitemap/', 'index.md',  # Root index
]

# 📋 Specific excluded files
self.exclude_files = [
    'blog/index.md',
    'blog/indexblog.md',
    'docs/index.md',
    'develop/index.md',
]
```

### 3. Configure AI API (Default is OpenAI, DeepSeek Recommended)
Set up your API credentials in `ai_summary.py`:

```python
# Configure DeepSeek API in ai_summary.py
'deepseek': {
    'url': 'https://api.deepseek.com/v1/chat/completions',
    'model': 'deepseek-chat',
    'api_key': os.getenv('DEEPSEEK_API_KEY', 'your-deepseek-api-key'),
    'max_tokens': 150,
    'temperature': 0.3
},
```

### 4. Build and Serve
The first run may take some time as the system generates summaries. Subsequent runs will use cached data:

```bash
# Build the site
mkdocs build 

# Serve locally
mkdocs serve
```

**Terminal Output:**
![Terminal Output](https://s1.imagehub.cc/images/2025/06/03/a287b109428d7e4e61afe7212e045860.png)

## 📖 Usage Guide

### AI Summary Configuration

#### Folder-Level Control
```python
# Enable for specific folders
configure_ai_summary(['blog/', 'docs/', 'tutorials/'])

# Enable globally (except excluded items)
configure_ai_summary([''])
```

#### Page-Level Control (Recommended)
Use YAML frontmatter in your Markdown files:

**Enable AI Summary:**
```yaml
---
title: Your Article Title
ai_summary: true   # Enable AI summary generation
---
```

![Page configuration example](https://s1.imagehub.cc/images/2025/06/03/6b40a854fe57ef33b40c580ab4a7c802.jpg)

**Disable AI Summary:**
```yaml
---
title: Your Article Title
ai_summary: false        # Disable AI summary
description: Custom summary text  # Optional manual summary
---
```

### Reading Time Configuration

#### Hide Reading Time for Specific Pages
```yaml
---
title: Page Title
hide_reading_time: true  # Hide reading time statistics
---
```

## 🎨 Display Examples

### AI Summary Display
```markdown
!!! info "🤖 AI Smart Summary"
    This article provides a comprehensive guide to MkDocs hooks development and implementation, covering AI summary generation, reading time statistics, and other advanced features. Through DeepSeek API integration and intelligent caching mechanisms, it offers automated content enhancement for technical documentation.

# Your Article Title
Your article content goes here...
```

### Reading Information Display
```markdown
!!! info "📖 Reading Information"
    Reading time: **3** minutes | Characters: **1,247** | Code lines: **45**

# Your Article Title
Your article content goes here...
```  

**Live Preview:**
![Live Preview](https://s1.imagehub.cc/images/2025/06/03/8e4818b5b73c07d9b90a7471b1bfcbae.jpg)

### 💰 API Cost
Approximately $0.005-0.008 USD per long document - very economical!

#### Free OpenAI API Access
Recommended: [ChatAnywhere](https://github.com/chatanywhere/GPT_API_free?tab=readme-ov-file#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)  
After application, you'll get an API key starting with `sk-`. Replace the following in the multi-AI service configuration section of `ai_summary.py`:

```python
'openai': {
    'url': 'https://api.chatanywhere.tech/v1/chat/completions',
    'model': 'gpt-3.5-turbo',  # or 'gpt-4', 'gpt-4-turbo'
    'api_key': os.getenv('OPENAI_API_KEY', 'your_openai_api_key'),
    'max_tokens': 150,
    'temperature': 0.3
},
```

```python
# Default AI service to use
self.default_service = 'openai'
```

However, we also recommend using [DeepSeek](https://platform.deepseek.com/usage) API for its generous quota and excellent performance.

## ⚙️ Advanced Configuration

### Custom AI Service Integration
```python
# Support for other AI services
self.ai_services = {
    'your_ai_service': {
        'url': 'your-api-endpoint',
        'model': 'your-model',
        'api_key': os.getenv('YOUR_API_KEY', 'your-api-key'),
        'max_tokens': 150,  # Maximum tokens
        'temperature': 0.3 
    }
}
```

### Custom Summary Prompts
```python
# Customize AI summary generation
def generate_ai_summary(self, content, page_title=""):
    prompt = f"""Your custom prompt...
    
    Article title: {page_title}
    Article content: {content[:2500]}
    """
```

### Cache Configuration
```python
# Modify cache expiration time (days)
cache_time = datetime.fromisoformat(cache_data.get('timestamp', '1970-01-01'))
if (datetime.now() - cache_time).days < 30:  # Extend to 30 days
    return cache_data
```

**Important Note**: After switching API services, the cache will be automatically cleared. No manual deletion required! **(This issue has been resolved - cache is automatically cleared when switching API services)**

### CI/Local Environment Configuration

```python
# 🚀 CI Environment Configuration - Local CI environment disabled by default
self.ci_config = {
    'enabled_in_ci': os.getenv('AI_SUMMARY_CI_ENABLED', 'true').lower() == 'true',  # Default enabled in CI
    'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'false').lower() == 'true',  # Default disabled locally
    # 'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'true').lower() == 'true',  # Enable locally
    'ci_only_cache': os.getenv('AI_SUMMARY_CI_ONLY_CACHE', 'false').lower() == 'true',  # Allow new generation in CI
    'ci_fallback_enabled': os.getenv('AI_SUMMARY_CI_FALLBACK', 'true').lower() == 'true'
}
```

### Custom Summary Formatting
```python
def format_summary(self, summary, ai_service):
    """Customize summary display format"""
    return f'''!!! note "✨ Custom AI Summary"
    {summary}
    
    *Generated by {ai_service}*
'''
```

## 🌍 Multi-Language Support

### English Summary Configuration

```python
# Language configuration
self.summary_language = 'en'  # Default Chinese, options: 'zh', 'en', 'both'
```

### Additional Language Extensions (TODO)

```python
# Support for Japanese, Korean, etc.
JAPANESE_CHARS = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
KOREAN_CHARS = re.compile(r'[\uAC00-\uD7AF]')
```

## 📊 Performance Optimizations

- **LRU Caching**: Function-level caching for improved performance
- **Precompiled Regex**: Faster text processing with compiled patterns
- **Smart Filtering**: Reduces unnecessary API calls
- **Async Support**: Ready for asynchronous processing (TODO)

## 🤝 Contributing

We welcome contributions of all kinds!

### How to Contribute
1. **Fork** this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

### Development Setup
```bash
# Clone the repository
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks

# Install dependencies
pip install -r requirements.txt
```

## 📝 Changelog

### [v1.0.0] (2025-06-01)
- ✨ Initial release with core functionality
- 🤖 AI-powered smart summary generation
- 📖 Intelligent reading time statistics
- 💾 Advanced caching system
- 🎯 Flexible configuration options

---

### [v1.2.0] (2025-06-03)

#### ✨ New Features

##### 🤖 AI Smart Summary System
- **Multi-AI Service Support**: Integrated DeepSeek, OpenAI, Gemini, and Claude services
- **Intelligent Service Switching**: Support for service priority configuration and automatic failover
- **Multi-Language Summaries**: Support for Chinese, English, and bilingual summary generation
- **Intelligent Content Cleaning**: Automatically remove irrelevant formatting and extract core text for AI processing
- **Fallback Summary Mechanism**: Automatically generate keyword-based local summaries when AI services are unavailable

##### 🌍 Environment-Adaptive Configuration
- **CI/Local Environment Detection**: Automatically recognizes 15+ CI environments including GitHub Actions, GitLab CI, Netlify
- **Separate Configuration**: CI and local environments can be independently configured for enable/disable status
- **Recommended Configuration**: Default enabled only in CI environments, disabled locally to reduce development interference

##### 💾 Intelligent Caching System
- **Content Hash Caching**: Generate unique cache identifiers based on article content + language settings
- **Cache Expiration Management**: 7-day automatic expiration mechanism ensures content freshness
- **Service Change Detection**: Automatically clear related cache when AI service or language settings change
- **Cache Robustness**: Support for directory-level and file-level cache cleanup strategies

##### 🎯 Flexible Configuration Options
- **Precise Folder Control**: Support specifying specific folders to enable AI summaries
- **Exclusion Patterns**: Support file patterns and specific file path exclusions
- **Page-Level Control**: Force enable/disable through `ai_summary` field in front matter
- **API Key Management**: Support both environment variables and code configuration

#### 🔧 Technical Features

##### 📡 API Integration
- **Unified Request Building**: Automatically adapt to different AI services' API formats and authentication methods
- **Error Handling**: Comprehensive network exception and API error handling mechanisms
- **Timeout Control**: 30-second request timeout to prevent build process blocking
- **Response Parsing**: Intelligently extract and clean AI-returned summary content

##### 🎨 Display Optimization
- **Adaptive Titles**: Dynamically generate summary titles based on AI service and language settings
- **Visual Differentiation**: Use different icons and colors to distinguish AI summaries from fallback summaries
- **Format Standardization**: Automatically clean summary format, remove redundant prefixes and suffixes

---

### Upcoming Features
- [x] Multi-AI service support (OpenAI, Claude, etc.)
- [x] Automatic best API selection
- [ ] Secure API key handling (Important)
- [ ] Batch processing mode
- [ ] Analytics and statistics export
- [ ] Web-based configuration interface

## 🐛 Issue Reporting

Encountered a problem? Please report it in our [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues) section.

**When reporting issues, please include:**
- MkDocs version
- Python version
- Complete error messages
- Steps to reproduce the issue
- Sample configuration files (if applicable)

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🙏 Acknowledgments

Special thanks to:
- [MkDocs](https://www.mkdocs.org/) - The amazing static site generator
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Beautiful and functional theme
- [DeepSeek](https://deepseek.com/) - Powerful and affordable AI API service
- All contributors and users who make this project better

## 🔗 Connect with the Author

<center>

**Join our Telegram Community**

<p align="center">
  <a href="https://t.me/wecowin" target="_blank">
    <img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Telegram Community" style="border-radius: 10px;" width="50%">
  </a>
</p>

**WeChat**
<p align="center">
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="50%">
</p>

</center>

## ⭐ Star History

<a href="https://www.star-history.com/#Wcowin/mkdocs-ai-hooks&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Wcowin/mkdocs-ai-hooks&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Wcowin/mkdocs-ai-hooks&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Wcowin/mkdocs-ai-hooks&type=Date" />
 </picture>
</a>

## ☕ Support the Project

<center>
  <a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
    <img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 450px; height: auto; border-radius: 25px;">
  </a>
</center>

<p align="center">
    <strong>If this project helps you, please consider giving it a ⭐ Star!</strong>
</p>

<p align="center">
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/stargazers">
        <img src="https://img.shields.io/github/stars/Wcowin/mkdocs-ai-hooks?style=social" alt="GitHub Stars">
    </a>
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/network/members">
        <img src="https://img.shields.io/github/forks/Wcowin/mkdocs-ai-hooks?style=social" alt="GitHub Forks">
    </a>
</p>

---

*📝 This project is dedicated to making MkDocs documentation smarter and more user-friendly. We'd love to hear your feedback and suggestions!*