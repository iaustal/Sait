-- Создание базы данных
CREATE DATABASE electronic_store;




-- Таблица "Категории"
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица "Производители"
CREATE TABLE manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица "Продукты"
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
    manufacturer_id INT REFERENCES manufacturers(manufacturer_id) ON DELETE CASCADE
);
-- Таблица "Клиенты"
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);
-- Таблица "Заказы"
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Таблица "Отзывы"
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    rating INT NOT NULL,
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица "Автоматически обновляемая таблица"
CREATE TABLE automatically_updated_table (
    id SERIAL PRIMARY KEY,
    related_data TEXT
);

-- Вставка данных в таблицу "Категории"
INSERT INTO categories (name) VALUES
    ('Смартфоны'),
    ('Ноутбуки'),
    ('Телевизоры'),
    ('Наушники'),
    ('Планшеты'),
    ('Фотоаппараты');

-- Вставка данных в таблицу "Производители"
INSERT INTO manufacturers (name) VALUES
    ('Samsung'),
    ('Apple'),
    ('Sony'),
    ('Dell'),
    ('HP'),
    ('Canon');

-- Вставка данных в таблицу "Продукты"
INSERT INTO products (name, price, category_id, manufacturer_id) VALUES
    ('Samsung Galaxy S21', 799.99, 1, 1),
    ('MacBook Pro', 1499.99, 2, 2),
    ('Sony Bravia 4K', 999.99, 3, 3),
    ('Bose QuietComfort 35', 349.99, 4, 1),
    ('iPad Air', 499.99, 5, 2),
    ('Canon EOS 5D Mark IV', 2499.99, 6, 6);

-- Вставка данных в таблицу "Клиенты"
INSERT INTO customers (name, email) VALUES
    ('Иван Иванов', 'ivan@example.com'),
    ('Мария Смирнова', 'maria@example.com'),
    ('Алексей Петров', 'alex@example.com'),
    ('Елена Козлова', 'elena@example.com'),
    ('Дмитрий Сидоров', 'dmitry@example.com'),
    ('Анна Федорова', 'anna@example.com');

-- Вставка данных в таблицу "Заказы"
INSERT INTO orders (customer_id) VALUES
    (1),
    (2),
    (3),
    (1),
    (4),
    (5);

-- Вставка данных в таблицу "Отзывы"
INSERT INTO reviews (product_id, customer_id, rating, comment) VALUES
    (1, 1, 5, 'Отличный смартфон!'),
    (2, 3, 4, 'Мощный ноутбук, но дорогой.'),
    (3, 2, 5, 'Прекрасный телевизор.'),
    (4, 4, 5, 'Замечательные наушники с хорошим шумоподавлением.'),
    (5, 5, 4, 'Легкий и компактный планшет.'),
    (6, 6, 5, 'Отличный фотоаппарат для профессионалов.');
