import tkinter as tk
from tkinter import ttk, messagebox

class Buyer:
    #нач знач
    def __init__(self, last_name, first_name, otchestvo, address, number_card, number_bank):
        self.last_name = last_name
        self.first_name = first_name
        self.otchestvo = otchestvo
        self.address = address
        self.number_card = number_card
        self.number_bank = number_bank

    #измен знач
    def установка_знач_атриб(self, last_name, first_name, otchestvo, address, number_card, number_bank):
        self.last_name = last_name
        self.first_name = first_name
        self.otchestvo = otchestvo
        self.address = address
        self.number_card = number_card
        self.number_bank = number_bank

    def получение_знач_атриб(self):
        return {
        "Фамилия": self.last_name,
        "Имя": self.first_name,
        "Отчество": self.otchestvo,
        "Адрес": self.address,
        "Номер кредитки": self.number_card,
        "Номер банковского счёта": self.number_bank,
        }

    def вывод_в_терминал(self):
        return (f'ФИО: {self.last_name} {self.first_name} {self.otchestvo}, '
                f'Адрес: {self.address}, '
                f'Номер кредитной карточки: {self.number_card}, '
                f'Номер банковского счета: {self.number_bank}')

class BuyerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление покупателями")
        
        # Создаем список покупателей
        self.customers = [
            Buyer("Иванов", "Иван", "Иванович", "Москва, ул. Ленина, д. 1", 1234567890123456, "4070281000000001"),
            Buyer("Петров", "Петр", "Петрович", "Санкт-Петербург, ул. Пушкина, д. 2", 2345678901234567, "4070281000000002"),
            Buyer("Сидоров", "Сидор", "Сидорович", "Екатеринбург, ул. Чехова, д. 3", 3456789012345678, "4070281000000003"),
            Buyer("Алексеев", "Алексей", "Алексеевич", "Казань, ул. Горького, д. 4", 4567890123456789, "4070281000000004"),
        ]
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление покупателя", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Создаем поля ввода
        fields = [
            ("Фамилия:", "last_name"),
            ("Имя:", "first_name"),
            ("Отчество:", "otchestvo"),
            ("Адрес:", "address"),
            ("Номер кредитки:", "number_card"),
            ("Номер банковского счета:", "number_bank")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w")
            self.entries[field] = ttk.Entry(input_frame)
            self.entries[field].grid(row=i, column=1, padx=5, pady=2)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Добавить покупателя", command=self.add_buyer).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Удалить выбранных", command=self.delete_selected).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Сортировка по алфавиту", command=self.sort_alphabetically).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Фильтр по номеру карты", command=self.filter_by_card).grid(row=0, column=3, padx=5)
        
        # Создаем Treeview
        self.tree = ttk.Treeview(self.root, columns=("name", "address", "card", "bank"), show="headings")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("card", text="Номер кредитки")
        self.tree.heading("bank", text="Номер банковского счета")
        
        # Настраиваем ширину колонок
        self.tree.column("name", width=200)
        self.tree.column("address", width=200)
        self.tree.column("card", width=150)
        self.tree.column("bank", width=150)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем Treeview и скроллбар
        self.tree.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")
        
        # Настройка сетки
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        # Заполняем таблицу данными
        self.update_tree()
        
    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for buyer in self.customers:
            self.tree.insert("", "end", values=(
                f"{buyer.last_name} {buyer.first_name} {buyer.otchestvo}",
                buyer.address,
                buyer.number_card,
                buyer.number_bank
            ))
            
    def add_buyer(self):
        try:
            # Получаем значения из полей ввода
            last_name = self.entries["last_name"].get()
            first_name = self.entries["first_name"].get()
            otchestvo = self.entries["otchestvo"].get()
            address = self.entries["address"].get()
            number_card = int(self.entries["number_card"].get())
            number_bank = self.entries["number_bank"].get()
            
            # Проверяем, что все поля заполнены
            if not all([last_name, first_name, otchestvo, address, number_bank]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            # Создаем нового покупателя
            new_buyer = Buyer(last_name, first_name, otchestvo, address, number_card, number_bank)
            self.customers.append(new_buyer)
            
            # Обновляем таблицу
            self.update_tree()
            
            # Очищаем поля ввода
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
            messagebox.showinfo("Успех", "Покупатель успешно добавлен")
        except ValueError:
            messagebox.showerror("Ошибка", "Номер кредитки должен быть числом")
            
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите покупателей для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранных покупателей?"):
            # Получаем индексы выбранных элементов
            indices_to_delete = []
            for item in selected_items:
                values = self.tree.item(item)['values']
                card_number = values[2]  # Номер кредитки находится в третьей колонке
                for i, buyer in enumerate(self.customers):
                    if buyer.number_card == card_number:
                        indices_to_delete.append(i)
                        break
            
            # Удаляем покупателей в обратном порядке, чтобы не сбить индексы
            for index in sorted(indices_to_delete, reverse=True):
                del self.customers[index]
                
            # Обновляем таблицу
            self.update_tree()
            messagebox.showinfo("Успех", "Выбранные покупатели удалены")
            
    def sort_alphabetically(self):
        self.customers.sort(key=lambda x: (x.last_name, x.first_name, x.otchestvo))
        self.update_tree()
        
    def filter_by_card(self):
        try:
            # Создаем диалоговое окно для ввода диапазона
            dialog = tk.Toplevel(self.root)
            dialog.title("Фильтр по номеру карты")
            dialog.geometry("300x150")
            
            ttk.Label(dialog, text="Введите диапазон номеров карт:").pack(pady=5)
            
            range_frame = ttk.Frame(dialog)
            range_frame.pack(pady=5)
            
            ttk.Label(range_frame, text="От:").grid(row=0, column=0, padx=5)
            from_entry = ttk.Entry(range_frame)
            from_entry.grid(row=0, column=1, padx=5)
            
            ttk.Label(range_frame, text="До:").grid(row=1, column=0, padx=5)
            to_entry = ttk.Entry(range_frame)
            to_entry.grid(row=1, column=1, padx=5)
            
            def apply_filter():
                try:
                    left = int(from_entry.get())
                    right = int(to_entry.get())
                    filtered_customers = [buyer for buyer in self.customers if left <= buyer.number_card <= right]
                    
                    # Обновляем таблицу только отфильтрованными покупателями
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                    for buyer in filtered_customers:
                        self.tree.insert("", "end", values=(
                            f"{buyer.last_name} {buyer.first_name} {buyer.otchestvo}",
                            buyer.address,
                            buyer.number_card,
                            buyer.number_bank
                        ))
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректные числовые значения")
            
            ttk.Button(dialog, text="Применить", command=apply_filter).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BuyerApp(root)
    root.mainloop()