# 🛒 MarketMind — AI-агент для умного подбора товаров на маркетплейсах

## Проблема

Онлайн-покупатель сталкивается с **информационной перегрузкой**:

- На одном маркетплейсе десятки вариантов одного и того же товара с разбросом цен в 2–5×.
- Отзывы противоречивы, часть из них — накрученные; читать сотни отзывов вручную нереально.
- Один и тот же товар может продаваться на Ozon, Wildberries, Яндекс Маркете — и цена, условия доставки, рейтинг продавца отличаются.
- Итог: человек либо тратит часы на ресёрч, либо покупает «наугад» и жалеет.

**Для кого:** для любого онлайн-покупателя, который хочет принять обоснованное решение о покупке, не тратя на это весь вечер.

## Что делает PoC (демо)

На демо будет показан end-to-end сценарий:

1. Пользователь вводит **текстовый запрос** на естественном языке, например:
   _«Хочу беспроводные наушники с шумоподавлением до 15 000 ₽ для бега»_
2. Агентная система:
   - **Парсит и уточняет** запрос (категория, бюджет, ключевые критерии).
   - **Собирает варианты** с 2–3 маркетплейсов (mock-данные или реальный парсинг).
   - **Анализирует отзывы** — суммаризирует плюсы/минусы каждого варианта.
   - **Сравнивает** варианты по цене, рейтингу, надёжности продавца.
   - **Выдаёт рекомендацию** — топ-3 варианта с объяснением, почему именно они.
3. Результат отображается в **CLI / простом web-интерфейсе (Streamlit)**.

## Что НЕ делает PoC (out-of-scope)

| Явно вне скоупа | Почему |
|---|---|
| Автоматическая покупка / оформление заказа | Требует OAuth-интеграций, платёжных данных, юридических аспектов |
| Поддержка всех маркетплейсов мира | PoC ограничен 2–3 российскими площадками |
| Мобильное приложение | PoC — CLI / Streamlit |
| Трекинг цен и уведомления | Нет персистентного хранилища и фоновых задач в PoC |
| Real-time обновление цен | Данные могут быть кэшированы / mock |
| Мультиязычность | Только русский язык |
| Персонализация на основе истории покупок | Нет пользовательских профилей |
| Гарантия юридической корректности сравнения цен | Проект — учебный pet-project |

## Tech Stack

- **LLM:** DeepSeek API (deepseek-chat / deepseek-reasoner)
- **Agent Framework:** LangGraph
- **Language:** Python 3.11+
- **UI (PoC):** Streamlit / CLI
- **Data sources:** mock JSON + опционально HTTP-парсинг открытых страниц

## Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
git clone https://github.com/<your-username>/MarketMind.git
cd MarketMind
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Настройка API-ключа

Создайте файл `.env` в корне проекта:

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Запуск

**CLI-режим:**

```bash
python app_cli.py
```

**Streamlit (веб-интерфейс):**

```bash
streamlit run app_streamlit.py
```

После запуска откроется браузер на `http://localhost:8501`.

### 4. Конфигурация

Основные настройки — в `config/settings.yaml`. По умолчанию используются mock-данные (`use_mock: true`), API-ключ не нужен для поиска товаров, только для LLM-анализа.

## Mock-данные: категории и товары

В проекте ~107 товаров на каждый из 3 маркетплейсов (Ozon, Wildberries, Яндекс Маркет) — 21 категория. Одни и те же модели представлены на разных площадках с разными ценами и продавцами.

### Примеры запросов для тестирования

| Запрос | Что проверяет |
|---|---|
| «Беспроводные наушники с шумоподавлением до 15 000» | Фильтрация по цене и атрибутам, 10 моделей в категории |
| «Ноутбук для учёбы до 60 000» | Сравнение 8 моделей, кросс-маркетплейс цены |
| «Робот-пылесос с влажной уборкой» | Анализ атрибутов (тип, функции), 6 моделей |
| «Смартфон с хорошей камерой до 40 000» | Работа с характеристиками камеры, 8 моделей |
| «Игровая мышь для шутеров» | Новая категория, 3 модели, сравнение сенсоров |
| «Портативная колонка для пляжа» | Фильтрация по водозащите IP67, 6 моделей |
| «Проектор для домашнего кинотеатра» | Сравнение технологий (DLP, лазер), 3 модели |
| «Повербанк для ноутбука» | Фильтрация по мощности USB-C PD, 3 модели |

### Полный список категорий

| Категория | Кол-во | Примеры товаров |
|---|---|---|
| Наушники | 9–10 | Sony WH-1000XM5, AirPods Pro 2, JBL Tune 770NC, Sennheiser Momentum 4, Marshall Major IV |
| Ноутбуки | 7–8 | ASUS Vivobook 15, Lenovo IdeaPad 3, MacBook Air M2, HP Pavilion 15, Acer Aspire 5 |
| Смартфоны | 8 | Samsung Galaxy S24, iPhone 15, Xiaomi Redmi Note 13 Pro, Google Pixel 8, POCO X6 Pro |
| Пылесосы | 6 | Roborock S8 Pro Ultra, Dyson V15 Detect, Dreame L10s Pro, Ecovacs Deebot T30 |
| Телевизоры | 6–7 | Samsung QLED Q80C, LG OLED C3, LG OLED C4, Sony Bravia A80L, Haier S4 |
| Планшеты | 6 | iPad Air M2, Samsung Galaxy Tab S9 FE, Xiaomi Pad 6, OnePlus Pad 2 |
| Умные часы | 6 | Apple Watch Series 9, Samsung Galaxy Watch 6, Huawei Watch GT 4, Garmin Forerunner 265 |
| Кофемашины | 6–7 | De'Longhi Magnifica S, Philips LatteGo, Saeco Xelsis, Nespresso Vertuo Next |
| Портативные колонки | 6 | JBL Charge 5, JBL Flip 6, Яндекс Станция 2, Marshall Stanmore III, Harman Kardon Aura Studio 4 |
| Электросамокаты | 5 | Ninebot MAX G2, Xiaomi Scooter 4 Pro, Xiaomi Scooter 4, Kugoo Kirin S1 Pro |
| Экшн-камеры | 4 | GoPro HERO12, DJI Osmo Action 4, DJI Action 2, Insta360 X4 |
| Фитнес-браслеты | 4 | Xiaomi Band 8, Huawei Band 9, Samsung Galaxy Fit3, Honor Band 7 |
| Клавиатуры | 4 | Logitech MX Keys S, Keychron K8 Pro, Razer BlackWidow V4, HyperX Alloy Origins 65 |
| Электрические зубные щётки | 4 | Oral-B iO 9, Philips Sonicare DC9000, Xiaomi T700, Soocas X3U |
| Мониторы | 5 | Samsung Odyssey G5, LG UltraFine 4K, Dell UltraSharp U2723QE, Xiaomi G27i |
| Принтеры | 3 | HP LaserJet Pro M404dn, Canon PIXMA G3430, Epson EcoTank L3250 |
| Внешние аккумуляторы | 3 | Xiaomi Power Bank 10000, Anker PowerCore 25600, Baseus Adaman2 20000 |
| Маршрутизаторы | 3 | Keenetic Giga, TP-Link Archer AX73, ASUS RT-AX86U Pro |
| Игровые мыши | 3 | Logitech G Pro X Superlight 2, Razer DeathAdder V3, SteelSeries Aerox 5 |
| Видеорегистраторы | 3 | 70mai A810 4K, Xiaomi Dash Cam 2, VIOFO A229 Pro Duo |
| Проекторы | 3 | XGIMI Halo+, Xiaomi Laser Cinema 2, BenQ TH685P |
