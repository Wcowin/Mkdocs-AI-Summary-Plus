# 自定义 AI 服务配置指南

本指南介绍如何在 MkDocs AI Summary 插件中配置自定义 AI 服务商。

## 内置服务

插件已内置以下 AI 服务：

| 服务名 | 说明 | 环境变量 |
|--------|------|----------|
| `glm` | 智谱AI GLM-4 | `GLM_API_KEY` |
| `deepseek` | DeepSeek | `DEEPSEEK_API_KEY` |
| `openai` | OpenAI | `OPENAI_API_KEY` |
| `gemini` | Google Gemini | `GOOGLE_API_KEY` |
| `siliconflow` | 硅基流动 | `SILICONFLOW_API_KEY` |

## 硅基流动配置示例

### 1. 获取 API 密钥

访问 [硅基流动官网](https://siliconflow.cn/) 注册并获取 API 密钥。

### 2. 配置环境变量

在 `.env` 文件中添加：

```env
SILICONFLOW_API_KEY=sk-your-siliconflow-api-key
```

### 3. 在 mkdocs.yml 中配置

```yaml
plugins:
  - ai-summary:
      ai_service: "siliconflow"  # 使用硅基流动作为主服务
      fallback_services:
        - "glm"
        - "deepseek"
      summary_language: "zh"
      cache_enabled: true
```

## 自定义 AI 服务配置

### 配置格式

在 `mkdocs.yml` 中使用 `custom_services` 参数：

```yaml
plugins:
  - ai-summary:
      ai_service: "my_custom_service"  # 使用自定义服务
      custom_services:
        my_custom_service:
          url: "https://api.example.com/v1/chat/completions"
          model: "my-model-name"
          api_key_env: "MY_SERVICE_API_KEY"  # 环境变量名
          type: "openai_compatible"  # 服务类型
```

### 配置参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `url` | ✅ | API 端点地址 | - |
| `model` | ✅ | 模型名称 | - |
| `api_key_env` | ❌ | API 密钥的环境变量名 | `{服务名大写}_API_KEY` |
| `type` | ❌ | 服务类型 | `openai_compatible` |
| `headers` | ❌ | 自定义请求头 | - |

### 服务类型

目前支持两种服务类型：

1. **`openai_compatible`** - OpenAI 兼容 API（默认）
   - 适用于大多数遵循 OpenAI API 格式的服务
   - 包括：DeepSeek、GLM、硅基流动等

2. **`gemini`** - Google Gemini API
   - 专门用于 Google Gemini 服务

## 完整配置示例

### 示例 1：使用多个自定义服务

```yaml
plugins:
  - ai-summary:
      ai_service: "my_service_1"
      fallback_services:
        - "my_service_2"
        - "siliconflow"
        - "glm"
      
      custom_services:
        # 自定义服务 1
        my_service_1:
          url: "https://api.provider1.com/v1/chat/completions"
          model: "provider1-model"
          api_key_env: "PROVIDER1_API_KEY"
          type: "openai_compatible"
        
        # 自定义服务 2
        my_service_2:
          url: "https://api.provider2.com/v1/chat/completions"
          model: "provider2-model"
          api_key_env: "PROVIDER2_API_KEY"
          type: "openai_compatible"
      
      summary_language: "zh"
      cache_enabled: true
```

对应的 `.env` 文件：

```env
PROVIDER1_API_KEY=your-provider1-api-key
PROVIDER2_API_KEY=your-provider2-api-key
SILICONFLOW_API_KEY=your-siliconflow-api-key
GLM_API_KEY=your-glm-api-key
```

### 示例 2：使用自定义请求头

某些 API 可能需要特殊的请求头：

```yaml
plugins:
  - ai-summary:
      ai_service: "special_service"
      
      custom_services:
        special_service:
          url: "https://api.special.com/v1/chat/completions"
          model: "special-model"
          api_key_env: "SPECIAL_API_KEY"
          type: "openai_compatible"
          headers:
            X-Custom-Header: "custom-value"
            X-API-Version: "2024-01"
```

### 示例 3：混合使用内置和自定义服务

```yaml
plugins:
  - ai-summary:
      ai_service: "siliconflow"  # 主服务：硅基流动（内置）
      fallback_services:
        - "my_backup"  # 备用服务 1：自定义
        - "glm"        # 备用服务 2：GLM（内置）
        - "deepseek"   # 备用服务 3：DeepSeek（内置）
      
      custom_services:
        my_backup:
          url: "https://api.mybackup.com/v1/chat/completions"
          model: "backup-model"
          api_key_env: "BACKUP_API_KEY"
```

## 常见 AI 服务配置

### 1. 硅基流动（SiliconFlow）

```yaml
plugins:
  - ai-summary:
      ai_service: "siliconflow"
      # 可选：指定其他模型
      custom_services:
        siliconflow_custom:
          url: "https://api.siliconflow.cn/v1/chat/completions"
          model: "Qwen/Qwen2.5-7B-Instruct"  # 使用其他模型
          api_key_env: "SILICONFLOW_API_KEY"
```

### 2. 阿里云百炼

```yaml
plugins:
  - ai-summary:
      ai_service: "aliyun_bailian"
      
      custom_services:
        aliyun_bailian:
          url: "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
          model: "qwen-turbo"
          api_key_env: "DASHSCOPE_API_KEY"
          type: "openai_compatible"
```

### 3. 月之暗面（Moonshot）

```yaml
plugins:
  - ai-summary:
      ai_service: "moonshot"
      
      custom_services:
        moonshot:
          url: "https://api.moonshot.cn/v1/chat/completions"
          model: "moonshot-v1-8k"
          api_key_env: "MOONSHOT_API_KEY"
          type: "openai_compatible"
```

### 4. 零一万物（01.AI）

```yaml
plugins:
  - ai-summary:
      ai_service: "yi"
      
      custom_services:
        yi:
          url: "https://api.lingyiwanwu.com/v1/chat/completions"
          model: "yi-large"
          api_key_env: "YI_API_KEY"
          type: "openai_compatible"
```

### 5. 讯飞星火

```yaml
plugins:
  - ai-summary:
      ai_service: "spark"
      
      custom_services:
        spark:
          url: "https://spark-api.xf-yun.com/v1/chat/completions"
          model: "spark-3.5"
          api_key_env: "SPARK_API_KEY"
          type: "openai_compatible"
```

## 调试自定义服务

启用调试模式查看详细信息：

```yaml
plugins:
  - ai-summary:
      ai_service: "my_service"
      debug: true  # 启用调试模式
      
      custom_services:
        my_service:
          url: "https://api.example.com/v1/chat/completions"
          model: "my-model"
          api_key_env: "MY_API_KEY"
```

运行构建时会显示：

```
🔍 API密钥状态检查:
   ✅ my_service: sk-abc...xyz
   ❌ glm: 未配置
   ❌ deepseek: 未配置
📊 可用AI服务: my_service
```

## 故障排除

### 1. API 密钥未找到

**错误信息：**
```
⚠️ my_service 不可用: 缺少API密钥
```

**解决方法：**
- 检查 `.env` 文件中是否配置了对应的环境变量
- 确认环境变量名与 `api_key_env` 配置一致

### 2. API 调用失败

**错误信息：**
```
⚠️ my_service 失败: Connection error...
```

**解决方法：**
- 检查 API 端点 URL 是否正确
- 验证 API 密钥是否有效
- 确认网络连接正常
- 检查模型名称是否正确

### 3. 响应格式不兼容

如果自定义服务的响应格式与 OpenAI 不完全兼容，可能需要：

1. 确认服务是否真的兼容 OpenAI API 格式
2. 联系服务提供商获取正确的 API 文档
3. 如果格式差异较大，可能需要在插件中添加专门的适配器

## 最佳实践

1. **优先使用内置服务**：内置服务已经过测试，稳定性更好
2. **配置多个备用服务**：确保至少有 2-3 个备用服务
3. **启用缓存**：减少 API 调用次数，降低成本
4. **使用环境变量**：不要在配置文件中直接写入 API 密钥
5. **测试自定义服务**：在本地充分测试后再部署到 CI/CD

## 贡献新的内置服务

如果你配置了一个常用的 AI 服务，欢迎提交 PR 将其添加为内置服务！

提交 PR 时请包含：
- 服务配置代码
- 使用文档
- 测试用例

---

如有问题，请在 [GitHub Issues](https://github.com/Wcowin/Mkdocs-AI-Summary-Plus/issues) 中反馈。
