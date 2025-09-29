BEGIN TRANSACTION;

-- Rebuild employees table
CREATE TABLE employees_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);
INSERT INTO employees_new (name, position, phone, email)
SELECT name, position, phone, email FROM employees ORDER BY id;
DROP TABLE employees;
ALTER TABLE employees_new RENAME TO employees;

-- Rebuild orders table
CREATE TABLE orders_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_point_id INTEGER,
    description TEXT,
    order_date TEXT NOT NULL,
    status TEXT,
    amount REAL DEFAULT 0,
    FOREIGN KEY (trade_point_id) REFERENCES trade_points(id)
);
INSERT INTO orders_new (trade_point_id, description, order_date, status, amount)
SELECT trade_point_id, description, order_date, status, amount FROM orders ORDER BY id;
DROP TABLE orders;
ALTER TABLE orders_new RENAME TO orders;

-- Rebuild raw_materials table
CREATE TABLE raw_materials_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    quantity REAL NOT NULL,
    supplier_id INTEGER NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
INSERT INTO raw_materials_new (name, unit, quantity, supplier_id)
SELECT name, unit, quantity, supplier_id FROM raw_materials ORDER BY id;
DROP TABLE raw_materials;
ALTER TABLE raw_materials_new RENAME TO raw_materials;

-- Rebuild suppliers table
CREATE TABLE suppliers_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);
INSERT INTO suppliers_new (name, contact_person, phone, email)
SELECT name, contact_person, phone, email FROM suppliers ORDER BY id;
DROP TABLE suppliers;
ALTER TABLE suppliers_new RENAME TO suppliers;

-- Rebuild trade_points table
CREATE TABLE trade_points_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);
INSERT INTO trade_points_new (name, address)
SELECT name, address FROM trade_points ORDER BY id;
DROP TABLE trade_points;
ALTER TABLE trade_points_new RENAME TO trade_points;

-- Rebuild work_schedules table
CREATE TABLE work_schedules_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
INSERT INTO work_schedules_new (employee_id, day, start_time, end_time)
SELECT employee_id, day, start_time, end_time FROM work_schedules ORDER BY id;
DROP TABLE work_schedules;
ALTER TABLE work_schedules_new RENAME TO work_schedules;

COMMIT; 