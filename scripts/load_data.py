import pandas as pd
from sqlalchemy import create_engine

# Настройки подключения к базе данных
DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/postgres'

# Путь к файлу CSV
csv_file_path = './data/supermarket_data.csv'

# Загрузка данных
data = pd.read_csv(csv_file_path)

# Удаляем первую колонку (нумерация строк)
data = data.iloc[:, 1:]

# Переименовываем колонки для соответствия таблице
data.columns = [
    'organization', 'sale_date', 'receipt_number', 'register_number',
    'transaction_number', 'cashier_name', 'article_number',
    'product_name', 'quantity', 'total_amount', 'discount'
]

# Приведение типов данных
data['sale_date'] = pd.to_datetime(data['sale_date'])  # Преобразуем дату
data['quantity'] = data['quantity'].astype(int)
data['total_amount'] = data['total_amount'].astype(float)
data['discount'] = data['discount'].fillna(0).astype(float)

# Подключение к базе данных
engine = create_engine(DATABASE_URI)

# Очистка таблицы перед загрузкой
def truncate_table():
    with engine.connect() as connection:
        connection.execute("TRUNCATE TABLE supermarket_sales.sales RESTART IDENTITY CASCADE;")

truncate_table()

# Загрузка данных в таблицу с указанием схемы
data.to_sql('sales', engine, schema='supermarket_sales', if_exists='append', index=False)

print("Данные успешно загружены в базу данных!")
