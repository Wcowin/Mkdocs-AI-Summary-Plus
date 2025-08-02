# MkDocs AI Summary Plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-ai-summary-wcowin.svg)](https://badge.fury.io/py/mkdocs-ai-summary-wcowin)
[![Python Support](https://img.shields.io/pypi/pyversions/mkdocs-ai-summary-wcowin.svg)](https://pypi.org/project/mkdocs-ai-summary-wcowin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent MkDocs plugin that automatically generates AI-powered summaries for your documentation pages using multiple AI services including OpenAI, DeepSeek, Google Gemini, and GLM.
![预览图1](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)
![预览图2](https://s1.imagehub.cc/images/2025/06/03/526b59b6a2e478f2ffa1629320e3e2ce.png)
## Features

✨ **Transform your documentation with AI-powered summaries!** This intelligent MkDocs plugin automatically generates concise, helpful summaries for your documentation pages using multiple AI services.

## 🌟 Why Choose This Plugin?

- 🤖 **Multiple AI Services**: OpenAI, DeepSeek, Google Gemini, and GLM support with automatic fallback
- 🚀 **Smart Caching**: Intelligent caching reduces API costs and speeds up builds
- 🌍 **Multi-language**: Generate summaries in Chinese, English, or both
- 🎯 **Easy Setup**: Get started in minutes with simple configuration
- 🔧 **CI/CD Ready**: Perfect for GitHub Actions and automated deployments
- ⚡ **Performance First**: Minimal impact on build times

## 🚀 Quick Start

### 1. Install the Plugin

```bash
pip install mkdocs-ai-summary-wcowin
```

### 2. Basic Configuration

Add to your `mkdocs.yml`:

```yaml
plugins:
  - ai-summary:
      ai_service: "deepseek"        # Recommended: deepseek, openai, gemini, or glm
      summary_language: "en"        # "en", "zh", or "both"
      local_enabled: true           # Enable for local development
      enabled_folders:
        - docs                    # Process files in docs folder
      exclude_patterns:
        - tags.md                # unexclude tags.md file
        - blog/posts/**
        - blog/archive/**
```

### 3. Get Your API Key

**DeepSeek (Recommended - Cost Effective):**
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create account and get your API key
3. Add to `.env` file: `DEEPSEEK_API_KEY=your_key_here`

**Other Services:** OpenAI, Gemini, or GLM - follow similar steps on their platforms.

### 4. Create Environment File

Create `.env` in your project root:

```env
# Add your chosen AI service API key
DEEPSEEK_API_KEY=sk-your-api-key-here
# OPENAI_API_KEY=sk-your-openai-key
# GEMINI_API_KEY=your-gemini-key
# GLM_API_KEY=your-glm-key
```

### 5. Build and Enjoy!

```bash
mkdocs build    # Generate summaries
mkdocs serve    # Preview locally
```

🎉 **That's it!** Your documentation now has beautiful AI-generated summaries.

## ⚙️ Configuration

### Page-Level Language Control

Override global language settings for specific pages:

```markdown
---
title: "My Page"
ai_summary_lang: "en"  # "en", "zh", or "both"
---

# Your content here
```

### Common Configuration Options

```yaml
plugins:
  - ai-summary:
      # AI Service Settings
      ai_service: "deepseek"          # Primary AI service
      fallback_services: ["openai"]   # Backup services
      
      # Language & Content
      summary_language: "en"           # Global language setting
      summary_length: "medium"         # short/medium/long
      
      # File Selection
      enabled_folders:
        - docs
      exclude_patterns:
        - tags.md                # unexclude tags.md file
        - blog/posts/**
        - blog/archive/**
      
      # Performance
      cache_enabled: true              # Smart caching
      local_enabled: true              # Enable locally
      ci_enabled: true                 # Enable in CI/CD
```

## 🚀 GitHub Pages Deployment

### 1. Add API Key to GitHub Secrets

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add your API key (e.g., `DEEPSEEK_API_KEY`)

### 2. Configure GitHub Actions Workflow

#### Option A: Create New Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: ci
on:
  push:
    branches: [main, master]
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
      
      # Install your existing dependencies
      - run: pip install mkdocs-material
      - run: pip install mkdocs-ai-summary-wcowin
      
      # Deploy with AI Summary
      - name: Deploy with AI Summary
        env:
          AI_SUMMARY_CI_ENABLED: 'true'
          AI_SUMMARY_CACHE_ENABLED: 'true'
          AI_SUMMARY_CACHE_EXPIRE_DAYS: '300'
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: mkdocs gh-deploy --force
      
      # Auto-commit AI cache files
      - name: Auto-commit AI cache
        run: |
          if [ -d ".ai_cache" ] && [ "$(ls -A .ai_cache 2>/dev/null)" ]; then
            git config --local user.email "action@github.com"
            git config --local user.name "GitHub Action"
            git add .ai_cache/
            if ! git diff --cached --quiet; then
              git commit -m "🤖 Auto-update AI summary cache [skip ci]"
              git push
            fi
          fi
```

#### Option B: Add to Existing Workflow

If you already have a `ci.yml` file, add these steps to your existing workflow:

```yaml
# Add to your existing dependencies installation
- run: pip install mkdocs-ai-summary-wcowin

# Replace your mkdocs build/deploy step with:
- name: Deploy with AI Summary
  env:
    AI_SUMMARY_CI_ENABLED: 'true'
    AI_SUMMARY_CACHE_ENABLED: 'true'
    DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
  run: mkdocs gh-deploy --force

# Add after deploy (optional - for cache management)
- name: Auto-commit AI cache
  run: |
    if [ -d ".ai_cache" ] && [ "$(ls -A .ai_cache 2>/dev/null)" ]; then
      git config --local user.email "action@github.com"
      git config --local user.name "GitHub Action"
      git add .ai_cache/
      if ! git diff --cached --quiet; then
        git commit -m "🤖 Auto-update AI summary cache [skip ci]"
        git push
      fi
    fi
```

### 3. Integration Steps for Existing Workflows

If you already have a working `ci.yml` file, follow these steps to add AI summary functionality:

#### Step 1: Add Plugin Installation
Add this line to your existing dependency installation section:
```yaml
- run: pip install mkdocs-ai-summary-wcowin
```

#### Step 2: Add API Key to Environment
Update your mkdocs build/deploy step to include the API key:
```yaml
- name: Deploy docs
  env:
    DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # Add this line
  run: mkdocs gh-deploy --force
```

#### Step 3: Configure AI Summary Settings (Optional)
For better CI performance, add these environment variables:
```yaml
env:
  AI_SUMMARY_CI_ENABLED: 'true'        # Enable in CI
  AI_SUMMARY_CACHE_ENABLED: 'true'     # Use caching
  AI_SUMMARY_CACHE_EXPIRE_DAYS: '300'  # Cache for 300 days
  DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
```

#### Step 4: Add Cache Management (Optional)
To automatically commit generated cache files, add this step after deployment:
```yaml
- name: Auto-commit AI cache
  run: |
    if [ -d ".ai_cache" ] && [ "$(ls -A .ai_cache 2>/dev/null)" ]; then
      git config --local user.email "action@github.com"
      git config --local user.name "GitHub Action"
      git add .ai_cache/
      if ! git diff --cached --quiet; then
        git commit -m "🤖 Auto-update AI summary cache [skip ci]"
        git push
      fi
    fi
```

### 4. Enable GitHub Pages

1. Repository **Settings** → **Pages**
2. Source: **"Deploy from a branch"**
3. Branch: **"gh-pages"**
4. **Save**

🎉 **Done!** Push to main branch to deploy automatically.

## 💡 Tips & Troubleshooting

### Smart Caching
- Summaries are cached automatically to save API costs
- Cache updates when content changes
- Clear cache: add `clear_cache: true` to config

### Multiple AI Services
- **DeepSeek**: Most cost-effective, great quality
- **OpenAI**: Premium option, excellent results
- **Gemini**: Good balance of cost and quality
- **GLM**: Great for Chinese content

### Common Issues

**Plugin not generating summaries?**
- Check API key in `.env` file
- Verify `local_enabled: true` in config
- Ensure files are in `enabled_folders`

**Build failing in CI?**
- Add API key to GitHub Secrets
- Check workflow file syntax
- Verify plugin installation step

---

## 🤝 Support & Contributing

- 📖 **Documentation**: [Full documentation](https://github.com/wcowin/mkdocs-ai-summary)
- 🐛 **Issues**: [Report bugs](https://github.com/wcowin/mkdocs-ai-summary/issues)
- 💡 **Feature requests**: [Suggest improvements](https://github.com/wcowin/mkdocs-ai-summary/discussions)
- ⭐ **Star us**: If this plugin helps you, please star the repository!

## 📄 License

MIT License - feel free to use in your projects!

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

**Made with ❤️ for the MkDocs community**
</div>


