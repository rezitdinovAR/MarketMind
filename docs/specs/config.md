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
  max_duration_seconds: 90
  stage_models:              # Per-stage LLM routing — если указано непустое значение,
    query_analysis: ""       # эта модель используется вместо дефолтной для данной стадии
    review_analysis: ""
    comparison: ""
    recommendation: ""

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

---

## 5. Per-stage Model Routing

Система поддерживает использование разных LLM-моделей для разных стадий пайплайна. Это позволяет оптимизировать баланс скорости, качества и стоимости.

### 5.1 Конфигурация

В `LLMConfig` встроена модель `StageModelConfig`, управляющая маршрутизацией:

```python
class StageModelConfig(BaseModel):
    """Per-stage LLM model routing."""
    query_analysis: str = ""
    review_analysis: str = ""
    comparison: str = ""
    recommendation: str = ""
```

| Поле | Стадия пайплайна | Описание |
|------|------------------|----------|
| query_analysis | QueryAnalyzer | Парсинг пользовательского запроса |
| review_analysis | ReviewAnalyzer | Суммаризация отзывов |
| comparison | Comparator | Сравнительный анализ товаров |
| recommendation | Recommender | Финальная рекомендация |

**Пустая строка** (`""`) означает использование модели по умолчанию из `llm.model`.

### 5.2 Пример конфигурации в settings.yaml

```yaml
llm:
  model: "deepseek-chat"         # модель по умолчанию
  stage_models:
    query_analysis: "deepseek-chat"       # быстрый парсинг
    review_analysis: ""                    # используется default
    comparison: "deepseek-reasoner"       # глубокий анализ
    recommendation: "deepseek-reasoner"   # сложное ранжирование
```

### 5.3 Механизм работы

1. **Резолвинг модели** — `LLMConfig.get_model_for_stage(stage)` возвращает модель для указанной стадии. Если для стадии задана пустая строка, возвращается `self.model` (default).

```python
def get_model_for_stage(self, stage: str) -> str:
    override = getattr(self.stage_models, stage, "")
    return override if override else self.model
```

2. **Передача в LLM** — `LLMClient.call()` и `LLMClient.call_json()` принимают параметр `model_override`. Если передан — используется он вместо default-модели. Каждый узел оркестратора вызывает `get_model_for_stage()` и передаёт результат как `model_override`.

### 5.4 Примеры использования

| Сценарий | query_analysis | review_analysis | comparison | recommendation |
|----------|---------------|-----------------|------------|----------------|
| Минимальная стоимость | deepseek-chat | deepseek-chat | deepseek-chat | deepseek-chat |
| Максимальное качество | deepseek-reasoner | deepseek-reasoner | deepseek-reasoner | deepseek-reasoner |
| Оптимальный баланс | deepseek-chat | deepseek-chat | deepseek-reasoner | deepseek-reasoner |
