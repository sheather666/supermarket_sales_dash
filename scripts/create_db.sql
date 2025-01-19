CREATE SCHEMA IF NOT EXISTS supermarket_sales;

CREATE TABLE IF NOT EXISTS supermarket_sales.sales (
    id SERIAL PRIMARY KEY, -- Уникальный идентификатор строки
    organization VARCHAR(255) NOT NULL, -- Название организации
    sale_date DATE NOT NULL, -- Дата покупки
    receipt_number VARCHAR(50) NOT NULL, -- Номер чека
    register_number VARCHAR(50) NOT NULL, -- Номер кассы
    transaction_number VARCHAR(50) NOT NULL, -- Номер транзакции
    cashier_name VARCHAR(100) NOT NULL, -- Имя кассира
    article_number VARCHAR(50) NOT NULL, -- Номер артикула
    product_name VARCHAR(255) NOT NULL, -- Название товара
    quantity INTEGER NOT NULL, -- Количество
    total_amount NUMERIC(10, 2) NOT NULL, -- Сумма покупки
    discount NUMERIC(10, 2) DEFAULT 0.00 -- Скидка
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_sale_date ON supermarket_sales.sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_receipt_number ON supermarket_sales.sales (receipt_number);
CREATE INDEX IF NOT EXISTS idx_cashier_name ON supermarket_sales.sales (cashier_name);
CREATE INDEX IF NOT EXISTS idx_product_name ON supermarket_sales.sales (product_name);

-- Представление: Общая выручка, количество продаж и средний чек
CREATE OR REPLACE VIEW supermarket_sales.sales_summary AS
SELECT 
    SUM(total_amount) AS total_revenue,
    SUM(quantity) AS total_sales,
    AVG(total_amount / NULLIF(receipt_number::NUMERIC, 0)) AS avg_receipt
FROM supermarket_sales.sales;

-- Представление: Топ-10 товаров по количеству продаж
CREATE OR REPLACE VIEW supermarket_sales.top_products AS
SELECT 
    product_name, 
    SUM(quantity) AS total_quantity
FROM supermarket_sales.sales
GROUP BY product_name
ORDER BY total_quantity DESC
LIMIT 10;

-- Представление: Топ-10 кассиров по выручке
CREATE OR REPLACE VIEW supermarket_sales.top_cashiers AS
SELECT 
    cashier_name, 
    SUM(total_amount) AS total_revenue
FROM supermarket_sales.sales
GROUP BY cashier_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Представление: Динамика выручки по дням
CREATE OR REPLACE VIEW supermarket_sales.revenue_by_day AS
SELECT 
    sale_date,
    SUM(total_amount) AS daily_revenue
FROM supermarket_sales.sales
GROUP BY sale_date
ORDER BY sale_date;

-- Представление: Товары со скидкой
CREATE OR REPLACE VIEW supermarket_sales.discounted_products AS
SELECT 
    product_name,
    SUM(total_amount) AS discounted_revenue,
    SUM(quantity) AS discounted_quantity
FROM supermarket_sales.sales
WHERE discount > 0
GROUP BY product_name
ORDER BY discounted_revenue DESC;
