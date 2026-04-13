"""
Script to generate additional mock data for MarketMind.
Adds ~21 new products per marketplace (ozon, wb, yandex) across 8 categories.
Some products overlap across marketplaces for cross-marketplace grouping testing.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "data" / "mock"


# ═══════════════════════════════════════════════════════════════
# NEW PRODUCTS DATA
# ═══════════════════════════════════════════════════════════════

# --- НАУШНИКИ ---

BOSE_QC_ULTRA = {
    "name": "Bose QuietComfort Ultra Headphones",
    "attributes": {"Тип": "полноразмерные", "Подключение": "Bluetooth 5.3", "Шумоподавление": "активное", "Время работы": "24 ч", "Вес": "250 г", "Пространственное аудио": "Immersive Audio"},
}

MARSHALL_MAJOR_IV = {
    "name": "Marshall Major IV Bluetooth",
    "attributes": {"Тип": "накладные", "Подключение": "Bluetooth 5.0", "Шумоподавление": "нет", "Время работы": "80 ч", "Вес": "165 г", "Зарядка": "беспроводная Qi"},
}

BEATS_SOLO_4 = {
    "name": "Beats Solo 4 Wireless",
    "attributes": {"Тип": "накладные", "Подключение": "Bluetooth 5.3", "Шумоподавление": "нет", "Время работы": "50 ч", "Вес": "217 г", "Пространственное аудио": "Dolby Atmos"},
}

# --- НОУТБУКИ ---

HP_PAVILION_15 = {
    "name": "HP Pavilion 15 (i5-1335U, 16GB, 512GB SSD)",
    "attributes": {"Процессор": "Intel Core i5-1335U", "ОЗУ": "16 ГБ", "SSD": "512 ГБ", "Экран": "15.6\" FHD IPS", "ОС": "Windows 11 Home"},
}

ACER_ASPIRE_5 = {
    "name": "Acer Aspire 5 A515 (Ryzen 5 7520U, 8GB, 256GB)",
    "attributes": {"Процессор": "AMD Ryzen 5 7520U", "ОЗУ": "8 ГБ", "SSD": "256 ГБ", "Экран": "15.6\" FHD IPS", "ОС": "Без ОС"},
}

MSI_THIN_15 = {
    "name": "MSI Thin 15 B12UC (i5-12450H, RTX 3050, 16GB)",
    "attributes": {"Процессор": "Intel Core i5-12450H", "ОЗУ": "16 ГБ", "SSD": "512 ГБ", "Видеокарта": "NVIDIA RTX 3050 4GB", "Экран": "15.6\" FHD IPS 144Hz"},
}

# --- СМАРТФОНЫ ---

IPHONE_15 = {
    "name": "Apple iPhone 15 128GB",
    "attributes": {"Экран": "6.1\" Super Retina XDR OLED", "Процессор": "Apple A16 Bionic", "ОЗУ": "6 ГБ", "Камера": "48 МП + 12 МП", "Батарея": "3877 мАч"},
}

POCO_X6_PRO = {
    "name": "POCO X6 Pro 5G 256GB",
    "attributes": {"Экран": "6.67\" AMOLED 120Hz", "Процессор": "MediaTek Dimensity 8300 Ultra", "ОЗУ": "8 ГБ", "Камера": "64 МП", "Батарея": "5000 мАч"},
}

NOTHING_PHONE_2 = {
    "name": "Nothing Phone (2) 256GB",
    "attributes": {"Экран": "6.7\" OLED LTPO 120Hz", "Процессор": "Snapdragon 8+ Gen 1", "ОЗУ": "12 ГБ", "Камера": "50 МП + 50 МП", "Батарея": "4700 мАч"},
}

# --- ПЫЛЕСОСЫ ---

DYSON_V15 = {
    "name": "Dyson V15 Detect Absolute Беспроводной",
    "attributes": {"Тип": "вертикальный беспроводной", "Мощность всасывания": "230 AW", "Время работы": "60 мин", "Лазерный датчик": "да", "Дисплей": "LCD"},
}

ECOVACS_T30 = {
    "name": "Ecovacs Deebot T30 Omni Робот-пылесос",
    "attributes": {"Тип": "робот-пылесос", "Влажная уборка": "да, поднимаемая швабра", "Мощность": "11000 Па", "Навигация": "LiDAR + камера", "Время работы": "200 мин"},
}

SAMSUNG_JET_BOT = {
    "name": "Samsung Jet Bot AI+ VR50T95735W Робот-пылесос",
    "attributes": {"Тип": "робот-пылесос", "Влажная уборка": "нет", "Мощность": "5000 Па", "Навигация": "LiDAR + камера AI", "Самоочистка": "Clean Station"},
}

# --- ТЕЛЕВИЗОРЫ ---

SONY_A80L = {
    "name": "Sony Bravia XR 55A80L OLED 55\"",
    "attributes": {"Диагональ": "55\"", "Разрешение": "4K UHD", "Тип матрицы": "OLED", "Smart TV": "Google TV", "Частота обновления": "120 Гц", "Звук": "Acoustic Surface Audio+"},
}

HAIER_S4 = {
    "name": "Haier 55 Smart TV S4 55\"",
    "attributes": {"Диагональ": "55\"", "Разрешение": "4K UHD", "Тип матрицы": "LED", "Smart TV": "Android TV", "Частота обновления": "60 Гц"},
}

PHILIPS_PUS8808 = {
    "name": "Philips 55PUS8808 Ambilight 55\"",
    "attributes": {"Диагональ": "55\"", "Разрешение": "4K UHD", "Тип матрицы": "LED", "Smart TV": "Google TV", "Частота обновления": "120 Гц", "Ambilight": "3-сторонний"},
}

# --- ПЛАНШЕТЫ ---

ONEPLUS_PAD_2 = {
    "name": "OnePlus Pad 2 128GB",
    "attributes": {"Процессор": "Snapdragon 8 Gen 3", "Экран": "12.1\" 3K IPS 144Hz", "Память": "128 ГБ", "ОЗУ": "8 ГБ", "ОС": "OxygenOS (Android 14)"},
}

IPAD_10 = {
    "name": "Apple iPad 10 поколения 64GB",
    "attributes": {"Процессор": "Apple A14 Bionic", "Экран": "10.9\" Liquid Retina IPS", "Память": "64 ГБ", "ОС": "iPadOS", "Разъём": "USB-C"},
}

REALME_PAD_2 = {
    "name": "Realme Pad 2 128GB",
    "attributes": {"Процессор": "MediaTek Helio G99", "Экран": "11.5\" IPS 120Hz", "Память": "128 ГБ", "ОЗУ": "6 ГБ", "ОС": "Android 13"},
}

# --- УМНЫЕ ЧАСЫ ---

XIAOMI_WATCH_2_PRO = {
    "name": "Xiaomi Watch 2 Pro",
    "attributes": {"Экран": "1.43\" AMOLED", "ОС": "Wear OS (Google)", "Батарея": "495 мАч", "Водозащита": "5 ATM", "Датчики": "пульс, SpO2, GPS, NFC"},
}

TICWATCH_PRO_5 = {
    "name": "TicWatch Pro 5 Enduro",
    "attributes": {"Экран": "1.43\" AMOLED + LCD", "ОС": "Wear OS 3.5", "Батарея": "628 мАч", "Водозащита": "5 ATM", "Датчики": "пульс, SpO2, компас, барометр"},
}

GARMIN_FORERUNNER_265 = {
    "name": "Garmin Forerunner 265",
    "attributes": {"Экран": "1.3\" AMOLED", "Батарея": "до 13 дней", "Водозащита": "5 ATM", "ОС": "Garmin OS", "Датчики": "GPS двухдиапазонный, пульс, SpO2"},
}

# --- КОФЕМАШИНЫ ---

SAECO_XELSIS = {
    "name": "Saeco Xelsis Suprema SM8889",
    "attributes": {"Тип": "автоматическая", "Давление": "15 бар", "Капучинатор": "автоматический LatteDuo", "Рецепты": "22 напитка", "Дисплей": "TFT сенсорный"},
}

MELITTA_BARISTA = {
    "name": "Melitta Barista TS Smart F860-100",
    "attributes": {"Тип": "автоматическая", "Давление": "15 бар", "Капучинатор": "автоматический", "Рецепты": "21 напиток", "Управление": "Bluetooth + приложение"},
}

NESPRESSO_VERTUO = {
    "name": "Nespresso Vertuo Next ENV120",
    "attributes": {"Тип": "капсульная", "Давление": "19 бар", "Технология": "Centrifusion", "Капсулы": "Vertuo (5 размеров)", "Время нагрева": "30 сек"},
}


# ═══════════════════════════════════════════════════════════════
# OZON NEW PRODUCTS
# ═══════════════════════════════════════════════════════════════

OZON_NEW = {
    "наушники": [
        {
            "id": "ozon_h004",
            **BOSE_QC_ULTRA,
            "price": 33990,
            "original_price": 39990,
            "rating": 4.8,
            "review_count": 670,
            "url": "https://ozon.ru/product/bose-qc-ultra-004",
            "image_url": "https://cdn.ozon.ru/img/bose-qc-ultra.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_bose",
            "seller_name": "Bose Official",
            "reviews": [
                {"id": "r200", "text": "Шумоподавление на уровне Sony XM5, но звук мне нравится больше — более натуральный и объёмный. Immersive Audio — реально крутая штука, эффект окружения впечатляет. Минус — батарея 24 часа, это меньше чем у Sony.", "rating": 5, "date": "2025-03-11", "verified_purchase": True, "helpful_count": 52},
                {"id": "r201", "text": "Перешёл с Bose QC45. Разница в звуке огромная, шумоподавление тоже улучшили. Пространственное аудио работает без привязки к Apple — большой плюс. Цена кусается, но качество того стоит.", "rating": 5, "date": "2025-02-24", "verified_purchase": True, "helpful_count": 34},
                {"id": "r202", "text": "Звук отличный, шумодав топовый. Но давят на уши через 2 часа — подушки жёстче чем у предыдущей модели. Для коротких сессий — идеальны, для длительного ношения — не уверен.", "rating": 4, "date": "2025-02-05", "verified_purchase": True, "helpful_count": 28},
                {"id": "r203", "text": "Сравнивал с Sony XM5 в магазине. Bose звучат теплее и натуральнее, Sony — детальнее и аналитичнее. Шумоподавление примерно одинаковое. Взял Bose — не жалею.", "rating": 5, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 41}
            ]
        },
        {
            "id": "ozon_h005",
            **MARSHALL_MAJOR_IV,
            "price": 7990,
            "original_price": 9990,
            "rating": 4.5,
            "review_count": 2100,
            "url": "https://ozon.ru/product/marshall-major-iv-005",
            "image_url": "https://cdn.ozon.ru/img/marshall-major4.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_marshall",
            "seller_name": "Marshall Official",
            "reviews": [
                {"id": "r204", "text": "80 часов батареи — это не шутка, заряжаю раз в 2-3 недели! Звук типичный Marshall — рок и метал звучат шикарно. Нет шумоподавления, но для улицы мне и не нужно. Беспроводная зарядка — приятный бонус.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 38},
                {"id": "r205", "text": "Стильные наушники с отличным звуком. Басы мощные, середина чёткая. Нет ANC — для метро не лучший вариант. Но для дома и офиса — идеально. Лёгкие, не давят.", "rating": 4, "date": "2025-02-19", "verified_purchase": True, "helpful_count": 22},
                {"id": "r206", "text": "Купил ради дизайна, остался ради звука. Marshall знают толк в музыке. Складная конструкция — удобно носить в сумке. Минус — нет шумоподавления и мультипоинта.", "rating": 4, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 15}
            ]
        },
        {
            "id": "ozon_h006",
            **BEATS_SOLO_4,
            "price": 18990,
            "original_price": 22990,
            "rating": 4.4,
            "review_count": 560,
            "url": "https://ozon.ru/product/beats-solo4-006",
            "image_url": "https://cdn.ozon.ru/img/beats-solo4.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_beats",
            "seller_name": "Beats by Dre Official",
            "reviews": [
                {"id": "r207", "text": "Beats наконец-то научились делать качественный звук! Solo 4 звучат сбалансированно, басы не задавливают остальное. Работают и с iPhone и с Android одинаково хорошо. Пространственное аудио с Dolby Atmos — бомба.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 33},
                {"id": "r208", "text": "50 часов батареи — заряжаю раз в неделю. Звук стал намного лучше по сравнению с Solo 3. Нет шумоподавления — жаль, за такую цену хотелось бы. Но для Apple-экосистемы — отличный выбор.", "rating": 4, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 19},
                {"id": "r209", "text": "Лёгкие и удобные, можно носить часами. Звук приятный, басы глубокие но не гудящие. UBS-C наконец-то! Складываются компактно. Для повседневного использования — рекомендую.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 12}
            ]
        }
    ],
    "ноутбуки": [
        {
            "id": "ozon_n003",
            **HP_PAVILION_15,
            "price": 57990,
            "original_price": 64990,
            "rating": 4.4,
            "review_count": 890,
            "url": "https://ozon.ru/product/hp-pavilion-15-003",
            "in_stock": True,
            "seller_id": "ozon_seller_hp",
            "seller_name": "HP Official Store",
            "reviews": [
                {"id": "r210", "text": "Хороший рабочий ноут. Windows 11 предустановлена — не нужно возиться с установкой. Экран IPS нормальный, не самый яркий. Клавиатура удобная, с цифровым блоком. Для офисной работы — отлично.", "rating": 4, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 25},
                {"id": "r211", "text": "За 58к — неплохой вариант с Windows. 16 ГБ ОЗУ хватает для всего. SSD быстрый. Минус — пластиковый корпус, выглядит не премиально. Но работает стабильно.", "rating": 4, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 16},
                {"id": "r212", "text": "Купил жене для работы с документами и Excel. Справляется отлично. Батарея 5-6 часов — могла бы быть лучше. Не шумит, не греется при обычной нагрузке. Рекомендую для офиса.", "rating": 4, "date": "2025-01-30", "verified_purchase": True, "helpful_count": 11}
            ]
        },
        {
            "id": "ozon_n004",
            **ACER_ASPIRE_5,
            "price": 33990,
            "original_price": 39990,
            "rating": 4.2,
            "review_count": 1230,
            "url": "https://ozon.ru/product/acer-aspire5-004",
            "in_stock": True,
            "seller_id": "ozon_seller_acer",
            "seller_name": "Acer Official",
            "reviews": [
                {"id": "r213", "text": "Бюджетный ноут для учёбы. 8 ГБ ОЗУ — минимум, Chrome с 10 вкладками уже тормозит. SSD 256 ГБ — мало, но можно докупить. За 34к — адекватный выбор для студента.", "rating": 4, "date": "2025-03-02", "verified_purchase": True, "helpful_count": 28},
                {"id": "r214", "text": "Простой рабочий ноут без излишеств. Ryzen 5 тянет все офисные задачи. Экран средний, но для работы хватает. ОС нет — ставил Ubuntu, работает отлично.", "rating": 4, "date": "2025-02-10", "verified_purchase": True, "helpful_count": 14},
                {"id": "r215", "text": "За свои деньги — нормально. Не флагман, но и не стоит как флагман. Для браузера, документов и видео — хватает. Батарея 4-5 часов.", "rating": 3, "date": "2025-01-15", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "ozon_n005",
            **MSI_THIN_15,
            "price": 64990,
            "original_price": 74990,
            "rating": 4.5,
            "review_count": 456,
            "url": "https://ozon.ru/product/msi-thin-15-005",
            "in_stock": True,
            "seller_id": "ozon_seller_msi",
            "seller_name": "MSI Official Store",
            "reviews": [
                {"id": "r216", "text": "Наконец-то бюджетный игровой ноут! RTX 3050 тянет большинство игр на средних-высоких настройках. Экран 144 Гц — плавно. Шумит при нагрузке, но это все игровые ноуты так.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 44},
                {"id": "r217", "text": "Для учёбы + игры по вечерам — идеальный вариант. CS2 на высоких 80-100 fps. Батарея при играх — 1.5 часа, при работе — 4-5. Тонкий для игрового ноута.", "rating": 4, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 31},
                {"id": "r218", "text": "RTX 3050 уже не топ, но для 1080p хватает. Корпус пластиковый, но крепкий. Клавиатура с подсветкой. Для своей цены — отличный игровой ноут начального уровня.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 18}
            ]
        }
    ],
    "смартфоны": [
        {
            "id": "ozon_s003",
            **IPHONE_15,
            "price": 79990,
            "original_price": 89990,
            "rating": 4.8,
            "review_count": 3450,
            "url": "https://ozon.ru/product/iphone-15-003",
            "in_stock": True,
            "seller_id": "ozon_seller_apple",
            "seller_name": "Apple Store",
            "reviews": [
                {"id": "r219", "text": "Перешёл с iPhone 13. Камера 48 МП — разница заметна, особенно при зуме. Dynamic Island удобный, привык за день. USB-C наконец-то! Батарея на день хватает при активном использовании.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 78},
                {"id": "r220", "text": "Лучший iPhone для большинства людей. Не Pro, но камера и так отличная. Экран яркий, Face ID быстрый. Минус — 128 ГБ базовой памяти маловато в 2025 году.", "rating": 4, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 45},
                {"id": "r221", "text": "Жена перешла с Android — в восторге. iOS интуитивно понятная, всё работает плавно. AirDrop, iMessage — экосистема Apple затягивает. Камера снимает великолепно.", "rating": 5, "date": "2025-02-05", "verified_purchase": True, "helpful_count": 33},
                {"id": "r222", "text": "Пользуюсь 4 месяца. Стабильный, быстрый, камера топ. Единственное — стекло бьётся при первом падении, сразу чехол и стекло покупайте. В остальном претензий нет.", "rating": 4, "date": "2025-01-14", "verified_purchase": True, "helpful_count": 21}
            ]
        },
        {
            "id": "ozon_s004",
            **POCO_X6_PRO,
            "price": 27990,
            "original_price": 32990,
            "rating": 4.4,
            "review_count": 1890,
            "url": "https://ozon.ru/product/poco-x6-pro-004",
            "in_stock": True,
            "seller_id": "ozon_seller_poco",
            "seller_name": "POCO Official",
            "reviews": [
                {"id": "r223", "text": "Убийца флагманов! Dimensity 8300 Ultra — мощный чип, Genshin на максималках идёт. Экран AMOLED 120 Гц яркий и красивый. За 28к — лучшее что есть на рынке.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 55},
                {"id": "r224", "text": "Телефон для тех, кто хочет флагманскую производительность за полцены. Камера 64 МП — нормально, но не уровень Samsung или Apple. Зарядка 67W — за 45 минут 100%.", "rating": 4, "date": "2025-02-15", "verified_purchase": True, "helpful_count": 32},
                {"id": "r225", "text": "MIUI на POCO всё ещё с рекламой, но отключается. Производительность топ, батарея на 1.5 дня. NFC работает. За свои деньги — конкурентов нет.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 24}
            ]
        },
        {
            "id": "ozon_s005",
            **NOTHING_PHONE_2,
            "price": 39990,
            "original_price": 49990,
            "rating": 4.5,
            "review_count": 780,
            "url": "https://ozon.ru/product/nothing-phone2-005",
            "in_stock": True,
            "seller_id": "ozon_seller_nothing",
            "seller_name": "Nothing Store",
            "reviews": [
                {"id": "r226", "text": "Glyph-подсветка — не просто понты, реально удобно: разные паттерны для разных контактов, не доставая телефон знаешь кто звонит. Snapdragon 8+ Gen 1 — быстрый, не греется. Экран OLED шикарный.", "rating": 5, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 42},
                {"id": "r227", "text": "Чистый Android без мусора — Nothing OS минималистичная и быстрая. 12 ГБ ОЗУ — всё летает. Камера хорошая, но не флагманская. Дизайн уникальный, все спрашивают что за телефон.", "rating": 4, "date": "2025-02-17", "verified_purchase": True, "helpful_count": 29},
                {"id": "r228", "text": "Необычный телефон. Прозрачная задняя панель с подсветкой — выглядит футуристично. По производительности не уступает Samsung S23. Камера днём отлично, ночью — средне.", "rating": 4, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 17}
            ]
        }
    ],
    "пылесосы": [
        {
            "id": "ozon_v003",
            **DYSON_V15,
            "price": 54990,
            "original_price": 64990,
            "rating": 4.7,
            "review_count": 1120,
            "url": "https://ozon.ru/product/dyson-v15-detect-003",
            "in_stock": True,
            "seller_id": "ozon_seller_dyson",
            "seller_name": "Dyson Official",
            "reviews": [
                {"id": "r229", "text": "Лазерный луч подсвечивает пыль, которую не видишь глазом — гениальная фишка! Мощность всасывания бешеная, собирает всё. LCD дисплей показывает размер частиц — прикольно. Минус — тяжеловат для длительной уборки.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 67},
                {"id": "r230", "text": "Дорого, но Dyson стоит своих денег. После него обычный пылесос кажется игрушкой. 60 минут работы в эко-режиме хватает на квартиру 80м². В максимальном — минут 15. Зарядка 4.5 часа — долго.", "rating": 4, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 43},
                {"id": "r231", "text": "Третий Dyson в семье, каждый раз улучшение. V15 Detect — самый мощный. Лазер реально помогает видеть грязь. Фильтрация HEPA — для аллергиков это важно. Рекомендую.", "rating": 5, "date": "2025-01-30", "verified_purchase": True, "helpful_count": 29}
            ]
        },
        {
            "id": "ozon_v004",
            **ECOVACS_T30,
            "price": 59990,
            "original_price": 69990,
            "rating": 4.6,
            "review_count": 340,
            "url": "https://ozon.ru/product/ecovacs-t30-004",
            "in_stock": True,
            "seller_id": "ozon_seller_ecovacs",
            "seller_name": "Ecovacs Official",
            "reviews": [
                {"id": "r232", "text": "11000 Па мощности — сосёт как промышленный! Ковры чистит идеально. Швабра поднимается когда заезжает на ковёр — умно. Самоочистка базы горячей водой — гигиенично.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 38},
                {"id": "r233", "text": "Конкурент Roborock S8 за меньшие деньги. Убирает отлично, моет хорошо. Навигация точная, обходит препятствия. Приложение Ecovacs удобное. Единственное — база громоздкая.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 25},
                {"id": "r234", "text": "Пользуюсь месяц — доволен. Убирает каждый день, квартира чистая. Влажная уборка лучше чем у предыдущих моделей. LiDAR строит карту точно. Хороший робот за свои деньги.", "rating": 5, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "ozon_v005",
            **SAMSUNG_JET_BOT,
            "price": 49990,
            "original_price": 59990,
            "rating": 4.3,
            "review_count": 560,
            "url": "https://ozon.ru/product/samsung-jet-bot-005",
            "in_stock": True,
            "seller_id": "ozon_seller_samsung",
            "seller_name": "Samsung Official",
            "reviews": [
                {"id": "r235", "text": "Samsung делает неплохие роботы-пылесосы. AI-камера распознаёт объекты — обходит провода и носки. Clean Station — удобно, мусор сам высасывается в мешок. Нет влажной уборки — минус.", "rating": 4, "date": "2025-03-03", "verified_purchase": True, "helpful_count": 31},
                {"id": "r236", "text": "Для сухой уборки — отлично. Мощность хорошая, ковры чистит. AI навигация работает — кота обходит, провода не наматывает. SmartThings интеграция — удобно управлять из одного приложения.", "rating": 4, "date": "2025-02-11", "verified_purchase": True, "helpful_count": 20},
                {"id": "r237", "text": "Дороговато для робота без влажной уборки. Конкуренты за эти деньги предлагают больше. Но качество Samsung, интеграция в экосистему — для фанатов бренда ок.", "rating": 3, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 35}
            ]
        }
    ],
    "телевизоры": [
        {
            "id": "ozon_t004",
            **SONY_A80L,
            "price": 99990,
            "original_price": 119990,
            "rating": 4.9,
            "review_count": 340,
            "url": "https://ozon.ru/product/sony-a80l-004",
            "image_url": "https://cdn.ozon.ru/img/sony-a80l.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_sony",
            "seller_name": "Sony Official Store",
            "reviews": [
                {"id": "r238", "text": "Acoustic Surface Audio+ — экран вибрирует и издаёт звук. Звучит как встроенный саундбар, это фантастика. Картинка OLED безупречна. Google TV с Chromecast — удобно. Лучший OLED на рынке.", "rating": 5, "date": "2025-03-11", "verified_purchase": True, "helpful_count": 58},
                {"id": "r239", "text": "Картинка лучше чем у LG C3 на мой взгляд — процессор XR делает магию с цветами. Звук из экрана — необычно и круто. Для PS5 — идеально, VRR и ALLM поддерживаются.", "rating": 5, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 39},
                {"id": "r240", "text": "Дорого, но Sony A80L — эталон. Кино смотреть одно удовольствие. Dolby Vision, Dolby Atmos, IMAX Enhanced — полный набор. Google TV быстрее чем webOS.", "rating": 5, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 27}
            ]
        },
        {
            "id": "ozon_t005",
            **HAIER_S4,
            "price": 27990,
            "original_price": 34990,
            "rating": 4.1,
            "review_count": 2340,
            "url": "https://ozon.ru/product/haier-s4-55-005",
            "image_url": "https://cdn.ozon.ru/img/haier-s4.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_haier",
            "seller_name": "Haier Official",
            "reviews": [
                {"id": "r241", "text": "За 28к — неплохой 4K телевизор. Android TV удобный, все приложения есть. Картинка нормальная для LED, не QLED конечно. Для кухни или спальни — самое то. Звук слабый, нужна колонка.", "rating": 4, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 32},
                {"id": "r242", "text": "Бюджетный телевизор с нормальной картинкой. Haier удивляют — за такие деньги качество приемлемое. Углы обзора средние, HDR базовый. Для ТВ-каналов и YouTube — хватает.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 18},
                {"id": "r243", "text": "Купил родителям. Простое меню, пульт удобный. Ютуб, Кинопоиск, Иви — всё работает. Картинка не вау, но за 28 тысяч грех жаловаться. Собран нормально.", "rating": 3, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 24}
            ]
        },
        {
            "id": "ozon_t006",
            **PHILIPS_PUS8808,
            "price": 52990,
            "original_price": 62990,
            "rating": 4.6,
            "review_count": 670,
            "url": "https://ozon.ru/product/philips-pus8808-006",
            "image_url": "https://cdn.ozon.ru/img/philips-8808.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_philips",
            "seller_name": "Philips Official",
            "reviews": [
                {"id": "r244", "text": "Ambilight — вот зачем покупают Philips! Подсветка стены за телевизором создаёт эффект погружения. Для кино вечером — магия. Картинка хорошая, 120 Гц для игр. Google TV удобная.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 47},
                {"id": "r245", "text": "Выбирал между Samsung Q80C и Philips 8808. Взял Philips из-за Ambilight — не пожалел. Картинка чуть уступает Samsung, но Ambilight компенсирует. Реально расслабляет глаза.", "rating": 4, "date": "2025-02-19", "verified_purchase": True, "helpful_count": 28},
                {"id": "r246", "text": "Хороший телевизор с уникальной фишкой. Ambilight реально впечатляет гостей. Картинка достойная, звук нормальный. Минус — Google TV иногда тормозит при обновлениях.", "rating": 4, "date": "2025-01-15", "verified_purchase": True, "helpful_count": 16}
            ]
        }
    ],
    "планшеты": [
        {
            "id": "ozon_p004",
            **ONEPLUS_PAD_2,
            "price": 39990,
            "original_price": 49990,
            "rating": 4.6,
            "review_count": 340,
            "url": "https://ozon.ru/product/oneplus-pad2-004",
            "image_url": "https://cdn.ozon.ru/img/oneplus-pad2.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_oneplus",
            "seller_name": "OnePlus Official",
            "reviews": [
                {"id": "r247", "text": "Snapdragon 8 Gen 3 в планшете — это зверь! Всё летает, игры на максималках. Экран 3K 144 Гц — невероятно плавный и чёткий. OxygenOS на планшете приятная. Лучший Android-планшет.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 45},
                {"id": "r248", "text": "Конкурент iPad Air по производительности, но дешевле. Экран огромный, 12.1 дюйма. Для работы с документами и рисования — отлично. Стилус покупается отдельно — минус.", "rating": 4, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 28},
                {"id": "r249", "text": "Купил для игр и фильмов. Динамики мощные, экран красивый. Батарея 9510 мАч — на 2 дня хватает. Зарядка 67W быстрая. Единственное — мало оптимизированных приложений.", "rating": 4, "date": "2025-01-30", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "ozon_p005",
            **IPAD_10,
            "price": 34990,
            "original_price": 39990,
            "rating": 4.5,
            "review_count": 2340,
            "url": "https://ozon.ru/product/ipad-10-gen-005",
            "image_url": "https://cdn.ozon.ru/img/ipad-10.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_apple",
            "seller_name": "Apple Store",
            "reviews": [
                {"id": "r250", "text": "Базовый iPad, но работает отлично. A14 Bionic хватает для всего — YouTube, Netflix, простые игры, рисование. USB-C — наконец-то! Экран хороший, не Pro, но для повседневных задач достаточно.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 34},
                {"id": "r251", "text": "Купил ребёнку. Для школы идеален — лёгкий, быстрый, батарея на весь день. Приложений в App Store море. Apple Pencil 1-го поколения поддерживается. Минус — 64 ГБ маловато.", "rating": 4, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 22},
                {"id": "r252", "text": "Для чтения, видео и интернета — лучший планшет за 35к. Экосистема Apple работает безупречно. Не нужен Pro или Air, если задачи простые. Рекомендую.", "rating": 5, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 16}
            ]
        }
    ],
    "умные часы": [
        {
            "id": "ozon_w004",
            **XIAOMI_WATCH_2_PRO,
            "price": 19990,
            "original_price": 24990,
            "rating": 4.4,
            "review_count": 890,
            "url": "https://ozon.ru/product/xiaomi-watch-2-pro-004",
            "image_url": "https://cdn.ozon.ru/img/xiaomi-watch2pro.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_xiaomi",
            "seller_name": "Xiaomi Official",
            "reviews": [
                {"id": "r253", "text": "Xiaomi на Wear OS — наконец-то нормальные смарт-часы! Google Maps, Google Pay (ну, в теории), Play Store. Экран AMOLED яркий. GPS точный. За 20к — лучшие часы на Wear OS после Samsung.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 41},
                {"id": "r254", "text": "Хорошие часы, но Wear OS жрёт батарею — 2 дня максимум. Если привыкли к Amazfit с 2 неделями — будет шок. Зато приложений много и интеграция с Android полная.", "rating": 4, "date": "2025-02-21", "verified_purchase": True, "helpful_count": 28},
                {"id": "r255", "text": "NFC есть, но Google Pay в России не работает. Для фитнеса — отлично, куча режимов тренировок. Сон мониторит точно. Wear OS 3.5 работает плавно на Snapdragon W5+ Gen 1.", "rating": 4, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "ozon_w005",
            **GARMIN_FORERUNNER_265,
            "price": 37990,
            "original_price": 44990,
            "rating": 4.7,
            "review_count": 340,
            "url": "https://ozon.ru/product/garmin-forerunner-265-005",
            "image_url": "https://cdn.ozon.ru/img/garmin-fr265.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_garmin",
            "seller_name": "Garmin Official",
            "reviews": [
                {"id": "r256", "text": "Идеальные часы для бегунов! AMOLED экран наконец-то в Forerunner — яркий, читабельный на солнце. Двухдиапазонный GPS — маршруты точные до метра. Тренировочные рекомендации реально помогают прогрессировать.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 52},
                {"id": "r257", "text": "Бегаю полумарафоны, Garmin 265 — мой помощник. Morning Report показывает готовность к тренировке. Training Status анализирует нагрузку. Батарея 13 дней в обычном режиме, 20 часов с GPS.", "rating": 5, "date": "2025-02-15", "verified_purchase": True, "helpful_count": 38},
                {"id": "r258", "text": "Для спортсменов — must have. Но для обычного пользователя функционал избыточный. Нет NFC оплаты, уведомления приходят но ответить нельзя. Если цель — спорт, то лучше нет.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 23}
            ]
        }
    ],
    "кофемашины": [
        {
            "id": "ozon_k004",
            **SAECO_XELSIS,
            "price": 119990,
            "original_price": 139990,
            "rating": 4.8,
            "review_count": 230,
            "url": "https://ozon.ru/product/saeco-xelsis-004",
            "image_url": "https://cdn.ozon.ru/img/saeco-xelsis.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_saeco",
            "seller_name": "Saeco (Philips) Official",
            "reviews": [
                {"id": "r259", "text": "22 напитка одной кнопкой — капучино, латте, флэт уайт, ристретто, всё! Сенсорный дисплей удобный. LatteDuo — два капучино одновременно, для пары идеально. Кофе великолепный, итальянское качество.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 44},
                {"id": "r260", "text": "Очень дорого, но это вершина домашних кофемашин. Каждый напиток можно настроить под себя — температура, крепость, объём молока. Профили пользователей — каждый член семьи настраивает под себя.", "rating": 5, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 31},
                {"id": "r261", "text": "Перешёл с De'Longhi Magnifica — небо и земля. Автоматический капучинатор делает идеальную пенку. Самоочистка работает. Дорого, но кофе как в лучших кофейнях.", "rating": 5, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 25}
            ]
        },
        {
            "id": "ozon_k005",
            **MELITTA_BARISTA,
            "price": 79990,
            "original_price": 94990,
            "rating": 4.6,
            "review_count": 450,
            "url": "https://ozon.ru/product/melitta-barista-ts-005",
            "image_url": "https://cdn.ozon.ru/img/melitta-barista.jpg",
            "in_stock": True,
            "seller_id": "ozon_seller_melitta",
            "seller_name": "Melitta Official",
            "reviews": [
                {"id": "r262", "text": "21 напиток через приложение — управляешь кофемашиной с дивана! Bluetooth-подключение стабильное. Кофе варит отлично, два контейнера для зёрен — можно разные сорта. Немецкое качество чувствуется.", "rating": 5, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 36},
                {"id": "r263", "text": "Автокапучинатор делает отличную пенку. Приложение Melitta Companion удобное — можно создавать свои рецепты. Два бункера для зёрен — утром бодрящий, вечером декаф.", "rating": 4, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 22},
                {"id": "r264", "text": "Дорогая, но качественная. Кофе вкуснее чем из Philips LatteGo. Молочная система моется легко. Единственное — шумная при помоле. В целом — отличная премиальная машина.", "rating": 4, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 17}
            ]
        }
    ]
}


# ═══════════════════════════════════════════════════════════════
# WILDBERRIES NEW PRODUCTS
# ═══════════════════════════════════════════════════════════════

WB_NEW = {
    "наушники": [
        {
            "id": "wb_h004",
            **BOSE_QC_ULTRA,
            "price": 32490,
            "original_price": 39990,
            "rating": 4.7,
            "review_count": 890,
            "url": "https://wildberries.ru/product/bose-qc-ultra-004",
            "in_stock": True,
            "seller_id": "wb_seller_bose",
            "seller_name": "Bose Store",
            "reviews": [
                {"id": "wr200", "text": "На WB нашёл дешевле чем в официальном магазине. Наушники топовые — шумоподавление на уровне Sony, звук даже лучше. Immersive Audio — реально окружает звуком. Доставка за день.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 48},
                {"id": "wr201", "text": "Сравнивал с Sony XM5 две недели. Bose звучат более натурально, Sony более аналитично. Шумодав примерно одинаковый. Выбрал Bose за пространственное аудио. Не пожалел.", "rating": 5, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 33},
                {"id": "wr202", "text": "Отличные наушники, но тяжеловаты. Через 2-3 часа хочется снять. Звук великолепный, шумодав мощный. Для перелётов — must have. Кейс в комплекте качественный.", "rating": 4, "date": "2025-02-01", "verified_purchase": True, "helpful_count": 21}
            ]
        },
        {
            "id": "wb_h005",
            **MARSHALL_MAJOR_IV,
            "price": 7490,
            "original_price": 9990,
            "rating": 4.6,
            "review_count": 2450,
            "url": "https://wildberries.ru/product/marshall-major-iv-005",
            "in_stock": True,
            "seller_id": "wb_seller_marshall",
            "seller_name": "Marshall Store",
            "reviews": [
                {"id": "wr203", "text": "Батарея 80 часов — заряжаю раз в месяц при ежедневном использовании по 2 часа! Звук Marshall — басистый, рок качает. Складные, компактные. Для тех, кому не нужен ANC — идеальные.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 42},
                {"id": "wr204", "text": "Стильные наушники в ретро-дизайне. Звук тёплый, приятный. Для рока, джаза, блюза — идеально. Для электронной музыки — не хватает деталей на верхах. Беспроводная зарядка — приятный бонус.", "rating": 4, "date": "2025-02-17", "verified_purchase": True, "helpful_count": 25},
                {"id": "wr205", "text": "Купил на WB со скидкой за 7.5к — за такие деньги это подарок. Лёгкие, удобные, звук отличный. Нет ANC — единственный минус. Но 80 часов автономности компенсируют.", "rating": 5, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 18}
            ]
        },
        {
            "id": "wb_h006",
            **BEATS_SOLO_4,
            "price": 17990,
            "original_price": 22990,
            "rating": 4.3,
            "review_count": 670,
            "url": "https://wildberries.ru/product/beats-solo4-006",
            "in_stock": True,
            "seller_id": "wb_seller_beats",
            "seller_name": "Beats Store",
            "reviews": [
                {"id": "wr206", "text": "Beats изменились в лучшую сторону. Звук сбалансированный, не только басы. Работают и с iPhone и Android. 50 часов батареи — супер. Складные, лёгкие. Нет ANC — но для этой цены и не жду.", "rating": 4, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 29},
                {"id": "wr207", "text": "Стильные наушники с хорошим звуком. Apple W1 чип — мгновенное подключение к iPhone. Dolby Atmos поддержка — для Apple Music круто. USB-C зарядка — удобно.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 17},
                {"id": "wr208", "text": "Подарил девушке — в восторге. Дизайн красивый, звук хороший. Для повседневного использования — отлично. Не давят на уши, лёгкие. Рекомендую как стильный аксессуар с хорошим звуком.", "rating": 5, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 12}
            ]
        }
    ],
    "ноутбуки": [
        {
            "id": "wb_n003",
            **HP_PAVILION_15,
            "price": 55990,
            "original_price": 64990,
            "rating": 4.3,
            "review_count": 780,
            "url": "https://wildberries.ru/product/hp-pavilion-15-003",
            "in_stock": True,
            "seller_id": "wb_seller_hp",
            "seller_name": "HP Store",
            "reviews": [
                {"id": "wr209", "text": "На WB нашёл дешевле на 3к чем на Ozon. Ноут нормальный — для работы хватает. Windows 11 предустановлена. 16 ГБ ОЗУ, SSD быстрый. Экран средний, но для офиса ок.", "rating": 4, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 22},
                {"id": "wr210", "text": "Хороший рабочий ноутбук без изысков. HP Pavilion — проверенная серия. Для Excel, Word, браузера — более чем достаточно. Батарея 5 часов — терпимо.", "rating": 4, "date": "2025-02-15", "verified_purchase": True, "helpful_count": 14},
                {"id": "wr211", "text": "Пластик дешёвый, но работает стабильно. i5-1335U хватает для повседневных задач. Камера на крышке — для видеозвонков нормально. За свою цену — адекватный ноут.", "rating": 3, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 18}
            ]
        },
        {
            "id": "wb_n004",
            **MSI_THIN_15,
            "price": 62990,
            "original_price": 74990,
            "rating": 4.5,
            "review_count": 560,
            "url": "https://wildberries.ru/product/msi-thin-15-004",
            "in_stock": True,
            "seller_id": "wb_seller_msi",
            "seller_name": "MSI Store",
            "reviews": [
                {"id": "wr212", "text": "Бюджетный гейминг! RTX 3050 тянет все игры на средних. 144 Гц экран — плавно. MSI Thin реально тонкий для игрового ноута. На WB нашёл дешевле чем везде.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 37},
                {"id": "wr213", "text": "Для студента-геймера — идеально. Днём учёба, вечером CS2. RTX 3050 для 1080p хватает. Батарея при играх — 1.5 часа, но кто играет без розетки? Клавиатура с RGB.", "rating": 4, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 24},
                {"id": "wr214", "text": "Шумит при нагрузке — это факт. Но все игровые ноуты шумят. Зато производительность отличная. Для своей цены — лучший игровой ноут. Корпус пластик, но крепкий.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 15}
            ]
        },
        {
            "id": "wb_n005",
            **ACER_ASPIRE_5,
            "price": 32990,
            "original_price": 39990,
            "rating": 4.1,
            "review_count": 1450,
            "url": "https://wildberries.ru/product/acer-aspire5-005",
            "in_stock": True,
            "seller_id": "wb_seller_acer",
            "seller_name": "Acer Store",
            "reviews": [
                {"id": "wr215", "text": "Самый бюджетный ноут, который реально работает. Ryzen 5 — быстрый для своей цены. 8 ГБ ОЗУ — впритык, но можно добавить. SSD 256 — мало, но можно расширить.", "rating": 4, "date": "2025-03-01", "verified_purchase": True, "helpful_count": 31},
                {"id": "wr216", "text": "Купил для интернета и документов — справляется. Большего не жду за 33к. Экран обычный, динамики слабые. Зато надёжный и не тормозит.", "rating": 3, "date": "2025-02-10", "verified_purchase": True, "helpful_count": 17},
                {"id": "wr217", "text": "Для школьника — отличный вариант. Уроки, YouTube, простые игры — всё тянет. Лёгкий, компактный. ОС нет — поставил Linux Mint, летает.", "rating": 4, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 12}
            ]
        }
    ],
    "смартфоны": [
        {
            "id": "wb_s003",
            **IPHONE_15,
            "price": 77990,
            "original_price": 89990,
            "rating": 4.8,
            "review_count": 4200,
            "url": "https://wildberries.ru/product/iphone-15-003",
            "in_stock": True,
            "seller_id": "wb_seller_apple",
            "seller_name": "Apple Reseller",
            "reviews": [
                {"id": "wr218", "text": "На WB дешевле чем в re:Store на 12к! iPhone 15 — отличный телефон. Камера 48 МП, USB-C, Dynamic Island. Работает быстро, батарея на день. Для большинства людей — лучший iPhone.", "rating": 5, "date": "2025-03-11", "verified_purchase": True, "helpful_count": 89},
                {"id": "wr219", "text": "Перешёл с Samsung S23. iOS после Android — другой мир. Всё плавно, без лагов. Камера снимает лучше. FaceTime с друзьями на iPhone — удобно. Минус — нельзя кастомизировать как Android.", "rating": 4, "date": "2025-02-24", "verified_purchase": True, "helpful_count": 52},
                {"id": "wr220", "text": "Жена довольна, я доволен. USB-C наконец-то, один кабель на всё. Камера отличная, портретный режим стал лучше. Батарея на день хватает. Apple есть Apple — работает безупречно.", "rating": 5, "date": "2025-02-05", "verified_purchase": True, "helpful_count": 34},
                {"id": "wr221", "text": "128 ГБ — мало, если снимаешь много видео. Но для обычного использования хватает. Телефон быстрый, камера супер. А16 Bionic не топовый, но скорости хватает с запасом.", "rating": 4, "date": "2025-01-15", "verified_purchase": True, "helpful_count": 25}
            ]
        },
        {
            "id": "wb_s004",
            **POCO_X6_PRO,
            "price": 26490,
            "original_price": 32990,
            "rating": 4.5,
            "review_count": 2340,
            "url": "https://wildberries.ru/product/poco-x6-pro-004",
            "in_stock": True,
            "seller_id": "wb_seller_poco",
            "seller_name": "POCO Store",
            "reviews": [
                {"id": "wr222", "text": "На WB самая низкая цена на POCO X6 Pro! Телефон — бомба за свои деньги. Dimensity 8300 тянет всё. Экран AMOLED шикарный. 67W зарядка — за 40 минут 100%. Лучший бюджетный флагман.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 67},
                {"id": "wr223", "text": "Играю в PUBG на максималках — не лагает. Батарея 5000 мАч — на 2 дня. NFC для оплаты работает. Камера 64 МП — днём хорошо, ночью так себе. За 26к — лучше не найти.", "rating": 5, "date": "2025-02-19", "verified_purchase": True, "helpful_count": 43},
                {"id": "wr224", "text": "MIUI бесит рекламой, но отключается. В остальном — отличный телефон. Мощный, быстрый, красивый экран. За эту цену — убийца флагманов. Рекомендую всем, кто не хочет переплачивать.", "rating": 4, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 29}
            ]
        },
        {
            "id": "wb_s005",
            **NOTHING_PHONE_2,
            "price": 38490,
            "original_price": 49990,
            "rating": 4.4,
            "review_count": 670,
            "url": "https://wildberries.ru/product/nothing-phone2-005",
            "in_stock": True,
            "seller_id": "wb_seller_nothing",
            "seller_name": "Nothing Official",
            "reviews": [
                {"id": "wr225", "text": "Уникальный дизайн — Glyph-подсветка реально крутая. Snapdragon 8+ Gen 1 мощный. Nothing OS чистая и быстрая, без мусора. Для тех, кто устал от Samsung и Xiaomi — отличная альтернатива.", "rating": 5, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 38},
                {"id": "wr226", "text": "Прозрачная задняя панель — вау-эффект. Все спрашивают что за телефон. Производительность на уровне флагманов прошлого года. Камера хорошая, но не топовая. NFC есть, зарядка беспроводная.", "rating": 4, "date": "2025-02-13", "verified_purchase": True, "helpful_count": 24},
                {"id": "wr227", "text": "Nothing Phone 2 — лучший телефон для тех, кто ценит дизайн и чистый Android. Обновления приходят быстро. 12 ГБ ОЗУ — приложения не выгружаются. Батарея на день.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 16}
            ]
        }
    ],
    "пылесосы": [
        {
            "id": "wb_v003",
            **DYSON_V15,
            "price": 52990,
            "original_price": 64990,
            "rating": 4.8,
            "review_count": 1560,
            "url": "https://wildberries.ru/product/dyson-v15-detect-003",
            "in_stock": True,
            "seller_id": "wb_seller_dyson",
            "seller_name": "Dyson Official",
            "reviews": [
                {"id": "wr228", "text": "Dyson V15 — лучший беспроводной пылесос. Лазер подсвечивает пыль — гениально! После уборки дисплей показывает сколько собрал. Мощность огромная. На WB дешевле чем на сайте Dyson.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 72},
                {"id": "wr229", "text": "Перешёл с V8 — разница колоссальная. Мощность, автономность, фильтрация — всё выросло. Лазер для пыли — не гimmick, реально помогает убирать тщательнее. Тяжеловат, но мощный.", "rating": 5, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 45},
                {"id": "wr230", "text": "Дорого, но это Dyson. Качество на высоте. HEPA-фильтр — для аллергиков спасение. 60 минут в эко — хватает на 3-комнатную. В турбо — 8 минут. Зарядка 4 часа — долго.", "rating": 4, "date": "2025-01-30", "verified_purchase": True, "helpful_count": 33}
            ]
        },
        {
            "id": "wb_v004",
            **ECOVACS_T30,
            "price": 57990,
            "original_price": 69990,
            "rating": 4.7,
            "review_count": 450,
            "url": "https://wildberries.ru/product/ecovacs-t30-004",
            "in_stock": True,
            "seller_id": "wb_seller_ecovacs",
            "seller_name": "Ecovacs Store",
            "reviews": [
                {"id": "wr231", "text": "Мощнейший робот — 11000 Па! Ковры чистит как промышленный пылесос. Швабра поднимается автоматически на коврах. Самоочистка горячей водой. За эти деньги — лучший робот 2025.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 41},
                {"id": "wr232", "text": "Купил вместо Roborock — не пожалел. Ecovacs T30 моет лучше, сосёт мощнее. Навигация точная, обходит все препятствия. База громоздкая, но функциональная.", "rating": 5, "date": "2025-02-16", "verified_purchase": True, "helpful_count": 28},
                {"id": "wr233", "text": "Отличный робот, но приложение Ecovacs иногда глючит. Сам робот работает безупречно. Влажная уборка намного лучше чем у конкурентов. LiDAR + камера = идеальная навигация.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "wb_v005",
            **SAMSUNG_JET_BOT,
            "price": 47990,
            "original_price": 59990,
            "rating": 4.2,
            "review_count": 780,
            "url": "https://wildberries.ru/product/samsung-jet-bot-005",
            "in_stock": True,
            "seller_id": "wb_seller_samsung",
            "seller_name": "Samsung Store",
            "reviews": [
                {"id": "wr234", "text": "AI-навигация реально работает — обходит провода, тапки, игрушки. Clean Station — удобно, мусор не нужно вытряхивать. Минус — нет влажной уборки. Для сухой уборки — отличный робот.", "rating": 4, "date": "2025-03-03", "verified_purchase": True, "helpful_count": 27},
                {"id": "wr235", "text": "Интеграция с SmartThings — управляю роботом через умную колонку. Для экосистемы Samsung — идеально. Убирает хорошо, но за эту цену хотелось бы влажную уборку.", "rating": 4, "date": "2025-02-11", "verified_purchase": True, "helpful_count": 18},
                {"id": "wr236", "text": "Нормальный робот, но переоценённый. За те же деньги Ecovacs или Dreame предлагают больше. Samsung берут за бренд и экосистему. Уборка хорошая, но без мытья.", "rating": 3, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 32}
            ]
        }
    ],
    "телевизоры": [
        {
            "id": "wb_t004",
            **SONY_A80L,
            "price": 97990,
            "original_price": 119990,
            "rating": 4.9,
            "review_count": 280,
            "url": "https://wildberries.ru/product/sony-a80l-004",
            "in_stock": True,
            "seller_id": "wb_seller_sony",
            "seller_name": "Sony Official",
            "reviews": [
                {"id": "wr237", "text": "Sony OLED — это искусство. Acoustic Surface Audio — звук из экрана, это надо слышать! Картинка невероятная, процессор XR творит чудеса. Для домашнего кинотеатра — лучший выбор.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 52},
                {"id": "wr238", "text": "Сравнивал с LG C3 в магазине — Sony A80L лучше в обработке движения и цветах. Звук вообще несравним — у Sony из коробки как саундбар. Дороже, но стоит каждого рубля.", "rating": 5, "date": "2025-02-21", "verified_purchase": True, "helpful_count": 38},
                {"id": "wr239", "text": "Google TV быстрее чем webOS. Chromecast встроенный. Для PS5 — идеально, HDMI 2.1 с VRR. Картинка OLED безупречна. Единственное — цена.", "rating": 5, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 24}
            ]
        },
        {
            "id": "wb_t005",
            **PHILIPS_PUS8808,
            "price": 49990,
            "original_price": 62990,
            "rating": 4.5,
            "review_count": 560,
            "url": "https://wildberries.ru/product/philips-pus8808-005",
            "in_stock": True,
            "seller_id": "wb_seller_philips",
            "seller_name": "Philips Official",
            "reviews": [
                {"id": "wr240", "text": "Ambilight — главная фишка! Подсветка стены меняется в такт картинке. Вечером смотреть кино — полное погружение. Картинка хорошая, 120 Гц для игр. На WB дешевле чем везде.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 43},
                {"id": "wr241", "text": "Для своей цены — отличный телевизор. Ambilight уникальная технология, больше никто так не делает. Картинка не OLED, но для LED — очень достойная. Google TV удобный.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 27},
                {"id": "wr242", "text": "Купил из-за Ambilight — не разочаровался. Реально снижает нагрузку на глаза. Картинка приятная, звук средний. Для кино и сериалов — рекомендую.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 16}
            ]
        }
    ],
    "планшеты": [
        {
            "id": "wb_p004",
            **ONEPLUS_PAD_2,
            "price": 38490,
            "original_price": 49990,
            "rating": 4.5,
            "review_count": 450,
            "url": "https://wildberries.ru/product/oneplus-pad2-004",
            "in_stock": True,
            "seller_id": "wb_seller_oneplus",
            "seller_name": "OnePlus Store",
            "reviews": [
                {"id": "wr243", "text": "Самый мощный Android-планшет! Snapdragon 8 Gen 3 — всё летает. Экран 3K 144 Гц гигантский и плавный. Для игр и мультимедиа — идеален. На WB нашёл дешевле на 2к чем на Ozon.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 39},
                {"id": "wr244", "text": "OxygenOS на планшете — быстрая и чистая. Батарея 9510 мАч — на 2 дня активного использования. Зарядка 67W за час. Динамики мощные. Для Android-мира — лучший планшет.", "rating": 5, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 26},
                {"id": "wr245", "text": "Хороший планшет, но мало оптимизированных Android-приложений для планшета. Производительность топ, экран красивый. Стилус и клавиатура покупаются отдельно — дорого.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 17}
            ]
        },
        {
            "id": "wb_p005",
            **IPAD_10,
            "price": 33990,
            "original_price": 39990,
            "rating": 4.6,
            "review_count": 3400,
            "url": "https://wildberries.ru/product/ipad-10-gen-005",
            "in_stock": True,
            "seller_id": "wb_seller_apple",
            "seller_name": "Apple Reseller",
            "reviews": [
                {"id": "wr246", "text": "Базовый iPad за 34к на WB — отличная цена! A14 Bionic хватает для всего. USB-C удобно. Для YouTube, Netflix, учёбы — лучший планшет. Apple экосистема работает идеально.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 45},
                {"id": "wr247", "text": "Купил маме — легко разобралась. Экран большой, яркий. Для чтения, видеозвонков, рецептов — идеально. Батарея на весь день. 64 ГБ хватает, если не забивать фильмами.", "rating": 5, "date": "2025-02-19", "verified_purchase": True, "helpful_count": 28},
                {"id": "wr248", "text": "Отличный планшет для детей. Надёжный, приложений море, родительский контроль есть. Apple Pencil 1-го поколения — для рисования нормально. Жаль что не Pro Motion 120 Гц.", "rating": 4, "date": "2025-01-15", "verified_purchase": True, "helpful_count": 19}
            ]
        }
    ],
    "умные часы": [
        {
            "id": "wb_w004",
            **XIAOMI_WATCH_2_PRO,
            "price": 18990,
            "original_price": 24990,
            "rating": 4.3,
            "review_count": 1120,
            "url": "https://wildberries.ru/product/xiaomi-watch-2-pro-004",
            "in_stock": True,
            "seller_id": "wb_seller_xiaomi",
            "seller_name": "Xiaomi Official",
            "reviews": [
                {"id": "wr249", "text": "Наконец-то Xiaomi на Wear OS! Google-приложения, Play Store, нормальные уведомления. Экран AMOLED красивый. GPS точный для бега. На WB — самая низкая цена. Минус — батарея 2 дня.", "rating": 4, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 38},
                {"id": "wr250", "text": "Хорошие часы за свои деньги на Wear OS. Snapdragon W5+ Gen 1 — работают плавно. NFC есть, но Google Pay в России не работает. Для фитнеса и уведомлений — отлично.", "rating": 4, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 24},
                {"id": "wr251", "text": "Wear OS 3.5 — наконец-то нормальная ОС от Xiaomi. После Amazfit — небо и земля по функционалу. Но автономность упала — с 14 дней до 2. Trade-off. Для активных пользователей — ок.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 18}
            ]
        },
        {
            "id": "wb_w005",
            **TICWATCH_PRO_5,
            "price": 27990,
            "original_price": 34990,
            "rating": 4.5,
            "review_count": 340,
            "url": "https://wildberries.ru/product/ticwatch-pro5-005",
            "in_stock": True,
            "seller_id": "wb_seller_mobvoi",
            "seller_name": "Mobvoi Official",
            "reviews": [
                {"id": "wr252", "text": "Двойной экран — гениальная идея! AMOLED для приложений, LCD для времени и пульса — батарея 4 дня, а не 1.5 как у других Wear OS часов. Snapdragon W5+ Gen 1 — быстрый.", "rating": 5, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 42},
                {"id": "wr253", "text": "Лучшие Wear OS часы по автономности. 4 дня реально, с AOD на LCD-экране — до 45 дней. Встроенный GPS, NFC, водозащита. Для спорта — отлично.", "rating": 5, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 31},
                {"id": "wr254", "text": "Хорошие часы, но тяжёлые — 44.3 г. Wear OS работает плавно. Google-приложения все на месте. Barometer и компас — для походов удобно. Дизайн строгий, офисный.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 19}
            ]
        }
    ],
    "кофемашины": [
        {
            "id": "wb_k004",
            **SAECO_XELSIS,
            "price": 114990,
            "original_price": 139990,
            "rating": 4.7,
            "review_count": 180,
            "url": "https://wildberries.ru/product/saeco-xelsis-004",
            "in_stock": True,
            "seller_id": "wb_seller_saeco",
            "seller_name": "Saeco Official",
            "reviews": [
                {"id": "wr255", "text": "Вершина домашних кофемашин. 22 напитка, сенсорный дисплей, LatteDuo. На WB нашёл дешевле на 5к чем на Ozon. Кофе как в ресторане. Профили пользователей — вся семья довольна.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 37},
                {"id": "wr256", "text": "Дорого, но это Saeco (Philips). Качество итальянское, надёжность немецкая. Кофе варит великолепно, молочная пенка идеальная. Самоочистка — не нужно возиться.", "rating": 5, "date": "2025-02-17", "verified_purchase": True, "helpful_count": 25},
                {"id": "wr257", "text": "Каждый напиток можно настроить — температура, крепость, объём молока, помол. Для кофеманов — рай. Цена пугает, но если считать экономию на кофейнях — окупается за год.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 18}
            ]
        },
        {
            "id": "wb_k005",
            **MELITTA_BARISTA,
            "price": 76990,
            "original_price": 94990,
            "rating": 4.5,
            "review_count": 390,
            "url": "https://wildberries.ru/product/melitta-barista-ts-005",
            "in_stock": True,
            "seller_id": "wb_seller_melitta",
            "seller_name": "Melitta Official",
            "reviews": [
                {"id": "wr258", "text": "Управление через Bluetooth — включаю кофемашину с кровати! 21 напиток, два бункера для зёрен. Кофе варит отлично. Немецкое качество. На WB лучшая цена.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 34},
                {"id": "wr259", "text": "Приложение Melitta Companion удобное — создаёшь свои рецепты, настраиваешь каждый параметр. Два бункера — утром крепкий, вечером мягкий. Автокапучинатор — пенка идеальная.", "rating": 4, "date": "2025-02-15", "verified_purchase": True, "helpful_count": 22},
                {"id": "wr260", "text": "Между Saeco и Melitta выбрал Melitta — дешевле и с Bluetooth. Кофе не хуже. Единственное — шумная при помоле. Но все зерновые кофемашины шумят.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 15}
            ]
        },
        {
            "id": "wb_k006",
            **NESPRESSO_VERTUO,
            "price": 12990,
            "original_price": 17990,
            "rating": 4.2,
            "review_count": 3450,
            "url": "https://wildberries.ru/product/nespresso-vertuo-006",
            "in_stock": True,
            "seller_id": "wb_seller_nespresso",
            "seller_name": "Nespresso Store",
            "reviews": [
                {"id": "wr261", "text": "Для тех, кто хочет кофе без заморочек — идеально. Вставил капсулу, нажал кнопку. Кофе хороший, 5 размеров чашки. Centrifusion технология — крема густая. Минус — капсулы дорогие.", "rating": 4, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 45},
                {"id": "wr262", "text": "Машинка компактная, на кухне не мешает. Нагревается за 30 секунд — утром это важно. Кофе вкусный, но капсулы выходят 40-60₽ за штуку. За месяц набегает прилично.", "rating": 4, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 31},
                {"id": "wr263", "text": "Удобно, быстро, вкусно. Но экологически — капсулы это зло. И дорого в пересчёте на чашку. Для офиса или если пьёшь 1-2 чашки в день — ок. Для кофемана — лучше зерновую.", "rating": 3, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 52}
            ]
        }
    ]
}


# ═══════════════════════════════════════════════════════════════
# YANDEX NEW PRODUCTS
# ═══════════════════════════════════════════════════════════════

YANDEX_NEW = {
    "наушники": [
        {
            "id": "ya_h004",
            **BOSE_QC_ULTRA,
            "price": 35490,
            "original_price": 39990,
            "rating": 4.8,
            "review_count": 450,
            "url": "https://market.yandex.ru/product/bose-qc-ultra-004",
            "in_stock": True,
            "seller_id": "ya_seller_bose",
            "seller_name": "Bose Official",
            "reviews": [
                {"id": "yr200", "text": "Заказал на Яндексе — доставка Яндекса быстрая и аккуратная. Наушники топовые. Шумоподавление мощное, звук натуральный и объёмный. Immersive Audio — это нечто, как в кинотеатре.", "rating": 5, "date": "2025-03-10", "verified_purchase": True, "helpful_count": 39},
                {"id": "yr201", "text": "Дороже чем на WB, но гарантия официальная. Bose QC Ultra — лучшие наушники для путешествий. Шумоподавление в самолёте — тишина. Звук богатый и детальный.", "rating": 5, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 27},
                {"id": "yr202", "text": "Сравнивал с Sony XM5 и Sennheiser Momentum 4. Bose — лучший баланс шумоподавления и звука. Sony шумодав чуть лучше, Sennheiser звучит чуть лучше, но Bose — золотая середина.", "rating": 4, "date": "2025-01-30", "verified_purchase": True, "helpful_count": 33}
            ]
        },
        {
            "id": "ya_h005",
            **BEATS_SOLO_4,
            "price": 19490,
            "original_price": 22990,
            "rating": 4.3,
            "review_count": 340,
            "url": "https://market.yandex.ru/product/beats-solo4-005",
            "in_stock": True,
            "seller_id": "ya_seller_beats",
            "seller_name": "Beats Store",
            "reviews": [
                {"id": "yr203", "text": "Beats сильно выросли в качестве звука. Solo 4 звучат сбалансированно, не только басы. Dolby Atmos для Apple Music — погружение. USB-C зарядка. 50 часов батареи — супер.", "rating": 4, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 24},
                {"id": "yr204", "text": "Стильные, лёгкие, удобные. Для повседневного использования — отлично. Нет ANC — для транспорта минус. Но для улицы и дома — хороший вариант.", "rating": 4, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 15},
                {"id": "yr205", "text": "Работают и с Android и с iPhone. Но с iPhone лучше — мгновенное подключение, Spatial Audio. Звук приятный, басы глубокие. За 19к — достойный выбор.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 11}
            ]
        },
        {
            "id": "ya_h006",
            **MARSHALL_MAJOR_IV,
            "price": 8490,
            "original_price": 9990,
            "rating": 4.5,
            "review_count": 1670,
            "url": "https://market.yandex.ru/product/marshall-major-iv-006",
            "in_stock": True,
            "seller_id": "ya_seller_marshall",
            "seller_name": "Marshall Official",
            "reviews": [
                {"id": "yr206", "text": "80 часов батареи — рекорд! Звук Marshall — тёплый, басовитый, идеальный для рока. Беспроводная зарядка — положил на подставку и забыл. Нет ANC, но для дома не нужен.", "rating": 5, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 35},
                {"id": "yr207", "text": "Купил на Яндексе с быстрой доставкой. Наушники стильные, звук качественный. Marshall Major IV — классика. Складные, лёгкие. Для музыки — отличный выбор.", "rating": 4, "date": "2025-02-16", "verified_purchase": True, "helpful_count": 20},
                {"id": "yr208", "text": "Нет шумоподавления — единственный минус. В остальном — прекрасные наушники. Звук детальный, басы упругие. Дизайн ретро — выделяешься из толпы AirPods Max.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 14}
            ]
        }
    ],
    "ноутбуки": [
        {
            "id": "ya_n003",
            **HP_PAVILION_15,
            "price": 59990,
            "original_price": 64990,
            "rating": 4.4,
            "review_count": 670,
            "url": "https://market.yandex.ru/product/hp-pavilion-15-003",
            "in_stock": True,
            "seller_id": "ya_seller_hp",
            "seller_name": "HP Official",
            "reviews": [
                {"id": "yr209", "text": "Доставка Яндекса на следующий день — очень удобно. HP Pavilion — надёжный рабочий ноут. Windows 11 из коробки. 16 ГБ ОЗУ для офисных задач — за глаза. Экран нормальный для IPS.", "rating": 4, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 19},
                {"id": "yr210", "text": "Нормальный ноут для работы. Не самый дешёвый на рынке, но HP — проверенный бренд. Клавиатура удобная, тачпад адекватный. Для офиса и учёбы — рекомендую.", "rating": 4, "date": "2025-02-13", "verified_purchase": True, "helpful_count": 12},
                {"id": "yr211", "text": "За 60к хотелось бы металлический корпус, а не пластик. Но работает стабильно, не шумит. SSD быстрый, 16 ГБ ОЗУ хватает. Батарея 5-6 часов — средне.", "rating": 3, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 22}
            ]
        },
        {
            "id": "ya_n004",
            **ACER_ASPIRE_5,
            "price": 35990,
            "original_price": 39990,
            "rating": 4.2,
            "review_count": 890,
            "url": "https://market.yandex.ru/product/acer-aspire5-004",
            "in_stock": True,
            "seller_id": "ya_seller_acer",
            "seller_name": "Acer Official",
            "reviews": [
                {"id": "yr212", "text": "Бюджетный ноут для студентов. Ryzen 5 тянет все базовые задачи. 8 ГБ ОЗУ — минимум, но можно расширить. SSD 256 — мало, рекомендую сразу докупить внешний. За 36к — адекватно.", "rating": 4, "date": "2025-03-02", "verified_purchase": True, "helpful_count": 25},
                {"id": "yr213", "text": "Первый ноут для ребёнка. Для школьных задач, интернета и YouTube хватает с головой. Не тяжёлый, батарея 5 часов. ОС нет — поставили Windows 11 сами.", "rating": 4, "date": "2025-02-08", "verified_purchase": True, "helpful_count": 16},
                {"id": "yr214", "text": "За свои деньги — ок. Не ждите чудес за 36к. Для браузера, офиса и видео — достаточно. Экран тусклый, динамики слабые. Но для работы хватает.", "rating": 3, "date": "2025-01-15", "verified_purchase": True, "helpful_count": 19}
            ]
        },
        {
            "id": "ya_n005",
            **MSI_THIN_15,
            "price": 66990,
            "original_price": 74990,
            "rating": 4.6,
            "review_count": 340,
            "url": "https://market.yandex.ru/product/msi-thin-15-005",
            "in_stock": True,
            "seller_id": "ya_seller_msi",
            "seller_name": "MSI Official",
            "reviews": [
                {"id": "yr215", "text": "Бюджетный игровой ноут с RTX 3050. На Яндексе немного дороже чем на WB, но доставка надёжнее. CS2 на высоких 80+ fps. Экран 144 Гц плавный. Для начинающего геймера — идеально.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 35},
                {"id": "yr216", "text": "i5-12450H + RTX 3050 — хорошая связка для 1080p гейминга. Тонкий для игрового ноута. Батарея при играх — 1.5 часа, но это нормально. Клавиатура с подсветкой, тачпад нормальный.", "rating": 4, "date": "2025-02-17", "verified_purchase": True, "helpful_count": 23},
                {"id": "yr217", "text": "Для учёбы днём и игр вечером — самый подходящий вариант. Не самый мощный, но за 67к — лучшее что есть с видеокартой. Пластик, но крепкий. Рекомендую.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 15}
            ]
        }
    ],
    "смартфоны": [
        {
            "id": "ya_s003",
            **IPHONE_15,
            "price": 82990,
            "original_price": 89990,
            "rating": 4.8,
            "review_count": 2100,
            "url": "https://market.yandex.ru/product/iphone-15-003",
            "in_stock": True,
            "seller_id": "ya_seller_apple",
            "seller_name": "Apple Store",
            "reviews": [
                {"id": "yr218", "text": "Заказал iPhone 15 на Яндексе — доставили за 2 часа (Яндекс Доставка)! Телефон отличный — камера 48 МП, USB-C, Dynamic Island. Работает идеально. Для большинства людей — лучший iPhone.", "rating": 5, "date": "2025-03-11", "verified_purchase": True, "helpful_count": 62},
                {"id": "yr219", "text": "На Яндексе дороже чем на WB, но зато гарантия Apple и быстрая доставка. iPhone 15 — надёжный, быстрый, камера отличная. USB-C — наконец-то один кабель на всё.", "rating": 4, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 38},
                {"id": "yr220", "text": "Перешёл с iPhone 12 — разница заметная. Камера стала намного лучше, Dynamic Island удобный, USB-C — не нужен отдельный кабель. A16 Bionic быстрый. Рекомендую.", "rating": 5, "date": "2025-02-05", "verified_purchase": True, "helpful_count": 27}
            ]
        },
        {
            "id": "ya_s004",
            **NOTHING_PHONE_2,
            "price": 41990,
            "original_price": 49990,
            "rating": 4.5,
            "review_count": 450,
            "url": "https://market.yandex.ru/product/nothing-phone2-004",
            "in_stock": True,
            "seller_id": "ya_seller_nothing",
            "seller_name": "Nothing Official",
            "reviews": [
                {"id": "yr221", "text": "Самый стильный телефон на рынке. Glyph-подсветка завораживает. Snapdragon 8+ Gen 1 мощный. Nothing OS минималистичная и быстрая. На Яндексе — с гарантией и быстрой доставкой.", "rating": 5, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 34},
                {"id": "yr222", "text": "Чистый Android — никакой рекламы и мусора. 12 ГБ ОЗУ — всё летает. Камера хорошая днём, ночью средняя. Дизайн уникальный — прозрачная задняя панель с подсветкой.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 22},
                {"id": "yr223", "text": "Nothing Phone 2 — для тех, кто хочет выделиться. Производительность флагманская, цена средняя. Обновления приходят регулярно. Беспроводная зарядка есть. Хороший выбор.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 16}
            ]
        },
        {
            "id": "ya_s005",
            **POCO_X6_PRO,
            "price": 28990,
            "original_price": 32990,
            "rating": 4.4,
            "review_count": 1450,
            "url": "https://market.yandex.ru/product/poco-x6-pro-005",
            "in_stock": True,
            "seller_id": "ya_seller_poco",
            "seller_name": "POCO Store",
            "reviews": [
                {"id": "yr224", "text": "POCO X6 Pro — лучший бюджетный флагман. Dimensity 8300 мощнее чем Snapdragon 7 Gen 1. Экран AMOLED яркий. За 29к — конкурентов нет. На Яндексе доставка быстрая.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 42},
                {"id": "yr225", "text": "Для игр и повседневных задач — идеален. Батарея 5000 мАч на 2 дня. Зарядка 67W быстрая. NFC работает. Камера 64 МП — хорошая для своей цены.", "rating": 4, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 28},
                {"id": "yr226", "text": "MIUI с рекламой — минус, но отключается. В остальном — отличный телефон за свои деньги. Мощный, красивый экран, быстрая зарядка. Рекомендую.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 19}
            ]
        }
    ],
    "пылесосы": [
        {
            "id": "ya_v003",
            **DYSON_V15,
            "price": 56990,
            "original_price": 64990,
            "rating": 4.7,
            "review_count": 890,
            "url": "https://market.yandex.ru/product/dyson-v15-detect-003",
            "in_stock": True,
            "seller_id": "ya_seller_dyson",
            "seller_name": "Dyson Official",
            "reviews": [
                {"id": "yr227", "text": "Dyson V15 Detect — вершина беспроводных пылесосов. Лазер подсвечивает пыль — убираешь на совесть. Дисплей показывает статистику. HEPA-фильтрация. Доставка Яндексом за день.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 55},
                {"id": "yr228", "text": "Дорого, но Dyson — это другой уровень. Мощность бешеная, фильтрация идеальная. Для аллергиков — must have. 60 минут в эко хватает на квартиру. Тяжеловат — 3 кг.", "rating": 4, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 37},
                {"id": "yr229", "text": "Третий Dyson, каждый раз лучше. V15 Detect — самый технологичный. Лазер, дисплей, HEPA — полный фарш. Зарядка долгая — 4.5 часа. Но мощность того стоит.", "rating": 5, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 24}
            ]
        },
        {
            "id": "ya_v004",
            **ECOVACS_T30,
            "price": 61990,
            "original_price": 69990,
            "rating": 4.6,
            "review_count": 280,
            "url": "https://market.yandex.ru/product/ecovacs-t30-004",
            "in_stock": True,
            "seller_id": "ya_seller_ecovacs",
            "seller_name": "Ecovacs Store",
            "reviews": [
                {"id": "yr230", "text": "11000 Па мощности — ковры чистит идеально. Швабра поднимается на коврах — умная функция. Самоочистка горячей водой — гигиенично. На Яндексе доставка бережная.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 33},
                {"id": "yr231", "text": "Хороший робот-пылесос, конкурент Roborock. Влажная уборка качественная. LiDAR навигация точная. Приложение удобное. Минус — база большая, нужно место.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 21},
                {"id": "yr232", "text": "За свои деньги — один из лучших роботов. Мощный, умный, хорошо моет. Убирает каждый день по расписанию. Для квартиры 70м² — идеально.", "rating": 5, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 17}
            ]
        },
        {
            "id": "ya_v005",
            **SAMSUNG_JET_BOT,
            "price": 51990,
            "original_price": 59990,
            "rating": 4.3,
            "review_count": 450,
            "url": "https://market.yandex.ru/product/samsung-jet-bot-005",
            "in_stock": True,
            "seller_id": "ya_seller_samsung",
            "seller_name": "Samsung Official",
            "reviews": [
                {"id": "yr233", "text": "Samsung Jet Bot — хороший робот для сухой уборки. AI-камера обходит препятствия. Clean Station автоматически опустошает контейнер. SmartThings интеграция. Нет влажной уборки — жаль.", "rating": 4, "date": "2025-03-03", "verified_purchase": True, "helpful_count": 25},
                {"id": "yr234", "text": "Для экосистемы Samsung — отличный выбор. Управляется через SmartThings вместе с ТВ и стиралкой. Убирает хорошо, но за эту цену хотелось бы и мытьё полов.", "rating": 4, "date": "2025-02-10", "verified_purchase": True, "helpful_count": 18},
                {"id": "yr235", "text": "AI навигация работает — обходит провода и носки. Clean Station — удобно, раз в месяц меняешь мешок. Но без влажной уборки в 2025 — уже архаизм. Конкуренты за эти деньги моют.", "rating": 3, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 29}
            ]
        }
    ],
    "телевизоры": [
        {
            "id": "ya_t004",
            **SONY_A80L,
            "price": 104990,
            "original_price": 119990,
            "rating": 4.9,
            "review_count": 230,
            "url": "https://market.yandex.ru/product/sony-a80l-004",
            "in_stock": True,
            "seller_id": "ya_seller_sony",
            "seller_name": "Sony Official",
            "reviews": [
                {"id": "yr236", "text": "Лучший OLED на рынке. Sony XR процессор делает невероятную картинку. Acoustic Surface — звук из экрана, не нужен саундбар. Google TV быстрый. На Яндексе доставили аккуратно.", "rating": 5, "date": "2025-03-11", "verified_purchase": True, "helpful_count": 48},
                {"id": "yr237", "text": "Дорого, но Sony A80L — это искусство. Для кинолюбителей — лучше не бывает. Dolby Vision, Dolby Atmos. Для PS5 — VRR, ALLM, HDMI 2.1. Универсальный телевизор для всего.", "rating": 5, "date": "2025-02-22", "verified_purchase": True, "helpful_count": 35},
                {"id": "yr238", "text": "На Яндексе дороже чем на WB, но гарантия и доставка лучше. Телевизор шикарный — картинка OLED, звук из экрана, Google TV. Лучше LG C3 по обработке движения.", "rating": 5, "date": "2025-01-28", "verified_purchase": True, "helpful_count": 24}
            ]
        },
        {
            "id": "ya_t005",
            **HAIER_S4,
            "price": 29990,
            "original_price": 34990,
            "rating": 4.0,
            "review_count": 1890,
            "url": "https://market.yandex.ru/product/haier-s4-55-005",
            "in_stock": True,
            "seller_id": "ya_seller_haier",
            "seller_name": "Haier Official",
            "reviews": [
                {"id": "yr239", "text": "Бюджетный 4K за 30к — для дачи или спальни отлично. Android TV есть, приложения работают. Картинка обычная LED, но для ТВ-каналов и YouTube хватает. Звук слабый.", "rating": 4, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 27},
                {"id": "yr240", "text": "Нормальный телевизор без претензий. Haier делают добротную технику за свои деньги. Для кухни — идеально. Пульт простой, меню понятное.", "rating": 3, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 15},
                {"id": "yr241", "text": "Купил родителям — им нравится. Большой экран, YouTube работает, Кинопоиск есть. Картинка не Samsung, но за 30к — грех жаловаться. Доставка Яндексом аккуратная.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 21}
            ]
        },
        {
            "id": "ya_t006",
            **PHILIPS_PUS8808,
            "price": 54990,
            "original_price": 62990,
            "rating": 4.6,
            "review_count": 450,
            "url": "https://market.yandex.ru/product/philips-pus8808-006",
            "in_stock": True,
            "seller_id": "ya_seller_philips",
            "seller_name": "Philips Official",
            "reviews": [
                {"id": "yr242", "text": "Ambilight — вот зачем покупают Philips. Подсветка стены создаёт эффект погружения. Для кино вечером — магия. Картинка LED, но хорошая. 120 Гц для игр. Google TV.", "rating": 5, "date": "2025-03-08", "verified_purchase": True, "helpful_count": 41},
                {"id": "yr243", "text": "Уникальный телевизор. Ambilight больше никто не делает — запатентованная технология Philips. Снижает нагрузку на глаза. Картинка хорошая, звук средний.", "rating": 4, "date": "2025-02-17", "verified_purchase": True, "helpful_count": 26},
                {"id": "yr244", "text": "На Яндексе чуть дороже, но с нормальной гарантией. Philips 8808 с Ambilight — красивый телевизор. Google TV работает быстро. Рекомендую для кинолюбителей.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 17}
            ]
        }
    ],
    "планшеты": [
        {
            "id": "ya_p004",
            **ONEPLUS_PAD_2,
            "price": 41990,
            "original_price": 49990,
            "rating": 4.6,
            "review_count": 280,
            "url": "https://market.yandex.ru/product/oneplus-pad2-004",
            "in_stock": True,
            "seller_id": "ya_seller_oneplus",
            "seller_name": "OnePlus Official",
            "reviews": [
                {"id": "yr245", "text": "Мощнейший Android-планшет! Snapdragon 8 Gen 3 тянет всё. Экран 3K 144 Гц — невероятно плавный. OxygenOS чистая. На Яндексе — с гарантией. Конкурент iPad Air.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 38},
                {"id": "yr246", "text": "Хороший планшет для работы и развлечений. Большой экран 12.1 дюйма. Батарея 9510 мАч — на 2 дня. Зарядка 67W быстрая. Стилус и клавиатура отдельно — минус.", "rating": 4, "date": "2025-02-20", "verified_purchase": True, "helpful_count": 24},
                {"id": "yr247", "text": "Для Android-мира — лучший планшет. Но приложений оптимизированных под планшет мало. Для медиа, игр и интернета — идеально. Для продуктивности — iPad Air лучше.", "rating": 4, "date": "2025-01-25", "verified_purchase": True, "helpful_count": 17}
            ]
        },
        {
            "id": "ya_p005",
            **REALME_PAD_2,
            "price": 17990,
            "original_price": 21990,
            "rating": 4.2,
            "review_count": 890,
            "url": "https://market.yandex.ru/product/realme-pad2-005",
            "in_stock": True,
            "seller_id": "ya_seller_realme",
            "seller_name": "Realme Official",
            "reviews": [
                {"id": "yr248", "text": "Самый бюджетный нормальный планшет! За 18к — экран 11.5 дюймов 120 Гц, Helio G99, 6 ГБ ОЗУ. Для YouTube, книг и простых игр — хватает. Стилус опционально.", "rating": 4, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 35},
                {"id": "yr249", "text": "Бюджетный планшет с хорошим экраном. 120 Гц — плавно. Helio G99 не топ, но для повседневных задач достаточно. Батарея 8360 мАч — на 2 дня.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 22},
                {"id": "yr250", "text": "Для ребёнка — отличный вариант. Большой экран, не тормозит, батарея долго. Если разобьёт — не так жалко как iPad. Камеры слабые, но для планшета это норма.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 16}
            ]
        }
    ],
    "умные часы": [
        {
            "id": "ya_w004",
            **XIAOMI_WATCH_2_PRO,
            "price": 20990,
            "original_price": 24990,
            "rating": 4.4,
            "review_count": 670,
            "url": "https://market.yandex.ru/product/xiaomi-watch-2-pro-004",
            "in_stock": True,
            "seller_id": "ya_seller_xiaomi",
            "seller_name": "Xiaomi Official",
            "reviews": [
                {"id": "yr251", "text": "Xiaomi на Wear OS — другой уровень. Google-приложения, Play Store, нормальные уведомления. Экран AMOLED яркий. За 21к — отличные Wear OS часы. Батарея 2 дня — компромисс.", "rating": 4, "date": "2025-03-07", "verified_purchase": True, "helpful_count": 32},
                {"id": "yr252", "text": "После Amazfit — шаг вперёд по функционалу, шаг назад по автономности. Wear OS даёт приложения и полную интеграцию с Android. Но 2 дня vs 14 — привыкать нужно.", "rating": 4, "date": "2025-02-16", "verified_purchase": True, "helpful_count": 21},
                {"id": "yr253", "text": "Хорошие часы на Wear OS за адекватные деньги. GPS точный, пульсометр нормальный. NFC есть. Для фитнеса и уведомлений — отлично. Доставка Яндексом быстрая.", "rating": 4, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 15}
            ]
        },
        {
            "id": "ya_w005",
            **TICWATCH_PRO_5,
            "price": 29990,
            "original_price": 34990,
            "rating": 4.5,
            "review_count": 230,
            "url": "https://market.yandex.ru/product/ticwatch-pro5-005",
            "in_stock": True,
            "seller_id": "ya_seller_mobvoi",
            "seller_name": "Mobvoi Official",
            "reviews": [
                {"id": "yr254", "text": "Двойной экран — AMOLED + LCD. Автономность 4 дня на Wear OS! Это рекорд. LCD показывает время и пульс, AMOLED включается при активном использовании. Гениально.", "rating": 5, "date": "2025-03-05", "verified_purchase": True, "helpful_count": 37},
                {"id": "yr255", "text": "Для Wear OS — лучшая автономность. 4 дня реально, в Essential Mode на LCD — 45 дней. Snapdragon W5+ Gen 1 быстрый. Для спорта и повседневки — отлично.", "rating": 5, "date": "2025-02-12", "verified_purchase": True, "helpful_count": 26},
                {"id": "yr256", "text": "Хорошие часы, но бренд малоизвестный в России. Функционал на уровне Samsung Galaxy Watch. Двойной экран — уникальная фишка. Тяжеловаты, но привыкаешь.", "rating": 4, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 17}
            ]
        }
    ],
    "кофемашины": [
        {
            "id": "ya_k004",
            **SAECO_XELSIS,
            "price": 122990,
            "original_price": 139990,
            "rating": 4.8,
            "review_count": 160,
            "url": "https://market.yandex.ru/product/saeco-xelsis-004",
            "in_stock": True,
            "seller_id": "ya_seller_saeco",
            "seller_name": "Saeco Official",
            "reviews": [
                {"id": "yr257", "text": "Вершина кофемашин для дома. 22 напитка, сенсорный дисплей, LatteDuo — два капучино одновременно. Кофе как в итальянском ресторане. Дорого, но для кофеманов — рай.", "rating": 5, "date": "2025-03-09", "verified_purchase": True, "helpful_count": 41},
                {"id": "yr258", "text": "На Яндексе немного дороже, но доставка и гарантия надёжнее. Saeco Xelsis — премиум во всём. Каждый напиток настраивается. Профили пользователей — каждый член семьи доволен.", "rating": 5, "date": "2025-02-18", "verified_purchase": True, "helpful_count": 28},
                {"id": "yr259", "text": "Лучшая кофемашина что у меня была. До этого De'Longhi и Philips — Saeco на голову выше. Самоочистка работает, молочная система идеальная. Инвестиция на годы.", "rating": 5, "date": "2025-01-22", "verified_purchase": True, "helpful_count": 22}
            ]
        },
        {
            "id": "ya_k005",
            **NESPRESSO_VERTUO,
            "price": 13990,
            "original_price": 17990,
            "rating": 4.1,
            "review_count": 2800,
            "url": "https://market.yandex.ru/product/nespresso-vertuo-005",
            "in_stock": True,
            "seller_id": "ya_seller_nespresso",
            "seller_name": "Nespresso Official",
            "reviews": [
                {"id": "yr260", "text": "Для тех, кто не хочет возиться с зёрнами — Nespresso идеален. Вставил капсулу, нажал кнопку — кофе готов за 30 секунд. Centrifusion делает густую крему. Минус — капсулы дорогие.", "rating": 4, "date": "2025-03-04", "verified_purchase": True, "helpful_count": 38},
                {"id": "yr261", "text": "Компактная машинка, стоит на подоконнике. Кофе вкусный, 5 размеров чашки. Для утренней чашки — идеально. Но если пить по 5 чашек в день — зерновая кофемашина выгоднее.", "rating": 4, "date": "2025-02-11", "verified_purchase": True, "helpful_count": 25},
                {"id": "yr262", "text": "Удобно, быстро, вкусно. Вертикальная загрузка капсул — Vertuo система. Разнообразие вкусов в магазине Nespresso. Экологический вопрос капсул смущает. За 14к — норм.", "rating": 3, "date": "2025-01-18", "verified_purchase": True, "helpful_count": 42}
            ]
        },
        {
            "id": "ya_k006",
            **MELITTA_BARISTA,
            "price": 82990,
            "original_price": 94990,
            "rating": 4.6,
            "review_count": 290,
            "url": "https://market.yandex.ru/product/melitta-barista-ts-006",
            "in_stock": True,
            "seller_id": "ya_seller_melitta",
            "seller_name": "Melitta Official",
            "reviews": [
                {"id": "yr263", "text": "Управление через Bluetooth — варю кофе не вставая с дивана! 21 напиток, два бункера для зёрен. Немецкое качество. Кофе вкусный, молочная пенка идеальная.", "rating": 5, "date": "2025-03-06", "verified_purchase": True, "helpful_count": 32},
                {"id": "yr264", "text": "Приложение Melitta Companion — создаёшь свои рецепты, делишься с друзьями. Два бункера — можно разные сорта. Автокапучинатор работает отлично. Дороговата, но качество на высоте.", "rating": 4, "date": "2025-02-14", "verified_purchase": True, "helpful_count": 21},
                {"id": "yr265", "text": "Между Saeco и Melitta выбрал Melitta — дешевле и с Bluetooth. Кофе отличный, молочная система удобная. Шумная при помоле, но это все зерновые такие. Рекомендую.", "rating": 4, "date": "2025-01-20", "verified_purchase": True, "helpful_count": 15}
            ]
        }
    ]
}


def merge_data(file_path: Path, new_data: dict):
    """Read existing JSON, append new products to each category."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for category, products in new_data.items():
        if category in data["categories"]:
            data["categories"][category].extend(products)
        else:
            data["categories"][category] = products

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Count
    total = sum(len(prods) for prods in data["categories"].values())
    new_count = sum(len(prods) for prods in new_data.values())
    print(f"  {file_path.name}: added {new_count} products, total now {total}")


