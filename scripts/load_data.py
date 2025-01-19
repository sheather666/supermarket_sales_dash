import pandas as pd
from sqlalchemy import create_engine, text

# Настройки подключения к базе данных
DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/postgres'

# Путь к SQL-файлу
sql_file_path = './scripts/create_db.sql'

# Подключение к базе данных
engine = create_engine(DATABASE_URI)

# Функция для выполнения SQL-файла
def execute_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()  # Считываем содержимое SQL-файла

    with engine.connect() as connection:
        trans = connection.begin()  # Начинаем транзакцию
        try:
            connection.execute(text(sql_commands))  # Выполняем SQL-команды
            trans.commit()  # Подтверждаем изменения
            print("SQL-файл успешно выполнен.")
        except Exception as e:
            trans.rollback()  # Откатываем изменения при ошибке
            print(f"Ошибка при выполнении SQL-файла: {e}")

# Выполняем SQL-скрипт
execute_sql_file(sql_file_path)

# Дальнейшие действия, например, загрузка данных
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

# Очистка таблицы перед загрузкой
def truncate_table():
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            connection.execute(text("TRUNCATE TABLE supermarket_sales.sales RESTART IDENTITY CASCADE;"))
            trans.commit()
            print("Таблица успешно очищена.")
        except Exception as e:
            trans.rollback()
            print(f"Ошибка при очистке таблицы: {e}")

truncate_table()

# Загрузка данных в таблицу с указанием схемы
data.to_sql('sales', engine, schema='supermarket_sales', if_exists='append', index=False)

print("Данные успешно загружены в базу данных!")
