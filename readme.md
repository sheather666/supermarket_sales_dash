# Supermarket Sales Dashboard

Этот проект представляет собой интерактивный дашборд для анализа данных о продажах супермаркета. Данные загружаются из базы данных PostgreSQL, а основные вычисления выполняются на стороне базы. Дашборд позволяет исследовать данные, используя фильтры и визуализации, и предоставляет ключевую информацию для бизнеса.

## Структура проекта

```
SUPERMARKET_SALES_DASH
│
├── data
│   └── supermarket_data.csv      # Исходные данные в формате CSV
│
├── notebooks
│   └── analysis.ipynb            # Jupyter Notebook для анализа данных
│
├── scripts
│   ├── create_db.sql             # SQL скрипт для создания базы данных и представлений
│   ├── dashboard.py              # Код для Streamlit-дашборда
│   └── load_data.py              # Скрипт для загрузки данных в базу
│
├── venv                          # Виртуальное окружение проекта
├── .gitignore                    # Файл для исключения ненужных файлов из Git
├── README.md                     # Документация проекта
├── REPORT.md                     # Отчет о выполнении проекта
└── requirements.txt              # Список зависимостей для проекта
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your_username/supermarket_sales_dash.git
   cd supermarket_sales_dash
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте PostgreSQL и создайте базу данных, выполнив скрипт `create_db.sql`:
   ```bash
   psql -U postgres -f scripts/create_db.sql
   ```

5. Загрузите данные в базу:
   ```bash
   python scripts/load_data.py
   ```

## Использование

1. Запустите дашборд:
   ```bash
   streamlit run scripts/dashboard.py
   ```

2. Откройте в браузере URL, указанный Streamlit (обычно `http://localhost:8501`).

## Основные функции дашборда

- Фильтры:
  - По диапазону дат
  - По товарам (поиск по ключевым словам)
  - По кассирам (поиск по ключевым словам)

- Визуализации:
  - Динамика выручки по дням
  - Топ-10 товаров по количеству продаж
  - Топ-10 кассиров по выручке
  - Популярные комбинации товаров
  - Товары со скидками

- Метрики:
  - Общая выручка
  - Общее количество продаж
  - Средний чек
  - Выручка и доля выручки со скидками

## Зависимости

Все зависимости перечислены в файле `requirements.txt`. Убедитесь, что PostgreSQL установлен и настроен на вашем устройстве.

## Лицензия

Этот проект распространяется под лицензией MIT. Для получения дополнительной информации ознакомьтесь с файлом LICENSE.
