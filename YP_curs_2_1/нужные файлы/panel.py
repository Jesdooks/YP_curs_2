import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from app.database.db import initialize_db, get_connection
from main import BakeryApp
import ctypes
import os
import re

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
        initialize_db()
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                email TEXT NOT NULL,
                description TEXT NOT NULL,
                event TEXT NOT NULL,
                event_address TEXT NOT NULL,
                delivery_time TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        try:
            cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                          ("admin", "admin123"))
            conn.commit()
        except sqlite3.Error:
            pass
        
        conn.close()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
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

    def create_background(self, canvas, width, height):
        # Горизонтальный градиент
        start_color = "#6B728E"  # Тёмный фиолетовый
        end_color = "#A7F3D0"    # Светлый зелёный
        
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
        
        # Узор из фигур
        for _ in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 50)
            shape_type = random.choice(["circle", "triangle"])
            fill_color = random.choice(["#D8B4FE", "#6EE7B7"])  # Светлый фиолетовый или зелёный
            opacity = random.uniform(0.2, 0.5)
            
            if shape_type == "circle":
                canvas.create_oval(x, y, x + size, y + size, fill=fill_color, stipple="gray50")
            else:
                canvas.create_polygon(
                    x, y,
                    x + size, y,
                    x + size // 2, y - size,
                    fill=fill_color, stipple="gray50"
                )

    def create_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Фон с градиентом и узором
        canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.create_background(canvas, 800, 600)
        
        # Основной фрейм для элементов
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(main_frame, text="Добро пожаловать!", style="Header.TLabel").pack(pady=(60, 30))
        
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(fill="x", padx=20)
        
        ttk.Label(login_frame, text="Логин:").pack(anchor="w", pady=(10, 0))
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.pack(fill="x", pady=(0, 10))
        
        ttk.Label(login_frame, text="Пароль:").pack(anchor="w")
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Войти как администратор",
                  command=self.login_admin).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Войти как клиент",
                  command=self.show_customer_form).pack(side="left", padx=10)

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
        
        # Фон с градиентом и узором
        canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.create_background(canvas, 800, 600)
        
        # Основной контейнер
        main_container = ttk.Frame(self.root, style="Customer.TFrame")
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)
        
        # Канвас для прокрутки
        canvas = tk.Canvas(main_container, highlightthickness=0, bg="#E0E0E0")
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Customer.TFrame")
        
        # Настройка прокрутки
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Создание окна в канвасе
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Размещение элементов
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(scrollable_frame, text="Оформление предварительного заказа",
                 style="Header.TLabel").pack(pady=(20, 20))
        
        # Основной контейнер для формы
        form_container = ttk.Frame(scrollable_frame, style="Customer.TFrame")
        form_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Форма с полями
        form_frame = ttk.Frame(form_container, style="Customer.TFrame")
        form_frame.pack(fill="x")

        # Словарь с подсказками для полей
        placeholders = {
            "full_name_entry": "Введите ФИО полностью",
            "phone_entry": "Формат: +7XXXXXXXXXX или 8XXXXXXXXXX",
            "address_entry": "Введите полный адрес доставки",
            "email_entry": "example@domain.com",
            "event_entry": "Название и тип мероприятия",
            "event_address_entry": "Полный адрес проведения мероприятия",
            "delivery_time_entry": "Формат: ЧЧ:ММ (например, 14:30)",
            "description_text": "Опишите детали заказа: тип выпечки, количество, особые пожелания..."
        }
        
        fields = [
            ("ФИО*", "full_name_entry"),
            ("📱 Телефон*", "phone_entry"),
            ("🏠 Адрес*", "address_entry"),
            ("📧 Email*", "email_entry"),
            ("🎉 Мероприятие*", "event_entry"),
            ("📍 Адрес мероприятия*", "event_address_entry"),
            ("⏰ Время доставки (ЧЧ:ММ)*", "delivery_time_entry"),
            ("🍰 Описание выпечки*", "description_text")
        ]
        
        self.entries = {}
        
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

        def add_placeholder_text(text_widget, placeholder_text):
            def on_focus_in(event):
                if text_widget.get("1.0", "end-1c") == placeholder_text:
                    text_widget.delete("1.0", tk.END)
                    text_widget.config(foreground='black')

            def on_focus_out(event):
                if not text_widget.get("1.0", "end-1c").strip():
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", placeholder_text)
                    text_widget.config(foreground='gray')

            text_widget.insert("1.0", placeholder_text)
            text_widget.config(foreground='gray')
            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)
        
        for label_text, field_name in fields:
            field_frame = ttk.Frame(form_frame, style="Customer.TFrame")
            field_frame.pack(fill="x", pady=(5, 0))
            
            ttk.Label(field_frame, text=label_text, font=("Helvetica", 14)).pack(anchor="w", pady=(5, 0))
            if field_name == "description_text":
                entry = tk.Text(form_frame, height=4, width=50, font=("Helvetica", 14), bg="#FFFFFF", relief="flat", bd=2)
                entry.pack(fill="x", pady=(0, 5))
                add_placeholder_text(entry, placeholders[field_name])
            else:
                entry = ttk.Entry(form_frame, font=("Helvetica", 14))
                entry.pack(fill="x", pady=(0, 5))
                add_placeholder(entry, placeholders[field_name])
            self.entries[field_name] = entry
        
        # Кнопки
        button_frame = ttk.Frame(form_container)
        button_frame.pack(fill="x", pady=(20, 20))
        
        ttk.Button(button_frame, text="✅ Отправить заказ",
                  command=self.submit_order, style="TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="⬅️ Вернуться",
                  command=self.create_login_window, style="TButton").pack(side="left", padx=10)
        
        ttk.Label(scrollable_frame, text="* - обязательные поля",
                 font=("Helvetica", 12, "italic"), background="#E0E0E0").pack(pady=(0, 10))

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
            if isinstance(entry, tk.Text):
                value = entry.get("1.0", tk.END).strip()
                placeholder = "Опишите детали заказа: тип выпечки, количество, особые пожелания..."
            else:
                value = entry.get().strip()
                placeholder = entry.get() if entry.cget("foreground") == "black" else ""
            return "" if value == placeholder else value

        full_name = get_entry_value(self.entries["full_name_entry"])
        phone = get_entry_value(self.entries["phone_entry"])
        address = get_entry_value(self.entries["address_entry"])
        email = get_entry_value(self.entries["email_entry"])
        description = get_entry_value(self.entries["description_text"])
        event = get_entry_value(self.entries["event_entry"])
        event_address = get_entry_value(self.entries["event_address_entry"])
        delivery_time = get_entry_value(self.entries["delivery_time_entry"])
        
        required_fields = {
            "ФИО": full_name,
            "Телефон": phone,
            "Адрес": address,
            "Email": email,
            "Описание выпечки": description,
            "Мероприятие": event,
            "Адрес мероприятия": event_address,
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
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customer_orders (
                    full_name, phone, address, email,
                    description, event, event_address, delivery_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                full_name, phone, address, email,
                description, event, event_address, delivery_time
            ))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Успех", "Ваш заказ успешно отправлен!")
            self.create_login_window()
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BakeryManagementApp(root)
    root.mainloop()