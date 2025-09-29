import tkinter as tk
from tkinter import ttk, messagebox

class Abonent:
    def __init__(self, id, last_name, first_name, otchestvo, address, credit_card_number, debit, credit, city_call_time, long_distance_call_time):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.otchestvo = otchestvo
        self.address = address
        self.credit_card_number = credit_card_number
        self.debit = debit
        self.credit = credit
        self.city_call_time = city_call_time
        self.long_distance_call_time = long_distance_call_time

    def установка_знач_атриб(self, id, last_name, first_name, otchestvo, address, credit_card_number, debit, credit, city_call_time, long_distance_call_time):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.otchestvo = otchestvo
        self.address = address
        self.credit_card_number = credit_card_number
        self.debit = debit
        self.credit = credit
        self.city_call_time = city_call_time
        self.long_distance_call_time = long_distance_call_time

    def вывод_в_терминал(self):
        return (f'ФИО: {self.last_name} {self.first_name} {self.otchestvo}, '
        f'Адрес: {self.address}, '
        f'Номер кредитной карточки: {self.credit_card_number}, '
        f'Дебет: {self.debit}, '
        f'Кредит: {self.credit}, '
        f'Время междугородных переговоров: {self.city_call_time}, '
        f'Время городских переговоров: {self.long_distance_call_time}')

class AbonentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление абонентами")
        
        # Создаем список абонентов
        self.subscribers = [
    Abonent(1, "Иванов", "Иван", "Иванович", "Москва, ул. Ленина, д. 1", "1234 5678 9012 3456", 1000, 5000, 120, 30),
    Abonent(2, "Петров", "Петр", "Петрович", "Санкт-Петербург, ул. Пушкина, д. 2", "2345 6789 0123 4567", 2000, 3000, 60, 10),
    Abonent(3, "Сидоров", "Сидор", "Сидорович", "Екатеринбург, ул. Чехова, д. 3", "3456 7890 1234 5678", 1500, 2500, 150, 0),
            Abonent(4, "Алексеев", "Алексей", "Алексеевич", "Казань, ул. Горького, д. 4", "4567 8901 2345 6789", 500, 1000, 30, 20)
        ]

        # Сохраняем оригинальный список для сброса
        self.original_subscribers = self.subscribers.copy()
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление абонента", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Создаем поля ввода
        fields = [
            ("ID:", "id"),
            ("Фамилия:", "last_name"),
            ("Имя:", "first_name"),
            ("Отчество:", "otchestvo"),
            ("Адрес:", "address"),
            ("Номер кредитки:", "credit_card_number"),
            ("Дебет:", "debit"),
            ("Кредит:", "credit"),
            ("Время городских переговоров:", "city_call_time"),
            ("Время междугородных переговоров:", "long_distance_call_time")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w")
            self.entries[field] = ttk.Entry(input_frame)
            self.entries[field].grid(row=i, column=1, padx=5, pady=2)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Добавить абонента", command=self.add_subscriber).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Удалить выбранных", command=self.delete_selected).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Сбросить", command=self.reset_list).grid(row=0, column=2, padx=5)
        
        # Кнопки фильтрации и сортировки
        filter_frame = ttk.Frame(self.root)
        filter_frame.grid(row=2, column=0, padx=10, pady=5)
        
        ttk.Button(filter_frame, text="Абоненты с временем городских переговоров больше заданного", 
                  command=self.filter_by_city_call_time).grid(row=0, column=0, padx=5)
        ttk.Button(filter_frame, text="Абоненты с междугородной связью", 
                  command=self.filter_by_long_distance).grid(row=0, column=1, padx=5)
        ttk.Button(filter_frame, text="Абоненты в алфавитном порядке", 
                  command=self.sort_alphabetically).grid(row=0, column=2, padx=5)
        
        # Создаем Treeview
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "address", "card", "debit", "credit", "city_time", "long_time"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("card", text="Номер кредитки")
        self.tree.heading("debit", text="Дебет")
        self.tree.heading("credit", text="Кредит")
        self.tree.heading("city_time", text="Городские переговоры")
        self.tree.heading("long_time", text="Междугородные переговоры")
        
        # Настраиваем ширину колонок
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("address", width=200)
        self.tree.column("card", width=150)
        self.tree.column("debit", width=100)
        self.tree.column("credit", width=100)
        self.tree.column("city_time", width=150)
        self.tree.column("long_time", width=150)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем Treeview и скроллбар
        self.tree.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        scrollbar.grid(row=3, column=1, sticky="ns")
        
        # Настройка сетки
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        
        # Заполняем таблицу данными
        self.update_tree()
        
    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for subscriber in self.subscribers:
            self.tree.insert("", "end", values=(
                subscriber.id,
                f"{subscriber.last_name} {subscriber.first_name} {subscriber.otchestvo}",
                subscriber.address,
                subscriber.credit_card_number,
                subscriber.debit,
                subscriber.credit,
                subscriber.city_call_time,
                subscriber.long_distance_call_time
            ))
            
    def add_subscriber(self):
        try:
            # Получаем значения из полей ввода
            id = int(self.entries["id"].get())
            last_name = self.entries["last_name"].get()
            first_name = self.entries["first_name"].get()
            otchestvo = self.entries["otchestvo"].get()
            address = self.entries["address"].get()
            credit_card_number = self.entries["credit_card_number"].get()
            debit = float(self.entries["debit"].get())
            credit = float(self.entries["credit"].get())
            city_call_time = int(self.entries["city_call_time"].get())
            long_distance_call_time = int(self.entries["long_distance_call_time"].get())
            
            # Проверяем, что все поля заполнены
            if not all([last_name, first_name, otchestvo, address, credit_card_number]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            # Создаем нового абонента
            new_subscriber = Abonent(id, last_name, first_name, otchestvo, address, credit_card_number, 
                                    debit, credit, city_call_time, long_distance_call_time)
            self.subscribers.append(new_subscriber)
            
            # Обновляем таблицу
            self.update_tree()
            
            # Очищаем поля ввода
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
            messagebox.showinfo("Успех", "Абонент успешно добавлен")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода числовых значений")
            
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите абонентов для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранных абонентов?"):
            # Получаем индексы выбранных элементов
            indices_to_delete = []
            for item in selected_items:
                values = self.tree.item(item)['values']
                id = values[0]  # ID находится в первой колонке
                for i, subscriber in enumerate(self.subscribers):
                    if subscriber.id == id:
                        indices_to_delete.append(i)
                        break
            
            # Удаляем абонентов в обратном порядке, чтобы не сбить индексы
            for index in sorted(indices_to_delete, reverse=True):
                del self.subscribers[index]
                
            # Обновляем таблицу
            self.update_tree()
            messagebox.showinfo("Успех", "Выбранные абоненты удалены")
            
    def reset_list(self):
        self.subscribers = self.original_subscribers.copy()
        self.update_tree()
        messagebox.showinfo("Информация", "Список абонентов сброшен к исходному состоянию")
            
    def filter_by_city_call_time(self):
        try:
            # Создаем диалоговое окно для ввода времени
            dialog = tk.Toplevel(self.root)
            dialog.title("Фильтр по времени городских переговоров")
            dialog.geometry("300x100")
            
            ttk.Label(dialog, text="Введите минимальное время (в минутах):").pack(pady=5)
            
            time_entry = ttk.Entry(dialog)
            time_entry.pack(pady=5)
            
            def apply_filter():
                try:
                    min_time = int(time_entry.get())
                    filtered_subscribers = [sub for sub in self.subscribers if sub.city_call_time > min_time]
                    
                    # Обновляем таблицу только отфильтрованными абонентами
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                    for subscriber in filtered_subscribers:
                        self.tree.insert("", "end", values=(
                            subscriber.id,
                            f"{subscriber.last_name} {subscriber.first_name} {subscriber.otchestvo}",
                            subscriber.address,
                            subscriber.credit_card_number,
                            subscriber.debit,
                            subscriber.credit,
                            subscriber.city_call_time,
                            subscriber.long_distance_call_time
                        ))
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректное числовое значение")
            
            ttk.Button(dialog, text="Применить", command=apply_filter).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            
    def filter_by_long_distance(self):
        # Фильтруем абонентов с междугородней связью
        filtered_subscribers = [sub for sub in self.subscribers if sub.long_distance_call_time > 0]
        
        # Обновляем таблицу только отфильтрованными абонентами
        for item in self.tree.get_children():
            self.tree.delete(item)
        for subscriber in filtered_subscribers:
            self.tree.insert("", "end", values=(
                subscriber.id,
                f"{subscriber.last_name} {subscriber.first_name} {subscriber.otchestvo}",
                subscriber.address,
                subscriber.credit_card_number,
                subscriber.debit,
                subscriber.credit,
                subscriber.city_call_time,
                subscriber.long_distance_call_time
            ))
            
    def sort_alphabetically(self):
        self.subscribers.sort(key=lambda x: (x.last_name, x.first_name, x.otchestvo))
        self.update_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = AbonentApp(root)
    root.mainloop()


