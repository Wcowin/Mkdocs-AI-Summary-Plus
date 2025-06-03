# MkDocs AI Hooks

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-Hooks-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>

🚀 **Supercharge Your MkDocs Documentation with AI!**   
This project provides powerful MkDocs hooks that add AI-driven summary generation and intelligent reading statistics to your technical documentation and blogs.
![iShot 2025 06 03 13.39.35](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)

## ✨ Features

### AI Smart Summary
- **Automatic Article Summaries**: Generate high-quality 80-120 word summaries using DeepSeek API
- **Intelligent Content Cleaning**: Automatically filter YAML, HTML, code blocks and other formatting content
- **Fallback Summary Mechanism**: Provides rule-based intelligent summaries when API fails
- **Efficient Caching System**: Avoid duplicate API calls with 7-day intelligent expiration
- **Flexible Configuration**: Support precise control at folder and page levels

### Intelligent Reading Statistics
- **Accurate Chinese Character Counting**: Specially optimized Chinese content recognition
- **Smart Code Detection**: Recognizes multiple programming languages and command-line code
- **Reading Time Estimation**: Based on Chinese reading habits at 400 characters/minute
- **Beautiful Information Display**: Uses MkDocs Material style info boxes

### Smart Features
- **Automatic Language Recognition**: Supports 30+ programming and markup languages
- **Content Type Detection**: Distinguishes between code, configuration, command-line and other content types
- **Cache Optimization**: LRU cache improves performance
- **Error Handling**: Comprehensive exception handling and logging

## 📦 Installation

### Method 1: Direct Download (Recommended)
Download from the releases page and place the following files in your MkDocs project's docs/overrides/hooks directory:
https://github.com/Wcowin/mkdocs-ai-hooks/releases  

```bash
# Place in your project directory
mkdir -p docs/overrides/hooks/
mv ai_summary.py docs/overrides/hooks/
mv reading_time.py docs/overrides/hooks/
```

