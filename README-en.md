# MkDocs AI Summary Plugin

[![PyPI version](https://badge.fury.io/py/mkdocs-ai-summary-wcowin.svg)](https://badge.fury.io/py/mkdocs-ai-summary-wcowin)
[![Python Support](https://img.shields.io/pypi/pyversions/mkdocs-ai-summary-wcowin.svg)](https://pypi.org/project/mkdocs-ai-summary-wcowin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent MkDocs plugin that automatically generates AI-powered summaries for your documentation pages using multiple AI services including OpenAI, DeepSeek, Google Gemini, and GLM.

## Features

- 🤖 **Multiple AI Services**: Support for OpenAI, DeepSeek, Google Gemini, and GLM
- 🚀 **Smart Caching**: Intelligent caching system to reduce API calls and costs
- 🎯 **Flexible Configuration**: Fine-grained control over which pages get summaries
- 🌍 **Multi-language Support**: Generate summaries in different languages
- 🔧 **CI/CD Ready**: Seamless integration with GitHub Actions and other CI/CD systems
- 📱 **Responsive Design**: Beautiful summary cards that work on all devices
- ⚡ **Performance Optimized**: Minimal impact on build times with smart caching

## Installation

### From PyPI (Recommended)

```bash
pip install mkdocs-ai-summary-wcowin
```

## Quick Start

### 1. Configure your MkDocs·

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - ai-summary:
      ai_service: "deepseek"  # or "openai", "gemini", "glm"
      summary_language: "en"  # or "zh"
      cache_enabled: true # Enable caching
      cache_expire_days: 30 # Cache expiration in days
      debug: true # Whether to display debug information (default: false)
      enabled_folders: # Folders to process
        - "docs"
        - blog/    # Add blog folder
      exclude_patterns:
        - "**/api/**"
        - "**/reference/**"
        - "**/about/**" # Exclude about folder
        - "index.md" # Exclude index.md
        - "tag.md" # Exclude tag.md
        - "blog/posts/update.md" # Exclude blog/posts/update.md
```

### 2. Set up Environment Variables

Create a `.env` file in your project root:

```env
# Choose one or more AI services
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
GLM_API_KEY=your_glm_api_key
```

### 3. Build Your Documentation

```bash
mkdocs build
```

The plugin will automatically generate AI summaries for your pages and inject them into the content.

## Configuration Guide

### Local Development Setup

#### Step 1: Get API Keys

Obtain API keys for your chosen AI service:

**DeepSeek (Recommended)**
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Register and log in
3. Go to API management
4. Create a new API key
5. Copy the key for later use

**OpenAI**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Log in to your account
3. Go to API Keys page
4. Click "Create new secret key"
5. Copy the key for later use

**Google Gemini**
1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Log in with your Google account
3. Create a new API key
4. Copy the key for later use

**GLM (Zhipu AI)**
1. Visit [Zhipu AI Platform](https://open.bigmodel.cn/)
2. Register and log in
3. Go to API management
4. Create an API key
5. Copy the key for later use

#### Step 2: Create .env File

Create a `.env` file in your project root (same level as `mkdocs.yml`):

```bash
# In your project root directory
touch .env
```

#### Step 3: Configure API Keys

Edit the `.env` file and add your API keys:

```env
# DeepSeek API Key (Recommended)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Gemini API Key
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GLM API Key
GLM_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx

# Optional: Debug mode
AI_SUMMARY_DEBUG=false

# Optional: API timeout (seconds)
AI_SUMMARY_TIMEOUT=30

# Optional: Maximum retry attempts
AI_SUMMARY_MAX_RETRIES=3
```

**Important Notes:**
- Only configure API keys for the services you plan to use
- Ensure `.env` file is added to `.gitignore` to prevent API key leakage
- API key formats vary by service, ensure you copy the complete key

#### Step 4: Verify Configuration

Run the following commands to verify your configuration:

```bash
# Local build test
mkdocs build

# Local preview
mkdocs serve
```

If configured correctly, you should see the plugin load successfully and generate AI summaries.

### GitHub Deployment Configuration

#### Step 1: Prepare GitHub Repository

1. Push your project to a GitHub repository
2. Ensure `.env` file is added to `.gitignore`
3. Ensure `mkdocs.yml` and plugin configuration are committed

#### Step 2: Configure Repository Secrets

Configure API keys in your GitHub repository:

1. **Access Repository Settings**
   - Open your GitHub repository
   - Click the "Settings" tab
   - Find "Secrets and variables" in the left menu
   - Click "Actions"

2. **Add Repository Secrets**
   
   Click "New repository secret" and add the following secrets:
   
   | Secret Name | Value | Description |
   |-------------|-------|-------------|
   | `DEEPSEEK_API_KEY` | Your DeepSeek API key | If using DeepSeek service |
   | `OPENAI_API_KEY` | Your OpenAI API key | If using OpenAI service |
   | `GEMINI_API_KEY` | Your Gemini API key | If using Gemini service |
   | `GLM_API_KEY` | Your GLM API key | If using GLM service |

   **Adding Steps:**
   - Name: Enter the secret name (e.g., `DEEPSEEK_API_KEY`)
   - Secret: Paste your API key
   - Click "Add secret"

#### Step 3: Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml` in your repository:

```yaml
name: Deploy MkDocs with AI Summary

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install mkdocs-material
        pip install mkdocs-ai-summary-wcowin
        # If you have requirements.txt
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Build documentation with AI summaries
      env:
        # Configure API key environment variables
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        GLM_API_KEY: ${{ secrets.GLM_API_KEY }}
        # Optional configuration
        AI_SUMMARY_DEBUG: false
        AI_SUMMARY_TIMEOUT: 30
      run: |
        mkdocs build --verbose
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
        # Optional: Custom domain
        # cname: your-domain.com
```

#### Step 4: Enable GitHub Pages

1. In repository settings, find "Pages" option
2. Source: select "Deploy from a branch"
3. Branch: select "gh-pages"
4. Click "Save"

#### Step 5: Trigger Deployment

Push code to main branch to trigger automatic deployment:

```bash
git add .
git commit -m "Add AI summary plugin configuration"
git push origin main
```

### Advanced CI/CD Configuration

#### Multi-Environment Configuration

```yaml
name: Deploy Documentation

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

env:
  PYTHON_VERSION: '3.x'
  NODE_VERSION: '18'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install and test
      run: |
        pip install mkdocs-material mkdocs-ai-summary-wcowin
        mkdocs build --strict
  
  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to staging
      env:
        DEEPSEEK_API_KEY: ${{ secrets.STAGING_DEEPSEEK_API_KEY }}
      run: |
        pip install mkdocs-material mkdocs-ai-summary-wcowin
        mkdocs build
        # Deploy to staging environment
  
  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to production
      env:
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pip install mkdocs-material mkdocs-ai-summary-wcowin
        mkdocs build
        # Deploy to production environment
```

#### Cache Optimization Configuration

```yaml
    - name: Cache AI summaries
      uses: actions/cache@v3
      with:
        path: .ai_cache
        key: ai-cache-${{ hashFiles('docs/**/*.md') }}-${{ hashFiles('mkdocs.yml') }}
        restore-keys: |
          ai-cache-${{ hashFiles('docs/**/*.md') }}-
          ai-cache-
```

## Configuration

### Basic Configuration

```yaml
plugins:
  - ai-summary:
      # AI Service Configuration
      ai_service: "deepseek"          # Primary AI service
      fallback_services:               # Fallback services if primary fails
        - "openai"
        - "gemini"
      
      # Summary Configuration
      summary_language: "en"           # Summary language (zh/en)
      summary_length: "medium"         # Summary length (short/medium/long)
      
      # Caching Configuration
      cache_enabled: true              # Enable caching
      cache_expire_days: 30            # Cache expiration in days
      
      # File Selection
      enabled_folders:                 # Folders to process
        - "docs"
        - "guides"
      exclude_patterns:                # Patterns to exclude
        - "**/api/**"
        - "**/reference/**"
      exclude_files:                   # Specific files to exclude
        - "index.md"
        - "404.md"
      
      # Environment Configuration
      local_enabled: true              # Enable in local development
      ci_enabled: true                 # Enable in CI/CD
      ci_cache_only: false             # Only use cache in CI (no new API calls)
      ci_fallback_summary: true        # Use fallback summary in CI if no cache
```

### File Selection Configuration Guide

#### enabled_folders Configuration Examples

The `enabled_folders` parameter specifies which folders contain Markdown files that should be processed by the plugin. Here are configuration examples for different project structures:

**Standard MkDocs Project Structure:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"                    # Process all files in docs/ folder
```

**Multi-Source Documentation Project:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"                    # Main documentation
        - "tutorials"               # Tutorial documentation
        - "guides"                  # Guide documentation
        - "blog"                    # Blog posts
        - "examples"                # Example documentation
```

**Multi-Language Project:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/zh"                 # Chinese documentation
        - "docs/en"                 # English documentation
        - "docs/shared"             # Shared documentation
```

**Complex Project Structure:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "documentation"           # Main documentation directory
        - "user-guides"             # User guides
        - "developer-docs"          # Developer documentation
        - "release-notes"           # Release notes
        - "knowledge-base"          # Knowledge base
```

#### exclude_patterns Configuration Examples

The `exclude_patterns` uses glob patterns to exclude files that don't need summaries. Here are common exclusion patterns:

**Exclude API Documentation and References:**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/api/**"               # Exclude all api folders
        - "**/reference/**"         # Exclude all reference folders
        - "**/generated/**"         # Exclude auto-generated documentation
```

**Exclude Specific Document Types:**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/changelog/**"         # Exclude changelogs
        - "**/archive/**"           # Exclude archived documents
        - "**/draft/**"             # Exclude draft documents
        - "**/temp/**"              # Exclude temporary documents
        - "**/internal/**"          # Exclude internal documents
```

**Exclude Specific File Patterns:**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/*-draft.md"           # Exclude draft files
        - "**/*-template.md"        # Exclude template files
        - "**/README.md"            # Exclude README files
        - "**/CONTRIBUTING.md"      # Exclude contribution guides
        - "**/LICENSE.md"           # Exclude license files
```

**Complex Exclusion Patterns:**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/api/**"               # Exclude API documentation
        - "**/reference/**"         # Exclude reference documentation
        - "**/examples/**/output/**" # Exclude example outputs
        - "docs/legacy/**"          # Exclude legacy documentation
        - "**/*-internal.md"        # Exclude internal documents
        - "**/node_modules/**"      # Exclude dependency files
```

#### Real-World Project Configuration Examples

**Blog Website Configuration:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "blog"                    # Blog posts
        - "pages"                   # Static pages
      exclude_patterns:
        - "**/drafts/**"            # Exclude drafts
        - "**/archive/**"           # Exclude archives
        - "blog/tags/**"            # Exclude tag pages
      exclude_files:
        - "index.md"                # Exclude homepage
        - "404.md"                  # Exclude error pages
        - "sitemap.md"              # Exclude sitemap
```

**Technical Documentation Website:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/user-guide"         # User guides
        - "docs/tutorials"          # Tutorials
        - "docs/how-to"             # How-to guides
      exclude_patterns:
        - "**/api-reference/**"     # Exclude API references
        - "**/generated/**"         # Exclude auto-generated content
        - "**/schemas/**"           # Exclude schema definitions
      exclude_files:
        - "glossary.md"             # Exclude glossary
        - "changelog.md"            # Exclude changelog
```

**Multi-Language Documentation:**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/zh-cn"              # Chinese documentation
        - "docs/en"                 # English documentation
      exclude_patterns:
        - "**/translations/**"      # Exclude translation work files
        - "**/locales/**"           # Exclude localization files
      exclude_files:
        - "translation-guide.md"    # Exclude translation guide
```

#### Configuration Best Practices

1. **Specify Folders Explicitly**: Use `enabled_folders` to explicitly specify which folders need processing, avoiding unnecessary file processing.

2. **Use Exclusion Patterns Wisely**: Use `exclude_patterns` to exclude file types that don't need summaries, such as API documentation and reference materials.

3. **Performance Considerations**: Excluding large files and auto-generated documentation can significantly improve build speed.

4. **Maintainability**: Regularly review and update configurations to ensure new documentation structures are properly handled.

5. **Test Configurations**: Test configurations in local environments to ensure all expected files are correctly processed or excluded.

### Advanced Configuration

```yaml
plugins:
  - ai-summary:
      # Custom API Endpoints
      custom_endpoints:
        deepseek:
          base_url: "https://api.deepseek.com"
          model: "deepseek-chat"
        openai:
          base_url: "https://api.openai.com/v1"
          model: "gpt-3.5-turbo"
      
      # Content Processing
      max_content_length: 8000         # Maximum content length for AI processing
      summary_position: "top"          # Position of summary (top/bottom)
      
      # Styling
      summary_style:
        theme: "material"               # Summary card theme
        show_icon: true                 # Show AI service icon
        show_language: true             # Show summary language
```

## Environment Variables

### Required API Keys

| Variable | Description | Required |
|----------|-------------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | If using DeepSeek |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `GEMINI_API_KEY` | Google Gemini API key | If using Gemini |
| `GLM_API_KEY` | GLM API key | If using GLM |

### Optional Configuration

| Variable | Description | Default |
|----------|-------------|----------|
| `AI_SUMMARY_DEBUG` | Enable debug logging | `false` |
| `AI_SUMMARY_TIMEOUT` | API request timeout (seconds) | `30` |
| `AI_SUMMARY_MAX_RETRIES` | Maximum API retry attempts | `3` |

## CI/CD Integration

### GitHub Actions

Add your API keys to GitHub Secrets and use them in your workflow:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x
      
      - name: Install dependencies
        run: |
          pip install mkdocs-material mkdocs-ai-summary-wcowin
      
      - name: Build documentation
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: mkdocs build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## AI Services

### Supported Services

| Service | Model | Languages | Rate Limits |
|---------|-------|-----------|-------------|
| DeepSeek | deepseek-chat | zh, en | High |
| OpenAI | gpt-3.5-turbo, gpt-4 | zh, en | Medium |
| Google Gemini | gemini-pro | zh, en | High |
| GLM | glm-4 | zh, en | Medium |

### Service Selection Strategy

1. **Primary Service**: The main AI service specified in configuration
2. **Fallback Services**: Used if primary service fails or is unavailable
3. **Automatic Retry**: Built-in retry mechanism with exponential backoff
4. **Cost Optimization**: Intelligent service selection based on content length

## Caching System

### How It Works

- **Content Hashing**: Each page's content is hashed to detect changes
- **Service Configuration**: Cache is invalidated when AI service settings change
- **Expiration**: Configurable cache expiration (default: 30 days)
- **CI Optimization**: Special caching behavior for CI/CD environments

### Cache Management

```bash
# Clear all cache
rm -rf .ai_cache/

# Clear expired cache (automatic during build)
# No manual action needed
```

## Troubleshooting

### Common Local Development Issues

#### 1. API Key Not Found

**Error Message:**
```
Error: No valid API key found for service 'deepseek'
Warning: No available AI services, please check API key configuration
```

**Solutions:**
1. Check if `.env` file exists in project root
2. Verify API key name spelling (case-sensitive)
3. Validate API key format
4. Ensure `.env` file has no syntax errors

**Verification Steps:**
```bash
# Check .env file content
cat .env

# Verify environment variables are loaded
python -c "import os; print('DEEPSEEK_API_KEY:', os.getenv('DEEPSEEK_API_KEY', 'Not found'))"
```

#### 2. Plugin Configuration Parameters Not Recognized

**Error Message:**
```
Config value: 'ai_service'. Warning: Unrecognised config name: ai_service
```

**Solutions:**
1. Ensure latest plugin version is installed:
   ```bash
   pip install --upgrade mkdocs-ai-summary-wcowin
   ```
2. Check plugin configuration format in `mkdocs.yml`:
   ```yaml
   plugins:
     - ai-summary:  # Note the space after colon
         ai_service: "deepseek"
   ```

#### 3. Network and Permission Issues

**Error Message:**
```
ConnectionError: Failed to connect to API endpoint
Timeout: Request timed out after 30 seconds
```

**Solutions:**
1. Check network connection
2. Verify API key validity
3. Increase timeout:
   ```env
   AI_SUMMARY_TIMEOUT=60
   ```
4. Check firewall settings

#### 4. Content Too Long Warning

**Warning Message:**
```
Warning: Content too long for AI processing, truncating...
```

**Solutions:**
1. Increase max content length in `mkdocs.yml`:
   ```yaml
   plugins:
     - ai-summary:
         max_content_length: 12000
   ```
2. Split long pages into smaller ones
3. Use `exclude_patterns` to exclude overly long pages

#### 5. File Selection Configuration Issues

**Problem: Cache file count is 0, no AI summaries generated**

**Common Causes and Solutions:**

**Cause 1: enabled_folders configuration mismatch**
```
# Incorrect configuration example
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"  # But actual files are in blog/ directory
```

**Solutions:**
1. Check actual document directory structure:
   ```bash
   find . -name "*.md" -type f | head -10
   ```
2. Adjust configuration based on actual structure:
   ```yaml
   plugins:
     - ai-summary:
         enabled_folders:
           - "blog"      # Match actual directory
           - "docs"
           - "pages"
   ```

**Cause 2: exclude_patterns too broad**
```yaml
# Overly broad exclusion pattern
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/*.md"  # This excludes ALL Markdown files!
```

**Solutions:**
1. Check if exclusion patterns are too broad
2. Use more precise exclusion patterns:
   ```yaml
   plugins:
     - ai-summary:
         exclude_patterns:
           - "**/draft/**"     # Only exclude draft directories
           - "**/temp/**"      # Only exclude temporary directories
           - "**/*-draft.md"   # Only exclude draft files
   ```

**Cause 3: Path separator issues**
```yaml
# Windows system might encounter this issue
plugins:
  - ai-summary:
      enabled_folders:
        - "docs\\tutorials"  # Incorrect path separator
```

**Solutions:**
Always use forward slashes (/) as path separators:
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/tutorials"   # Correct path separator
```

**Cause 4: Incorrect relative path configuration**
```yaml
# Incorrect absolute path configuration
plugins:
  - ai-summary:
      enabled_folders:
        - "/home/user/project/docs"  # Absolute paths not recommended
```

**Solutions:**
Use paths relative to project root:
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"             # Relative path
        - "content/posts"    # Relative path
```

**Methods to Debug Configuration Issues:**

1. **Enable debug mode**:
   ```bash
   export AI_SUMMARY_DEBUG=true
   mkdocs serve
   ```

2. **Check debug output**:
   ```
   DEBUG: Processing page: blog/post1.md
   DEBUG: should_generate_summary: False
   DEBUG: enabled_folders: ['docs']
   DEBUG: Skipping page: Path not in enabled folders
   ```

3. **Verify file paths**:
   ```bash
   # List all Markdown files and their paths
   find . -name "*.md" -type f | grep -v node_modules
   ```

4. **Test configuration**:
   ```yaml
   # Temporary configuration: process all folders
   plugins:
     - ai-summary:
         enabled_folders:
           - "."  # Process all directories (for testing only)
         exclude_patterns: []  # Temporarily exclude no files
   ```

### GitHub Actions Deployment Issues

#### 1. Secrets Configuration Error

**Error Message:**
```
Error: No valid API key found for service 'deepseek'
```

**Solutions:**
1. Check Repository Secrets configuration:
   - Go to GitHub repository → Settings → Secrets and variables → Actions
   - Verify secret names match environment variable names in workflow
   - Re-add potentially corrupted secrets

2. Verify workflow configuration:
   ```yaml
   env:
     DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # Ensure names match
   ```

#### 2. Build Failure

**Error Message:**
```
ERROR - Config value: 'plugins'. Error: The "ai-summary" plugin is not installed
```

**Solutions:**
1. Ensure plugin is installed in workflow:
   ```yaml
   - name: Install dependencies
     run: |
       pip install mkdocs-material
       pip install mkdocs-ai-summary-wcowin  # Ensure this line is included
   ```

2. Check Python version compatibility:
   ```yaml
   - name: Setup Python
     uses: actions/setup-python@v4
     with:
       python-version: '3.8'  # Or higher version
   ```

#### 3. Deployment Permission Issues

**Error Message:**
```
Error: The process '/usr/bin/git' failed with exit code 128
```

**Solutions:**
1. Ensure GitHub Pages is enabled
2. Check `GITHUB_TOKEN` permissions
3. Verify branch name is correct (main/master)

### Performance Optimization Issues

#### 1. Long Build Times

**Solutions:**
1. Enable caching:
   ```yaml
   plugins:
     - ai-summary:
         cache_enabled: true
         cache_expire_days: 30
   ```

2. Use caching in GitHub Actions:
   ```yaml
   - name: Cache AI summaries
     uses: actions/cache@v3
     with:
       path: .ai_cache
       key: ai-cache-${{ hashFiles('docs/**/*.md') }}
   ```

3. Limit processing scope:
   ```yaml
   plugins:
     - ai-summary:
         enabled_folders:
           - "docs/important"  # Only process important docs
         exclude_patterns:
           - "**/archive/**"   # Exclude archived content
   ```

#### 2. Too Many API Calls

**Solutions:**
1. Optimize caching strategy
2. Use CI cache mode:
   ```yaml
   plugins:
     - ai-summary:
         ci_cache_only: true  # Only use cache in CI
   ```

### Debugging and Diagnostics

#### Enable Verbose Logging

**Local Debugging:**
```bash
# Enable debug mode
export AI_SUMMARY_DEBUG=true
mkdocs build --verbose
```

**GitHub Actions Debugging:**
```yaml
- name: Build with debug
  env:
    AI_SUMMARY_DEBUG: true
  run: |
    mkdocs build --verbose
```

#### Check Plugin Status

```bash
# Check if plugin is correctly installed
pip show mkdocs-ai-summary-wcowin

# Check MkDocs plugin list
mkdocs --help

# Verify configuration file
mkdocs config
```

#### Test API Connection

Create test script `test_api.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test API keys
services = {
    'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
    'GLM_API_KEY': os.getenv('GLM_API_KEY')
}

for service, key in services.items():
    if key:
        print(f"✅ {service}: {key[:10]}...{key[-4:]}")
    else:
        print(f"❌ {service}: Not configured")
```

Run test:
```bash
python test_api.py
```

### Getting Help

If the above solutions don't resolve your issue, please:

1. **Check Detailed Logs**: Enable debug mode for more information
2. **Check Version Compatibility**: Ensure you're using the latest plugin and MkDocs versions
3. **Submit an Issue**: Create an issue in the [GitHub repository](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues)
4. **Provide Information**: Include error logs, configuration files, and environment information

**Issue Template:**
```
## Problem Description
[Describe the issue you're experiencing]

## Environment Information
- Operating System:
- Python Version:
- MkDocs Version:
- Plugin Version:

## Configuration File
```yaml
[Paste your mkdocs.yml configuration]
```

## Error Logs
```
[Paste complete error messages]
```

## Reproduction Steps
1. 
2. 
3. 
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/Wcowin/Mkdocs-AI-Summary-Plus.git
cd Mkdocs-AI-Summary-Plus
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black .
flake8 .
mypy .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Support

- 📖 [Documentation](https://wcowin.work/mkdocs-ai-hooks/)
- 🐛 [Issue Tracker](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues)
- 💬 [Discussions](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/discussions)
- 📧 [Email Support](mailto:wcowin@qq.com)

## Acknowledgments

- [MkDocs](https://www.mkdocs.org/) - The static site generator this plugin extends
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - The beautiful theme that inspired our design
- All the AI service providers for making this plugin possible