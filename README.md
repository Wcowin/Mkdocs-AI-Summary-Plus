# MkDocs AI Summary

![alt text](logo-2.png)
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
- **环境自适应**: 自动识别CI/本地环境，本地或者部署都可选启用/禁用
- **自动语言识别**: 支持30+编程语言和标记语言
- **内容类型检测**: 区分代码、配置、命令行等不同内容
- **LRU缓存优化**: 提升处理性能（Todo）
- **完善错误处理**: 异常处理和日志记录（Todo）

---

## 📦 快速安装

### 方法1: 直接下载（推荐）

**步骤1**: 下载文件
- 从 [Releases页面](https://github.com/Wcowin/mkdocs-ai-hooks/releases) 下载最新版本
- 或直接下载 `ai_summary.py`文件

**步骤2**: 创建目录并放置文件
```bash
# 在您的MkDocs项目根目录下执行
mkdir -p docs/overrides/hooks/
mv ai_summary.py docs/overrides/hooks/
```

**步骤3**: 配置MkDocs主题以及覆写路径
```yaml
# 在 mkdocs.yml 中添加
theme:
  name: material
  custom_dir: docs/overrides  # 必需配置！！！
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

**步骤1**: 配置hooks
ai_summary.py务必放到docs/overrides/hooks目录下，然后：
```yaml
# 在 mkdocs.yml 中添加
hooks:
  - docs/overrides/hooks/ai_summary.py      # AI摘要hook
```
**步骤2**: 本地配置
根目录下创建 `.env` 文件存放密钥（记得添加到 `.gitignore`）：
```bash
# .env 文件内容
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

```bash
#.gitignore 文件内容
# 环境变量文件（敏感信息）
.env
.env.local
.env.*.local
*.key

# MkDocs 构建输出目录
site/

# AI 摘要缓存目录（项目根目录）- 需要被提交
!.ai_cache/
```

到这里检查下目录树状图:
```
$ tree -a
文件名
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
├──.gitignore
├── README.md
└── mkdocs.yml
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

**获取的密钥存放于上一步创建的`.env` 文件中！！！**

### 3. 设置参数

在 `ai_summary.py` 中配置需要AI摘要的目录：
```python
# 📂 启用AI摘要的文件夹
self.enabled_folders = [
    'blog/',      # 博客文章
    # 添加更多文件夹...
]
```

### 4. 本地运行和测试

```bash
mkdocs serve  # 本地预览
```
### 5. 部署配置

```yaml
#ci.yml
name: ci 
on:
  push:
    branches:
      - master 
      - main
  # 禁止从 fork 仓库访问 secrets
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
          # AI摘要开关控制
          AI_SUMMARY_CI_ENABLED: 'true'           # CI部署环境启用AI摘要 (true=在CI中为文章生成AI摘要)
          AI_SUMMARY_CI_ONLY_CACHE: 'true'       # CI部署不生成新摘要 (true=使用本地部署过的摘要缓存，不再重复调用API)
          AI_SUMMARY_CI_FALLBACK: 'true'          # CI部署启用备用摘要 (true=API失败时生成离线基础摘要)
          # AI_SUMMARY_LOCAL_ENABLED: 'false'       # 本地部署环境禁用AI摘要 (true=本地开发时也生成摘要)（不需要管这条）
          # AI_SUMMARY_CACHE_ENABLED: 'true'        # 本地启用缓存功能 (true=缓存摘要避免重复生成)（不需要管这条）
          # API密钥配置
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: mkdocs gh-deploy --force
      
      # 自动提交新生成的AI缓存文件
      - name: Auto-commit AI cache (if any new files)
        run: |
          if [ -d ".ai_cache" ] && [ "$(ls -A .ai_cache 2>/dev/null)" ]; then
            git config --local user.email "action@github.com"
            git config --local user.name "GitHub Action"
            git add .ai_cache/
            if ! git diff --cached --quiet; then
              git commit -m "🤖 Auto-update AI summary cache [skip ci]"
              git push
              echo "✅ 自动提交了新的 AI 缓存文件"
            else
              echo "ℹ️ 没有新的缓存文件需要提交"
            fi
          else
            echo "ℹ️ 没有找到缓存目录或缓存为空"
          fi
```

```python
# ai_summary.py 中配置
# AI摘要本地环境配置
self.ci_config = {
    # CI部署环境开关 (不用管，只在ci.yml中设置有效)
    'enabled_in_ci': os.getenv('AI_SUMMARY_CI_ENABLED', 'true').lower() == 'true',
    
    # 本地部署环境开关 (true=本地开发时启用AI摘要)
    'enabled_in_local': os.getenv('AI_SUMMARY_LOCAL_ENABLED', 'true').lower() == 'true',
    
    # CI部署仅缓存模式(不用管，只在ci.yml中设置有效)
    'ci_only_cache': os.getenv('AI_SUMMARY_CI_ONLY_CACHE', 'false').lower() == 'true',
    
    # 本地部署缓存功能开关 (true=启用缓存避免重复生成, false=总是生成新摘要)
    'cache_enabled': os.getenv('AI_SUMMARY_CACHE_ENABLED', 'true').lower() == 'true',
    
    # CI部署备用摘要开关 (不用管，只在ci.yml中设置有效)
    'ci_fallback_enabled': os.getenv('AI_SUMMARY_CI_FALLBACK', 'true').lower() == 'true',
}
```  

**几种运行模式**：
1. **完全禁用**: 本地和CI部署都不运行摘要生成
2. **仅CI部署启用**: 本地禁用，CI部署生成新摘要
3. **缓存模式**：本地已经生成过摘要，CI部署使用缓存（**推荐。上方配置项中已默认CI部署的缓存模式，可自行搭配选择**）
4. **完全启用**: 本地和CI部署都运行(API消耗会更多)

### 6. GitHub Secrets配置

**步骤1**: 设置Repository Secrets
1. 进入GitHub仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret** 添加：
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
![image](https://s1.imagehub.cc/images/2025/06/04/b5fd63d839bb6443c8560a5f690d2c41.png)
---

然后部署到GitHub Pages或其他平台即可。

**有报错可以去问ChatGPT或者在Issues中提问。**

## 📖 使用指南

### AI摘要控制

#### 方法1: 页面级控制（推荐）
如果只想为特定文件生成摘要，在Markdown文件最上面的yaml meta中：

**启用AI摘要**：
```yaml
---
title: 文章标题
ai_summary: true   # 启用AI摘要
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
# 📂 可自定义的文件夹配置
self.enabled_folders = [
    'blog/',      # blog文件夹
    'index.md',     
    # 'develop/',   # develop文件夹
    # 'posts/',     # posts文件夹
    # 'trip/',     # trip文件夹
    # 'about/',     # about文件夹
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

## 🎨 显示效果

### AI摘要显示  
**实际效果预览**：
![image](https://s1.imagehub.cc/images/2025/06/04/152205c10ef1bfd7658b383a3e5e6e9f.png)


### 💰 成本说明
- **单次费用**: 一次全部总结约0.03-0.05元（中大型文档）
- **月度预估**: 普通博客约1～3¥
- **免费额度**: 多数AI服务商提供新用户免费额度

---

## ⚙️ 高级配置

### 自定义AI服务

#### 方法1: 使用配置函数（推荐）
```python
# 在 mkdocs.yml 同级目录创建 hooks_config.py
from docs.overrides.hooks.ai_summary import configure_ai_summary, add_ai_service, add_openai_service

# 添加OpenAI兼容的服务
add_openai_service(
    'my_deepseek',
    'https://api.deepseek.com/v1/chat/completions',
    'deepseek-chat',
    'your-deepseek-key'
)

# 添加本地部署的模型
add_openai_service(
    'local_llm',
    'http://localhost:8000/v1/chat/completions',
    'local-model',
    'dummy-key',
    temperature=0.7
)

# 添加完全自定义的服务
add_ai_service('custom_service', {
    'url': 'https://api.custom.com/v1/chat/completions',
    'model': 'custom-model',
    'api_key': 'your-custom-key',
    'format': 'openai',  # 或 'claude', 'gemini', 'custom'
    'max_tokens': 200,
    'temperature': 0.3,
    'headers': {'Custom-Header': 'value'}
})

# 配置基本设置和服务优先级
configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='zh',
    service_priority=['my_deepseek', 'local_llm', 'custom_service', 'openai']
)
```

#### 方法2: 从环境变量配置
```python
# 在 mkdocs.yml 同级目录创建 hooks_config.py
from docs.overrides.hooks.ai_summary import add_service_from_env, configure_ai_summary

# 从环境变量自动配置
add_service_from_env('my_service', 'MYAPI')

configure_ai_summary(
    enabled_folders=['blog/'],
    service_priority=['my_service', 'openai']
)
```

```bash
# .env 文件中添加
MYAPI_URL=https://api.myservice.com/v1/chat/completions
MYAPI_MODEL=my-model
MYAPI_API_KEY=your-api-key
MYAPI_MAX_TOKENS=150
MYAPI_TEMPERATURE=0.3
MYAPI_FORMAT=openai
```

#### 方法3: 直接在configure_ai_summary中配置
```python
# 在 mkdocs.yml 同级目录创建 hooks_config.py
from docs.overrides.hooks.ai_summary import configure_ai_summary

configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='zh',
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

### 支持的API格式

#### OpenAI兼容格式
```python
{
    'url': 'https://api.openai.com/v1/chat/completions',
    'model': 'gpt-4',
    'api_key': 'your-key',
    'format': 'openai'
}
```

#### Claude格式
```python
{
    'url': 'https://api.anthropic.com/v1/messages',
    'model': 'claude-3-haiku-20240307',
    'api_key': 'your-key',
    'format': 'claude'
}
```

#### Gemini格式
```python
{
    'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
    'model': 'gemini-pro',
    'api_key': 'your-key',
    'format': 'gemini'
}
```

#### 完全自定义格式
```python
def custom_payload_builder(content, title, config):
    return {
        "prompt": f"请总结以下内容：{content}",
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

### 常见自定义配置示例

#### 1. 使用Azure OpenAI
```python
add_ai_service('azure_openai', {
    'url': 'https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2023-12-01-preview',
    'model': 'gpt-4',
    'api_key': 'your-azure-key',
    'format': 'openai',
    'headers': {'api-key': 'your-azure-key'}  # Azure使用api-key头部
})
```

#### 2. 使用Ollama本地模型
```python
add_openai_service(
    'ollama',
    'http://localhost:11434/v1/chat/completions',
    'llama2',
    'dummy-key'  # Ollama不需要真实key
)
```

#### 3. 使用通义千问
```python
add_openai_service(
    'qwen',
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    'qwen-turbo',
    'your-dashscope-key'
)
```

#### 4. 使用智谱AI
```python
add_openai_service(
    'zhipu',
    'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    'glm-4',
    'your-zhipu-key'
)
```

### 服务管理功能

```python
from docs.overrides.hooks.ai_summary import list_ai_services, set_service_priority

# 列出所有可用服务
list_ai_services()

# 动态调整服务优先级
set_service_priority('my_custom_service', 'openai', 'deepseek')
```

### 配置文件组织

推荐在项目根目录创建 `hooks_config.py` 来管理所有自定义配置：

```python
# hooks_config.py
from docs.overrides.hooks.ai_summary import *

# 自定义服务配置
add_openai_service('my_gpt4', 'https://api.openai.com/v1/chat/completions', 'gpt-4', os.getenv('OPENAI_API_KEY'))
add_service_from_env('aliyun_qwen', 'QWEN')

# 基础配置
configure_ai_summary(
    enabled_folders=['blog/', 'docs/'],
    language='zh',
    service_priority=['my_gpt4', 'aliyun_qwen', 'deepseek'],
    cache_enabled=True
)
```

然后在 `mkdocs.yml` 中引入：

```yaml
hooks:
  - docs/overrides/hooks/ai_summary.py
  - hooks_config.py  # 引入自定义配置
```

---

## 🔐 安全配置

### 密钥管理
- **使用环境变量**: 在 `.env` 文件中配置您的API密钥
- **GitHub Secrets**: 在GitHub仓库的Secrets中配置密钥，名称为 `DEEPSEEK_API_KEY` 和 `OPENAI_API_KEY`

### 安全注意事项
- 切勿将密钥直接写入代码中
- 定期轮换您的API密钥
- 监控API使用情况，及时发现异常

---

## 🌍 多语言支持

### 默认全局语言配置
```python
# 在 ai_summary.py 中设置
self.summary_language = 'zh'    # 中文摘要
# self.summary_language = 'en'  # 英文摘要
# self.summary_language = 'both' # 双语摘要
```

### 在页面中指定摘要语言  

```yaml
---
title: "我的技术文章"
ai_summary_lang: zh
---
```
```
---
title: "My Technical Article"
ai_summary_lang: en
---
```

```
---
title: "双语技术文章 / Bilingual Technical Article"
ai_summary_lang: both
---
```


### 支持的语言
- **完全支持**: 中文、English
- **部分支持**: 日本語です、한글、Français、Deutsch

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

### [v1.3.0] (2025-06-04) - 最新版本  

#### 核心改进

- **统一缓存架构**
- **缓存路径统一为项目根目录 .ai_cache**
- **本地和 CI 环境使用相同缓存策略**
- **增强 CI/CD 支持**，**支持 CI 仅缓存模式，大幅减少部署时间**
- **智能识别 15+ 部署平台（GitHub Actions、GitLab CI 等）**
- **可配置备用摘要机制**

### [v1.2.0] (2025-06-03)

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
- 🤖 **AI智能摘要功能**
- 📖 **阅读时间统计功能**
- 💾 **基础缓存系统**
- 🎯 **基本配置选项**

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

📝 *让MkDocs文档更加智能化*

**[⬆ 回到顶部](#mkdocs-ai-hooks)**

</div>