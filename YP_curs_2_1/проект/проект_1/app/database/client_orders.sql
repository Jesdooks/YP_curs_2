-- Создание таблицы для клиентских заказов
CREATE TABLE IF NOT EXISTS client_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    description TEXT NOT NULL,
    event TEXT NOT NULL,
    event_address TEXT NOT NULL,
    delivery_time TEXT NOT NULL,
    status TEXT DEFAULT 'Новый',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 