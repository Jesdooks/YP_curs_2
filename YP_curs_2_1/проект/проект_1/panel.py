import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from app.database.db import initialize_db, get_connection
from main import BakeryApp
import ctypes
import os
import re
import math
from tkmacosx import Button
import time
import json
  
class GradientButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, width=250, height=45, 
                 hover_color="#E0A8A3", text_color="#333333", font=("Arial", 16, "bold")):
        super().__init__(master, width=width, height=height, highlightthickness=0)
        self.command = command
        self.width = width
        self.height = height
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.text = text
        
        # Создаем тень
        self.shadow = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg="#A7F3D0")
        self.shadow.place(x=4, y=4)
        
        # Основной холст для кнопки
        self.button_canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.button_canvas.place(x=0, y=0)
        
        self.draw_gradient()
        self.create_text()
        
        # Привязываем события (для наведения)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        # Делаем кнопку кликабельной
        self.button_canvas.bind("<Enter>", self.on_enter)
        self.button_canvas.bind("<Leave>", self.on_leave)
        self.button_canvas.bind("<Button-1>", self.on_click)
        self.button_canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def draw_gradient(self):
        # Цвета для градиента
        color1 = "#FFFACD"  # Нежно-желтый
        color2 = "#FFB6C1"  # Нежно-розовый
        
        # Создаем градиент от нежно-желтого к нежно-розовому
        for i in range(self.height):
            r1, g1, b1 = self.winfo_rgb(color1)
            r2, g2, b2 = self.winfo_rgb(color2)
            
            r = int(r1 + (r2 - r1) * i / self.height)
            g = int(g1 + (g2 - g1) * i / self.height)
            b = int(b1 + (b2 - b1) * i / self.height)
            
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            self.button_canvas.create_line(0, i, self.width, i, fill=color)
        
        # Обновляем цвет тени на нежно-желтый
        self.shadow.config(bg="#FFFACD")
    
    def create_text(self):
        #размещаю текст по центру
        self.button_canvas.create_text(
            self.width//2, self.height//2,
            text=self.text,
            fill=self.text_color,
            font=self.font
        )
    
    def on_enter(self, event):
        #при наведение чтобы кнопка меняла цвет
        self.button_canvas.delete("all")
        self.button_canvas.create_rectangle(0, 0, self.width, self.height, fill=self.hover_color)
        self.create_text()
    
    def on_leave(self, event):
        #при уходе чтобы кнопка меняла цвет обратно
        self.button_canvas.delete("all")
        self.draw_gradient()
        self.create_text()
    
    def on_click(self, event):
        #при нажатии чтобы кнопка закрашивалась цветом наведения
        self.button_canvas.delete("all")
        self.button_canvas.create_rectangle(0, 0, self.width, self.height, fill="#A7F3D0")
        self.create_text()
    
    def on_release(self, event):
        #при нажатии выхывается команда
        if self.command:
            self.command()
        self.on_leave(None)

class BakeryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления хлебопекарней")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        if os.name == "nt":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        elif os.name == "posix":
            self.root.tk.call('tk', 'scaling', 2.0)
        
        self.initialize_database()
        self.setup_styles()
        self.create_login_window()

    def initialize_database(self):
        #инициализация бд и создание таблиц
        initialize_db()
        conn = get_connection()
        cursor = conn.cursor()
        # Проверяем, есть ли поле description в customer_orders
        cursor.execute("PRAGMA table_info(customer_orders)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'description' not in columns:
            try:
                cursor.execute("ALTER TABLE customer_orders ADD COLUMN description TEXT NOT NULL DEFAULT ''")
                conn.commit()
            except Exception:
                pass
        #табл пользователь
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        #табл покупатель
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        try:
            #добавление пользователя (по умолчанию лог/пар 0 и 0)
            cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                          ("0", "0"))
            conn.commit()
        except sqlite3.Error:
            pass
        conn.close()

    def setup_styles(self):
        #настройка стилей элементов интерфейса
        style = ttk.Style()
        style.theme_use('clam')
        
        #стиль фрейма
        style.configure("TFrame", background="#E0E0E0")
        style.configure("TLabel", background="#E0E0E0", foreground="#4A4A4A", font=("Helvetica", 14))
        style.configure("TEntry", fieldbackground="#FFFFFF", font=("Helvetica", 12), relief="flat", borderwidth=2)
        style.map("TEntry", background=[("focus", "#FFF9B0")])
        
        style.configure("TButton",
                       font=("Helvetica", 12, "bold"),
                       padding=10,
                       background="#A3DFFA",
                       foreground="#4A4A4A",
                       borderwidth=0,
                       relief="flat")
        style.map("TButton",
                 background=[("active", "#B8E994"), ("pressed", "#B8E994")],
                 foreground=[("active", "#4A4A4A")])
        
        style.configure("Header.TLabel",
                       font=("Helvetica", 28, "bold"),
                       background="#E0E0E0",
                       foreground="black")
        
        style.configure("TCombobox",
                       font=("Helvetica", 12),
                       padding=5,
                       background="#FFFFFF",
                       fieldbackground="#FFFFFF",
                       foreground="#4A4A4A")
        style.map("TCombobox",
                 fieldbackground=[("focus", "#FFF9B0")])
        
        style.configure("Customer.TFrame", background="#E0E0E0")

    #фон    
    def create_background(self, canvas, width, height):
        #генерирую фигуры
        self.bg_shapes = []
        canvas.delete("all")

        #цвет градиента 
        start_color = "#6B728E"
        end_color = "#A7F3D0"

        r1, g1, b1 = self.root.winfo_rgb(start_color)
        r2, g2, b2 = self.root.winfo_rgb(end_color)
        r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
        r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
        for i in range(width):
            r = int(r1 + (r2 - r1) * i / width)
            g = int(g1 + (g2 - g1) * i / width)
            b = int(b1 + (b2 - b1) * i / width)
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(i, 0, i, height, fill=color)
        # Генерируем фигуры и сохраняем их параметры
        for _ in range(50):
            x = random.randint(-50, width + 50)
            y = random.randint(-50, height + 50)
            size = random.randint(30, 60)
            shape_type = random.choice(["circle", "triangle", "pentagon", "star"])
            fill_color = random.choice(["#D8B4FE", "#6EE7B7", "#FCA5A5", "#93C5FD", "#FCD34D"])
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            self.bg_shapes.append({
                "type": shape_type, "x": x, "y": y, "size": size, "color": fill_color,
                "dx": dx, "dy": dy, "id": None
            })
        self.animate_background(canvas, width, height)

    #анимация фона
    def animate_background(self, canvas, width, height):
        canvas.delete("shapes")
        for shape in self.bg_shapes:
            shape["x"] += shape["dx"]
            shape["y"] += shape["dy"]

            # Отражение от границ
            if shape["x"] < -60 or shape["x"] > width + 10:
                shape["dx"] *= -1
            if shape["y"] < -60 or shape["y"] > height + 10:
                shape["dy"] *= -1
            x, y, size, color = shape["x"], shape["y"], shape["size"], shape["color"]
            if shape["type"] == "circle":
                shape["id"] = canvas.create_oval(x, y, x + size, y + size, fill=color, stipple="gray50", tags="shapes")
            elif shape["type"] == "triangle":
                canvas.create_polygon(
                    x, y,
                    x + size, y,
                    x + size // 2, y - size,
                    fill=color, stipple="gray50", tags="shapes"
                )
            elif shape["type"] == "pentagon":
                points = []
                for i in range(5):
                    angle = i * 72 - 90
                    px = x + size * 0.5 + size * 0.5 * math.cos(math.radians(angle))
                    py = y + size * 0.5 + size * 0.5 * math.sin(math.radians(angle))
                    points.extend([px, py])
                canvas.create_polygon(points, fill=color, stipple="gray50", tags="shapes")
            elif shape["type"] == "star":
                points = []
                for i in range(10):
                    angle = i * 36 - 90
                    radius = size * 0.5 if i % 2 == 0 else size * 0.2
                    px = x + size * 0.5 + radius * math.cos(math.radians(angle))
                    py = y + size * 0.5 + radius * math.sin(math.radians(angle))
                    points.extend([px, py])
                canvas.create_polygon(points, fill=color, stipple="gray50", tags="shapes")
        canvas.after(30, lambda: self.animate_background(canvas, width, height))

    #окно входа 
    def create_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # 1. Градиентный фон через Canvas
        canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.create_background(canvas, 800, 600)
    
    # 2. Разместить Frame поверх Canvas через create_window
        main_frame = ttk.Frame(self.root, style="TFrame")
        canvas.create_window(400, 300, window=main_frame, anchor="center")
    
    # 3. Добавлять элементы в main_frame как обычно
        ttk.Label(main_frame, text="Добро пожаловать!", style="Header.TLabel").pack(pady=(60, 30))
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(fill="x", padx=20)
        ttk.Label(login_frame, text="Логин:", font=('Arial', 14, 'bold')).pack(anchor="w", pady=(10, 0))
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(login_frame, text="Пароль:", font=('Arial', 14, 'bold')).pack(anchor="w")
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.pack(fill="x", pady=(0, 20))
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        btn_admin = GradientButton(button_frame, text="Войти как администратор", command=self.login_admin)
        btn_admin.pack(side="left", padx=10)
        btn_client = GradientButton(button_frame, text="Войти как клиент", command=self.show_customer_form)
        btn_client.pack(side="left", padx=10)


    def login_admin(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                          (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                for widget in self.root.winfo_children():
                    widget.destroy()
                self.root.geometry("1200x800")
                BakeryApp(self.root)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
                
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")

    def show_customer_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Оформление заказа")
        
        canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.create_background(canvas, 800, 600)
        
        main_container = ttk.Frame(self.root, style="Customer.TFrame")
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)
        
        canvas = tk.Canvas(main_container, highlightthickness=0, bg="#E0E0E0")
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Customer.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(scrollable_frame, text="Оформление предварительного заказа",
                 style="Header.TLabel").pack(pady=(20, 20))
        
        form_container = ttk.Frame(scrollable_frame, style="Customer.TFrame")
        form_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Поля формы
        placeholders = {
            "full_name_entry": "Введите ФИО полностью",
            "phone_entry": "Формат: +7XXXXXXXXXX или 8XXXXXXXXXX",
            "address_entry": "Введите полный адрес доставки",
            "email_entry": "example@domain.com",
            "event_entry": "Название и тип мероприятия",
            "event_date_entry": "Формат: ДД-ММ-ГГГГ (например, 01-02-2024)",
            "delivery_time_entry": "Формат: ЧЧ:ММ (например, 14:30)"
        }
        
        fields = [
            ("ФИО*", "full_name_entry"),
            ("📱 Телефон*", "phone_entry"),
            ("🏠 Адрес*", "address_entry"),
            ("📧 Email*", "email_entry"),
            ("🎉 Мероприятие*", "event_entry"),
            ("📅 Дата мероприятия*", "event_date_entry"),
            ("⏰ Время доставки (ЧЧ:ММ)*", "delivery_time_entry")
        ]
        
        self.entries = {}
        #доп текст для пользователя (подсказки)
        def add_placeholder(entry, placeholder_text):
            def on_focus_in(event):
                if entry.get() == placeholder_text:
                    entry.delete(0, tk.END)
                    entry.config(foreground='black')
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder_text)
                    entry.config(foreground='gray')
            entry.insert(0, placeholder_text)
            entry.config(foreground='gray')
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        for label_text, field_name in fields:
            field_frame = ttk.Frame(form_container, style="Customer.TFrame")
            field_frame.pack(fill="x", pady=(5, 0))
            ttk.Label(field_frame, text=label_text, font=("Helvetica", 14)).pack(anchor="w", pady=(5, 0))
            entry = ttk.Entry(field_frame, font=("Helvetica", 14))
            entry.pack(fill="x", pady=(0, 5))
            add_placeholder(entry, placeholders.get(field_name, ""))
            self.entries[field_name] = entry
        
        # Кнопка меню и область заказа
        order_frame = ttk.Frame(form_container, style="Customer.TFrame")
        order_frame.pack(fill="x", pady=10)
        btn_menu = GradientButton(order_frame, text="Меню изделий",
                                command=self.show_menu)
        btn_menu.pack(pady=20)
        
        self.order_display_frame = ttk.Frame(form_container, style="Customer.TFrame")
        self.order_display_frame.pack(fill="x", pady=10)
        
        self.total_amount_var = tk.StringVar(value="Итого: 0.00 руб.")
        total_label = ttk.Label(form_container, textvariable=self.total_amount_var,
                              font=("Helvetica", 15, "bold"), background="#E0E0E0")
        total_label.pack(anchor="e", pady=(5, 0), padx=10)
        
        # Инициализация заказа
        self.order = {}
        
        button_frame = ttk.Frame(form_container)
        button_frame.pack(fill="x", pady=(20, 20))
        
        btn_submit = GradientButton(button_frame, text="✅ Отправить заказ",
                                  command=self.submit_order)
        btn_submit.pack(side="left", padx=10)
        
        btn_back = GradientButton(button_frame, text="⬅️ Вернуться",
                                command=self.create_login_window)
        btn_back.pack(side="left", padx=10)
        
        ttk.Label(scrollable_frame, text="* - обязательные поля",
                 font=("Helvetica", 12, "italic"), background="#E0E0E0").pack(pady=(0, 10))
        
        self.update_order_display()

    def show_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Выбор изделий")
        menu_window.geometry("400x500")
        menu_window.configure(bg="#E0E0E0")
        menu_window.grab_set()  # Make window modal
        menu_window.transient(self.root)  # Make window always on top of parent
        
        #фрейм для меню
        main_frame = ttk.Frame(menu_window)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        #canvas для меню чтобы пользоваться скролл баром
        canvas = tk.Canvas(main_frame, highlightthickness=0, bg="#E0E0E0")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        #фрейм для содержимого
        scrollable_frame = ttk.Frame(canvas, style="Customer.TFrame")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        #создаю окно для меню
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=365)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        #размещаю канвас и скролл бар
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        #наведение на скролл бар
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        #загружаю меню и бд
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu_items")
        menu_items = cursor.fetchall()
        conn.close()
        
        self.menu_item_qty_vars = {}
        #проверка на ввод кол-ва
        def validate_qty(new_value, item_id):
            if new_value == "":
                return True
            if new_value.isdigit():
                return True
            messagebox.showerror("Ошибка", "Введите только целое число для количества!")
            self.menu_item_qty_vars[item_id].set("0")
            return False
        
        #список для меню
        for item in menu_items:
            item_frame = ttk.Frame(scrollable_frame, style="Customer.TFrame")
            item_frame.pack(fill="x", pady=5, padx=10)
            
            ttk.Label(item_frame, text=f"{item['name']} ({item['price']:.2f} руб.)",
                     font=("Helvetica", 13)).pack(side="left")
            
            qty_var = tk.StringVar(value=str(self.order.get(item['id'], 0)))
            self.menu_item_qty_vars[item['id']] = qty_var
            vcmd = (menu_window.register(lambda nv, iid=item['id']: validate_qty(nv, iid)), '%P')
            qty_entry = ttk.Entry(item_frame, textvariable=qty_var, width=5,
                                font=("Helvetica", 13), validate='key', validatecommand=vcmd)
            qty_entry.pack(side="right", padx=5)
            qty_entry.bind("<FocusOut>", lambda e, iid=item['id']: self.update_order(iid))
            qty_entry.bind("<Return>", lambda e, iid=item['id']: self.update_order(iid))
            
            ttk.Label(item_frame, text="шт.", font=("Helvetica", 13)).pack(side="right")
        
        #фрейм для кнопок
        buttons_frame = ttk.Frame(scrollable_frame)
        buttons_frame.pack(fill="x", pady=20, padx=10)
        
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            menu_window.destroy()
        
        btn_done = GradientButton(buttons_frame, text="Готово", command=on_close)
        btn_done.pack(expand=True)

    #обновление заказов
    def update_order(self, item_id):
        qty = self.menu_item_qty_vars[item_id].get()
        if qty.isdigit() and int(qty) > 0:
            self.order[item_id] = int(qty)
        elif item_id in self.order:
            del self.order[item_id]
        self.update_order_display()

    def update_order_display(self):
        for widget in self.order_display_frame.winfo_children():
            widget.destroy()
        
        conn = get_connection()
        cursor = conn.cursor()
        total = 0.0
        
        for item_id, qty in self.order.items():
            cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if item:
                price = item['price'] * qty
                total += price
                item_frame = ttk.Frame(self.order_display_frame, style="Customer.TFrame")
                item_frame.pack(fill="x", pady=2)
                ttk.Label(item_frame, text=f"{item['name']} x{qty}",
                         font=("Helvetica", 13)).pack(side="left")
                ttk.Label(item_frame, text=f"{price:.2f} руб.",
                         font=("Helvetica", 13)).pack(side="right")
        
        conn.close()
        self.total_amount_var.set(f"Итого: {total:.2f} руб.")

    def validate_phone(self, phone):
        pattern = re.compile(r'^\+7\d{10}$|^8\d{10}$')
        return bool(pattern.match(phone))

    def validate_email(self, email):
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(pattern.match(email))

    def validate_time(self, time_str):
        pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        return bool(pattern.match(time_str))

    def submit_order(self):
        def get_entry_value(entry):
            value = entry.get().strip()
            placeholder = entry.get() if entry.cget("foreground") == "black" else ""
            return "" if value == placeholder else value

        full_name = get_entry_value(self.entries["full_name_entry"])
        phone = get_entry_value(self.entries["phone_entry"])
        address = get_entry_value(self.entries["address_entry"])
        email = get_entry_value(self.entries["email_entry"])
        event = get_entry_value(self.entries["event_entry"])
        event_date = get_entry_value(self.entries["event_date_entry"])
        delivery_time = get_entry_value(self.entries["delivery_time_entry"])
        
        required_fields = {
            "ФИО": full_name,
            "Телефон": phone,
            "Адрес": address,
            "Email": email,
            "Мероприятие": event,
            "Дата мероприятия": event_date,
            "Время доставки": delivery_time
        }
        
        for field_name, value in required_fields.items():
            if not value:
                messagebox.showwarning("Предупреждение", f"Заполните поле: {field_name}")
                return
                   
        if not self.validate_phone(phone):
            messagebox.showwarning("Предупреждение",
                                  "Неверный формат телефона. Используйте +7XXXXXXXXXX или 8XXXXXXXXXX")
            return
            
        if not self.validate_email(email):
            messagebox.showwarning("Предупреждение",
                                  "Неверный формат email")
            return
            
        if not self.validate_time(delivery_time):
            messagebox.showwarning("Предупреждение",
                                  "Неверный формат времени. Используйте ЧЧ:ММ")
            return
        
        if not self.order:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы одну позицию и укажите количество!")
            return
        
        # Валидация даты мероприятия
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", event_date):
            messagebox.showwarning("Предупреждение", "Неверный формат даты мероприятия. Используйте ДД-ММ-ГГГГ")
            return
        
        try:
            import datetime
            conn = get_connection()
            cursor = conn.cursor()
            order_lines = []
            order_items = []
            total = 0.0
            for item_id, qty in self.order.items():
                cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
                item = cursor.fetchone()
                if item:
                    order_lines.append(f"{item['name']} — {qty} шт. (по {item['price']:.2f} руб.)")
                    order_items.append({
                        'id': item_id,
                        'name': item['name'],
                        'price': item['price'],
                        'quantity': qty,
                        'sum': item['price'] * qty
                    })
                    total += item['price'] * qty
            description = "\n".join(order_lines)
            order_items_json = json.dumps(order_items, ensure_ascii=False)
            admin_description = (
                f"ФИО: {full_name}\n"
                f"Телефон: {phone}\n"
                f"Email: {email}\n"
                f"Адрес: {address}\n"
                f"Мероприятие: {event}\n"
                f"Дата мероприятия: {event_date}\n"
                f"Время доставки: {delivery_time}\n"
                f"Описание заказа: {description}"
            )
            order_date = datetime.datetime.now().strftime("%Y-%m-%d")
            status = "Новый"
            cursor.execute(
                """
                INSERT INTO customer_orders (full_name, phone, address, email, description, event, event_date, delivery_time, order_items, total_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (full_name, phone, address, email, description, event, event_date, delivery_time, order_items_json, total)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Ваш заказ успешно отправлен!")
            self.create_login_window()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {str(e)}")

    def load_preorders(self):
        # Очистить текущий список
        for item in self.preorders_tree.get_children():
            self.preorders_tree.delete(item)
        # Загрузить из базы
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, phone, address, event, event_date, delivery_time, description FROM customer_orders ORDER BY created_at DESC")
        for row in cursor.fetchall():
            self.preorders_tree.insert("", "end", values=(
                row['id'],
                row['full_name'],
                row['phone'],
                row['address'],
                row['event'],
                row['event_date'],
                row['delivery_time'],
                row['description']
            ))
        conn.close()

    def show_order_details(self, event):
        selected = self.orders_tree.selection()
        if not selected:
            return
        item = self.orders_tree.item(selected[0])['values']
        order_id = item[0]
        # Получаем описание заказа из customer_orders.description
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT description FROM customer_orders WHERE id=?", (order_id,))
            row = cursor.fetchone()
            conn.close()
            if not row or not row['description']:
                messagebox.showinfo("Информация о заказе", "Нет информации о заказанных позициях.")
                return
            description = row['description']
            # Парсим описание (ожидается формат: 'название — qty шт. (по price руб.)')
            lines = [l for l in description.split('\n') if l.strip()]
            total = 0.0
            details = []
            for line in lines:
                m = re.match(r"(.+?) — (\d+) шт\. \(по ([\d\.]+) руб\.\)", line)
                if m:
                    name, qty, price = m.group(1), int(m.group(2)), float(m.group(3))
                    cost = qty * price
                    total += cost
                    details.append(f"{name}: {qty} шт. × {price:.2f} руб. = {cost:.2f} руб.")
            msg = "\n".join(details)
            msg += f"\n\nОбщая стоимость: {total:.2f} руб."
            messagebox.showinfo("Информация о заказе", msg)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить детали заказа: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BakeryManagementApp(root)
    root.mainloop()