import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.database.db import initialize_db, get_connection
from app.reports import get_company_report, get_company_names
import random
import math

class BakeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления пекарней")
        self.root.geometry("1200x800")
        
        # Initialize row tags for alternating colors
        self.row_tags = ('evenrow', 'oddrow')
        
        # Initialize database
        initialize_db()
        
        # Create notebook for tabs
        self.tab_control = ttk.Notebook(self.root)
        
        # Create tabs
        self.create_main_tab()
        self.create_trade_points_tab()
        self.create_orders_tab()
        self.create_suppliers_tab()
        self.create_employees_tab()
        self.create_reports_tab()
        self.create_menu_tab()
        
        # Pack notebook
        self.tab_control.pack(expand=1, fill="both")
        
        # Setup treeview style
        self.setup_treeview_style()
        
        # Configure treeview tags
        self.configure_treeview_tags()
        
        # Load initial data
        self.load_trade_points()
        self.load_orders()
        self.load_suppliers()
        self.load_raw_materials()
        self.load_employees()
        self.load_menu_items()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка стилей для градиентного фона
        style.configure("Gradient.TFrame", background="#6B728E")
        
        # Оставляем оригинальные стили для кнопок и других элементов
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
        
        # Увеличиваем количество фигур до 50
        for _ in range(50):
            # Случайное положение с учетом границ окна
            x = random.randint(-50, width + 50)  # Разрешаем частичное появление за границами
            y = random.randint(-50, height + 50)
            size = random.randint(30, 60)  # Увеличиваем диапазон размеров
            shape_type = random.choice(["circle", "triangle", "pentagon", "star"])
            fill_color = random.choice(["#D8B4FE", "#6EE7B7", "#FCA5A5", "#93C5FD", "#FCD34D"])
            opacity = random.uniform(0.2, 0.5)
            
            if shape_type == "circle":
                canvas.create_oval(x, y, x + size, y + size, fill=fill_color, stipple="gray50")
            elif shape_type == "triangle":
                canvas.create_polygon(
                    x, y,
                    x + size, y,
                    x + size // 2, y - size,
                    fill=fill_color, stipple="gray50"
                )
            elif shape_type == "pentagon":
                points = []
                for i in range(5):
                    angle = i * 72 - 90  # 72 градуса между вершинами пятиугольника
                    px = x + size * 0.5 + size * 0.5 * math.cos(math.radians(angle))
                    py = y + size * 0.5 + size * 0.5 * math.sin(math.radians(angle))
                    points.extend([px, py])
                canvas.create_polygon(points, fill=fill_color, stipple="gray50")
            elif shape_type == "star":
                points = []
                for i in range(10):  # 5 вершин звезды, каждая вершина имеет внутреннюю и внешнюю точку
                    angle = i * 36 - 90  # 36 градусов между точками
                    radius = size * 0.5 if i % 2 == 0 else size * 0.2  # Чередуем длинные и короткие лучи
                    px = x + size * 0.5 + radius * math.cos(math.radians(angle))
                    py = y + size * 0.5 + radius * math.sin(math.radians(angle))
                    points.extend([px, py])
                canvas.create_polygon(points, fill=fill_color, stipple="gray50")

    def create_gradient_frame(self, parent, width, height):
        frame = ttk.Frame(parent, style="Gradient.TFrame")
        canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        try:
            self.create_background(canvas, width, height)
        except Exception as e:
            print(f"Ошибка при создании градиентного фона: {e}")
        return frame
    
    def get_next_id(self, cursor, table_name):
        cursor.execute(f"SELECT id FROM {table_name} ORDER BY id")
        ids = [row['id'] for row in cursor.fetchall()]
        if not ids:
            return 1
        for i in range(len(ids)):
            if ids[i] != i + 1:
                return i + 1
        return max(ids) + 1
    
    def __del__(self):
        try:
            conn = get_connection()
            conn.close()
        except:
            pass
    
    def setup_treeview_style(self):
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#FFFFFF",
                        foreground="black", 
                        rowheight=25, 
                        fieldbackground="#FFFFFF",
                        borderwidth=1)
        style.configure("Treeview.Heading", 
                        font=('Arial', 10, 'bold'),
                        background="#E6E6E6", 
                        foreground="black",
                        relief="solid",
                        borderwidth=1)
        style.map('Treeview', 
                background=[('selected', '#0078D7')])
        style.map('Treeview', 
                foreground=[('selected', 'white')])
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe', 'border': '1'})
        ])
        style.configure("Treeview.Cell", padding=5)
        style.map("Treeview",
                background=[('selected', '#0078D7')],
                foreground=[('selected', 'white')])
        style.configure("Transparent.TFrame", background="")
    
    def configure_treeview_tags(self):
        tree_names = ["trade_points_tree", "orders_tree", "suppliers_tree", "raw_materials_tree", "employees_tree", "menu_tree"]
        for tree_name in tree_names:
            if hasattr(self, tree_name):
                tree = getattr(self, tree_name)
                tree.tag_configure("evenrow", background="#FFFFFF")
                tree.tag_configure("oddrow", background="#F5F5F5")
                tree.tag_configure("selected", background="#0078D7", foreground="white")
    
    def create_main_tab(self):
        main_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(main_frame, text="Главная страница")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(main_frame, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(content_frame, text="Система управления хлебопекарней", font=("Arial", 16), background="#E0E0E0").pack(pady=20)
        ttk.Button(content_frame, text="Управление торговыми точками", 
                  width=30, command=lambda: self.tab_control.select(1)).pack(pady=5)
        ttk.Button(content_frame, text="Управление предварительными заказами", 
                  width=30, command=lambda: self.tab_control.select(2)).pack(pady=5)
        ttk.Button(content_frame, text="Управление поставщиками и сырьем", 
                  width=30, command=lambda: self.tab_control.select(3)).pack(pady=5)
        ttk.Button(content_frame, text="Управление персоналом", 
                  width=30, command=lambda: self.tab_control.select(4)).pack(pady=5)
        ttk.Button(content_frame, text="Отчетность и налоги", 
                  width=30, command=lambda: self.tab_control.select(5)).pack(pady=5)
    
    def create_trade_points_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Торговые точки")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Добавить торговую точку", 
                  command=self.add_trade_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать торговую точку", 
                  command=self.edit_trade_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить торговую точку", 
                  command=self.delete_trade_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Просмотреть график поставок", 
                  command=self.view_delivery_schedule).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)
        
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы остается без изменений
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        self.trade_points_tree = ttk.Treeview(table_frame,
                                          columns=("ID", "Название", "Адрес"),
                                          show="headings",
                                          yscrollcommand=y_scrollbar.set,
                                          xscrollcommand=x_scrollbar.set,
                                          selectmode="browse",
                                          height=20)
        self.trade_points_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.trade_points_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.trade_points_tree.heading("Адрес", text="Адрес", anchor=tk.CENTER)
        self.trade_points_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.trade_points_tree.column("Название", width=200, minwidth=150, anchor=tk.W)
        self.trade_points_tree.column("Адрес", width=300, minwidth=200, anchor=tk.W)
        y_scrollbar.config(command=self.trade_points_tree.yview)
        x_scrollbar.config(command=self.trade_points_tree.xview)
        self.trade_points_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.load_trade_points()
    
    def create_orders_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Предварительные заказы")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Добавить предварительный заказ", 
                  command=self.add_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать предварительный заказ", 
                  command=self.edit_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить предварительный заказ", 
                  command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Просмотреть список заказов", 
                  command=self.view_orders).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)
        
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы остается без изменений
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        self.orders_tree = ttk.Treeview(table_frame,
                                     columns=("ID", "Торговая точка", "Описание", "Дата", "Статус"),
                                     show="headings",
                                     yscrollcommand=y_scrollbar.set,
                                     xscrollcommand=x_scrollbar.set,
                                     selectmode="browse")
        self.orders_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.orders_tree.heading("Торговая точка", text="Торговая точка", anchor=tk.CENTER)
        self.orders_tree.heading("Описание", text="Описание", anchor=tk.CENTER)
        self.orders_tree.heading("Дата", text="Дата", anchor=tk.CENTER)
        self.orders_tree.heading("Статус", text="Статус", anchor=tk.CENTER)
        self.orders_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.orders_tree.column("Торговая точка", width=150, minwidth=120, anchor=tk.W)
        self.orders_tree.column("Описание", width=200, minwidth=150, anchor=tk.W)
        self.orders_tree.column("Дата", width=100, minwidth=80, anchor=tk.CENTER)
        self.orders_tree.column("Статус", width=100, minwidth=80, anchor=tk.CENTER)
        y_scrollbar.config(command=self.orders_tree.yview)
        x_scrollbar.config(command=self.orders_tree.xview)
        self.orders_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.load_orders()
    
    def create_suppliers_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Поставщики и сырье")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        return_button_frame = ttk.Frame(content_frame)
        return_button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(return_button_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right")
        
        sub_notebook = ttk.Notebook(content_frame)
        sub_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Остальной код создания вкладок поставщиков и сырья остается без изменений
        suppliers_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(suppliers_tab, text="Поставщики")
        
        suppliers_buttons = ttk.Frame(suppliers_tab)
        suppliers_buttons.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(suppliers_buttons, text="Добавить поставщика", 
                  command=lambda: self.add_supplier(self.suppliers_tree)).pack(side="left", padx=5)
        ttk.Button(suppliers_buttons, text="Редактировать поставщика", 
                  command=lambda: self.edit_supplier(self.suppliers_tree)).pack(side="left", padx=5)
        ttk.Button(suppliers_buttons, text="Удалить поставщика", 
                  command=lambda: self.delete_supplier(self.suppliers_tree)).pack(side="left", padx=5)
        
        suppliers_table_frame = ttk.Frame(suppliers_tab)
        suppliers_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы поставщиков остается без изменений
        suppliers_y_scrollbar = ttk.Scrollbar(suppliers_table_frame, orient="vertical")
        suppliers_x_scrollbar = ttk.Scrollbar(suppliers_table_frame, orient="horizontal")
        self.suppliers_tree = ttk.Treeview(suppliers_table_frame, 
                                        columns=("ID", "Название", "Контакт", "Телефон"), 
                                        show="headings",
                                        yscrollcommand=suppliers_y_scrollbar.set,
                                        xscrollcommand=suppliers_x_scrollbar.set,
                                        selectmode="browse",
                                        style="Treeview")
        self.suppliers_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.suppliers_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.suppliers_tree.heading("Контакт", text="Контакт", anchor=tk.CENTER)
        self.suppliers_tree.heading("Телефон", text="Телефон", anchor=tk.CENTER)
        self.suppliers_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.suppliers_tree.column("Название", width=200, minwidth=150, anchor=tk.W)
        self.suppliers_tree.column("Контакт", width=150, minwidth=100, anchor=tk.W)
        self.suppliers_tree.column("Телефон", width=150, minwidth=100, anchor=tk.W)
        suppliers_y_scrollbar.config(command=self.suppliers_tree.yview)
        suppliers_x_scrollbar.config(command=self.suppliers_tree.xview)
        self.suppliers_tree.grid(row=0, column=0, sticky="nsew")
        suppliers_y_scrollbar.grid(row=0, column=1, sticky="ns")
        suppliers_x_scrollbar.grid(row=1, column=0, sticky="ew")
        suppliers_table_frame.columnconfigure(0, weight=1)
        suppliers_table_frame.rowconfigure(0, weight=1)
        
        raw_materials_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(raw_materials_tab, text="Сырье")
        
        raw_buttons = ttk.Frame(raw_materials_tab)
        raw_buttons.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(raw_buttons, text="Добавить сырье", 
                  command=lambda: self.add_raw_material(self.raw_materials_tree, self.suppliers_tree)).pack(side="left", padx=5)
        ttk.Button(raw_buttons, text="Редактировать сырье", 
                  command=lambda: self.edit_raw_material(self.raw_materials_tree, self.suppliers_tree)).pack(side="left", padx=5)
        ttk.Button(raw_buttons, text="Удалить сырье", 
                  command=lambda: self.delete_raw_material(self.raw_materials_tree)).pack(side="left", padx=5)
        ttk.Button(raw_buttons, text="Заказать сырье", 
                  command=self.order_raw_material).pack(side="left", padx=5)
        ttk.Button(raw_buttons, text="Просмотреть запасы", 
                  command=self.view_inventory).pack(side="left", padx=5)
        
        raw_table_frame = ttk.Frame(raw_materials_tab)
        raw_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы сырья остается без изменений
        raw_y_scrollbar = ttk.Scrollbar(raw_table_frame, orient="vertical")
        raw_x_scrollbar = ttk.Scrollbar(raw_table_frame, orient="horizontal")
        self.raw_materials_tree = ttk.Treeview(raw_table_frame, 
                                           columns=("ID", "Название", "Поставщик", "Количество", "Ед.изм."), 
                                           show="headings",
                                           yscrollcommand=raw_y_scrollbar.set,
                                           xscrollcommand=raw_x_scrollbar.set,
                                           selectmode="browse",
                                           style="Treeview")
        self.raw_materials_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Поставщик", text="Поставщик", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Количество", text="Количество", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Ед.изм.", text="Ед.изм.", anchor=tk.CENTER)
        self.raw_materials_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.raw_materials_tree.column("Название", width=150, minwidth=120, anchor=tk.W)
        self.raw_materials_tree.column("Поставщик", width=150, minwidth=120, anchor=tk.W)
        self.raw_materials_tree.column("Количество", width=100, minwidth=80, anchor=tk.CENTER)
        self.raw_materials_tree.column("Ед.изм.", width=80, minwidth=60, anchor=tk.CENTER)
        raw_y_scrollbar.config(command=self.raw_materials_tree.yview)
        raw_x_scrollbar.config(command=self.raw_materials_tree.xview)
        self.raw_materials_tree.grid(row=0, column=0, sticky="nsew")
        raw_y_scrollbar.grid(row=0, column=1, sticky="ns")
        raw_x_scrollbar.grid(row=1, column=0, sticky="ew")
        raw_table_frame.columnconfigure(0, weight=1)
        raw_table_frame.rowconfigure(0, weight=1)
        
        self.load_suppliers()
        self.load_raw_materials()
    
    def create_employees_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Персонал")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Добавить сотрудника", 
                  command=self.add_employee).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать сотрудника", 
                  command=self.edit_employee).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить сотрудника", 
                  command=self.delete_employee).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Просмотреть график работы", 
                  command=self.view_work_schedule).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)
        
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы остается без изменений
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        self.employees_tree = ttk.Treeview(table_frame, 
                                       columns=("ID", "Имя", "Должность", "Телефон"), 
                                       show="headings",
                                       yscrollcommand=y_scrollbar.set,
                                       xscrollcommand=x_scrollbar.set,
                                       selectmode="browse")
        self.employees_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.employees_tree.heading("Имя", text="Имя", anchor=tk.CENTER)
        self.employees_tree.heading("Должность", text="Должность", anchor=tk.CENTER)
        self.employees_tree.heading("Телефон", text="Телефон", anchor=tk.CENTER)
        self.employees_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.employees_tree.column("Имя", width=200, minwidth=150, anchor=tk.W)
        self.employees_tree.column("Должность", width=150, minwidth=100, anchor=tk.W)
        self.employees_tree.column("Телефон", width=150, minwidth=100, anchor=tk.W)
        y_scrollbar.config(command=self.employees_tree.yview)
        x_scrollbar.config(command=self.employees_tree.xview)
        self.employees_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.load_employees()
    
    def create_reports_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Отчетность и налоги")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Сформировать налоговый отчет", 
                  command=self.generate_tax_report).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Экспортировать данные", 
                  command=self.export_data).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)
        
        reports_frame = ttk.LabelFrame(content_frame, text="Доступные отчеты")
        reports_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(reports_frame, text="Отчет по продажам", 
                  command=lambda: self.generate_report("sales")).pack(anchor="w", padx=10, pady=5)
        ttk.Button(reports_frame, text="Отчет по поставщикам", 
                  command=lambda: self.generate_report("suppliers")).pack(anchor="w", padx=10, pady=5)
        ttk.Button(reports_frame, text="Отчет по сырью", 
                  command=lambda: self.generate_report("materials")).pack(anchor="w", padx=10, pady=5)
    
    def create_menu_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Меню изделий")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1200, 800)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Добавить изделие", 
                  command=self.add_menu_item).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать изделие", 
                  command=self.edit_menu_item).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить изделие", 
                  command=self.delete_menu_item).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)
        
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Остальной код создания таблицы остается без изменений
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        self.menu_tree = ttk.Treeview(table_frame,
                                    columns=("ID", "Название", "Цена"),
                                    show="headings",
                                    yscrollcommand=y_scrollbar.set,
                                    xscrollcommand=x_scrollbar.set,
                                    selectmode="browse")
        self.menu_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.menu_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.menu_tree.heading("Цена", text="Цена", anchor=tk.CENTER)
        self.menu_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.menu_tree.column("Название", width=200, minwidth=150, anchor=tk.W)
        self.menu_tree.column("Цена", width=100, minwidth=80, anchor=tk.CENTER)
        y_scrollbar.config(command=self.menu_tree.yview)
        x_scrollbar.config(command=self.menu_tree.xview)
        self.menu_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        self.load_menu_items()

    def load_menu_items(self):
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price FROM menu_items")
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.menu_tree.insert("", "end", values=(row['id'], row['name'], f"{row['price']:.2f}"), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить меню: {str(e)}")

    def add_menu_item(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить изделие")
        dialog.geometry("300x180")
        dialog.grab_set()
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Цена:").pack()
        price_entry = ttk.Entry(dialog, width=30)
        price_entry.pack(pady=(5, 10))
        def save():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            if not name or not price:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            try:
                price_val = float(price)
                if price_val < 0:
                    messagebox.showwarning("Предупреждение", "Цена не может быть отрицательной")
                    return
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректную цену")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                next_id = self.get_next_id(cursor, "menu_items")
                cursor.execute("INSERT INTO menu_items (id, name, price) VALUES (?, ?, ?)", 
                             (next_id, name, price_val))
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'menu_items'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('menu_items', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_menu_items()
                dialog.destroy()
                messagebox.showinfo("Успех", "Изделие добавлено")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить изделие: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()

    def edit_menu_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите изделие для редактирования")
            return
        item = self.menu_tree.item(selected[0])['values']
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать изделие")
        dialog.geometry("300x180")
        dialog.grab_set()
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, item[1])
        name_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Цена:").pack()
        price_entry = ttk.Entry(dialog, width=30)
        price_entry.insert(0, item[2])
        price_entry.pack(pady=(5, 10))
        def save():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            if not name or not price:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            try:
                price_val = float(price)
                if price_val < 0:
                    messagebox.showwarning("Предупреждение", "Цена не может быть отрицательной")
                    return
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректную цену")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE menu_items SET name=?, price=? WHERE id=?", 
                             (name, price_val, item[0]))
                conn.commit()
                conn.close()
                self.load_menu_items()
                dialog.destroy()
                messagebox.showinfo("Успех", "Изделие обновлено")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось обновить изделие: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()

    def delete_menu_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите изделие для удаления")
            return
        item = self.menu_tree.item(selected[0])['values']
        if messagebox.askyesno("Подтверждение", f"Удалить изделие '{item[1]}'?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM menu_items WHERE id=?", (item[0],))
                conn.commit()
                conn.close()
                self.load_menu_items()
                messagebox.showinfo("Успех", "Изделие удалено")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось удалить изделие: {str(e)}")
    
    def load_trade_points(self):
        for item in self.trade_points_tree.get_children():
            self.trade_points_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, address FROM trade_points")
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.trade_points_tree.insert("", "end", values=(row['id'], row['name'], row['address']), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить торговые точки: {str(e)}")
    
    def load_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, t.name, o.description, o.order_date, o.status 
                FROM orders o
                LEFT JOIN trade_points t ON o.trade_point_id = t.id
            """)
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.orders_tree.insert("", "end", values=(
                    row['id'], 
                    row['name'] if row['name'] else "Не указано", 
                    row['description'], 
                    row['order_date'], 
                    row['status']
                ), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить заказы: {str(e)}")
    
    def load_suppliers(self):
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, contact, phone FROM suppliers")
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.suppliers_tree.insert("", "end", values=(
                    row['id'], 
                    row['name'], 
                    row['contact'] if row['contact'] else "", 
                    row['phone'] if row['phone'] else ""
                ), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить поставщиков: {str(e)}")
    
    def load_raw_materials(self):
        for item in self.raw_materials_tree.get_children():
            self.raw_materials_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id, r.name, s.name as supplier_name, r.quantity, r.unit 
                FROM raw_materials r
                LEFT JOIN suppliers s ON r.supplier_id = s.id
            """)
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.raw_materials_tree.insert("", "end", values=(
                    row['id'], 
                    row['name'], 
                    row['supplier_name'] if row['supplier_name'] else "Не указано", 
                    row['quantity'] if row['quantity'] else 0, 
                    row['unit'] if row['unit'] else ""
                ), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить сырье: {str(e)}")
    
    def load_employees(self):
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, position, phone FROM employees")
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.employees_tree.insert("", "end", values=(
                    row['id'], 
                    row['name'], 
                    row['position'] if row['position'] else "", 
                    row['phone'] if row['phone'] else ""
                ), tags=(tag,))
                count += 1
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить сотрудников: {str(e)}")
    
    def add_trade_point(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить торговую точку")
        dialog.geometry("300x200")
        dialog.grab_set()
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Адрес:").pack()
        address_entry = ttk.Entry(dialog, width=30)
        address_entry.pack(pady=(5, 10))
        def save_trade_point():
            name = name_entry.get().strip()
            address = address_entry.get().strip()
            if not name or not address:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                next_id = self.get_next_id(cursor, "trade_points")
                cursor.execute(
                    "INSERT INTO trade_points (id, name, address) VALUES (?, ?, ?)",
                    (next_id, name, address)
                )
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'trade_points'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('trade_points', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_trade_points()
                dialog.destroy()
                messagebox.showinfo("Успех", "Торговая точка добавлена")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить торговую точку: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save_trade_point).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def edit_trade_point(self):
        selected = self.trade_points_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите торговую точку для редактирования")
            return
        item_id = self.trade_points_tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, address FROM trade_points WHERE id = ?", (item_id,))
            trade_point = cursor.fetchone()
            conn.close()
            if not trade_point:
                messagebox.showerror("Ошибка", "Торговая точка не найдена")
                return
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать торговую точку")
            dialog.geometry("300x200")
            dialog.grab_set()
            ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, trade_point['name'])
            name_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Адрес:").pack()
            address_entry = ttk.Entry(dialog, width=30)
            address_entry.insert(0, trade_point['address'])
            address_entry.pack(pady=(5, 10))
            def update_trade_point():
                name = name_entry.get().strip()
                address = address_entry.get().strip()
                if not name or not address:
                    messagebox.showwarning("Предупреждение", "Заполните все поля")
                    return
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE trade_points SET name = ?, address = ? WHERE id = ?",
                        (name, address, item_id)
                    )
                    conn.commit()
                    conn.close()
                    self.load_trade_points()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Торговая точка обновлена")
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось обновить торговую точку: {str(e)}")
            ttk.Button(dialog, text="Сохранить", command=update_trade_point).pack(pady=10)
            ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
    
    def delete_trade_point(self):
        selected = self.trade_points_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите торговую точку для удаления")
            return
        item_id = self.trade_points_tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE trade_point_id = ?", (item_id,))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                if not messagebox.askyesno(
                    "Предупреждение", 
                    f"Данная торговая точка имеет {result['count']} связанных заказов.\n"
                    "При удалении торговой точки будут удалены все связанные заказы.\n"
                    "Вы уверены, что хотите продолжить?"
                ):
                    conn.close()
                    return
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту торговую точку?"):
                cursor.execute("DELETE FROM orders WHERE trade_point_id = ?", (item_id,))
                cursor.execute("DELETE FROM trade_points WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                self.load_trade_points()
                messagebox.showinfo("Успех", "Торговая точка и связанные заказы удалены")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить торговую точку: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    def view_delivery_schedule(self):
        messagebox.showinfo("Информация", "Функция просмотра графика поставок в разработке")
    
    def add_order(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить предварительный заказ")
        dialog.geometry("400x300")
        dialog.grab_set()
        ttk.Label(dialog, text="Торговая точка:").pack(pady=(10, 0))
        trade_point_var = tk.StringVar()
        trade_point_combo = ttk.Combobox(dialog, textvariable=trade_point_var, width=30)
        trade_point_combo.pack(pady=(5, 10))
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM trade_points")
            trade_points = {row['name']: row['id'] for row in cursor.fetchall()}
            trade_point_combo['values'] = list(trade_points.keys())
            if trade_point_combo['values']:
                trade_point_combo.current(0)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список торговых точек: {str(e)}")
        ttk.Label(dialog, text="Описание:").pack()
        description_entry = tk.Text(dialog, width=40, height=5)
        description_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Дата (ГГГГ-ММ-ДД):").pack()
        date_entry = ttk.Entry(dialog, width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Статус:").pack()
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(dialog, textvariable=status_var, width=30, state="readonly")
        status_combo['values'] = ["Новый", "В обработке", "Выполнен", "Отменен"]
        status_combo.current(0)
        status_combo.pack(pady=(5, 10))
        def save_order():
            trade_point_name = trade_point_var.get()
            if not trade_point_name in trade_points:
                messagebox.showwarning("Предупреждение", "Выберите торговую точку")
                return
            description = description_entry.get("1.0", tk.END).strip()
            if not description:
                messagebox.showwarning("Предупреждение", "Введите описание заказа")
                return
            order_date = date_entry.get().strip()
            try:
                datetime.strptime(order_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите дату в формате ГГГГ-ММ-ДД")
                return
            status = status_var.get()
            try:
                conn = get_connection()
                cursor = conn.cursor()
                next_id = self.get_next_id(cursor, "orders")
                cursor.execute(
                    "INSERT INTO orders (id, trade_point_id, description, order_date, status) VALUES (?, ?, ?, ?, ?)",
                    (next_id, trade_points[trade_point_name], description, order_date, status)
                )
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'orders'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('orders', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_orders()
                dialog.destroy()
                messagebox.showinfo("Успех", "Заказ добавлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить заказ: {str(e)}")
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text="Сохранить", command=save_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для редактирования")
            return
        item_id = self.orders_tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.trade_point_id, o.description, o.order_date, o.status, t.name as trade_point_name 
                FROM orders o
                LEFT JOIN trade_points t ON o.trade_point_id = t.id
                WHERE o.id = ?
            """, (item_id,))
            order = cursor.fetchone()
            if not order:
                messagebox.showerror("Ошибка", "Заказ не найден")
                conn.close()
                return
            cursor.execute("SELECT id, name FROM trade_points")
            trade_points = {row['name']: row['id'] for row in cursor.fetchall()}
            conn.close()
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать заказ")
            dialog.geometry("400x300")
            dialog.grab_set()
            ttk.Label(dialog, text="Торговая точка:").pack(pady=(10, 0))
            trade_point_var = tk.StringVar()
            trade_point_combo = ttk.Combobox(dialog, textvariable=trade_point_var, width=30)
            trade_point_combo['values'] = list(trade_points.keys())
            current_trade_point = order['trade_point_name'] if order['trade_point_name'] else ""
            if current_trade_point in trade_points:
                trade_point_var.set(current_trade_point)
            elif trade_point_combo['values']:
                trade_point_combo.current(0)
            trade_point_combo.pack(pady=(5, 10))
            ttk.Label(dialog, text="Описание:").pack()
            description_entry = tk.Text(dialog, width=40, height=5)
            description_entry.insert("1.0", order['description'])
            description_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Дата (ГГГГ-ММ-ДД):").pack()
            date_entry = ttk.Entry(dialog, width=30)
            date_entry.insert(0, order['order_date'])
            date_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Статус:").pack()
            status_var = tk.StringVar()
            status_combo = ttk.Combobox(dialog, textvariable=status_var, width=30, state="readonly")
            status_combo['values'] = ["Новый", "В обработке", "Выполнен", "Отменен"]
            if order['status'] in status_combo['values']:
                status_var.set(order['status'])
            else:
                status_combo.current(0)
            status_combo.pack(pady=(5, 10))
            def update_order():
                trade_point_name = trade_point_var.get()
                if not trade_point_name in trade_points:
                    messagebox.showwarning("Предупреждение", "Выберите торговую точку")
                    return
                description = description_entry.get("1.0", tk.END).strip()
                if not description:
                    messagebox.showwarning("Предупреждение", "Введите описание заказа")
                    return
                order_date = date_entry.get().strip()
                try:
                    datetime.strptime(order_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Предупреждение", "Введите дату в формате ГГГГ-ММ-ДД")
                    return
                status = status_var.get()
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """UPDATE orders 
                           SET trade_point_id = ?, description = ?, order_date = ?, status = ? 
                           WHERE id = ?""",
                        (trade_points[trade_point_name], description, order_date, status, item_id)
                    )
                    conn.commit()
                    conn.close()
                    self.load_orders()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Заказ обновлен")
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось обновить заказ: {str(e)}")
            buttons_frame = ttk.Frame(dialog)
            buttons_frame.pack(pady=10)
            ttk.Button(buttons_frame, text="Сохранить", command=update_order).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
    
    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для удаления")
            return
        item_id = self.orders_tree.item(selected[0], "values")[0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот заказ?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM orders WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                self.load_orders()
                messagebox.showinfo("Успех", "Заказ удален")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить заказ: {str(e)}")
                if 'conn' in locals():
                    conn.close()
    
    def view_orders(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Просмотр списка заказов")
        report_window.geometry("900x600")
        filter_frame = ttk.LabelFrame(report_window, text="Фильтры")
        filter_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(filter_frame, text="Статус:").grid(row=0, column=0, padx=5, pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, width=20)
        status_combo['values'] = ["Все", "Новый", "В обработке", "Выполнен", "Отменен"]
        status_combo.current(0)
        status_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="Дата от:").grid(row=0, column=2, padx=5, pady=5)
        start_date_entry = ttk.Entry(filter_frame, width=12)
        start_date_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(filter_frame, text="до:").grid(row=0, column=4, padx=5, pady=5)
        end_date_entry = ttk.Entry(filter_frame, width=12)
        end_date_entry.grid(row=0, column=5, padx=5, pady=5)
        today = datetime.now()
        end_date_entry.insert(0, today.strftime("%Y-%m-%d"))
        start_date = today - datetime.timedelta(days=30)
        start_date_entry.insert(0, start_date.strftime("%Y-%m-%d"))
        report_frame = ttk.Frame(report_window)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        y_scrollbar = ttk.Scrollbar(report_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(report_frame, orient="horizontal")
        report_tree = ttk.Treeview(report_frame,
                               columns=("ID", "Торговая точка", "Описание", "Дата", "Статус"),
                               show="headings",
                               yscrollcommand=y_scrollbar.set,
                               xscrollcommand=x_scrollbar.set,
                               selectmode="browse")
        report_tree.heading("ID", text="ID", anchor=tk.CENTER)
        report_tree.heading("Торговая точка", text="Торговая точка", anchor=tk.CENTER)
        report_tree.heading("Описание", text="Описание", anchor=tk.CENTER)
        report_tree.heading("Дата", text="Дата", anchor=tk.CENTER)
        report_tree.heading("Статус", text="Статус", anchor=tk.CENTER)
        report_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        report_tree.column("Торговая точка", width=150, minwidth=120, anchor=tk.W)
        report_tree.column("Описание", width=200, minwidth=150, anchor=tk.W)
        report_tree.column("Дата", width=100, minwidth=80, anchor=tk.CENTER)
        report_tree.column("Статус", width=100, minwidth=80, anchor=tk.CENTER)
        y_scrollbar.config(command=report_tree.yview)
        x_scrollbar.config(command=report_tree.xview)
        report_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)
        def load_filtered_orders():
            for item in report_tree.get_children():
                report_tree.delete(item)
            status = status_var.get()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            try:
                if start_date:
                    datetime.strptime(start_date, "%Y-%m-%d")
                if end_date:
                    datetime.strptime(end_date, "%Y-%m-%d")
                conn = get_connection()
                cursor = conn.cursor()
                query = """
                    SELECT o.id, t.name as trade_point_name, o.description, o.order_date, o.status 
                    FROM orders o
                    LEFT JOIN trade_points t ON o.trade_point_id = t.id
                    WHERE 1=1
                """
                params = []
                if status != "Все":
                    query += " AND o.status = ?"
                    params.append(status)
                if start_date:
                    query += " AND o.order_date >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND o.order_date <= ?"
                    params.append(end_date)
                query += " ORDER BY o.order_date DESC"
                cursor.execute(query, params)
                count = 0
                for row in cursor.fetchall():
                    tag = "evenrow" if count % 2 == 0 else "oddrow"
                    report_tree.insert("", "end", values=(
                        row['id'],
                        row['trade_point_name'] if row['trade_point_name'] else "Не указано",
                        row['description'],
                        row['order_date'],
                        row['status']
                    ), tags=(tag,))
                    count += 1
                conn.close()
                status_label.config(text=f"Найдено заказов: {count}")
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите даты в формате ГГГГ-ММ-ДД")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {str(e)}")
        ttk.Button(filter_frame, text="Применить фильтр", command=load_filtered_orders).grid(row=0, column=6, padx=10, pady=5)
        status_label = ttk.Label(report_window, text="Загрузка данных...")
        status_label.pack(anchor="w", padx=10, pady=5)
        buttons_frame = ttk.Frame(report_window)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(buttons_frame, text="Экспорт в CSV", command=lambda: self.export_to_csv(report_tree, "orders_report.csv")).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Закрыть", command=report_window.destroy).pack(side="right", padx=5)
        load_filtered_orders()
    
    def add_supplier(self, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить поставщика")
        dialog.geometry("300x250")
        dialog.grab_set()
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Контактное лицо:").pack()
        contact_entry = ttk.Entry(dialog, width=30)
        contact_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Телефон:").pack()
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.pack(pady=(5, 10))
        def save_supplier():
            name = name_entry.get().strip()
            contact = contact_entry.get().strip()
            phone = phone_entry.get().strip()
            if not name:
                messagebox.showwarning("Предупреждение", "Введите название поставщика")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                next_id = self.get_next_id(cursor, "suppliers")
                cursor.execute(
                    "INSERT INTO suppliers (id, name, contact, phone) VALUES (?, ?, ?, ?)",
                    (next_id, name, contact, phone)
                )
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'suppliers'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('suppliers', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_suppliers()
                dialog.destroy()
                messagebox.showinfo("Успех", "Поставщик добавлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить поставщика: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save_supplier).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def edit_supplier(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите поставщика для редактирования")
            return
        item_id = tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, contact, phone FROM suppliers WHERE id = ?", (item_id,))
            supplier = cursor.fetchone()
            conn.close()
            if not supplier:
                messagebox.showerror("Ошибка", "Поставщик не найден")
                return
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать поставщика")
            dialog.geometry("300x250")
            dialog.grab_set()
            ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, supplier['name'])
            name_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Контактное лицо:").pack()
            contact_entry = ttk.Entry(dialog, width=30)
            contact_entry.insert(0, supplier['contact'] if supplier['contact'] else "")
            contact_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Телефон:").pack()
            phone_entry = ttk.Entry(dialog, width=30)
            phone_entry.insert(0, supplier['phone'] if supplier['phone'] else "")
            phone_entry.pack(pady=(5, 10))
            def update_supplier():
                name = name_entry.get().strip()
                contact = contact_entry.get().strip()
                phone = phone_entry.get().strip()
                if not name:
                    messagebox.showwarning("Предупреждение", "Введите название поставщика")
                    return
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE suppliers SET name = ?, contact = ?, phone = ? WHERE id = ?",
                        (name, contact, phone, item_id)
                    )
                    conn.commit()
                    conn.close()
                    self.load_suppliers()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Поставщик обновлен")
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось обновить поставщика: {str(e)}")
            ttk.Button(dialog, text="Сохранить", command=update_supplier).pack(pady=10)
            ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
    
    def delete_supplier(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите поставщика для удаления")
            return
        item_id = tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM raw_materials WHERE supplier_id = ?", (item_id,))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                if not messagebox.askyesno(
                    "Предупреждение", 
                    f"Данный поставщик имеет {result['count']} связанных видов сырья.\n"
                    "При удалении поставщика будут удалены все связанные записи о сырье.\n"
                    "Вы уверены, что хотите продолжить?"
                ):
                    conn.close()
                    return
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого поставщика?"):
                cursor.execute("DELETE FROM raw_materials WHERE supplier_id = ?", (item_id,))
                cursor.execute("DELETE FROM suppliers WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                self.load_suppliers()
                self.load_raw_materials()
                messagebox.showinfo("Успех", "Поставщик и связанные записи удалены")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить поставщика: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    def add_raw_material(self, raw_tree, suppliers_tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить сырье")
        dialog.geometry("300x300")
        dialog.grab_set()
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Единица измерения:").pack()
        unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(dialog, textvariable=unit_var, width=30)
        unit_combo['values'] = ["кг", "л", "шт", "т"]
        unit_combo.current(0)
        unit_combo.pack(pady=(5, 10))
        ttk.Label(dialog, text="Количество:").pack()
        quantity_entry = ttk.Entry(dialog, width=30)
        quantity_entry.pack(pady=(5, 10))
        ttk.Label(dialog, text="Поставщик:").pack()
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=30)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers_list = cursor.fetchall()
            supplier_combo['values'] = [supplier['name'] for supplier in suppliers_list]
            if supplier_combo['values']:
                supplier_combo.current(0)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список поставщиков: {str(e)}")
        supplier_combo.pack(pady=(5, 10))
        def save_raw_material():
            name = name_entry.get().strip()
            unit = unit_var.get()
            quantity = quantity_entry.get().strip()
            supplier_name = supplier_var.get()
            if not name or not quantity or not supplier_name:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            try:
                quantity_val = float(quantity)
                if quantity_val < 0:
                    messagebox.showwarning("Предупреждение", "Количество не может быть отрицательным")
                    return
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректное количество")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier_name,))
                supplier_id = cursor.fetchone()
                if not supplier_id:
                    messagebox.showwarning("Предупреждение", "Выберите действующего поставщика")
                    conn.close()
                    return
                next_id = self.get_next_id(cursor, "raw_materials")
                cursor.execute(
                    "INSERT INTO raw_materials (id, name, supplier_id, quantity, unit) VALUES (?, ?, ?, ?, ?)",
                    (next_id, name, supplier_id['id'], quantity_val, unit)
                )
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'raw_materials'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('raw_materials', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_raw_materials()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сырье добавлено")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сырье: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save_raw_material).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def edit_raw_material(self, raw_tree, suppliers_tree):
        selected = raw_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сырье для редактирования")
            return
        item_id = raw_tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.name, r.quantity, r.unit, s.name as supplier_name 
                FROM raw_materials r 
                LEFT JOIN suppliers s ON r.supplier_id = s.id 
                WHERE r.id = ?
            """, (item_id,))
            material = cursor.fetchone()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers_list = cursor.fetchall()
            conn.close()
            if not material:
                messagebox.showerror("Ошибка", "Сырье не найдено")
                return
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать сырье")
            dialog.geometry("300x300")
            dialog.grab_set()
            ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, material['name'])
            name_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Единица измерения:").pack()
            unit_var = tk.StringVar()
            unit_combo = ttk.Combobox(dialog, textvariable=unit_var, width=30)
            unit_combo['values'] = ["кг", "л", "шт", "т"]
            unit_combo.set(material['unit'])
            unit_combo.pack(pady=(5, 10))
            ttk.Label(dialog, text="Количество:").pack()
            quantity_entry = ttk.Entry(dialog, width=30)
            quantity_entry.insert(0, material['quantity'])
            quantity_entry.pack(pady=(5, 10))
            ttk.Label(dialog, text="Поставщик:").pack()
            supplier_var = tk.StringVar()
            supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=30)
            supplier_combo['values'] = [supplier['name'] for supplier in suppliers_list]
            supplier_combo.set(material['supplier_name'] if material['supplier_name'] else "")
            supplier_combo.pack(pady=(5, 10))
            def update_raw_material():
                name = name_entry.get().strip()
                unit = unit_var.get()
                quantity = quantity_entry.get().strip()
                supplier_name = supplier_var.get()
                if not name or not quantity or not supplier_name:
                    messagebox.showwarning("Предупреждение", "Заполните все поля")
                    return
                try:
                    quantity_val = float(quantity)
                    if quantity_val < 0:
                        messagebox.showwarning("Предупреждение", "Количество не может быть отрицательным")
                        return
                except ValueError:
                    messagebox.showwarning("Предупреждение", "Введите корректное количество")
                    return