![image](https://s1.imagehub.cc/images/2025/06/03/8b1c7485da460dfd6f61c15cde89b5e5.png)

### Method 2: Git Submodule
```bash
# Add as submodule
git submodule add https://github.com/Wcowin/mkdocs-ai-hooks.git hooks
git submodule update --init --recursive

# Copy to your project
cp hooks/*.py docs/overrides/hooks/
```

### Dependencies Installation
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Configure MkDocs
First run `mkdocs build` once to generate cache files
```bash
mkdocs build 
```
Add hooks in `mkdocs.yml`:
```yaml
hooks:
  - docs/overrides/hooks/ai_summary.py # Add AI summary hook
  - docs/overrides/hooks/reading_time.py # Add reading time statistics hook

# Optional: Material theme configuration
theme:
  name: material
  features:
    - content.code.copy
    - content.code.select
```

### 2. Configure directories for AI summaries in ai_summary.py
```python
# 📂 Customizable folder configuration
self.enabled_folders = [
    'blog/',      # blog folder
    'develop/',   # develop folder
    # Add folders where you want to enable AI summaries
]

# 📋 Excluded files and folders
self.exclude_patterns = [
    'waline.md', 'link.md', '404.md', 'tag.md', 'tags.md',
    '/about/', '/search/', '/sitemap', 'index.md',  # Root directory index.md
]

# 📋 Excluded specific files
self.exclude_files = [
    'blog/index.md',
    'blog/indexblog.md',
    'docs/index.md',
    'develop/index.md',
]
```

### 3. Set DeepSeek API in ai_summary.py
```python
# Modify API configuration in ai_summary.py
self.api_config = {
    'url': 'https://api.deepseek.com/v1/chat/completions',
    'model': 'deepseek-chat',
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer *YOUR_API_KEY_HERE*'  # Replace with your API key
    }
}
```
Test API: sk-7dbcd6e21fb3417299b50aecff76c7bf (replace `*YOUR_API_KEY_HERE*`)

### 4. Run MkDocs
The first run may take some time as the system automatically generates summaries. Subsequent runs will use cached data to speed up generation.
```bash
# Run commands in sequence
mkdocs build 
mkdocs serve
```
Terminal output:
![image](https://s1.imagehub.cc/images/2025/06/03/a287b109428d7e4e61afe7212e045860.png)

## 📖 Usage Guide

### AI Summary Configuration

#### Folder Level Control
```python
# Enable specific folders
configure_ai_summary(['blog/', 'docs/', 'tutorials/'])

# Enable globally (except excluded items)
configure_ai_summary([''])
```

#### Page Level Control (Recommended)
In the YAML front matter of Markdown files:

```yaml
---
title: Article Title
ai_summary: true   # Enable AI summary
---
```
![iShot 2025 06 03 13.46.03](https://s1.imagehub.cc/images/2025/06/03/6b40a854fe57ef33b40c580ab4a7c802.jpg)
```yaml
---
title: Article Title
ai_summary: false  # Disable AI summary
description: Manual summary  # Optional
---
```

### Reading Time Configuration

#### Exclude Specific Pages
```python
# In the page's YAML front matter
---
title: Page Title
hide_reading_time: true  # Hide reading time
---
```

## 🎨 Display Effects

### AI Summary Display
```markdown
!!! info "🤖 AI Smart Summary"
    This article provides a detailed introduction to MkDocs hooks development and usage, covering AI summary generation, reading time statistics and other functionality implementations. Through DeepSeek API integration and intelligent caching mechanisms, it provides automated content enhancement services for technical documentation.

# Your Article Title
Article content...
```

### Reading Information Display
```markdown
!!! info "📖 Reading Information"
    Reading time: **3** minutes | Chinese characters: **1247** | Effective code lines: **45**

# Your Article Title
Article content...
```  

**Actual Effect:**
![iShot 2025 06 03 13.22.14](https://s1.imagehub.cc/images/2025/06/03/8e4818b5b73c07d9b90a7471b1bfcbae.jpg)

### API Cost
About 0.03-0.05 yuan per large document
Very economical!

## ⚙️ Advanced Configuration

### Custom API Service
```python
# Support other AI services
self.api_config = {
    'url': 'https://your-api-endpoint.com/v1/chat/completions',
    'model': 'your-model',
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'
    }
}
```

### Custom Prompts
```python
# Modify AI summary prompts
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
if (datetime.now() - cache_time).days < 30:  # Change to 30 days
    return cache_data
```

## 🔧 Custom Development

### Extend AI Service Support
```python
class AISummaryGenerator:
    def add_ai_service(self, service_name, config):
        """Add new AI service support"""
        self.ai_services[service_name] = config
    
    def generate_summary_with_service(self, content, service_name):
        """Generate summary using specified service"""
        # Your implementation
        pass
```

### Custom Summary Format
```python
def format_summary(self, summary, ai_service):
    """Custom summary display format"""
    return f'''!!! note "✨ Custom Summary"
    {summary}
    
    *Generated by {ai_service}*
'''
```

## 🌍 Multi-language Support

### English Content Optimization
```python
# Reading time calculation (English: 200 words/minute)
def calculate_english_reading_time(word_count):
    return max(1, round(word_count / 200))
```

### Other Language Extensions
```python
# Support Japanese, Korean, etc.
JAPANESE_CHARS_PATTERN = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
KOREAN_CHARS_PATTERN = re.compile(r'[\uAC00-\uD7AF]')
```

## 📊 Performance Optimization

- **LRU Cache**: Function-level caching improves performance
- **Precompiled Regex**: Improves text processing speed
- **Smart Filtering**: Reduces unnecessary API calls
- **Async Support**: Extensible to async processing (TODO)

## 🤝 Contributing

We welcome all forms of contributions!

1. **Fork** this repository
2. Create your feature branch 
3. Commit your changes
4. Push to the branch
5. Open a **Pull Request**

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/Wcowin/mkdocs-ai-hooks.git
cd mkdocs-ai-hooks

# Install dependencies
pip install -r requirements.txt

# Run tests
mkdocs serve
```

## 📝 Changelog

### v1.0.0 (2025-06-03)
- ✨ Initial release
- 🤖 AI smart summary functionality
- 📖 Reading time statistics functionality
- 💾 Intelligent caching system
- 🎯 Flexible configuration options

### Planned Features
- [ ] Multi-AI service support (OpenAI, Claude, etc.)
- [ ] Async processing support
- [ ] Batch processing mode
- [ ] Statistics data export
- [ ] Web interface configuration

## 🐛 Issue Reporting

If you encounter any issues, please submit them in [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues).

When submitting issues, please include:
- MkDocs version
- Python version
- Error messages
- Reproduction steps

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [MkDocs](https://www.mkdocs.org/) - Static site generator
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Excellent theme
- [DeepSeek](https://deepseek.com/) - AI API service
- All contributors and users

# Connect with me

<center>

**Telegram**

<p align="center">
  <a href="https://t.me/wecowin" target="_blank">
    <img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Personal Card" style="border-radius: 10px;" width="50%">
  </a>
</p>


**WeChat**  
<!-- ![](https://s1.imagehub.cc/images/2024/02/02/bb9ee71b03ee7a3b87caad5cc4bcebff.jpeg) -->
<p align="center">
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="50%">
</p>

</center>


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Wcowin/mkdocs-ai-hooks&type=Date)](https://www.star-history.com/#Wcowin/mkdocs-ai-hooks&Date)


## Buy the Author a Coffee

  <a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
   <center>
    <img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 450px; height: auto; border-radius: 25px;" >
    </center>  
  </a>

<p align="center">
    If this project helps you, please give it a ⭐ Star!
</p>

<p align="center">
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/stargazers">
        <img src="https://img.shields.io/github/stars/Wcowin/mkdocs-ai-hooks?style=social" alt="Stars">
    </a>
    <a href="https://github.com/Wcowin/mkdocs-ai-hooks/network/members">
        <img src="https://img.shields.io/github/forks/Wcowin/mkdocs-ai-hooks?style=social" alt="Forks">
    </a>
</p>

---

*📝 This project is dedicated to making MkDocs documentation more intelligent and user-friendly. Feel free to share suggestions or ideas!*