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
import ctypes
import time
import re
import json
import traceback

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
        
        # Привязываем события
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
        self.button_canvas.create_text(
            self.width//2, self.height//2,
            text=self.text,
            fill=self.text_color,
            font=self.font
        )
    
    def on_enter(self, event):
        self.button_canvas.delete("all")
        self.button_canvas.create_rectangle(0, 0, self.width, self.height, fill=self.hover_color)
        self.create_text()
    
    def on_leave(self, event):
        self.button_canvas.delete("all")
        self.draw_gradient()
        self.create_text()
    
    def on_click(self, event):
        self.button_canvas.delete("all")
        self.button_canvas.create_rectangle(0, 0, self.width, self.height, fill="#A7F3D0")
        self.create_text()
    
    def on_release(self, event):
        if self.command:
            self.command()
        self.on_leave(None)

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
        
        # Создаем вкладки в нужном порядке
        self.create_main_tab()           # 0
        self.create_menu_tab()           # 1
        self.create_trade_points_tab()   # 2
        self.create_orders_tab()         # 3
        self.create_suppliers_tab()      # 4
        self.create_employees_tab()      # 5
        self.create_reports_tab()        # 6
        
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
        # Close database connection when app is closed
        try:
            conn = get_connection()
            conn.close()
        except:
            pass
    
    def setup_treeview_style(self):
        """Настройка стиля для всех таблиц (Treeview)"""
        style = ttk.Style()
        
        # Основной стиль для Treeview
        style.configure("Treeview", 
                        background="#FFFFFF",
                        foreground="black", 
                        rowheight=25, 
                        fieldbackground="#FFFFFF",
                        borderwidth=1)
        
        # Стиль для заголовков столбцов (как в Excel)
        style.configure("Treeview.Heading", 
                        font=('Arial', 10, 'bold'),
                        background="#E6E6E6", 
                        foreground="black",
                        relief="solid",
                        borderwidth=1)
        
        # Настройка цветов строк в таблице (чередование)
        style.map('Treeview', 
                background=[('selected', '#0078D7')])
        
        # Установка цвета выделенного текста
        style.map('Treeview', 
                foreground=[('selected', 'white')])
        
        # Создаем тэги для чередующихся строк
        self.row_tags = ("evenrow", "oddrow")
        
        # Настройка стиля для ячеек (добавление сетки)
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe', 'border': '1'})
        ])
        
        # Настройка отступов в ячейках
        style.configure("Treeview.Cell", padding=5)
        
        # Настройка стиля для выделенных ячеек
        style.map("Treeview",
                background=[('selected', '#0078D7')],
                foreground=[('selected', 'white')])
    
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
        gradient_frame = self.create_gradient_frame(main_frame, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="Gradient.TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.7)
        
        ttk.Label(content_frame, text="Система управления хлебопекарней", font=("Arial", 30, "bold")).pack(pady=20)
        
        # Фрейм для кнопок строго по центру
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Кнопки по центру и шире
        GradientButton(buttons_frame, text="Меню изделий", width=340, command=lambda: self.tab_control.select(1)).pack(pady=10)
        GradientButton(buttons_frame, text="Управление торговыми точками", width=340, command=lambda: self.tab_control.select(2)).pack(pady=10)
        GradientButton(buttons_frame, text="Управление предварительными заказами", width=340, command=lambda: self.tab_control.select(3)).pack(pady=10)
        GradientButton(buttons_frame, text="Управление поставщиками и сырьем", width=340, command=lambda: self.tab_control.select(4)).pack(pady=10)
        GradientButton(buttons_frame, text="Управление персоналом", width=340, command=lambda: self.tab_control.select(5)).pack(pady=10)
        GradientButton(buttons_frame, text="Отчетность и налоги", width=340, command=lambda: self.tab_control.select(6)).pack(pady=10)
    
    def create_trade_points_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Торговые точки")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Добавить торговую точку", 
                  command=self.add_trade_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать торговую точку", 
                  command=self.edit_trade_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить торговую точку", 
                  command=self.delete_trade_point).pack(side="left", padx=5)
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
        orders_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(orders_frame, text="Заказы")

        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(orders_frame, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)

        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Создаем фрейм для кнопок
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        # Добавляем кнопки
        ttk.Button(buttons_frame, text="Добавить заказ", 
                  command=self.add_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать заказ", 
                  command=self.edit_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить заказ", 
                  command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Просмотреть список заказов", 
                  command=self.view_orders).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Вернуться в меню", 
                  command=lambda: self.tab_control.select(0)).pack(side="right", padx=5)

        # Создаем фрейм для таблицы
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Создаем Treeview с полосами прокрутки
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        
        self.orders_tree = ttk.Treeview(table_frame, columns=(
            "id", "full_name", "phone", "address", 
            "email", "event", "event_date", "delivery_time", "status"
        ), show="headings", yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Определяем заголовки
        self.orders_tree.heading("id", text="ID")
        self.orders_tree.heading("full_name", text="ФИО")
        self.orders_tree.heading("phone", text="Телефон")
        self.orders_tree.heading("address", text="Адрес")
        self.orders_tree.heading("email", text="Email")
        self.orders_tree.heading("event", text="Мероприятие")
        self.orders_tree.heading("event_date", text="Дата")
        self.orders_tree.heading("delivery_time", text="Время доставки")
        self.orders_tree.heading("status", text="Статус")
        
        # Настраиваем ширину колонок
        self.orders_tree.column("id", width=50)
        self.orders_tree.column("full_name", width=150)
        self.orders_tree.column("phone", width=120)
        self.orders_tree.column("address", width=200)
        self.orders_tree.column("email", width=150)
        self.orders_tree.column("event", width=150)
        self.orders_tree.column("event_date", width=100)
        self.orders_tree.column("delivery_time", width=100)
        self.orders_tree.column("status", width=100)

        # Настраиваем полосы прокрутки
        y_scrollbar.config(command=self.orders_tree.yview)
        x_scrollbar.config(command=self.orders_tree.xview)

        # Размещаем элементы в таблице
        self.orders_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Настраиваем веса строк и столбцов
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Привязываем двойной клик
        self.orders_tree.bind("<Double-1>", self.show_order_details)

        # Загружаем данные
        self.load_orders()
    
    def create_suppliers_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Поставщики и сырье")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
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
        
        # Создаем скроллбары
        suppliers_y_scrollbar = ttk.Scrollbar(suppliers_table_frame, orient="vertical")
        suppliers_x_scrollbar = ttk.Scrollbar(suppliers_table_frame, orient="horizontal")
        
        # Create treeview for suppliers
        self.suppliers_tree = ttk.Treeview(suppliers_table_frame, 
                                        columns=("ID", "Название", "Контакт", "Телефон"), 
                                        show="headings",
                                        yscrollcommand=suppliers_y_scrollbar.set,
                                        xscrollcommand=suppliers_x_scrollbar.set,
                                        selectmode="browse",
                                        style="Treeview")
        
        # Настройка заголовков
        self.suppliers_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.suppliers_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.suppliers_tree.heading("Контакт", text="Контакт", anchor=tk.CENTER)
        self.suppliers_tree.heading("Телефон", text="Телефон", anchor=tk.CENTER)
        
        # Настройка столбцов
        self.suppliers_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.suppliers_tree.column("Название", width=200, minwidth=150, anchor=tk.W)
        self.suppliers_tree.column("Контакт", width=150, minwidth=100, anchor=tk.W)
        self.suppliers_tree.column("Телефон", width=150, minwidth=100, anchor=tk.W)
        
        # Настройка скроллбаров
        suppliers_y_scrollbar.config(command=self.suppliers_tree.yview)
        suppliers_x_scrollbar.config(command=self.suppliers_tree.xview)
        
        # Размещение компонентов
        self.suppliers_tree.grid(row=0, column=0, sticky="nsew")
        suppliers_y_scrollbar.grid(row=0, column=1, sticky="ns")
        suppliers_x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка весов строк и столбцов
        suppliers_table_frame.columnconfigure(0, weight=1)
        suppliers_table_frame.rowconfigure(0, weight=1)
        
        # Raw materials sub-tab
        raw_materials_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(raw_materials_tab, text="Сырье")
        
        # Buttons frame for raw materials
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
        
        # Создаем фрейм для таблицы и скроллбара
        raw_table_frame = ttk.Frame(raw_materials_tab)
        raw_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создаем скроллбары
        raw_y_scrollbar = ttk.Scrollbar(raw_table_frame, orient="vertical")
        raw_x_scrollbar = ttk.Scrollbar(raw_table_frame, orient="horizontal")
        
        # Create treeview for raw materials
        self.raw_materials_tree = ttk.Treeview(raw_table_frame, 
                                           columns=("ID", "Название", "Поставщик", "Количество", "Ед.изм."), 
                                           show="headings",
                                           yscrollcommand=raw_y_scrollbar.set,
                                           xscrollcommand=raw_x_scrollbar.set,
                                           selectmode="browse",
                                           style="Treeview")
        
        # Настройка заголовков
        self.raw_materials_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Название", text="Название", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Поставщик", text="Поставщик", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Количество", text="Количество", anchor=tk.CENTER)
        self.raw_materials_tree.heading("Ед.изм.", text="Ед.изм.", anchor=tk.CENTER)
        
        # Настройка столбцов
        self.raw_materials_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.raw_materials_tree.column("Название", width=150, minwidth=120, anchor=tk.W)
        self.raw_materials_tree.column("Поставщик", width=150, minwidth=120, anchor=tk.W)
        self.raw_materials_tree.column("Количество", width=100, minwidth=80, anchor=tk.CENTER)
        self.raw_materials_tree.column("Ед.изм.", width=80, minwidth=60, anchor=tk.CENTER)
        
        # Настройка скроллбаров
        raw_y_scrollbar.config(command=self.raw_materials_tree.yview)
        raw_x_scrollbar.config(command=self.raw_materials_tree.xview)
        
        # Размещение компонентов
        self.raw_materials_tree.grid(row=0, column=0, sticky="nsew")
        raw_y_scrollbar.grid(row=0, column=1, sticky="ns")
        raw_x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка весов строк и столбцов
        raw_table_frame.columnconfigure(0, weight=1)
        raw_table_frame.rowconfigure(0, weight=1)
        
        # Load suppliers and raw materials data
        self.load_suppliers()
        self.load_raw_materials()
    
    def create_employees_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Персонал")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
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
        
        # Создаем фрейм для таблицы и скроллбара
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создаем скроллбары
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # Create treeview for employees
        self.employees_tree = ttk.Treeview(table_frame, 
                                       columns=("ID", "Имя", "Должность", "Телефон"), 
                                       show="headings",
                                       yscrollcommand=y_scrollbar.set,
                                       xscrollcommand=x_scrollbar.set,
                                       selectmode="browse")
        
        # Настройка заголовков
        self.employees_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.employees_tree.heading("Имя", text="Имя", anchor=tk.CENTER)
        self.employees_tree.heading("Должность", text="Должность", anchor=tk.CENTER)
        self.employees_tree.heading("Телефон", text="Телефон", anchor=tk.CENTER)
        
        # Настройка столбцов
        self.employees_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        self.employees_tree.column("Имя", width=200, minwidth=150, anchor=tk.W)
        self.employees_tree.column("Должность", width=150, minwidth=100, anchor=tk.W)
        self.employees_tree.column("Телефон", width=150, minwidth=100, anchor=tk.W)
        
        # Настройка скроллбаров
        y_scrollbar.config(command=self.employees_tree.yview)
        x_scrollbar.config(command=self.employees_tree.xview)
        
        # Размещение компонентов
        self.employees_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка весов строк и столбцов
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Load employees data
        self.load_employees()
    
    def create_reports_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Отчетность и налоги")
        
        # Создаем контейнер с градиентным фоном
        gradient_frame = self.create_gradient_frame(tab, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.7)
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        
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
        gradient_frame = self.create_gradient_frame(tab, 1600, 1000)
        gradient_frame.pack(fill="both", expand=True)
        
        # Создаем фрейм для содержимого поверх градиента
        content_frame = ttk.Frame(gradient_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
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
                tag = self.row_tags[count % 2] if hasattr(self, 'row_tags') else ''
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
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректную цену")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                # Получаем следующий доступный ID
                next_id = self.get_next_id(cursor, "menu_items")
                cursor.execute("INSERT INTO menu_items (id, name, price) VALUES (?, ?, ?)", (next_id, name, price_val))
                # Обновляем значение автоинкремента
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'menu_items'", (next_id,))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('menu_items', ?)", (next_id,))
                conn.commit()
                conn.close()
                self.load_menu_items()
                dialog.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить изделие: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

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
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректную цену")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE menu_items SET name=?, price=? WHERE id=?", (name, price_val, item[0]))
                conn.commit()
                conn.close()
                self.load_menu_items()
                dialog.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось обновить изделие: {str(e)}")
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_menu_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите изделие для удаления")
            return
        item = self.menu_tree.item(selected[0])['values']
        if messagebox.askyesno("Подтвердите удаление", f"Удалить изделие '{item[1]}'?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM menu_items WHERE id=?", (item[0],))
                conn.commit()
                conn.close()
                self.load_menu_items()
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось удалить изделие: {str(e)}")
    
    # Database operations methods
    def load_trade_points(self):
        # Clear current data
        for item in self.trade_points_tree.get_children():
            self.trade_points_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, address FROM trade_points")
            
            # Добавляем строки с чередующимися цветами
            count = 0
            for row in cursor.fetchall():
                tag = self.row_tags[count % 2]
                self.trade_points_tree.insert("", "end", values=(row['id'], row['name'], row['address']), tags=(tag,))
                count += 1
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить торговые точки: {str(e)}")
    
    def load_orders(self):
        # Clear current data
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, full_name, phone, address, email, event, 
                       event_date, delivery_time, status
                FROM customer_orders
                ORDER BY id ASC
            """)
            orders = cursor.fetchall()
            
            for order in orders:
                # Форматируем номер телефона, если возможно
                phone_display = order["phone"]
                if phone_display:
                    # Попытка форматирования номера в маску
                    digits = ''.join(filter(str.isdigit, phone_display))
                    if len(digits) == 11:
                        phone_display = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
                
                self.orders_tree.insert("", "end", values=(
                    order["id"],
                    order["full_name"],
                    phone_display,
                    order["address"],
                    order["email"],
                    order["event"],
                    order["event_date"],
                    order["delivery_time"],
                    order["status"]
                ))
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить заказы: {str(e)}")
    
    def load_suppliers(self):
        # Clear current data
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, contact, phone FROM suppliers")
            
            # Добавляем строки с чередующимися цветами
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
        # Clear current data
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
            
            # Добавляем строки с чередующимися цветами
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
        # Clear current data
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, position, phone FROM employees")
            
            # Добавляем строки с чередующимися цветами
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
    
    # Trade points methods
    def add_trade_point(self):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить торговую точку")
        dialog.geometry("300x200")
        dialog.grab_set()  # Make dialog modal
        
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
                
                # Получаем максимальный существующий ID
                cursor.execute("SELECT MAX(id) FROM trade_points")
                max_id = cursor.fetchone()[0]
                next_id = 1 if max_id is None else max_id + 1
                
                # Вставляем новую запись с явным указанием ID
                cursor.execute(
                    "INSERT INTO trade_points (id, name, address) VALUES (?, ?, ?)",
                    (next_id, name, address)
                )
                
                # Обновляем значение автоинкремента
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
        
        # Get selected item data
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
            
            # Create dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать торговую точку")
            dialog.geometry("300x200")
            dialog.grab_set()  # Make dialog modal
            
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
        
        # Check if trade point has related orders
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
                # First delete related orders
                cursor.execute("DELETE FROM orders WHERE trade_point_id = ?", (item_id,))
                
                # Then delete the trade point
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
    
    # Orders methods
    def add_order(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить заказ")
        dialog.geometry("800x800")
        dialog.grab_set()

        # --- Форма заказа ---
        order_frame = ttk.LabelFrame(dialog, text="Данные заказа")
        order_frame.pack(fill="x", padx=10, pady=5)

        placeholders = {
            "full_name": "Введите ФИО полностью",
            "phone": "Формат: +7XXXXXXXXXX или 8XXXXXXXXXX",
            "address": "Введите полный адрес доставки",
            "email": "example@domain.com",
            "event": "Название и тип мероприятия",
            "event_date": "Формат: ДД-ММ-ГГГГ (например, 01-03-2025)",
            "delivery_time": "Формат: ЧЧ:ММ (например, 14:30)"
        }

        fields = [
            ("ID", "id", None),
            ("ФИО*", "full_name", None),
            ("📱 Телефон*", "phone", None),
            ("🏠 Адрес доставки*", "address", None),
            ("📧 Email*", "email", None),
            ("🎉 Мероприятие*", "event", None),
            ("📅 Дата мероприятия*", "event_date", None),
            ("⏰ Время доставки (ЧЧ:ММ)*", "delivery_time", None)
        ]

        entries = {}
        for label, key, _ in fields:
            frame = ttk.Frame(order_frame)
            frame.pack(fill="x", pady=(8, 0), padx=18)
            ttk.Label(frame, text=label, font=("Helvetica", 13)).pack(anchor="w")
            entry = ttk.Entry(frame, font=("Helvetica", 13))
            entry.pack(fill="x", pady=(0, 2))
            if key in placeholders:
                entry.insert(0, placeholders[key])
                entry.config(foreground='gray')
                def on_focus_in(event, e=entry, p=placeholders[key]):
                    if e.get() == p:
                        e.delete(0, tk.END)
                        e.config(foreground='black')
                def on_focus_out(event, e=entry, p=placeholders[key]):
                    if not e.get():
                        e.insert(0, p)
                        e.config(foreground='gray')
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)
            entries[key] = entry
        # Автоматически подставляем следующий ID
        try:
            conn = get_connection()
            cursor = conn.cursor()
            next_id = self.get_next_id(cursor, "customer_orders")
            entries["id"].insert(0, str(next_id))
            entries["id"].config(state="readonly", foreground='black')
            conn.close()
        except Exception:
            pass

        # --- Меню выбора изделий ---
        order = {}
        def show_menu():
            menu_window = tk.Toplevel(dialog)
            menu_window.title("Выбор изделий")
            menu_window.geometry("400x500")
            menu_window.configure(bg="#E0E0E0")
            menu_window.grab_set()  # Make window modal
            menu_window.transient(dialog)  # Make window always on top of parent
            
            # Create main frame
            main_frame = ttk.Frame(menu_window)
            main_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Create canvas with scrollbar
            canvas = tk.Canvas(main_frame, highlightthickness=0, bg="#E0E0E0")
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            
            # Create frame for content
            scrollable_frame = ttk.Frame(canvas)
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            # Configure canvas
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=365)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Bind mouse wheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Load menu items
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price FROM menu_items")
            menu_items = cursor.fetchall()
            conn.close()
            
            menu_item_qty_vars = {}
            
            def validate_qty(new_value, item_id):
                if new_value == "":
                    return True
                if new_value.isdigit():
                    return True
                messagebox.showerror("Ошибка", "Введите только целое число для количества!")
                menu_item_qty_vars[item_id].set("0")
                return False
            
            def update_order_local(item_id):
                qty = menu_item_qty_vars[item_id].get()
                if qty.isdigit() and int(qty) > 0:
                    order[item_id] = int(qty)
                elif item_id in order:
                    del order[item_id]
                update_order_display()
            
            # Create items list
            for item in menu_items:
                item_frame = ttk.Frame(scrollable_frame)
                item_frame.pack(fill="x", pady=5, padx=10)
                
                ttk.Label(item_frame, text=f"{item['name']} ({item['price']:.2f} руб.)",
                         font=("Helvetica", 13)).pack(side="left")
                
                qty_var = tk.StringVar(value=str(order.get(item['id'], 0)))
                menu_item_qty_vars[item['id']] = qty_var
                vcmd = (menu_window.register(lambda nv, iid=item['id']: validate_qty(nv, iid)), '%P')
                qty_entry = ttk.Entry(item_frame, textvariable=qty_var, width=5,
                                    font=("Helvetica", 13), validate='key', validatecommand=vcmd)
                qty_entry.pack(side="right", padx=5)
                qty_entry.bind("<FocusOut>", lambda e, iid=item['id']: update_order_local(iid))
                qty_entry.bind("<Return>", lambda e, iid=item['id']: update_order_local(iid))
                
                ttk.Label(item_frame, text="шт.", font=("Helvetica", 13)).pack(side="right")
            
            # Add buttons frame
            buttons_frame = ttk.Frame(scrollable_frame)
            buttons_frame.pack(fill="x", pady=20, padx=10)
            
            def on_close():
                canvas.unbind_all("<MouseWheel>")
                menu_window.destroy()
                update_order_display()
            
            btn_done = GradientButton(buttons_frame, text="Готово", command=on_close)
            btn_done.pack(expand=True)

        # Кнопка меню
        menu_btn_frame = ttk.Frame(dialog)
        menu_btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(menu_btn_frame, text="Меню изделий", command=show_menu).pack(pady=10)
        # --- Отображение выбранных изделий и суммы ---
        order_display_frame = ttk.Frame(dialog)
        order_display_frame.pack(fill="x", padx=10, pady=5)
        total_amount_var = tk.StringVar(value="Итого: 0.00 руб.")
        total_label = ttk.Label(dialog, textvariable=total_amount_var, font=("Helvetica", 15, "bold"), background="#E0E0E0")
        total_label.pack(anchor="e", pady=(5, 0), padx=10)
        def update_order_display():
            for widget in order_display_frame.winfo_children():
                widget.destroy()
            conn = get_connection()
            cursor = conn.cursor()
            total = 0.0
            for item_id, qty in order.items():
                cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
                item = cursor.fetchone()
                if item:
                    price = item['price'] * qty
                    total += price
                    item_frame = ttk.Frame(order_display_frame)
                    item_frame.pack(fill="x", pady=2)
                    ttk.Label(item_frame, text=f"{item['name']} x{qty}", font=("Helvetica", 13)).pack(side="left")
                    ttk.Label(item_frame, text=f"{price:.2f} руб.", font=("Helvetica", 13)).pack(side="right")
            conn.close()
            total_amount_var.set(f"Итого: {total:.2f} руб.")
        # --- Валидация ---
        def validate_phone(phone):
            # Remove all non-digit characters
            digits = ''.join(filter(str.isdigit, phone))
            
            # Check if the number has the correct length (11 digits for Russian numbers)
            if len(digits) != 11:
                return False, "Номер телефона должен содержать 11 цифр"
            
            # Format the phone number
            formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            return True, formatted
        def validate_email(email):
            pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
            return bool(pattern.match(email))
        def validate_time(time_str):
            pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
            return bool(pattern.match(time_str))
        def get_entry_value(entry, key):
            val = entry.get().strip()
            if key in placeholders and (val == placeholders[key] or not val):
                return ""
            return val
        # --- Сохранение заказа ---
        def save():
            # Получаем значения из полей
            values = {}
            for key, entry in entries.items():
                values[key] = get_entry_value(entry, key)
                if not values[key]:
                    messagebox.showwarning("Предупреждение", f"Заполните поле {placeholders[key]}")
                    return

            # Проверяем формат телефона
            if not validate_phone(values["phone"]):
                messagebox.showwarning("Предупреждение", "Неверный формат телефона")
                return

            # Проверяем формат email
            if not validate_email(values["email"]):
                messagebox.showwarning("Предупреждение", "Неверный формат email")
                return

            # Проверяем формат времени
            if not validate_time(values["delivery_time"]):
                messagebox.showwarning("Предупреждение", "Неверный формат времени (используйте ЧЧ:ММ)")
                return

            # Проверяем, что выбраны товары
            if not order:
                messagebox.showwarning("Предупреждение", "Выберите хотя бы один товар")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Получаем следующий доступный ID
                next_id = self.get_next_id(cursor, "customer_orders")
                
                # Подготавливаем данные о заказанных товарах
                order_items = []
                total_price = 0.0
                
                # Получаем информацию о каждом товаре
                for item_id, qty in order.items():
                    cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
                    item = cursor.fetchone()
                    if item:
                        item_total = item['price'] * qty
                        total_price += item_total
                        order_items.append({
                            'id': item_id,
                            'name': item['name'],
                            'price': item['price'],
                            'quantity': qty,
                            'sum': item_total
                        })
                
                # Преобразуем список товаров в JSON
                order_items_json = json.dumps(order_items)
                
                # Формируем описание заказа
                description = "\n".join([f"{item['name']} — {item['quantity']} шт. (по {item['price']:.2f} руб.)" for item in order_items])

                # Вставляем заказ
                cursor.execute("""
                    INSERT INTO customer_orders (
                        full_name, phone, address, email, event, event_date, 
                        delivery_time, description, order_items, total_price, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'новый')
                """, (
                    values["full_name"], values["phone"], values["address"], 
                    values["email"], values["event"], values["event_date"], 
                    values["delivery_time"], description,
                    order_items_json, total_price
                ))

                conn.commit()
                conn.close()
                self.load_orders()
                dialog.destroy()
                messagebox.showinfo("Успех", "Заказ добавлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить заказ: {str(e)}")
        # --- Кнопки ---
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Назад", command=dialog.destroy).pack(side="left", padx=10)
    
    def edit_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для редактирования")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, full_name, phone, address, email, event, event_date, 
                       delivery_time, description, order_items, total_price, status 
                FROM customer_orders WHERE id = ?
            """, (order_id,))
            order_data = cursor.fetchone()
            conn.close()
            
            if not order_data:
                messagebox.showerror("Ошибка", "Заказ не найден")
                return
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать заказ")
            dialog.geometry("800x800")
            dialog.grab_set()

            # --- Форма заказа ---
            order_frame = ttk.LabelFrame(dialog, text="Данные заказа")
            order_frame.pack(fill="x", padx=10, pady=5)

            placeholders = {
                "full_name": "Введите ФИО полностью",
                "phone": "Формат: +7XXXXXXXXXX или 8XXXXXXXXXX",
                "address": "Введите полный адрес доставки",
                "email": "example@domain.com",
                "event": "Название и тип мероприятия",
                "event_date": "Формат: ДД-ММ-ГГГГ (например, 01-03-2025)",
                "delivery_time": "Формат: ЧЧ:ММ (например, 14:30)"
            }

            fields = [
                ("ID", "id", None),
                ("ФИО*", "full_name", None),
                ("📱 Телефон*", "phone", None),
                ("🏠 Адрес доставки*", "address", None),
                ("📧 Email*", "email", None),
                ("🎉 Мероприятие*", "event", None),
                ("📅 Дата мероприятия*", "event_date", None),
                ("⏰ Время доставки (ЧЧ:ММ)*", "delivery_time", None)
            ]
            entries = {}
            
            for label, key, _ in fields:
                frame = ttk.Frame(order_frame)
                frame.pack(fill="x", pady=(8, 0), padx=18)
                ttk.Label(frame, text=label, font=("Helvetica", 13)).pack(anchor="w")
                entry = ttk.Entry(frame, font=("Helvetica", 13))
                entry.pack(fill="x", pady=(0, 2))
                
                # Заполняем поля текущими значениями
                if key == "id":
                    entry.insert(0, str(order_data[key]))
                    entry.config(state="readonly", foreground='black')
                else:
                    entry.insert(0, str(order_data[key] if order_data[key] else ""))
                    if key in placeholders:
                        def on_focus_in(event, e=entry, p=placeholders[key]):
                            if e.get() == p:
                                e.delete(0, tk.END)
                                e.config(foreground='black')
                        def on_focus_out(event, e=entry, p=placeholders[key]):
                            if not e.get():
                                e.insert(0, p)
                                e.config(foreground='gray')
                        entry.bind('<FocusIn>', on_focus_in)
                        entry.bind('<FocusOut>', on_focus_out)
                entries[key] = entry

            # --- Добавляем выпадающий список для статуса ---
            status_frame = ttk.Frame(order_frame)
            status_frame.pack(fill="x", pady=(8, 0), padx=18)
            ttk.Label(status_frame, text="Статус заказа*", font=("Helvetica", 13)).pack(anchor="w")
            status_var = tk.StringVar(value=order_data['status'])
            status_combobox = ttk.Combobox(status_frame, 
                                         textvariable=status_var,
                                         values=["новый", "в обработке", "выполнен", "отменён"],
                                         state="readonly",
                                         font=("Helvetica", 13))
            status_combobox.pack(fill="x", pady=(0, 2))

            # --- Меню выбора изделий ---
            order = {}
            if order_data['order_items']:
                order_items = json.loads(order_data['order_items'])
                for item in order_items:
                    order[item['id']] = item['quantity']

            def show_menu():
                menu_window = tk.Toplevel(dialog)
                menu_window.title("Выбор изделий")
                menu_window.geometry("400x500")
                menu_window.configure(bg="#E0E0E0")
                menu_window.grab_set()
                menu_window.transient(dialog)
                
                main_frame = ttk.Frame(menu_window)
                main_frame.pack(fill="both", expand=True, padx=5, pady=5)
                
                canvas = tk.Canvas(main_frame, highlightthickness=0, bg="#E0E0E0")
                scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
                
                scrollable_frame = ttk.Frame(canvas)
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=365)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, price FROM menu_items")
                menu_items = cursor.fetchall()
                conn.close()
                
                menu_item_qty_vars = {}
                
                def validate_qty(new_value, item_id):
                    if new_value == "":
                        return True
                    if new_value.isdigit():
                        return True
                    messagebox.showerror("Ошибка", "Введите только целое число для количества!")
                    menu_item_qty_vars[item_id].set("0")
                    return False
                
                def update_order_local(item_id):
                    qty = menu_item_qty_vars[item_id].get()
                    if qty.isdigit() and int(qty) > 0:
                        order[item_id] = int(qty)
                    elif item_id in order:
                        del order[item_id]
                    update_order_display()
                
                for item in menu_items:
                    item_frame = ttk.Frame(scrollable_frame)
                    item_frame.pack(fill="x", pady=5, padx=10)
                    
                    ttk.Label(item_frame, text=f"{item['name']} ({item['price']:.2f} руб.)",
                             font=("Helvetica", 13)).pack(side="left")
                    
                    qty_var = tk.StringVar(value=str(order.get(item['id'], 0)))
                    menu_item_qty_vars[item['id']] = qty_var
                    vcmd = (menu_window.register(lambda nv, iid=item['id']: validate_qty(nv, iid)), '%P')
                    qty_entry = ttk.Entry(item_frame, textvariable=qty_var, width=5,
                                        font=("Helvetica", 13), validate='key', validatecommand=vcmd)
                    qty_entry.pack(side="right", padx=5)
                    qty_entry.bind("<FocusOut>", lambda e, iid=item['id']: update_order_local(iid))
                    qty_entry.bind("<Return>", lambda e, iid=item['id']: update_order_local(iid))
                    
                    ttk.Label(item_frame, text="шт.", font=("Helvetica", 13)).pack(side="right")
                
                buttons_frame = ttk.Frame(scrollable_frame)
                buttons_frame.pack(fill="x", pady=20, padx=10)
                
                def on_close():
                    canvas.unbind_all("<MouseWheel>")
                    menu_window.destroy()
                    update_order_display()
                
                btn_done = GradientButton(buttons_frame, text="Готово", command=on_close)
                btn_done.pack(expand=True)

            menu_btn_frame = ttk.Frame(dialog)
            menu_btn_frame.pack(fill="x", padx=10, pady=5)
            ttk.Button(menu_btn_frame, text="Меню изделий", command=show_menu).pack(pady=10)

            order_display_frame = ttk.Frame(dialog)
            order_display_frame.pack(fill="x", padx=10, pady=5)
            total_amount_var = tk.StringVar(value="Итого: 0.00 руб.")
            total_label = ttk.Label(dialog, textvariable=total_amount_var, font=("Helvetica", 15, "bold"), background="#E0E0E0")
            total_label.pack(anchor="e", pady=(5, 0), padx=10)

            def update_order_display():
                for widget in order_display_frame.winfo_children():
                    widget.destroy()
                conn = get_connection()
                cursor = conn.cursor()
                total = 0.0
                for item_id, qty in order.items():
                    cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
                    item = cursor.fetchone()
                    if item:
                        price = item['price'] * qty
                        total += price
                        item_frame = ttk.Frame(order_display_frame)
                        item_frame.pack(fill="x", pady=2)
                        ttk.Label(item_frame, text=f"{item['name']} x{qty}", font=("Helvetica", 13)).pack(side="left")
                        ttk.Label(item_frame, text=f"{price:.2f} руб.", font=("Helvetica", 13)).pack(side="right")
                conn.close()
                total_amount_var.set(f"Итого: {total:.2f} руб.")

            update_order_display()

            def validate_phone(phone):
                # Remove all non-digit characters
                digits = ''.join(filter(str.isdigit, phone))
                
                # Check if the number has the correct length (11 digits for Russian numbers)
                if len(digits) != 11:
                    return False, "Номер телефона должен содержать 11 цифр"
                
                # Format the phone number
                formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
                return True, formatted

            def validate_email(email):
                pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
                return bool(pattern.match(email))

            def validate_time(time_str):
                pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
                return bool(pattern.match(time_str))

            def get_entry_value(entry, key):
                val = entry.get().strip()
                if key in placeholders and (val == placeholders[key] or not val):
                    return ""
                return val

            def save():
                # Получаем значения из полей
                values = {}
                for key, entry in entries.items():
                    values[key] = get_entry_value(entry, key)
                    if not values[key]:
                        messagebox.showwarning("Предупреждение", f"Заполните поле {placeholders[key]}")
                        return

                # Проверяем формат телефона
                is_valid, phone_result = validate_phone(values["phone"])
                if not is_valid:
                    messagebox.showwarning("Предупреждение", phone_result)
                    return
                values["phone"] = phone_result

                # Проверяем формат email
                if not validate_email(values["email"]):
                    messagebox.showwarning("Предупреждение", "Неверный формат email")
                    return

                # Проверяем формат времени
                if not validate_time(values["delivery_time"]):
                    messagebox.showwarning("Предупреждение", "Неверный формат времени (используйте ЧЧ:ММ)")
                    return

                # Проверяем, что выбраны товары
                if not order:
                    messagebox.showwarning("Предупреждение", "Выберите хотя бы один товар")
                    return

                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    # Подготавливаем данные о заказанных товарах
                    order_items = []
                    total_price = 0.0
                    
                    # Получаем информацию о каждом товаре
                    for item_id, qty in order.items():
                        cursor.execute("SELECT name, price FROM menu_items WHERE id = ?", (item_id,))
                        item = cursor.fetchone()
                        if item:
                            item_total = item['price'] * qty
                            total_price += item_total
                            order_items.append({
                                'id': item_id,
                                'name': item['name'],
                                'price': item['price'],
                                'quantity': qty,
                                'sum': item_total
                            })
                    
                    # Преобразуем список товаров в JSON
                    order_items_json = json.dumps(order_items)
                    
                    # Формируем описание заказа
                    description = "\n".join([f"{item['name']} — {item['quantity']} шт. (по {item['price']:.2f} руб.)" for item in order_items])

                    # Обновляем заказ
                    cursor.execute("""
                        UPDATE customer_orders SET 
                            full_name = ?, phone = ?, address = ?, email = ?, 
                            event = ?, event_date = ?, delivery_time = ?, description = ?,
                            order_items = ?, total_price = ?, status = ?
                        WHERE id = ?
                    """, (
                        values["full_name"], values["phone"], values["address"], 
                        values["email"], values["event"], values["event_date"], 
                        values["delivery_time"], description,
                        order_items_json, total_price, status_var.get(), order_id
                    ))

                    conn.commit()
                    conn.close()
                    self.load_orders()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Заказ обновлен")
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка базы данных", f"Не удалось обновить заказ: {str(e)}")

            # --- Кнопки ---
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(pady=18)
            ttk.Button(btn_frame, text="Сохранить", command=save).pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Назад", command=dialog.destroy).pack(side="left", padx=10)
        
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для удаления")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот заказ?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Удаляем заказ
                cursor.execute("DELETE FROM customer_orders WHERE id = ?", (order_id,))
                
                # Получаем максимальный ID после удаления
                cursor.execute("SELECT MAX(id) FROM customer_orders")
                max_id = cursor.fetchone()[0]
                
                # Обновляем sequence
                if max_id is None:
                    # Если таблица пуста, сбрасываем sequence в 0
                    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'customer_orders'")
                    if cursor.rowcount == 0:
                        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('customer_orders', 0)")
                else:
                    # Иначе устанавливаем sequence в максимальный ID
                    cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'customer_orders'", (max_id,))
                    if cursor.rowcount == 0:
                        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('customer_orders', ?)", (max_id,))
                
                conn.commit()
                conn.close()
                
                self.load_orders()
                messagebox.showinfo("Успех", "Заказ удален")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось удалить заказ: {str(e)}")
    
    def view_orders(self):
        # Create a report window
        report_window = tk.Toplevel(self.root)
        report_window.title("Просмотр списка заказов")
        report_window.geometry("1200x600")

        # Create a frame for filters
        filter_frame = ttk.LabelFrame(report_window, text="Фильтры")
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Status filter
        ttk.Label(filter_frame, text="Статус:").grid(row=0, column=0, padx=5, pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, width=20)
        status_combo['values'] = ["Все", "новый", "в обработке", "выполнен", "отменён"]
        status_combo.current(0)
        status_combo.grid(row=0, column=1, padx=5, pady=5)

        # Date range filter
        ttk.Label(filter_frame, text="Дата от:").grid(row=0, column=2, padx=5, pady=5)
        start_date_entry = ttk.Entry(filter_frame, width=12)
        start_date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="до:").grid(row=0, column=4, padx=5, pady=5)
        end_date_entry = ttk.Entry(filter_frame, width=12)
        end_date_entry.grid(row=0, column=5, padx=5, pady=5)

        # Set default date range (last 30 days)
        import datetime
        today = datetime.datetime.now()
        end_date_entry.insert(0, today.strftime("%d-%m-%Y"))
        start_date = today - datetime.timedelta(days=30)
        start_date_entry.insert(0, start_date.strftime("%d-%m-%Y"))

        # Create a frame for the table
        table_frame = ttk.Frame(report_window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")

        # Create treeview for orders with the same columns as the main orders table
        report_tree = ttk.Treeview(table_frame,
                             columns=("id", "full_name", "phone", "address", 
                                       "email", "event", "event_date", "delivery_time", "status"),
                             show="headings",
                             yscrollcommand=y_scrollbar.set,
                             xscrollcommand=x_scrollbar.set)
        
        # Configure headings
        report_tree.heading("id", text="ID")
        report_tree.heading("full_name", text="ФИО")
        report_tree.heading("phone", text="Телефон")
        report_tree.heading("address", text="Адрес")
        report_tree.heading("email", text="Email")
        report_tree.heading("event", text="Мероприятие")
        report_tree.heading("event_date", text="Дата")
        report_tree.heading("delivery_time", text="Время доставки")
        report_tree.heading("status", text="Статус")
        
        # Configure columns
        report_tree.column("id", width=50)
        report_tree.column("full_name", width=150)
        report_tree.column("phone", width=120)
        report_tree.column("address", width=200)
        report_tree.column("email", width=150)
        report_tree.column("event", width=150)
        report_tree.column("event_date", width=100)
        report_tree.column("delivery_time", width=100)
        report_tree.column("status", width=100)

        # Configure scrollbars
        y_scrollbar.config(command=report_tree.yview)
        x_scrollbar.config(command=report_tree.xview)

        # Position components
        report_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        def load_filtered_orders(is_initial_load=False):
            # Clear current data
            for item in report_tree.get_children():
                report_tree.delete(item)

            # Get filter values
            status = status_var.get()
            print(f"DEBUG - Selected status: '{status}'")  # Отладка статуса из комбобокса
            start = start_date_entry.get().strip()
            end = end_date_entry.get().strip()

            try:
                # Обновляем статус
                status_label.config(text="Загрузка данных...")

                # Проверяем формат дат (без преобразования), так как в базе даты хранятся как DD-MM-YYYY
                if start:
                    try:
                        # Проверка корректности формата
                        datetime.datetime.strptime(start, "%d-%m-%Y")
                    except ValueError:
                        messagebox.showwarning("Предупреждение", "Введите дату начала в формате ДД-ММ-ГГГГ")
                        # Сбрасываем дату начала и перезапускаем
                        start_date_entry.delete(0, tk.END)
                        load_filtered_orders(is_initial_load)
                        return
                if end:
                    try:
                        # Проверка корректности формата
                        datetime.datetime.strptime(end, "%d-%m-%Y")
                    except ValueError:
                        messagebox.showwarning("Предупреждение", "Введите дату окончания в формате ДД-ММ-ГГГГ")
                        # Сбрасываем дату окончания и перезапускаем
                        end_date_entry.delete(0, tk.END)
                        load_filtered_orders(is_initial_load)
                        return

                conn = get_connection()
                if conn is None:
                    messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
                    status_label.config(text="Ошибка подключения к базе данных")
                    return

                cursor = conn.cursor()

                # Проверяем существование таблицы
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customer_orders'")
                if not cursor.fetchone():
                    print("ОШИБКА: Таблица customer_orders не существует!")
                    messagebox.showerror("Ошибка", "Таблица customer_orders не существует!")
                    conn.close()
                    status_label.config(text="Ошибка: таблица customer_orders не существует")
                    return

                # Формируем SQL-запрос с фильтрами
                query = """
                    SELECT id, full_name, phone, address, email, event, 
                        event_date, delivery_time, status
                    FROM customer_orders
                    WHERE 1=1
                """
                params = []

                # Проверяем, применены ли фильтры
                filters_applied = False

                if status and status != "Все":
                    query += " AND status = ?"
                    params.append(status)
                    print(f"DEBUG - Фильтрация по статусу: '{status}'")  # Отладка
                    filters_applied = True

                # Для дат используем простое строковое сравнение, так как формат в БД уже DD-MM-YYYY
                if start:
                    query += " AND event_date >= ?"
                    params.append(start)
                    filters_applied = True

                if end:
                    query += " AND event_date <= ?"
                    params.append(end)
                    filters_applied = True

                query += " ORDER BY id ASC"

                print(f"DEBUG - Executing query: {query} with params: {params}")  # Debugging
                cursor.execute(query, params)
                orders = cursor.fetchall()
                print(f"DEBUG - Found {len(orders)} orders")  # Debugging
                
                # Выводим детали каждого найденного заказа
                for i, order in enumerate(orders):
                    print(f"DEBUG - Order {i+1}:")
                    for key in order.keys():
                        print(f"  {key}: {order[key]}")
                
                # Проверяем, есть ли записи
                if len(orders) == 0:
                    print("DEBUG - Нет данных по указанным фильтрам")
                    # Если применялись фильтры, предложим сбросить их
                    # Показываем диалог только если это не первоначальная загрузка и применены фильтры
                    if filters_applied and not is_initial_load:
                        if messagebox.askyesno("Нет данных", "По указанным фильтрам заказов не найдено. Сбросить фильтры?"):
                            status_combo.current(0)
                            start_date_entry.delete(0, tk.END)
                            end_date_entry.delete(0, tk.END)
                            # Повторяем запрос без фильтров
                            load_filtered_orders(False)
                            return
                
                # Отображаем полученные данные в точности как в методе load_orders
                for order in orders:
                    # Форматируем номер телефона, если возможно
                    phone_display = order["phone"]
                    if phone_display:
                        # Попытка форматирования номера в маску
                        digits = ''.join(filter(str.isdigit, phone_display))
                        if len(digits) == 11:
                            phone_display = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
                    
                    # Вставляем строку в дерево
                    report_tree.insert("", "end", values=(
                        order["id"],
                        order["full_name"],
                        phone_display,
                        order["address"],
                        order["email"],
                        order["event"],
                        order["event_date"],  # Используем дату как есть
                        order["delivery_time"],
                        order["status"]
                    ))
                
                conn.close()
                
                # Обновляем статус
                status_label.config(text=f"Найдено заказов: {len(orders)}")

            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить заказы: {str(e)}")
                print(f"SQL Error: {str(e)}")
                traceback.print_exc()
                status_label.config(text=f"Ошибка: {str(e)}")
                
                # Сбрасываем все фильтры и пробуем еще раз только если не первоначальная загрузка
                if not is_initial_load:
                    if messagebox.askyesno("Ошибка", "Произошла ошибка при загрузке данных. Сбросить фильтры и попробовать снова?"):
                        status_combo.current(0)
                        start_date_entry.delete(0, tk.END)
                        end_date_entry.delete(0, tk.END)
                        # Повторяем запрос без фильтров
                        load_filtered_orders(False)
            except Exception as e:
                messagebox.showerror("Неизвестная ошибка", f"Произошла неизвестная ошибка: {str(e)}")
                print(f"Unknown error: {str(e)}")
                traceback.print_exc()
                status_label.config(text=f"Неизвестная ошибка: {str(e)}")

        # Add filter button
        ttk.Button(filter_frame, text="Применить фильтр", command=lambda: load_filtered_orders(False)).grid(row=0, column=6, padx=10, pady=5)

        # Status label
        status_label = ttk.Label(report_window, text="Загрузка данных...")
        status_label.pack(anchor="w", padx=10, pady=5)

        # Buttons frame
        buttons_frame = ttk.Frame(report_window)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(buttons_frame, text="Закрыть", command=report_window.destroy).pack(side="right", padx=5)

        # Bind double-click event to show order details
        report_tree.bind("<Double-1>", lambda event: self.show_order_details(event, report_tree))

        # Load data initially
        load_filtered_orders()
    
    def export_to_csv(self, tree, filename):
        import csv
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = []
                for col in tree['columns']:
                    headers.append(tree.heading(col)['text'])
                writer.writerow(headers)
                
                # Write data
                for item_id in tree.get_children():
                    values = tree.item(item_id)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Успех", f"Данные экспортированы в файл {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")
    
    # Suppliers methods
    def add_supplier(self, tree):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить поставщика")
        dialog.geometry("300x250")
        dialog.grab_set()  # Make dialog modal
        
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Контактное лицо:").pack()
        contact_entry = ttk.Entry(dialog, width=30)
        contact_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Телефон:").pack()
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.pack(pady=(5, 10))
        
        def validate_phone(phone):
            # Remove all non-digit characters
            digits = ''.join(filter(str.isdigit, phone))
            
            # Check if the number has the correct length (11 digits for Russian numbers)
            if len(digits) != 11:
                return False, "Номер телефона должен содержать 11 цифр"
            
            # Format the phone number
            formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            return True, formatted
        
        def save_supplier():
            name = name_entry.get().strip()
            contact = contact_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Предупреждение", "Заполните название поставщика")
                return
            
            if phone:
                is_valid, result = validate_phone(phone)
                if not is_valid:
                    messagebox.showwarning("Предупреждение", result)
                    return
                phone = result
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Получаем следующий доступный ID
                next_id = self.get_next_id(cursor, "suppliers")
                
                # Вставляем новую запись с явным указанием ID
                cursor.execute(
                    "INSERT INTO suppliers (id, name, contact, phone) VALUES (?, ?, ?, ?)",
                    (next_id, name, contact, phone)
                )
                
                # Обновляем значение автоинкремента
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
        
        item = tree.item(selected[0])
        item_id = item['values'][0]
        
        dialog = tk.Toplevel()
        dialog.title("Редактировать поставщика")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Название:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, item['values'][1])
        name_entry.pack()
        
        ttk.Label(dialog, text="Контактное лицо:").pack(pady=5)
        contact_entry = ttk.Entry(dialog)
        contact_entry.insert(0, item['values'][2])
        contact_entry.pack()
        
        ttk.Label(dialog, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(dialog)
        phone_entry.insert(0, item['values'][3])
        phone_entry.pack()
        
        def validate_phone(phone):
            # Удаляем все нецифровые символы
            digits = ''.join(filter(str.isdigit, phone))
            
            # Проверяем длину и первую цифру
            if len(digits) != 11:
                return False
            if not (digits.startswith('7') or digits.startswith('8')):
                return False
            
            return True
        
        def update_supplier():
            name = name_entry.get().strip()
            contact = contact_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name or not contact or not phone:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            if not validate_phone(phone):
                messagebox.showwarning("Предупреждение", "Неверный формат телефона. Используйте формат +7(XXX)XXX-XX-XX или 8XXXXXXXXXX")
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
    
    def delete_supplier(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите поставщика для удаления")
            return
        
        item_id = tree.item(selected[0], "values")[0]
        
        # Check if supplier is used in raw materials
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM raw_materials WHERE supplier_id = ?", (item_id,))
            result = cursor.fetchone()
            
            if result and result['count'] > 0:
                if not messagebox.askyesno(
                    "Предупреждение", 
                    f"Данный поставщик имеет {result['count']} связанных позиций сырья.\n"
                    "При удалении поставщика будут удалены все связанные позиции сырья.\n"
                    "Вы уверены, что хотите продолжить?"
                ):
                    conn.close()
                    return
            
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого поставщика?"):
                # First delete related raw materials
                cursor.execute("DELETE FROM raw_materials WHERE supplier_id = ?", (item_id,))
                
                # Then delete the supplier
                cursor.execute("DELETE FROM suppliers WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                
                self.load_suppliers()
                messagebox.showinfo("Успех", "Поставщик и связанные позиции сырья удалены")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить поставщика: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    # Raw materials methods
    def add_raw_material(self, raw_tree, suppliers_tree):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить сырье")
        dialog.geometry("400x350")
        dialog.grab_set()  # Make dialog modal
        
        # Supplier selection
        ttk.Label(dialog, text="Поставщик:").pack(pady=(10, 0))
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=30)
        supplier_combo.pack(pady=(5, 10))
        
        # Material name
        ttk.Label(dialog, text="Наименование сырья:").pack()
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        
        # Quantity
        ttk.Label(dialog, text="Количество:").pack()
        quantity_frame = ttk.Frame(dialog)
        quantity_frame.pack(pady=(5, 10))
        
        quantity_entry = ttk.Entry(quantity_frame, width=15)
        quantity_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Unit
        unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(quantity_frame, textvariable=unit_var, width=10)
        unit_combo['values'] = ["кг", "л", "шт", "т"]
        unit_combo.current(0)
        unit_combo.pack(side=tk.LEFT)
        
        # Populate suppliers
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers = {row['name']: row['id'] for row in cursor.fetchall()}
            supplier_combo['values'] = list(suppliers.keys())
            if supplier_combo['values']:
                supplier_combo.current(0)
            
            # Also populate existing materials for selection
            ttk.Label(dialog, text="или выберите из существующих:").pack(pady=(10, 0))
            material_var = tk.StringVar()
            material_combo = ttk.Combobox(dialog, textvariable=material_var, width=30)
            
            cursor.execute("SELECT id, name FROM raw_materials")
            materials = [row['name'] for row in cursor.fetchall()]
            material_combo['values'] = materials
            material_combo.pack(pady=(5, 10))
            
            def on_material_select(event):
                selected_material = material_var.get()
                if selected_material:
                    # Fill the name field with selected material
                    name_entry.delete(0, tk.END)
                    name_entry.insert(0, selected_material)
                    
                    # Get details of this material
                    try:
                        cursor.execute("""
                            SELECT r.supplier_id, r.unit, s.name as supplier_name
                            FROM raw_materials r
                            LEFT JOIN suppliers s ON r.supplier_id = s.id
                            WHERE r.name = ?
                        """, (selected_material,))
                        material = cursor.fetchone()
                        if material:
                            # Set supplier and unit if found
                            if material['supplier_name'] in suppliers:
                                supplier_var.set(material['supplier_name'])
                            if material['unit']:
                                unit_var.set(material['unit'])
                    except sqlite3.Error as e:
                        pass  # Ignore errors here
            
            material_combo.bind("<<ComboboxSelected>>", on_material_select)
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список поставщиков: {str(e)}")
        
        def save_raw_material():
            supplier_name = supplier_var.get()
            if not supplier_name in suppliers:
                messagebox.showwarning("Предупреждение", "Выберите поставщика")
                return
                
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Предупреждение", "Введите наименование сырья")
                return
                
            quantity_str = quantity_entry.get().strip()
            try:
                quantity = float(quantity_str)
                if quantity <= 0:
                    raise ValueError("Количество должно быть положительным числом")
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректное количество (число)")
                return
                
            unit = unit_var.get()
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Check if this material already exists
                cursor.execute("SELECT id, quantity FROM raw_materials WHERE name = ? AND supplier_id = ?", 
                              (name, suppliers[supplier_name]))
                existing = cursor.fetchone()
                
                if existing:
                    # Update quantity for existing material
                    new_quantity = existing['quantity'] + quantity
                    cursor.execute(
                        "UPDATE raw_materials SET quantity = ? WHERE id = ?",
                        (new_quantity, existing['id'])
                    )
                    message = f"Добавлено {quantity} {unit} к существующему сырью"
                else:
                    # Получаем следующий доступный ID
                    next_id = self.get_next_id(cursor, "raw_materials")
                    
                    # Add new material with explicit ID
                    cursor.execute(
                        "INSERT INTO raw_materials (id, name, supplier_id, quantity, unit) VALUES (?, ?, ?, ?, ?)",
                        (next_id, name, suppliers[supplier_name], quantity, unit)
                    )
                    
                    # Обновляем значение автоинкремента
                    cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'raw_materials'", (next_id,))
                    if cursor.rowcount == 0:
                        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('raw_materials', ?)", (next_id,))
                    
                    message = "Новое сырье добавлено"
                
                conn.commit()
                conn.close()
                
                self.load_raw_materials()
                dialog.destroy()
                messagebox.showinfo("Успех", message)
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сырье: {str(e)}")
        
        # Buttons
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text="Заказать", command=save_raw_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_raw_material(self, raw_tree, suppliers_tree):
        selected = raw_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сырье для редактирования")
            return
        
        # Get selected item data
        item_id = raw_tree.item(selected[0], "values")[0]
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, unit, price, supplier_id, quantity FROM raw_materials WHERE id = ?", (item_id,))
            raw_material = cursor.fetchone()
            # Получаем список поставщиков
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers_list = cursor.fetchall()
            conn.close()
            
            if not raw_material:
                messagebox.showerror("Ошибка", "Сырье не найдено")
                return
            
            # Create dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать сырье")
            dialog.geometry("300x380")
            dialog.grab_set()  # Make dialog modal
            
            ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, raw_material['name'])
            name_entry.pack(pady=(5, 10))
            
            ttk.Label(dialog, text="Единица измерения:").pack()
            unit_var = tk.StringVar()
            unit_combo = ttk.Combobox(dialog, textvariable=unit_var, width=30)
            unit_combo['values'] = ["кг", "л", "шт", "т"]
            unit_combo.pack(pady=(5, 10))
            if raw_material['unit'] in unit_combo['values']:
                unit_var.set(raw_material['unit'])
            else:
                unit_combo.current(0)
            
            ttk.Label(dialog, text="Количество:").pack()
            quantity_entry = ttk.Entry(dialog, width=30)
            quantity_entry.insert(0, str(raw_material['quantity']))
            quantity_entry.pack(pady=(5, 10))
            
            ttk.Label(dialog, text="Цена:").pack()
            price_entry = ttk.Entry(dialog, width=30)
            price_entry.insert(0, raw_material['price'])
            price_entry.pack(pady=(5, 10))
            
            ttk.Label(dialog, text="Поставщик:").pack()
            supplier_var = tk.StringVar()
            supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=30)
            supplier_names = [supplier['name'] for supplier in suppliers_list]
            supplier_combo['values'] = supplier_names
            # Установить текущего поставщика
            current_supplier = next((s['name'] for s in suppliers_list if s['id'] == raw_material['supplier_id']), None)
            if current_supplier:
                supplier_var.set(current_supplier)
            elif supplier_names:
                supplier_combo.current(0)
                supplier_combo.pack(pady=(5, 10))
            
            def update_raw_material():
                name = name_entry.get().strip()
                unit = unit_var.get().strip()
                price = price_entry.get().strip()
                quantity = quantity_entry.get().strip()
                supplier_name = supplier_var.get().strip()
                
                if not name or not unit or not price or not quantity or not supplier_name:
                    messagebox.showwarning("Предупреждение", "Заполните все поля")
                    return
                try:
                    quantity_val = float(quantity)
                except ValueError:
                    messagebox.showwarning("Предупреждение", "Введите корректное количество (число)")
                    return
                # Найти id поставщика по имени
                supplier_id = next((s['id'] for s in suppliers_list if s['name'] == supplier_name), None)
                if supplier_id is None:
                    messagebox.showwarning("Предупреждение", "Поставщик не найден")
                    return
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE raw_materials SET name = ?, unit = ?, price = ?, quantity = ?, supplier_id = ? WHERE id = ?",
                        (name, unit, price, quantity_val, supplier_id, item_id)
                    )
                    conn.commit()
                    conn.close()
                    
                    self.load_raw_materials()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Сырье обновлено")
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось обновить сырье: {str(e)}")
            
            ttk.Button(dialog, text="Сохранить", command=update_raw_material).pack(fill="x", padx=20, pady=(15, 5))
            ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack(fill="x", padx=20, pady=(0, 10))
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
    
    def delete_raw_material(self, raw_tree):
        selected = raw_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сырье для удаления")
            return
        
        item_id = raw_tree.item(selected[0], "values")[0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это сырье?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM raw_materials WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                
                self.load_raw_materials()
                messagebox.showinfo("Успех", "Сырье удалено")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить сырье: {str(e)}")
                if 'conn' in locals():
                    conn.close()
    
    # Employees methods
    def add_employee(self):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить сотрудника")
        dialog.geometry("300x250")
        dialog.grab_set()  # Make dialog modal
        
        ttk.Label(dialog, text="ФИО:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Должность:").pack()
        position_entry = ttk.Entry(dialog, width=30)
        position_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Телефон:").pack()
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.pack(pady=(5, 10))
        
        def validate_phone(phone):
            # Remove all non-digit characters
            digits = ''.join(filter(str.isdigit, phone))
            
            # Check if the number has the correct length (11 digits for Russian numbers)
            if len(digits) != 11:
                return False, "Номер телефона должен содержать 11 цифр"
            
            # Format the phone number
            formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            return True, formatted
        
        def save_employee():
            name = name_entry.get().strip()
            position = position_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Предупреждение", "Заполните ФИО сотрудника")
                return
            
            if phone:
                is_valid, result = validate_phone(phone)
                if not is_valid:
                    messagebox.showwarning("Предупреждение", result)
                    return
                phone = result
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO employees (name, position, phone) VALUES (?, ?, ?)",
                    (name, position, phone)
                )
                conn.commit()
                conn.close()
                
                self.load_employees()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сотрудник добавлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {str(e)}")
        
        ttk.Button(dialog, text="Сохранить", command=save_employee).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def edit_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника для редактирования")
            return
        
        item = self.employees_tree.item(selected[0])
        item_id = item['values'][0]
        
        dialog = tk.Toplevel()
        dialog.title("Редактировать сотрудника")
        dialog.geometry("300x300")
        
        ttk.Label(dialog, text="ФИО:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, item['values'][1])
        name_entry.pack()
        
        ttk.Label(dialog, text="Должность:").pack(pady=5)
        position_entry = ttk.Entry(dialog)
        position_entry.insert(0, item['values'][2])
        position_entry.pack()
        
        ttk.Label(dialog, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(dialog)
        phone_entry.insert(0, item['values'][3])
        phone_entry.pack()
        
        def validate_phone(phone):
            # Удаляем все нецифровые символы
            digits = ''.join(filter(str.isdigit, phone))
            
            # Проверяем длину и первую цифру
            if len(digits) != 11:
                return False
            if not (digits.startswith('7') or digits.startswith('8')):
                return False
            
            return True
        
        def update_employee():
            name = name_entry.get().strip()
            position = position_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name or not position or not phone:
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            if not validate_phone(phone):
                messagebox.showwarning("Предупреждение", "Неверный формат телефона. Используйте формат +7(XXX)XXX-XX-XX или 8XXXXXXXXXX")
                return
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE employees SET name = ?, position = ?, phone = ? WHERE id = ?",
                    (name, position, phone, item_id)
                )
                conn.commit()
                conn.close()
                
                self.load_employees()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сотрудник обновлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить сотрудника: {str(e)}")
        
        ttk.Button(dialog, text="Сохранить", command=update_employee).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def delete_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника для удаления")
            return
        
        item_id = self.employees_tree.item(selected[0], "values")[0]
        
        # Check if employee has work schedules
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM work_schedules WHERE employee_id = ?", (item_id,))
            result = cursor.fetchone()
            
            if result and result['count'] > 0:
                if not messagebox.askyesno(
                    "Предупреждение", 
                    f"Данный сотрудник имеет {result['count']} записей в графике работы.\n"
                    "При удалении сотрудника будут удалены все связанные графики.\n"
                    "Вы уверены, что хотите продолжить?"
                ):
                    conn.close()
                    return
            
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого сотрудника?"):
                # First delete related work schedules
                cursor.execute("DELETE FROM work_schedules WHERE employee_id = ?", (item_id,))
                
                # Then delete the employee
                cursor.execute("DELETE FROM employees WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                
                self.load_employees()
                messagebox.showinfo("Успех", "Сотрудник и связанные графики удалены")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить сотрудника: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    def view_work_schedule(self):
        # Check if we have employees first
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM employees")
            result = cursor.fetchone()
            
            if result and result['count'] == 0:
                messagebox.showinfo("Информация", "Сначала добавьте сотрудников")
                conn.close()
                return
            
            # Create work schedule window
            schedule_window = tk.Toplevel(self.root)
            schedule_window.title("График работы сотрудников")
            schedule_window.geometry("900x600")
            
            # Create a frame for employee selection
            selection_frame = ttk.LabelFrame(schedule_window, text="Выбор сотрудника")
            selection_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(selection_frame, text="Сотрудник:").grid(row=0, column=0, padx=5, pady=5)
            employee_var = tk.StringVar()
            employee_combo = ttk.Combobox(selection_frame, textvariable=employee_var, width=30)
            
            # Populate employees
            cursor.execute("SELECT id, name FROM employees")
            employees = {row['name']: row['id'] for row in cursor.fetchall()}
            employee_combo['values'] = list(employees.keys())
            if employee_combo['values']:
                employee_combo.current(0)
            
            employee_combo.grid(row=0, column=1, padx=5, pady=5)
            
            # Create a frame for schedule display
            schedule_frame = ttk.Frame(schedule_window)
            schedule_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create scrollbars
            y_scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical")
            x_scrollbar = ttk.Scrollbar(schedule_frame, orient="horizontal")
            
            # Create treeview for schedule
            schedule_tree = ttk.Treeview(schedule_frame,
                                    columns=("ID", "День недели", "Начало", "Окончание"),
                                    show="headings",
                                    yscrollcommand=y_scrollbar.set,
                                    xscrollcommand=x_scrollbar.set,
                                    selectmode="browse")
            
            # Configure headings
            schedule_tree.heading("ID", text="ID", anchor=tk.CENTER)
            schedule_tree.heading("День недели", text="День недели", anchor=tk.CENTER)
            schedule_tree.heading("Начало", text="Начало смены", anchor=tk.CENTER)
            schedule_tree.heading("Окончание", text="Окончание смены", anchor=tk.CENTER)
            
            # Configure columns
            schedule_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
            schedule_tree.column("День недели", width=150, minwidth=120, anchor=tk.W)
            schedule_tree.column("Начало", width=100, minwidth=80, anchor=tk.CENTER)
            schedule_tree.column("Окончание", width=100, minwidth=80, anchor=tk.CENTER)
            
            # Configure tags for weekdays
            schedule_tree.tag_configure("weekday", background="#FFFFFF")
            schedule_tree.tag_configure("weekend", background="#FFE6E6")  # Light red for weekends
            
            # Configure scrollbars
            y_scrollbar.config(command=schedule_tree.yview)
            x_scrollbar.config(command=schedule_tree.xview)
            
            # Position components
            schedule_tree.grid(row=0, column=0, sticky="nsew")
            y_scrollbar.grid(row=0, column=1, sticky="ns")
            x_scrollbar.grid(row=1, column=0, sticky="ew")
            
            # Configure grid weights
            schedule_frame.columnconfigure(0, weight=1)
            schedule_frame.rowconfigure(0, weight=1)
            
            # Control buttons frame
            control_frame = ttk.Frame(schedule_window)
            control_frame.pack(fill="x", padx=10, pady=10)
            
            def load_schedule():
                # Clear current data
                for item in schedule_tree.get_children():
                    schedule_tree.delete(item)
                
                employee_name = employee_var.get()
                if not employee_name in employees:
                    return
                
                try:
                    cursor.execute("""
                        SELECT id, day, start_time, end_time 
                        FROM work_schedules 
                        WHERE employee_id = ?
                        ORDER BY CASE 
                            WHEN day = 'Понедельник' THEN 1
                            WHEN day = 'Вторник' THEN 2
                            WHEN day = 'Среда' THEN 3
                            WHEN day = 'Четверг' THEN 4
                            WHEN day = 'Пятница' THEN 5
                            WHEN day = 'Суббота' THEN 6
                            WHEN day = 'Воскресенье' THEN 7
                            ELSE 8
                        END
                    """, (employees[employee_name],))
                    
                    count = 0
                    for row in cursor.fetchall():
                        # Weekend tag for Saturday and Sunday
                        tag = "weekend" if row['day'] in ('Суббота', 'Воскресенье') else "weekday"
                        
                        schedule_tree.insert("", "end", values=(
                            row['id'],
                            row['day'],
                            row['start_time'],
                            row['end_time']
                        ), tags=(tag,))
                        count += 1
                    
                    status_label.config(text=f"Найдено смен: {count}")
                    
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось загрузить график: {str(e)}")
            
            def add_schedule():
                employee_name = employee_var.get()
                if not employee_name in employees:
                    messagebox.showwarning("Предупреждение", "Выберите сотрудника")
                    return
                
                # Create dialog for adding shift
                dialog = tk.Toplevel(schedule_window)
                dialog.title("Добавить смену")
                dialog.geometry("300x200")
                dialog.grab_set()
                
                ttk.Label(dialog, text="День недели:").pack(pady=(10, 0))
                day_var = tk.StringVar()
                day_combo = ttk.Combobox(dialog, textvariable=day_var, width=20)
                day_combo['values'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
                day_combo.current(0)
                day_combo.pack(pady=(5, 10))
                
                ttk.Label(dialog, text="Начало смены (ЧЧ:ММ):").pack()
                start_entry = ttk.Entry(dialog, width=10)
                start_entry.insert(0, "08:00")
                start_entry.pack(pady=(5, 10))
                
                ttk.Label(dialog, text="Окончание смены (ЧЧ:ММ):").pack()
                end_entry = ttk.Entry(dialog, width=10)
                end_entry.insert(0, "17:00")
                end_entry.pack(pady=(5, 10))
                
                def save_shift():
                    day = day_var.get()
                    start_time = start_entry.get().strip()
                    end_time = end_entry.get().strip()
                    
                    # Basic validation for time format
                    import re
                    time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
                    
                    if not time_pattern.match(start_time) or not time_pattern.match(end_time):
                        messagebox.showwarning("Предупреждение", "Неверный формат времени. Используйте ЧЧ:ММ")
                        return
                    
                    try:
                        cursor.execute(
                            "INSERT INTO work_schedules (employee_id, day, start_time, end_time) VALUES (?, ?, ?, ?)",
                            (employees[employee_name], day, start_time, end_time)
                        )
                        conn.commit()
                        
                        dialog.destroy()
                        load_schedule()  # Refresh the schedule view
                        messagebox.showinfo("Успех", "Смена добавлена")
                    except sqlite3.Error as e:
                        messagebox.showerror("Ошибка", f"Не удалось добавить смену: {str(e)}")
                
                # Buttons
                buttons_frame = ttk.Frame(dialog)
                buttons_frame.pack(pady=10)
                ttk.Button(buttons_frame, text="Сохранить", command=save_shift).pack(side=tk.LEFT, padx=5)
                ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
            
            def edit_schedule():
                selected = schedule_tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите смену для редактирования")
                    return
                
                # Get selected item data
                item_id = schedule_tree.item(selected[0], "values")[0]
                
                try:
                    cursor.execute("SELECT day, start_time, end_time FROM work_schedules WHERE id = ?", (item_id,))
                    shift = cursor.fetchone()
                    
                    if not shift:
                        messagebox.showerror("Ошибка", "Смена не найдена")
                        return
                    
                    # Create dialog for editing shift
                    dialog = tk.Toplevel(schedule_window)
                    dialog.title("Редактировать смену")
                    dialog.geometry("300x200")
                    dialog.grab_set()
                    
                    ttk.Label(dialog, text="День недели:").pack(pady=(10, 0))
                    day_var = tk.StringVar()
                    day_combo = ttk.Combobox(dialog, textvariable=day_var, width=20)
                    day_combo['values'] = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
                    if shift['day'] in day_combo['values']:
                        day_var.set(shift['day'])
                    else:
                        day_combo.current(0)
                    day_combo.pack(pady=(5, 10))
                    
                    ttk.Label(dialog, text="Начало смены (ЧЧ:ММ):").pack()
                    start_entry = ttk.Entry(dialog, width=10)
                    start_entry.insert(0, shift['start_time'])
                    start_entry.pack(pady=(5, 10))
                    
                    ttk.Label(dialog, text="Окончание смены (ЧЧ:ММ):").pack()
                    end_entry = ttk.Entry(dialog, width=10)
                    end_entry.insert(0, shift['end_time'])
                    end_entry.pack(pady=(5, 10))
                    
                    def update_shift():
                        day = day_var.get()
                        start_time = start_entry.get().strip()
                        end_time = end_entry.get().strip()
                        
                        # Basic validation for time format
                        import re
                        time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
                        
                        if not time_pattern.match(start_time) or not time_pattern.match(end_time):
                            messagebox.showwarning("Предупреждение", "Неверный формат времени. Используйте ЧЧ:ММ")
                            return
                        
                        try:
                            cursor.execute(
                                "UPDATE work_schedules SET day = ?, start_time = ?, end_time = ? WHERE id = ?",
                                (day, start_time, end_time, item_id)
                            )
                            conn.commit()
                            
                            dialog.destroy()
                            load_schedule()  # Refresh the schedule view
                            messagebox.showinfo("Успех", "Смена обновлена")
                        except sqlite3.Error as e:
                            messagebox.showerror("Ошибка", f"Не удалось обновить смену: {str(e)}")
                    
                    # Buttons
                    buttons_frame = ttk.Frame(dialog)
                    buttons_frame.pack(pady=10)
                    ttk.Button(buttons_frame, text="Сохранить", command=update_shift).pack(side=tk.LEFT, padx=5)
                    ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
                
                except sqlite3.Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось получить данные: {str(e)}")
            
            def delete_schedule():
                selected = schedule_tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите смену для удаления")
                    return
                
                item_id = schedule_tree.item(selected[0], "values")[0]
                
                if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту смену?"):
                    try:
                        cursor.execute("DELETE FROM work_schedules WHERE id = ?", (item_id,))
                        conn.commit()
                        
                        load_schedule()  # Refresh the schedule view
                        messagebox.showinfo("Успех", "Смена удалена")
                    except sqlite3.Error as e:
                        messagebox.showerror("Ошибка", f"Не удалось удалить смену: {str(e)}")
            
            # Add control buttons
            ttk.Button(selection_frame, text="Загрузить график", command=load_schedule).grid(row=0, column=2, padx=10, pady=5)
            ttk.Button(control_frame, text="Добавить смену", command=add_schedule).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Редактировать смену", command=edit_schedule).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Удалить смену", command=delete_schedule).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Закрыть", command=lambda: [conn.close(), schedule_window.destroy()]).pack(side="right", padx=5)
            
            # Status label
            status_label = ttk.Label(schedule_window, text="Выберите сотрудника и нажмите 'Загрузить график'")
            status_label.pack(anchor="w", padx=10, pady=5)
            
            # Legend for weekends
            legend_frame = ttk.Frame(schedule_window)
            legend_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(legend_frame, text="Обозначения:", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
            
            weekend_sample = ttk.Label(legend_frame, text="  ", background="#FFE6E6")
            weekend_sample.pack(side=tk.LEFT, padx=2)
            ttk.Label(legend_frame, text="- Выходные дни").pack(side=tk.LEFT, padx=2)
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
    # Reports methods
    def generate_tax_report(self):
        """Генерация налогового отчета"""
        # Создаем новое окно для отчета
        report_window = tk.Toplevel(self.root)
        report_window.title("Налоговый отчет")
        report_window.geometry("800x600")
        
        # Создаем фрейм для выбора периода
        period_frame = ttk.Frame(report_window)
        period_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Выбор года
        ttk.Label(period_frame, text="Год:").pack(side=tk.LEFT, padx=5)
        year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(period_frame, textvariable=year_var, values=[str(y) for y in range(2020, 2031)], width=6)
        year_combo.pack(side=tk.LEFT, padx=5)
        
        # Выбор квартала
        ttk.Label(period_frame, text="Квартал:").pack(side=tk.LEFT, padx=5)
        quarter_var = tk.StringVar(value="1")
        quarter_combo = ttk.Combobox(period_frame, textvariable=quarter_var, values=["1", "2", "3", "4"], width=4)
        quarter_combo.pack(side=tk.LEFT, padx=5)
        
        # Выбор предприятия
        ttk.Label(period_frame, text="Предприятие:").pack(side=tk.LEFT, padx=5)
        company_var = tk.StringVar()
        company_combo = ttk.Combobox(period_frame, textvariable=company_var, values=get_company_names(), width=30)
        company_combo.pack(side=tk.LEFT, padx=5)
        
        # Создаем текстовую область для отчета
        report_text = scrolledtext.ScrolledText(report_window, wrap=tk.WORD, width=80, height=30)
        report_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем фрейм для кнопок
        button_frame = ttk.Frame(report_window)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Создаем кнопку сохранения (изначально неактивна)
        save_button = ttk.Button(button_frame, text="Сохранить отчет", state=tk.DISABLED)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        def generate_report():
            """Генерация отчета"""
            company = company_var.get()
            if not company:
                messagebox.showerror("Ошибка", "Выберите предприятие")
                return
                
            # Получаем данные отчета
            report_data = get_company_report(company)
            if not report_data:
                messagebox.showerror("Ошибка", "Данные отчета не найдены")
                return
            
            # Формируем отчет
            report = f"""Налоговый отчет
Предприятие: {company}
ИНН: {report_data['inn']}
КПП: {report_data['kpp']}
ОГРН: {report_data['ogrn']}
Период: {year_var.get()} год, {quarter_var.get()} квартал

1. Финансовые показатели:
   Выручка: {report_data['revenue']:,.2f} руб.
   Материальные затраты: {report_data['material_costs']:,.2f} руб.
   Затраты на оплату труда: {report_data['labor_costs']:,.2f} руб.
   Операционные расходы: {report_data['operational_costs']:,.2f} руб.
   Валовая прибыль: {report_data['gross_profit']:,.2f} руб.

2. Налог на добавленную стоимость:
   Налоговая база: {report_data['vat_base']:,.2f} руб.
   Ставка НДС: {report_data['vat_rate']}%
   Сумма НДС: {report_data['vat_amount']:,.2f} руб.

3. Налог на прибыль:
   Налоговая база: {report_data['profit_tax_base']:,.2f} руб.
   Ставка налога: {report_data['profit_tax_rate']}%
   Сумма налога: {report_data['profit_tax_amount']:,.2f} руб.

4. Страховые взносы:
   База для начисления: {report_data['insurance_base']:,.2f} руб.
   Пенсионные взносы ({report_data['pension_rate']}%): {report_data['pension_amount']:,.2f} руб.
   Медицинские взносы ({report_data['medical_rate']}%): {report_data['medical_amount']:,.2f} руб.
   Социальные взносы ({report_data['social_rate']}%): {report_data['social_amount']:,.2f} руб.
   Итого страховых взносов: {report_data['total_insurance']:,.2f} руб.

5. Налог на имущество:
   Налоговая база: {report_data['property_base']:,.2f} руб.
   Ставка налога: {report_data['property_rate']}%
   Сумма налога: {report_data['property_amount']:,.2f} руб.

6. Общая сумма налогов: {report_data['total_tax']:,.2f} руб.

7. Статистика предприятия:
   Количество торговых точек: {report_data['trade_points_count']}
   Количество заказов: {report_data['orders_count']}
   Количество сотрудников: {report_data['employees_count']}
"""
            
            # Отображаем отчет
            report_text.delete(1.0, tk.END)
            report_text.insert(tk.END, report)
            
            # Активируем кнопку сохранения и обновляем её команду
            save_button.config(state=tk.NORMAL, command=lambda: save_report_to_file(company, report))
        
        # Добавляем кнопку генерации отчета
        generate_button = ttk.Button(period_frame, text="Сформировать отчет", command=generate_report)
        generate_button.pack(side=tk.LEFT, padx=5)
    
    def export_data(self):
        # Create export dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Экспорт данных")
        dialog.geometry("400x300")
        dialog.grab_set()  # Make dialog modal
        
        # Data selection
        selection_frame = ttk.LabelFrame(dialog, text="Выберите данные для экспорта")
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        # Create checkboxes for each data type
        trade_points_var = tk.BooleanVar(value=True)
        orders_var = tk.BooleanVar(value=True)
        suppliers_var = tk.BooleanVar(value=True)
        materials_var = tk.BooleanVar(value=True)
        employees_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(selection_frame, text="Торговые точки", variable=trade_points_var).pack(anchor="w", padx=10, pady=2)
        messagebox.showinfo("Информация", "Функция экспорта данных в разработке")
    
    def generate_report(self, report_type):
        # Create report window
        report_window = tk.Toplevel(self.root)
        report_window.title(f"Отчет по {report_type}")
        report_window.geometry("800x600")
        
        # Create text widget for report
        report_text = tk.Text(report_window, wrap=tk.WORD, width=80, height=30)
        report_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=report_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        report_text.configure(yscrollcommand=scrollbar.set)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if report_type == "sales":
                # Отчет по продажам
                report_text.insert(tk.END, "ОТЧЕТ ПО ПРОДАЖАМ\n")
                report_text.insert(tk.END, "=" * 50 + "\n\n")
                
                # Получаем данные о заказах
                cursor.execute("""
                    SELECT id, full_name, address, event, event_date, delivery_time, status, total_price, description
                    FROM customer_orders
                    ORDER BY event_date DESC
                    """)

                
                total_amount = 0
                completed_orders = 0
                total_orders = 0

                for row in cursor.fetchall():
                    report_text.insert(tk.END, f"Заказ №{row['id']}\n")
                    report_text.insert(tk.END, f"ФИО: {row['full_name']}\n")
                    report_text.insert(tk.END, f"Адрес: {row['address']}\n")
                    
                    report_text.insert(tk.END, f"Дата: {row['event_date']}\n")
                    report_text.insert(tk.END, f"Время доставки: {row['delivery_time']}\n")
                    
                    report_text.insert(tk.END, f"Состав заказа: {row['description']}\n")
                    report_text.insert(tk.END, f"Сумма: {row['total_price']:.2f} руб.\n")
                    report_text.insert(tk.END, "-" * 50 + "\n\n")
                    total_orders += 1
                    if row['status'].lower() == 'выполнен' or row['status'].lower() == 'выполнено':
                        completed_orders += 1
                    if row['total_price']:
                        total_amount += row['total_price']

                report_text.insert(tk.END, "ИТОГИ:\n")
                report_text.insert(tk.END, f"Всего заказов: {total_orders}\n")
                report_text.insert(tk.END, f"Выполнено заказов: {completed_orders}\n")
                report_text.insert(tk.END, f"Общая сумма: {total_amount:.2f} руб.\n")

                
            elif report_type == "suppliers":
                # Отчет по поставщикам
                report_text.insert(tk.END, "ОТЧЕТ ПО ПОСТАВЩИКАМ\n")
                report_text.insert(tk.END, "=" * 50 + "\n\n")
                
                cursor.execute("""
                    SELECT s.id, s.name, s.contact, s.phone,
                           COUNT(r.id) as materials_count,
                           SUM(r.quantity) as total_quantity
                    FROM suppliers s
                    LEFT JOIN raw_materials r ON s.id = r.supplier_id
                    GROUP BY s.id
                    ORDER BY s.name
                """)
                
                for row in cursor.fetchall():
                    report_text.insert(tk.END, f"Поставщик: {row['name']}\n")
                    report_text.insert(tk.END, f"Контактное лицо: {row['contact'] if row['contact'] else 'Не указано'}\n")
                    report_text.insert(tk.END, f"Телефон: {row['phone'] if row['phone'] else 'Не указан'}\n")
                    report_text.insert(tk.END, f"Количество видов сырья: {row['materials_count']}\n")
                    report_text.insert(tk.END, f"Общее количество сырья: {row['total_quantity'] if row['total_quantity'] else 0:.2f}\n")
                    report_text.insert(tk.END, "-" * 50 + "\n\n")
                
            elif report_type == "materials":
                # Отчет по сырью
                report_text.insert(tk.END, "ОТЧЕТ ПО СЫРЬЮ\n")
                report_text.insert(tk.END, "=" * 50 + "\n\n")
                
                cursor.execute("""
                    SELECT r.id, r.name, r.quantity, r.unit, r.price,
                           s.name as supplier_name
                    FROM raw_materials r
                    LEFT JOIN suppliers s ON r.supplier_id = s.id
                    ORDER BY r.name
                """)
                
                total_value = 0
                low_stock_items = []
                
                for row in cursor.fetchall():
                    report_text.insert(tk.END, f"Наименование: {row['name']}\n")
                    report_text.insert(tk.END, f"Поставщик: {row['supplier_name'] if row['supplier_name'] else 'Не указан'}\n")
                    report_text.insert(tk.END, f"Количество: {row['quantity'] if row['quantity'] else 0:.2f} {row['unit']}\n")
                    report_text.insert(tk.END, f"Цена за единицу: {row['price'] if row['price'] else 0:.2f} руб.\n")
                    
                    # Рассчитываем стоимость
                    if row['quantity'] and row['price']:
                        item_value = row['quantity'] * row['price']
                        total_value += item_value
                        report_text.insert(tk.END, f"Общая стоимость: {item_value:.2f} руб.\n")
                    
                    # Проверяем на низкий запас
                    if row['quantity'] and float(row['quantity']) < 10:
                        low_stock_items.append(row['name'])
                    
                    report_text.insert(tk.END, "-" * 50 + "\n\n")
                
                # Добавляем итоги
                report_text.insert(tk.END, "ИТОГИ:\n")
                report_text.insert(tk.END, f"Общая стоимость сырья: {total_value:.2f} руб.\n")
                if low_stock_items:
                    report_text.insert(tk.END, "\nТребует пополнения:\n")
                    for item in low_stock_items:
                        report_text.insert(tk.END, f"- {item}\n")
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось сформировать отчет: {str(e)}")
        
        # Make the text read-only
        report_text.configure(state="disabled")
        
        # Create export frame
        export_frame = ttk.Frame(report_window)
        export_frame.pack(pady=10)
        
        # Add export format selection
        ttk.Label(export_frame, text="Формат экспорта:").pack(side=tk.LEFT, padx=5)
        format_var = tk.StringVar(value="csv")
        ttk.Radiobutton(export_frame, text="CSV", variable=format_var, value="csv").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(export_frame, text="PDF", variable=format_var, value="pdf").pack(side=tk.LEFT, padx=5)
        
        def export_report():
            export_format = format_var.get()
            base_filename = f"{report_type}_report"
            
            if export_format == "csv":
                filename = f"{base_filename}.csv"
                self.export_to_csv(report_text, filename)
            else:  # pdf
                filename = f"{base_filename}.pdf"
                self.export_to_pdf(report_text, filename)
        
        # Add export button
        ttk.Button(export_frame, text="Экспортировать", command=export_report).pack(side=tk.LEFT, padx=5)
    
    def export_to_csv(self, text_widget, filename):
        try:
            content = text_widget.get("1.0", tk.END)
            
            # Create 'reports' directory if it doesn't exist
            os.makedirs("reports", exist_ok=True)
            
            filepath = os.path.join("reports", filename)
            
            # Используем UTF-8 с BOM для корректного отображения кириллицы на MacOS
            with open(filepath, 'w', encoding='utf-8-sig') as f:
                f.write(content)
            
            messagebox.showinfo("Успех", f"Отчет сохранен в файл {filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить отчет: {str(e)}")
    
    def export_to_pdf(self, text_widget, filename):
        """Export report to PDF format"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            
            # Register Helvetica font for Cyrillic support
            pdfmetrics.registerFont(TTFont('CustomHelvetica', '/System/Library/Fonts/Helvetica.ttc'))
            
            # Create reports directory if it doesn't exist
            if not os.path.exists('reports'):
                os.makedirs('reports')
            
            # Get the content from the text widget
            content = text_widget.get("1.0", tk.END)
            
            # Create the PDF document with smaller margins
            doc = SimpleDocTemplate(
                os.path.join('reports', filename),
                pagesize=letter,
                rightMargin=36,  # Уменьшаем правое поле
                leftMargin=36,   # Уменьшаем левое поле
                topMargin=36,    # Уменьшаем верхнее поле
                bottomMargin=36  # Уменьшаем нижнее поле
            )
            
            # Create styles with custom Helvetica font and smaller spacing
            styles = getSampleStyleSheet()
            normal_style = ParagraphStyle(
                'CustomStyle',
                parent=styles['Normal'],
                fontName='CustomHelvetica',
                fontSize=10,
                leading=12,      # Уменьшаем межстрочный интервал
                spaceBefore=3,   # Уменьшаем отступ перед параграфом
                spaceAfter=3     # Уменьшаем отступ после параграфа
            )
            
            # Build the document
            story = []
            
            # Split content into paragraphs and add them to the story
            paragraphs = content.split('\n')
            for para in paragraphs:
                if para.strip():
                    # Convert text to proper encoding
                    text = para.encode('utf-8').decode('utf-8')
                    p = Paragraph(text, normal_style)
                    story.append(p)
                    story.append(Spacer(1, 6))  # Уменьшаем отступ между параграфами
            
            # Build the PDF
            doc.build(story)
            
            messagebox.showinfo("Успех", f"Отчет сохранен в файл {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении PDF: {str(e)}")
    
    def order_raw_material(self):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Заказать сырье")
        dialog.geometry("400x350")
        dialog.grab_set()  # Make dialog modal
        
        # Create form
        ttk.Label(dialog, text="Название:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Поставщик:").pack()
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=30)
        
        # Get suppliers for combobox
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM suppliers")
            suppliers = [row['name'] for row in cursor.fetchall()]
            supplier_combo['values'] = suppliers
            if suppliers:
                supplier_combo.current(0)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список поставщиков: {str(e)}")
        
        supplier_combo.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Количество:").pack()
        quantity_entry = ttk.Entry(dialog, width=30)
        quantity_entry.pack(pady=(5, 10))
        
        ttk.Label(dialog, text="Единица измерения:").pack()
        unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(dialog, textvariable=unit_var, width=30)
        unit_combo['values'] = ["кг", "л", "шт", "уп"]
        unit_combo.current(0)
        unit_combo.pack(pady=(5, 10))
        
        def save_order():
            name = name_entry.get().strip()
            supplier = supplier_var.get()
            quantity = quantity_entry.get().strip()
            unit = unit_var.get()
            
            if not all([name, supplier, quantity, unit]):
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            try:
                quantity = float(quantity)
                if quantity <= 0:
                    raise ValueError("Количество должно быть положительным числом")
                
                conn = get_connection()
                cursor = conn.cursor()
                
                # Get supplier_id
                cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier,))
                supplier_id = cursor.fetchone()['id']
                
                # Check if raw material exists
                cursor.execute("SELECT id, quantity FROM raw_materials WHERE name = ? AND supplier_id = ?",
                             (name, supplier_id))
                existing = cursor.fetchone()
                
                if existing:
                    # Update quantity
                    new_quantity = existing['quantity'] + quantity
                    cursor.execute("UPDATE raw_materials SET quantity = ? WHERE id = ?",
                                 (new_quantity, existing['id']))
                else:
                    # Insert new raw material
                    cursor.execute("""
                        INSERT INTO raw_materials (name, supplier_id, quantity, unit)
                        VALUES (?, ?, ?, ?)
                    """, (name, supplier_id, quantity, unit))
                
                conn.commit()
                conn.close()
                
                self.load_raw_materials()
                dialog.destroy()
                messagebox.showinfo("Успех", "Сырье успешно заказано")
                
            except ValueError as e:
                messagebox.showwarning("Ошибка", str(e))
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {str(e)}")
        
        # Add buttons
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Сохранить", command=save_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def view_inventory(self):
        # Create inventory report window
        report_window = tk.Toplevel(self.root)
        report_window.title("Просмотр запасов сырья")
        report_window.geometry("800x500")
        
        # Create a frame for filters
        filter_frame = ttk.LabelFrame(report_window, text="Фильтры")
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # Supplier filter
        ttk.Label(filter_frame, text="Поставщик:").grid(row=0, column=0, padx=5, pady=5)
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(filter_frame, textvariable=supplier_var, width=20)
        
        # Populate suppliers for filter
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers = {row['name']: row['id'] for row in cursor.fetchall()}
            supplier_combo['values'] = ["Все"] + list(suppliers.keys())
            supplier_combo.current(0)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список поставщиков: {str(e)}")
        
        supplier_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Min quantity filter
        ttk.Label(filter_frame, text="Мин. количество:").grid(row=0, column=2, padx=5, pady=5)
        min_quantity_entry = ttk.Entry(filter_frame, width=10)
        min_quantity_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Create a treeview for inventory
        report_frame = ttk.Frame(report_window)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create scrollbars
        y_scrollbar = ttk.Scrollbar(report_frame, orient="vertical")
        x_scrollbar = ttk.Scrollbar(report_frame, orient="horizontal")
        
        inventory_tree = ttk.Treeview(report_frame,
                               columns=("ID", "Название", "Поставщик", "Количество", "Ед.изм."),
                               show="headings",
                               yscrollcommand=y_scrollbar.set,
                               xscrollcommand=x_scrollbar.set,
                               selectmode="browse")
        
        # Configure headings
        inventory_tree.heading("ID", text="ID", anchor=tk.CENTER)
        inventory_tree.heading("Название", text="Название", anchor=tk.CENTER)
        inventory_tree.heading("Поставщик", text="Поставщик", anchor=tk.CENTER)
        inventory_tree.heading("Количество", text="Количество", anchor=tk.CENTER)
        inventory_tree.heading("Ед.изм.", text="Ед.изм.", anchor=tk.CENTER)
        
        # Configure columns
        inventory_tree.column("ID", width=50, minwidth=50, anchor=tk.CENTER)
        inventory_tree.column("Название", width=200, minwidth=120, anchor=tk.W)
        inventory_tree.column("Поставщик", width=200, minwidth=120, anchor=tk.W)
        inventory_tree.column("Количество", width=100, minwidth=80, anchor=tk.CENTER)
        inventory_tree.column("Ед.изм.", width=80, minwidth=60, anchor=tk.CENTER)
        
        # Configure tags for alternating row colors
        inventory_tree.tag_configure("evenrow", background="#FFFFFF")
        inventory_tree.tag_configure("oddrow", background="#F0F0F0")
        inventory_tree.tag_configure("lowstock", background="#FFCCCC")  # Red for low stock
        
        # Configure scrollbars
        y_scrollbar.config(command=inventory_tree.yview)
        x_scrollbar.config(command=inventory_tree.xview)
        
        # Position components
        inventory_tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)
        
        def load_filtered_inventory():
            # Clear current data
            for item in inventory_tree.get_children():
                inventory_tree.delete(item)
            
            # Get filter values
            supplier_name = supplier_var.get()
            min_quantity_str = min_quantity_entry.get().strip()
            
            try:
                # Validate min quantity
                min_quantity = 0
                if min_quantity_str:
                    min_quantity = float(min_quantity_str)
                
                conn = get_connection()
                cursor = conn.cursor()
                
                # Build query based on filters
                query = """
                    SELECT r.id, r.name, s.name as supplier_name, r.quantity, r.unit 
                    FROM raw_materials r
                    LEFT JOIN suppliers s ON r.supplier_id = s.id
                    WHERE 1=1
                """
                params = []
                
                if supplier_name and supplier_name != "Все":
                    query += " AND r.supplier_id = ?"
                    params.append(suppliers[supplier_name])
                
                if min_quantity > 0:
                    query += " AND r.quantity >= ?"
                    params.append(min_quantity)
                
                query += " ORDER BY r.name"
                
                cursor.execute(query, params)
                
                # Add rows with alternating colors
                count = 0
                for row in cursor.fetchall():
                    tag = "evenrow" if count % 2 == 0 else "oddrow"
                    # Add low stock tag if quantity is less than 10
                    if row['quantity'] and float(row['quantity']) < 10:
                        tag = "lowstock"
                        
                    inventory_tree.insert("", "end", values=(
                        row['id'], 
                        row['name'], 
                        row['supplier_name'] if row['supplier_name'] else "Не указано", 
                        row['quantity'] if row['quantity'] else 0, 
                        row['unit'] if row['unit'] else ""
                    ), tags=(tag,))
                    count += 1
                
                conn.close()
                
                # Update status label
                status_label.config(text=f"Найдено записей: {count}")
                
            except ValueError:
                messagebox.showwarning("Предупреждение", "Введите корректное число для минимального количества")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
        
        # Add filter button
        ttk.Button(filter_frame, text="Применить фильтр", command=load_filtered_inventory).grid(row=0, column=4, padx=10, pady=5)
        
        # Status label
        status_label = ttk.Label(report_window, text="Загрузка данных...")
        status_label.pack(anchor="w", padx=10, pady=5)
        
        # Legend for low stock
        legend_frame = ttk.Frame(report_window)
        legend_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(legend_frame, text="Обозначения:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        low_stock_sample = ttk.Label(legend_frame, text="  ", background="#FFCCCC")
        low_stock_sample.pack(side=tk.LEFT, padx=2)
        ttk.Label(legend_frame, text="- Низкий запас (менее 10)").pack(side=tk.LEFT, padx=2)
        
        # Buttons frame
        buttons_frame = ttk.Frame(report_window)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        
        ttk.Button(buttons_frame, text="Закрыть", command=report_window.destroy).pack(side="right", padx=5)
        
        # Load data initially
        load_filtered_inventory()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        # Настройка стилей для градиентного фона
        style.configure("Gradient.TFrame", background="#6B728E")
        # Оставляем оригинальные стили для других элементов
        style.configure("TFrame", background="#E0E0E0")
        style.configure("TLabel", background="#E0E0E0", foreground="#4A4A4A", font=("Helvetica", 14))
        style.configure("TEntry", fieldbackground="#FFFFFF", font=("Helvetica", 12), relief="flat", borderwidth=2)
        style.map("TEntry", background=[("focus", "#FFF9B0")])
        # Новый стиль для всех кнопок
        style.configure("TButton",
                       font=("Helvetica", 12, "bold"),
                       padding=10,
                       background="#F4C7C3",
                       foreground="#333333",
                       borderwidth=0,
                       relief="flat")
        style.map("TButton",
                 background=[("active", "#E0A8A3"), ("pressed", "#E0A8A3")],
                 foreground=[("active", "#333333")])
        # Стиль для больших кнопок
        style.configure("Big.TButton", font=("Arial", 32, "bold"), padding=(20, 30), anchor="center",
                       background="#F4C7C3", foreground="#333333", borderwidth=0, relief="flat")
        style.map("Big.TButton",
                 background=[("active", "#E0A8A3"), ("pressed", "#E0A8A3")],
                 foreground=[("active", "#333333")])
        style.configure("Header.TLabel", font=("Helvetica", 28, "bold"), background="#E0E0E0", foreground="black")
        style.configure("TCombobox", font=("Helvetica", 12), padding=5, background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#4A4A4A")
        style.map("TCombobox", fieldbackground=[("focus", "#FFF9B0")])
        style.configure("Customer.TFrame", background="#E0E0E0")

    def create_background(self, canvas, width, height):
        self.bg_shapes = []
        canvas.delete("all")
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
        for _ in range(100):
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

    def animate_background(self, canvas, width, height):
        canvas.delete("shapes")
        for shape in self.bg_shapes:
            shape["x"] += shape["dx"]
            shape["y"] += shape["dy"]
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

    def create_gradient_frame(self, parent, width, height):
        frame = ttk.Frame(parent, style="Gradient.TFrame")
        canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        try:
            self.create_background(canvas, width, height)
        except Exception as e:
            print(f"Ошибка при создании градиентного фона: {e}")
        return frame

    def show_order_details(self, event, tree=None):
        if tree is None:
            tree = self.orders_tree
            
        selected = tree.selection()
        if not selected:
            return
        
        item = tree.item(selected[0])
        order_id = item['values'][0]
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *, order_items, total_price 
                FROM customer_orders 
                WHERE id=?
            """, (order_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row or not row['order_items']:
                messagebox.showinfo("Информация о заказе", "Нет информации о заказанных позициях")
                return
            
            # Форматируем номер телефона для отображения
            phone_display = row["phone"]
            if phone_display:
                digits = ''.join(filter(str.isdigit, phone_display))
                if len(digits) == 11:
                    phone_display = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            
            # Создаем окно с деталями заказа
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Детали заказа №{order_id}")
            details_window.geometry("400x500")
            details_window.grab_set()
            
            # Создаем фрейм с прокруткой
            main_frame = ttk.Frame(details_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Заголовок
            ttk.Label(main_frame, text=f"Заказ №{order_id}", 
                     font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
            
            # Информация о клиенте
            client_frame = ttk.Frame(main_frame)
            client_frame.pack(fill="x", pady=(0, 10))
            ttk.Label(client_frame, text=f"ФИО: {row['full_name']}", font=("Helvetica", 12)).pack(anchor="w")
            ttk.Label(client_frame, text=f"Телефон: {phone_display}", font=("Helvetica", 12)).pack(anchor="w")
            ttk.Label(client_frame, text=f"Адрес: {row['address']}", font=("Helvetica", 12)).pack(anchor="w")
            ttk.Label(client_frame, text=f"Email: {row['email']}", font=("Helvetica", 12)).pack(anchor="w")
            
            # Создаем текстовое поле для отображения деталей
            details_text = tk.Text(main_frame, wrap=tk.WORD, width=40, height=20)
            details_text.pack(fill="both", expand=True)
            
            # Парсим JSON с заказанными позициями
            try:
                order_items = json.loads(row['order_items'])
                
                # Формируем текст с деталями
                details = "Заказанные позиции:\n\n"
                for item in order_items:
                    details += f"{item['name']}\n"
                    details += f"Количество: {item['quantity']} шт.\n"
                    details += f"Цена за шт.: {item['price']:.2f} руб.\n"
                    details += f"Сумма: {item['sum']:.2f} руб.\n"
                    details += "-" * 40 + "\n"
                
                details += f"\nОбщая сумма: {row['total_price']:.2f} руб."
            except (json.JSONDecodeError, TypeError) as e:
                details = f"Не удалось загрузить детали заказа: {str(e)}\n\n"
                if row['order_items']:
                    details += f"Сырые данные: {row['order_items']}\n"
                details += f"\nОбщая сумма: {row['total_price'] if row['total_price'] else 0:.2f} руб."
            
            # Вставляем текст и делаем поле только для чтения
            details_text.insert("1.0", details)
            details_text.configure(state="disabled")
            
            # Кнопка закрытия
            ttk.Button(main_frame, text="Закрыть", 
                      command=details_window.destroy).pack(pady=(10, 0))
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить детали заказа: {str(e)}")
            print(f"SQLite Error in show_order_details: {str(e)}")
            traceback.print_exc()


if __name__ == "__main__":
    root = tk.Tk()
    app = BakeryApp(root)
    root.mainloop() 