def main():
    print("Generating additional mock data for MarketMind...\n")

    merge_data(BASE_DIR / "ozon_products.json", OZON_NEW)
    merge_data(BASE_DIR / "wb_products.json", WB_NEW)
    merge_data(BASE_DIR / "yandex_products.json", YANDEX_NEW)

    print("\nDone! Cross-marketplace overlapping products:")
    print("  - Bose QuietComfort Ultra Headphones (ozon, wb, yandex)")
    print("  - Marshall Major IV Bluetooth (ozon, wb, yandex)")
    print("  - Beats Solo 4 Wireless (ozon, wb, yandex)")
    print("  - HP Pavilion 15 (ozon, wb, yandex)")
    print("  - MSI Thin 15 B12UC (ozon, wb, yandex)")
    print("  - Acer Aspire 5 A515 (ozon, wb, yandex)")
    print("  - Apple iPhone 15 128GB (ozon, wb, yandex)")
    print("  - POCO X6 Pro 5G (ozon, wb, yandex)")
    print("  - Nothing Phone (2) (ozon, wb, yandex)")
    print("  - Dyson V15 Detect Absolute (ozon, wb, yandex)")
    print("  - Ecovacs Deebot T30 Omni (ozon, wb, yandex)")
    print("  - Samsung Jet Bot AI+ (ozon, wb, yandex)")
    print("  - Sony Bravia XR 55A80L (ozon, wb, yandex)")
    print("  - Haier 55 Smart TV S4 (ozon, yandex)")
    print("  - Philips 55PUS8808 Ambilight (ozon, wb, yandex)")
    print("  - OnePlus Pad 2 (ozon, wb, yandex)")
    print("  - iPad 10 поколения (ozon, wb)")
    print("  - Xiaomi Watch 2 Pro (ozon, wb, yandex)")
    print("  - TicWatch Pro 5 Enduro (wb, yandex)")
    print("  - Saeco Xelsis Suprema (ozon, wb, yandex)")
    print("  - Melitta Barista TS Smart (ozon, wb, yandex)")
    print("  - Nespresso Vertuo Next (wb, yandex)")


if __name__ == "__main__":
    main()
