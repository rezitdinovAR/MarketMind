# Configuration & Serving

## 1. Общее описание

Модуль конфигурации управляет настройками приложения, секретами, и точками входа (CLI, Streamlit).

---

## 2. Configuration Layers

Приоритет (выше переопределяет ниже):

1. **Environment Variables** — `MARKETMIND_*`
2. **.env file** — локальная разработка
3. **config/settings.yaml** — defaults
4. **Hardcoded defaults** — в коде

---

## 3. Configuration Schema

### 3.1 settings.yaml

```yaml
app:
  name: "MarketMind"
  version: "0.1.0"
  debug: false
  log_level: "INFO"

llm:
  provider: "deepseek"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com"
  timeout: 30
  max_retries: 2
  max_calls_per_request: 10
  max_tokens_per_request: 50000
  max_cost_per_request: 0.10

search:
  sources:
    ozon:
      enabled: true
      use_mock: true
      timeout: 10
    wildberries:
      enabled: true
      use_mock: true
      timeout: 10
    yandex:
      enabled: true
      use_mock: true
      timeout: 10
  max_results_per_source: 20
  max_results_total: 10
  min_rating: 3.5

analysis:
  max_reviews_per_product: 15
  review_token_limit: 3000
  batch_size: 3

ui:
  type: "streamlit"  # or "cli"
  show_debug_info: false

paths:
  mock_data: "data/mock/"
  logs: "logs/"
  prompts: "prompts/"
```

### 3.2 Environment Variables
```Bash
# Required
DEEPSEEK_API_KEY=sk-...

# Optional overrides
MARKETMIND_DEBUG=true
MARKETMIND_LOG_LEVEL=DEBUG
MARKETMIND_LLM_MODEL=deepseek-chat
```

### 4. Secrets Management
Secret|Источник|Required
|---|---|---|
DEEPSEEK_API_KEY|env var|Yes

**Секреты никогда не пишутся в код или config файлы.**  
При старте приложения валидируется наличие обязательных секретов.
