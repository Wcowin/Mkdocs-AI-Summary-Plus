# MkDocs AI Summary Plugin  
![alt text](logo-2.png)

[![PyPI version](https://badge.fury.io/py/mkdocs-ai-summary-wcowin.svg)](https://badge.fury.io/py/mkdocs-ai-summary-wcowin)
[![Python Support](https://img.shields.io/pypi/pyversions/mkdocs-ai-summary-wcowin.svg)](https://pypi.org/project/mkdocs-ai-summary-wcowin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个智能的 MkDocs 插件，使用多种 AI 服务（包括 OpenAI、DeepSeek、Google Gemini 和 GLM）为您的文档页面自动生成 AI 驱动的摘要。
![预览图1](https://s1.imagehub.cc/images/2025/06/03/d1563500263b22cfd0ffc3679993aa83.jpg)
![预览图2](https://s1.imagehub.cc/images/2025/06/03/526b59b6a2e478f2ffa1629320e3e2ce.png)
## 功能特性

- 🤖 **多种 AI 服务**：支持 OpenAI、DeepSeek、Google Gemini 和 GLM
- 🚀 **智能缓存**：智能缓存系统减少 API 调用和成本
- 🎯 **灵活配置**：精细控制哪些页面生成摘要
- 🌍 **多语言支持**：生成不同语言的摘要
- 🔧 **CI/CD 就绪**：与 GitHub Actions 和其他 CI/CD 系统无缝集成
- 📱 **响应式设计**：在所有设备上都能正常工作的美观摘要卡片
- ⚡ **性能优化**：通过智能缓存对构建时间的影响最小

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install mkdocs-ai-summary-wcowin
```

## 快速开始

### 1. 配置您的 MkDocs

在您的 `mkdocs.yml` 中添加插件：

```yaml
plugins:
  - ai-summary:
      ai_service: "deepseek"  # 或 "openai", "gemini", "glm"
      summary_language: "zh"  # 或 "en"
      cache_enabled: true # 启用缓存
      # clear_cache: true  # 下次构建时清理所有缓存
      cache_expire_days: 30  # 缓存过期时间（天）
      local_enabled: true # 在本地开发中启用
      debug: true # 是否显示调试信息（默认：false）
      enabled_folders:
        - blog/    # 添加blog文件夹
        - docs/    # 保留docs文件夹
      exclude_patterns:
        - "**/api/**"
        - "**/reference/**"
        - "**about/**" # 排除about文件夹
        - "index.md" # 排除index.md
        - "tag.md" # 排除tag.md
        - "blog/posts/update.md" # 排除blog/posts/update.md
```

### 2. 设置环境变量

在项目**根目录**创建 `.env` 文件：

```env
# 选择一个或多个 AI 服务
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
GLM_API_KEY=your_glm_api_key
```

### 3. 构建您的文档

```bash
mkdocs build # 构建文档

mkdocs serve # 在本地预览
```

插件将自动为您的页面生成 AI 摘要并将其注入到内容中。

## 详细配置指南

### 本地开发配置

#### 步骤1：获取API密钥

根据您选择的AI服务，获取相应的API密钥：

**DeepSeek (推荐)**
1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 进入API管理页面
4. 创建新的API密钥
5. 复制密钥备用

**OpenAI**
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录您的账号
3. 进入API Keys页面
4. 点击"Create new secret key"
5. 复制密钥备用

**Google Gemini**
1. 访问 [Google AI Studio](https://makersuite.google.com/)
2. 登录Google账号
3. 创建新的API密钥
4. 复制密钥备用

**GLM (智谱AI)(最推荐)**
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 进入API管理
4. 创建API密钥
5. 复制密钥备用

#### 步骤2：创建.env文件

在您的项目根目录（与`mkdocs.yml`同级）创建`.env`文件：

```bash
# 在项目根目录执行
touch .env
```

#### 步骤3：配置API密钥

编辑`.env`文件，添加您的API密钥：

```env
# DeepSeek API密钥 (推荐)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI API密钥
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Gemini API密钥
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GLM API密钥
GLM_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx

# 可选：调试模式
AI_SUMMARY_DEBUG=false

# 可选：API超时设置（秒）
AI_SUMMARY_TIMEOUT=30

# 可选：最大重试次数
AI_SUMMARY_MAX_RETRIES=3
```

**重要提示：**
- 只需要配置您计划使用的AI服务的API密钥
- 确保`.env`文件已添加到`.gitignore`中，避免泄露API密钥
- API密钥格式因服务而异，请确保复制完整的密钥

#### 步骤4：验证配置

运行以下命令验证配置是否正确：

```bash
# 本地构建测试
mkdocs build

# 本地预览
mkdocs serve
```

如果配置正确，您应该能看到插件成功加载并生成AI摘要。

### GitHub部署配置

#### 步骤1：准备GitHub仓库

1. 将您的项目推送到GitHub仓库
2. 确保`.env`文件已添加到`.gitignore`中
3. 确保`mkdocs.yml`和插件配置已提交

#### 步骤2：配置Repository Secrets

在GitHub仓库中配置API密钥：

1. **进入仓库设置**
   - 打开您的GitHub仓库
   - 点击"Settings"选项卡
   - 在左侧菜单中找到"Secrets and variables"
   - 点击"Actions"

2. **添加Repository Secrets**
   
   点击"New repository secret"按钮，逐个添加以下密钥：
   
   | Secret名称 | 值 | 说明 |
   |-----------|----|----------|
   | `DEEPSEEK_API_KEY` | 您的DeepSeek API密钥 | 如果使用DeepSeek服务 |
   | `OPENAI_API_KEY` | 您的OpenAI API密钥 | 如果使用OpenAI服务 |
   | `GEMINI_API_KEY` | 您的Gemini API密钥 | 如果使用Gemini服务 |
   | `GLM_API_KEY` | 您的GLM API密钥 | 如果使用GLM服务 |

   **添加步骤：**
   - Name: 输入密钥名称（如`DEEPSEEK_API_KEY`）
   - Secret: 粘贴您的API密钥
   - 点击"Add secret"

#### 步骤3：创建GitHub Actions工作流

在您的仓库中创建`.github/workflows/deploy.yml`文件：

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
        # 如果有requirements.txt文件
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Build documentation with AI summaries
      env:
        # 配置API密钥环境变量
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        GLM_API_KEY: ${{ secrets.GLM_API_KEY }}
        # 可选配置
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
        # 可选：自定义域名
        # cname: your-domain.com
```

#### 步骤4：启用GitHub Pages

1. 在仓库设置中找到"Pages"选项
2. Source选择"Deploy from a branch"
3. Branch选择"gh-pages"
4. 点击"Save"

#### 步骤5：触发部署

推送代码到main分支即可触发自动部署：

```bash
git add .
git commit -m "Add AI summary plugin configuration"
git push origin main
```

### 高级CI/CD配置

#### 多环境配置

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
        # 部署到staging环境
  
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
        # 部署到生产环境
```

#### 缓存优化配置

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

## 配置

### 基础配置

```yaml
# mkdocs.yml
plugins:
  - ai-summary:
      # AI 服务配置
      ai_service: "deepseek"          # 主要 AI 服务
      fallback_services:               # 主要服务失败时的备用服务
        - "openai"
        - "gemini"
      
      # 摘要配置
      summary_language: "zh"           # 摘要语言 (zh/en)
      summary_length: "medium"         # 摘要长度 (short/medium/long)
      
      # 缓存配置
      cache_enabled: true              # 启用缓存
      cache_expire_days: 30            # 缓存过期天数
      
      # 文件选择
      enabled_folders:                 # 要处理的文件夹
        - "docs"
        - "guides"
      exclude_patterns:                # 要排除的模式
        - "**/api/**"
        - "**/reference/**"
      exclude_files:                   # 要排除的特定文件
        - "index.md"
        - "404.md"
      
      # 环境配置
      local_enabled: true              # 在本地开发中启用
      ci_enabled: true                 # 在 CI/CD 中启用
      ci_cache_only: false             # 在 CI 中仅使用缓存（不进行新的 API 调用）
      ci_fallback_summary: true        # 在 CI 中如果没有缓存则使用备用摘要
```

### 文件选择配置详解

#### enabled_folders 配置示例

`enabled_folders` 参数指定插件应该处理哪些文件夹中的 Markdown 文件。以下是针对不同项目结构的配置示例：

**标准 MkDocs 项目结构：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"                    # 处理 docs/ 文件夹下的所有文件
```

**多文档源项目：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"                    # 主要文档
        - "tutorials"               # 教程文档
        - "guides"                  # 指南文档
        - "blog"                    # 博客文章
        - "examples"                # 示例文档
```

**多语言项目：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/zh"                 # 中文文档
        - "docs/en"                 # 英文文档
        - "docs/shared"             # 共享文档
```

**复杂项目结构：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "documentation"           # 主文档目录
        - "user-guides"             # 用户指南
        - "developer-docs"          # 开发者文档
        - "release-notes"           # 发布说明
        - "knowledge-base"          # 知识库
```

#### exclude_patterns 配置示例

`exclude_patterns` 使用 glob 模式来排除不需要生成摘要的文件。以下是常见的排除模式：

**排除 API 文档和参考资料：**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/api/**"               # 排除所有 api 文件夹
        - "**/reference/**"         # 排除所有 reference 文件夹
        - "**/generated/**"         # 排除自动生成的文档
```

**排除特定类型的文档：**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/changelog/**"         # 排除更新日志
        - "**/archive/**"           # 排除归档文档
        - "**/draft/**"             # 排除草稿文档
        - "**/temp/**"              # 排除临时文档
        - "**/internal/**"          # 排除内部文档
```

**排除特定文件模式：**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/*-draft.md"           # 排除草稿文件
        - "**/*-template.md"        # 排除模板文件
        - "**/README.md"            # 排除 README 文件
        - "**/CONTRIBUTING.md"      # 排除贡献指南
        - "**/LICENSE.md"           # 排除许可证文件
```

**复合排除模式：**
```yaml
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/api/**"               # 排除 API 文档
        - "**/reference/**"         # 排除参考文档
        - "**/examples/**/output/**" # 排除示例输出
        - "docs/legacy/**"          # 排除遗留文档
        - "**/*-internal.md"        # 排除内部文档
        - "**/node_modules/**"      # 排除依赖文件
```

#### 实际项目配置示例

**博客网站配置：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "blog"                    # 博客文章
        - "pages"                   # 静态页面
      exclude_patterns:
        - "**/drafts/**"            # 排除草稿
        - "**/archive/**"           # 排除归档
        - "blog/tags/**"            # 排除标签页面
      exclude_files:
        - "index.md"                # 排除首页
        - "404.md"                  # 排除错误页面
        - "sitemap.md"              # 排除站点地图
```

**技术文档网站配置：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/user-guide"         # 用户指南
        - "docs/tutorials"          # 教程
        - "docs/how-to"             # 操作指南
      exclude_patterns:
        - "**/api-reference/**"     # 排除 API 参考
        - "**/generated/**"         # 排除自动生成内容
        - "**/schemas/**"           # 排除模式定义
      exclude_files:
        - "glossary.md"             # 排除术语表
        - "changelog.md"            # 排除更新日志
```

**多语言文档配置：**
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/zh-cn"              # 中文文档
        - "docs/en"                 # 英文文档
      exclude_patterns:
        - "**/translations/**"      # 排除翻译工作文件
        - "**/locales/**"           # 排除本地化文件
      exclude_files:
        - "translation-guide.md"    # 排除翻译指南
```

#### 配置最佳实践

1. **明确指定文件夹**：使用 `enabled_folders` 明确指定需要处理的文件夹，避免处理不必要的文件。

2. **合理使用排除模式**：使用 `exclude_patterns` 排除不需要摘要的文件类型，如 API 文档、参考资料等。

3. **性能考虑**：排除大型文件和自动生成的文档可以显著提高构建速度。

4. **维护性**：定期检查和更新配置，确保新增的文档结构被正确处理。

5. **测试配置**：在本地环境中测试配置，确保所有期望的文件都被正确处理或排除。

### 高级配置

```yaml
plugins:
  - ai-summary:
      # 自定义 API 端点
      custom_endpoints:
        deepseek:
          base_url: "https://api.deepseek.com"
          model: "deepseek-chat"
        openai:
          base_url: "https://api.openai.com/v1"
          model: "gpt-3.5-turbo"
      
      # 内容处理
      max_content_length: 8000         # AI 处理的最大内容长度
      summary_position: "top"          # 摘要位置 (top/bottom)
      
      # 样式
      summary_style:
        theme: "material"               # 摘要卡片主题
        show_icon: true                 # 显示 AI 服务图标
        show_language: true             # 显示摘要语言
```

## 环境变量

### 必需的 API 密钥

| 变量 | 描述 | 必需 |
|------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 如果使用 DeepSeek |
| `OPENAI_API_KEY` | OpenAI API 密钥 | 如果使用 OpenAI |
| `GEMINI_API_KEY` | Google Gemini API 密钥 | 如果使用 Gemini |
| `GLM_API_KEY` | GLM API 密钥 | 如果使用 GLM |

### 可选配置

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `AI_SUMMARY_DEBUG` | 启用调试日志 | `false` |
| `AI_SUMMARY_TIMEOUT` | API 请求超时（秒） | `30` |
| `AI_SUMMARY_MAX_RETRIES` | 最大 API 重试次数 | `3` |

## CI/CD 集成

### GitHub Actions

将您的 API 密钥添加到 GitHub Secrets 并在工作流中使用：

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

## AI 服务

### 支持的服务

| 服务 | 模型 | 语言 | 速率限制 |
|------|------|------|----------|
| DeepSeek | deepseek-chat | zh, en | 高 |
| OpenAI | gpt-3.5-turbo, gpt-4 | zh, en | 中等 |
| Google Gemini | gemini-pro | zh, en | 高 |
| GLM | glm-4 | zh, en | 中等 |

### 服务选择策略

1. **主要服务**：配置中指定的主要 AI 服务
2. **备用服务**：主要服务失败或不可用时使用
3. **自动重试**：内置重试机制，采用指数退避
4. **成本优化**：基于内容长度的智能服务选择

## 缓存系统

### 工作原理

- **内容哈希**：每个页面的内容都会被哈希以检测变化
- **服务配置**：AI 服务设置更改时缓存会失效
- **过期**：可配置的缓存过期时间（默认：30天）
- **CI 优化**：CI/CD 环境的特殊缓存行为

### 缓存管理

```bash
# 清除所有缓存
rm -rf .ai_cache/

# 清除过期缓存（构建时自动进行）
# 无需手动操作
```

## 故障排除和常见问题

### 本地开发常见问题

#### 1. API密钥未找到

**错误信息：**
```
Error: No valid API key found for service 'deepseek'
警告: 没有可用的AI服务，请检查API密钥配置
```

**解决方案：**
1. 检查`.env`文件是否存在于项目根目录
2. 确认API密钥名称拼写正确（区分大小写）
3. 验证API密钥格式是否正确
4. 确保`.env`文件没有语法错误

**验证步骤：**
```bash
# 检查.env文件内容
cat .env

# 验证环境变量是否加载
python -c "import os; print('DEEPSEEK_API_KEY:', os.getenv('DEEPSEEK_API_KEY', 'Not found'))"
```

#### 2. 插件配置参数未识别

**错误信息：**
```
Config value: 'ai_service'. Warning: Unrecognised config name: ai_service
```

**解决方案：**
1. 确保安装了最新版本的插件：
   ```bash
   pip install --upgrade mkdocs-ai-summary-wcowin
   ```
2. 检查`mkdocs.yml`中的插件配置格式：
   ```yaml
   plugins:
     - ai-summary:  # 注意冒号后的空格
         ai_service: "deepseek"
   ```

#### 3. 权限和网络问题

**错误信息：**
```
ConnectionError: Failed to connect to API endpoint
Timeout: Request timed out after 30 seconds
```

**解决方案：**
1. 检查网络连接
2. 验证API密钥是否有效
3. 增加超时时间：
   ```env
   AI_SUMMARY_TIMEOUT=60
   ```
4. 检查防火墙设置

#### 4. 内容过长警告

**警告信息：**
```
Warning: Content too long for AI processing, truncating...
```

**解决方案：**
1. 在`mkdocs.yml`中增加最大内容长度：
   ```yaml
   plugins:
     - ai-summary:
         max_content_length: 12000
   ```
2. 将长页面拆分为多个较小的页面
3. 使用`exclude_patterns`排除过长的页面

#### 5. 文件选择配置问题

**问题：缓存文件数量为0，没有生成AI摘要**

**常见原因和解决方案：**

**原因1：enabled_folders配置不匹配**
```
# 错误配置示例
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"  # 但实际文件在 blog/ 目录下
```

**解决方案：**
1. 检查实际文档目录结构：
   ```bash
   find . -name "*.md" -type f | head -10
   ```
2. 根据实际结构调整配置：
   ```yaml
   plugins:
     - ai-summary:
         enabled_folders:
           - "blog"      # 匹配实际目录
           - "docs"
           - "pages"
   ```

**原因2：exclude_patterns过于宽泛**
```yaml
# 过于宽泛的排除模式
plugins:
  - ai-summary:
      exclude_patterns:
        - "**/*.md"  # 这会排除所有Markdown文件！
```

**解决方案：**
1. 检查排除模式是否过于宽泛
2. 使用更精确的排除模式：
   ```yaml
   plugins:
     - ai-summary:
         exclude_patterns:
           - "**/draft/**"     # 只排除草稿目录
           - "**/temp/**"      # 只排除临时目录
           - "**/*-draft.md"   # 只排除草稿文件
   ```

**原因3：路径分隔符问题**
```yaml
# Windows系统可能遇到的问题
plugins:
  - ai-summary:
      enabled_folders:
        - "docs\\tutorials"  # 错误的路径分隔符
```

**解决方案：**
始终使用正斜杠（/）作为路径分隔符：
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs/tutorials"   # 正确的路径分隔符
```

**原因4：相对路径配置错误**
```yaml
# 错误的绝对路径配置
plugins:
  - ai-summary:
      enabled_folders:
        - "/home/user/project/docs"  # 绝对路径不推荐
```

**解决方案：**
使用相对于项目根目录的路径：
```yaml
plugins:
  - ai-summary:
      enabled_folders:
        - "docs"             # 相对路径
        - "content/posts"    # 相对路径
```

**调试配置问题的方法：**

1. **启用调试模式**：
   ```bash
   export AI_SUMMARY_DEBUG=true
   mkdocs serve
   ```

2. **检查调试输出**：
   ```
   DEBUG: Processing page: blog/post1.md
   DEBUG: should_generate_summary: False
   DEBUG: enabled_folders: ['docs']
   DEBUG: Skipping page: Path not in enabled folders
   ```

3. **验证文件路径**：
   ```bash
   # 列出所有Markdown文件及其路径
   find . -name "*.md" -type f | grep -v node_modules
   ```

4. **测试配置**：
   ```yaml
   # 临时配置：处理所有文件夹
   plugins:
     - ai-summary:
         enabled_folders:
           - "."  # 处理所有目录（仅用于测试）
         exclude_patterns: []  # 暂时不排除任何文件
   ```

### GitHub Actions部署问题

#### 1. Secrets配置错误

**错误信息：**
```
Error: No valid API key found for service 'deepseek'
```

**解决方案：**
1. 检查Repository Secrets配置：
   - 进入GitHub仓库 → Settings → Secrets and variables → Actions
   - 确认密钥名称与工作流中的环境变量名称一致
   - 重新添加可能损坏的密钥

2. 验证工作流配置：
   ```yaml
   env:
     DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # 确保名称匹配
   ```

#### 2. 构建失败

**错误信息：**
```
ERROR - Config value: 'plugins'. Error: The "ai-summary" plugin is not installed
```

**解决方案：**
1. 确保工作流中安装了插件：
   ```yaml
   - name: Install dependencies
     run: |
       pip install mkdocs-material
       pip install mkdocs-ai-summary-wcowin  # 确保包含此行
   ```

2. 检查Python版本兼容性：
   ```yaml
   - name: Setup Python
     uses: actions/setup-python@v4
     with:
       python-version: '3.8'  # 或更高版本
   ```

#### 3. 部署权限问题

**错误信息：**
```
Error: The process '/usr/bin/git' failed with exit code 128
```

**解决方案：**
1. 确保GitHub Pages已启用
2. 检查`GITHUB_TOKEN`权限
3. 验证分支名称是否正确（main/master）

### 性能优化问题

#### 1. 构建时间过长

**解决方案：**
1. 启用缓存：
   ```yaml
   plugins:
     - ai-summary:
         cache_enabled: true
         cache_expire_days: 30
   ```

2. 在GitHub Actions中使用缓存：
   ```yaml
   - name: Cache AI summaries
     uses: actions/cache@v3
     with:
       path: .ai_cache
       key: ai-cache-${{ hashFiles('docs/**/*.md') }}
   ```

3. 限制处理范围：
   ```yaml
   plugins:
     - ai-summary:
         enabled_folders:
           - "docs/important"  # 只处理重要文档
         exclude_patterns:
           - "**/archive/**"   # 排除归档内容
   ```

#### 2. API调用次数过多

**解决方案：**
1. 优化缓存策略
2. 使用CI缓存模式：
   ```yaml
   plugins:
     - ai-summary:
         ci_cache_only: true  # CI中只使用缓存
   ```

### 调试和诊断

#### 启用详细日志

**本地调试：**
```bash
# 启用调试模式
export AI_SUMMARY_DEBUG=true
mkdocs build --verbose
```

**GitHub Actions调试：**
```yaml
- name: Build with debug
  env:
    AI_SUMMARY_DEBUG: true
  run: |
    mkdocs build --verbose
```

#### 检查插件状态

```bash
# 检查插件是否正确安装
pip show mkdocs-ai-summary-wcowin

# 检查MkDocs插件列表
mkdocs --help

# 验证配置文件
mkdocs config
```

#### 测试API连接

创建测试脚本`test_api.py`：

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试API密钥
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

运行测试：
```bash
python test_api.py
```

### 获取帮助

如果以上解决方案都无法解决您的问题，请：

1. **查看详细日志**：启用调试模式获取更多信息
2. **检查版本兼容性**：确保使用最新版本的插件和MkDocs
3. **提交Issue**：在[GitHub仓库](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues)中提交问题
4. **提供信息**：包含错误日志、配置文件和环境信息

**Issue模板：**

```
## 问题描述

[描述您遇到的问题]

## 环境信息
- 操作系统：
- Python版本：
- MkDocs版本：
- 插件版本：

## 配置文件

[粘贴您的mkdocs.yml配置]


## 错误日志
```


## 贡献(暂未开放)

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 开发设置

```bash
git clone https://github.com/Wcowin/Mkdocs-AI-Summary-Plus.git
cd Mkdocs-AI-Summary-Plus
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码质量

```bash
black .
flake8 .
mypy .
```

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。


## 支持

- 📖 [文档](https://wcowin.work/mkdocs-ai-hooks/)
- 🐛 [问题跟踪](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues)
- 💬 [讨论](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/discussions)
- 📧 [邮件支持](mailto:wcowin@qq.com)

## 致谢

- [MkDocs](https://www.mkdocs.org/) - 本插件扩展的静态站点生成器
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - 启发我们设计的美观主题
- 所有使这个插件成为可能的 AI 服务提供商