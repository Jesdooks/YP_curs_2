import sqlite3
import os

DB_PATH = 'bakery.db'

def get_connection():
    """Establish connection to SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Create database tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trade_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        inn TEXT NOT NULL,
        kpp TEXT NOT NULL,
        ogrn TEXT NOT NULL,
        property_value REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        phone TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        phone TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_point_id INTEGER,
        description TEXT,
        order_date DATE,
        status TEXT,
        amount REAL,
        material_costs REAL,
        labor_costs REAL,
        operational_costs REAL,
        FOREIGN KEY (trade_point_id) REFERENCES trade_points(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        supplier_id INTEGER,
        quantity REAL,
        unit TEXT,
        price REAL DEFAULT 0,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS work_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        day TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS delivery_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_point_id INTEGER,
        day TEXT NOT NULL,
        delivery_time TEXT NOT NULL,
        FOREIGN KEY (trade_point_id) REFERENCES trade_points(id)
    )
    ''')
    
    # Создаем временную таблицу для menu_items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            event TEXT NOT NULL,
            event_date TEXT NOT NULL,
            delivery_time TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            order_items TEXT,
            total_price REAL,
            status TEXT DEFAULT 'новый',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Проверяем наличие колонок
    cursor.execute("PRAGMA table_info(customer_orders)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'order_items' not in columns:
        cursor.execute("ALTER TABLE customer_orders ADD COLUMN order_items TEXT")
    if 'total_price' not in columns:
        cursor.execute("ALTER TABLE customer_orders ADD COLUMN total_price REAL")
    if 'status' not in columns:
        cursor.execute("ALTER TABLE customer_orders ADD COLUMN status TEXT DEFAULT 'новый'")
    
    # Initialize menu items
    menu_items = [
        ("Хлеб пшеничный (1 кг)", 68),
        ("Хлеб ржано-пшеничный (1 кг)", 62),
        ("Хлеб ржаной (1 кг)", 61),
        ("Батон нарезной (400 г)", 28),
        ("Багет французский (300 г)", 45),
        ("Булочка с маком (80 г)", 20),
        ("Булочка с повидлом (80 г)", 22),
        ("Булочка с изюмом (80 г)", 23),
        ("Слойка с яблоком (100 г)", 32),
        ("Слойка с творогом (100 г)", 34),
        ("Круассан классический (60 г)", 38),
        ("Круассан с шоколадом (60 г)", 44),
        ("Плюшка московская (100 г)", 29),
        ("Булочка для гамбургера (70 г)", 16),
        ("Булочка для хот-дога (60 г)", 15),
        ("Пирожок с картошкой (80 г)", 28),
        ("Пирожок с капустой (80 г)", 27),
        ("Пирожок с мясом (80 г)", 35),
        ("Лепёшка пшеничная (150 г)", 26),
        ("Лепёшка узбекская (250 г)", 38),
        ("Хлеб бородинский (400 г)", 32),
        ("Хлеб зерновой (400 г)", 37),
        ("Хлеб бездрожжевой (400 г)", 41),
        ("Хлеб с отрубями (400 г)", 36),
        ("Хлеб цельнозерновой (400 г)", 39)
    ]
    
    # Проверяем, существует ли таблица menu_items
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='menu_items'")
    if cursor.fetchone() is None:
        # Если таблицы нет, создаем её
        cursor.execute('''
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        ''')
        # Вставляем начальные данные
        cursor.executemany("INSERT INTO menu_items (name, price) VALUES (?, ?)", menu_items)
    else:
        # Если таблица существует, сохраняем текущие данные
        cursor.execute("SELECT name, price FROM menu_items")
        existing_items = cursor.fetchall()
        
        # Удаляем старую таблицу и создаем новую
        cursor.execute("DROP TABLE menu_items")
        cursor.execute('''
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        ''')
        
        # Восстанавливаем данные с новыми ID
        cursor.executemany("INSERT INTO menu_items (name, price) VALUES (?, ?)", existing_items)
    
    conn.commit()
    conn.close() 