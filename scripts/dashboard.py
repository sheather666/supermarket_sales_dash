import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Подключение к базе данных
DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)

# Функция для загрузки данных с фильтрацией
def load_filtered_data(date_range, product_keywords, cashier_keywords):
    filters = []
    if len(date_range) == 2:
        filters.append(f"sale_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    if product_keywords.strip():
        product_conditions = " OR ".join([f"product_name ILIKE '%%{kw.strip()}%%'" for kw in product_keywords.split(',') if kw.strip()])
        filters.append(f"({product_conditions})")
    if cashier_keywords.strip():
        cashier_conditions = " OR ".join([f"cashier_name ILIKE '%%{kw.strip()}%%'" for kw in cashier_keywords.split(',') if kw.strip()])
        filters.append(f"({cashier_conditions})")
    
    where_clause = " AND ".join(filters) if filters else "1=1"

    query = f"""
        SELECT *
        FROM supermarket_sales.sales
        WHERE {where_clause}
    """
    return pd.read_sql(query, engine)

# Заголовок
st.title("📊 Дашборд продаж супермаркета")
st.markdown(
    "Добро пожаловать в дашборд анализа продаж супермаркета! Используйте фильтры слева для исследования данных. "
    "Графики и таблицы будут обновляться автоматически."
)

# **Фильтры**
st.sidebar.header("🔎 Фильтры")

# Фильтр по диапазону дат
date_query = "SELECT MIN(sale_date) AS min_date, MAX(sale_date) AS max_date FROM supermarket_sales.sales"
dates = pd.read_sql(date_query, engine)
min_date = dates['min_date'][0]
max_date = dates['max_date'][0]
date_range = st.sidebar.date_input(
    "Выберите диапазон дат",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

# Фильтр по товарам (с поиском)
product_keywords = st.sidebar.text_input("Введите ключевые слова для товаров (через запятую)", "")

# Фильтр по кассирам (с поиском)
cashier_keywords = st.sidebar.text_input("Введите ключевые слова для кассиров (через запятую)", "")

# Загрузка данных
data = load_filtered_data(date_range, product_keywords, cashier_keywords)

# **Раздел 1: Общая информация**
st.header("📌 Общая информация")
total_revenue = data['total_amount'].sum()
total_sales = data['quantity'].sum()
avg_receipt = total_revenue / data['receipt_number'].nunique() if data['receipt_number'].nunique() > 0 else 0
st.metric("Общая выручка", f"{total_revenue:,.2f} руб.")
st.metric("Общее количество продаж", total_sales)
st.metric("Средний чек", f"{avg_receipt:,.2f} руб.")

# **Раздел 2: Тренды**
st.header("📈 Тренды")
# Динамика выручки по дням
revenue_by_day = data.groupby('sale_date')['total_amount'].sum()
st.line_chart(revenue_by_day)
st.caption("Этот график показывает, как выручка изменялась с течением времени.")

# **Раздел 3: Топы**
st.header("🏆 Топы")
# Топ-10 товаров
st.subheader("Топ-10 товаров по количеству продаж")
top_products = data.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)
st.caption("На этом графике представлены самые популярные товары по количеству продаж.")

# Топ-10 кассиров
st.subheader("Топ-10 кассиров по выручке")
top_cashiers = data.groupby('cashier_name')['total_amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_cashiers)
st.caption("Этот график показывает, какие кассиры генерируют наибольшую выручку.")

# **Раздел 4: Популярные комбинации товаров**
st.header("🔗 Популярные комбинации товаров")
basket_data = data.groupby('receipt_number')['product_name'].apply(list)
from collections import Counter
from itertools import combinations

basket_combinations = Counter()
for basket in basket_data:
    basket_combinations.update(combinations(sorted(basket), 2))

top_combinations = basket_combinations.most_common(10)
combos = [f"{a} & {b}" for (a, b), count in top_combinations]
counts = [count for (a, b), count in top_combinations]

st.subheader("График популярных комбинаций товаров")
combos_df = pd.DataFrame({'Комбинация': combos, 'Количество': counts})
st.bar_chart(combos_df.set_index('Комбинация'))
st.table(combos_df)

# **Раздел 5: Товары со скидкой**
st.header("💸 Товары со скидкой")
discount_data = data[data['discount'] > 0]
discount_revenue = discount_data['total_amount'].sum()
discount_share = (discount_revenue / total_revenue) * 100 if total_revenue > 0 else 0
st.metric("Выручка со скидками", f"{discount_revenue:,.2f} руб.")
st.metric("Доля выручки со скидками", f"{discount_share:.2f} %")
top_discounted_products = discount_data.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_discounted_products)