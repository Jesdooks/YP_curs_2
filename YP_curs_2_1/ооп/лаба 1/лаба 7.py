import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from abc import ABC, abstractmethod
import json

class Animal(ABC):
    def __init__(self, id, name, food_amount):
        self.id = id
        self.name = name
        self.food_amount = food_amount

    @abstractmethod
    def calculate_food(self):
        pass

    def __str__(self):
        return f"ID: {self.id}, Имя: {self.name}, Тип: {self.__class__.__name__}, Количество пищи: {self.food_amount}"

class Predator(Animal):
    def __init__(self, id, name, food_amount):
        super().__init__(id, name, food_amount)
        self.food_type = "мясо"

    def calculate_food(self):
        return f"{self.food_amount} кг {self.food_type}"

class Omnivore(Animal):
    def __init__(self, id, name, food_amount):
        super().__init__(id, name, food_amount)
        self.food_type = "смешанная пища"

    def calculate_food(self):
        return f"{self.food_amount} кг {self.food_type}"

class Herbivore(Animal):
    def __init__(self, id, name, food_amount):
        super().__init__(id, name, food_amount)
        self.food_type = "растительная пища"

    def calculate_food(self):
        return f"{self.food_amount} кг {self.food_type}"

class ZooApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление животными в зоопарке")
        
        # Создаем список животных
        self.animals = [
            Predator(1, "Лев", 10),
            Omnivore(2, "Медведь", 15),
            Herbivore(3, "Корова", 20),
            Predator(4, "Тигр", 12),
            Omnivore(5, "Кабан", 8),
            Herbivore(6, "Лошадь", 25)
        ]
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление животного", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Создаем поля ввода
        fields = [
            ("ID:", "id"),
            ("Имя:", "name"),
            ("Количество пищи:", "food_amount"),
            ("Тип животного:", "animal_type")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w")
            if field == "animal_type":
                self.entries[field] = ttk.Combobox(input_frame, values=["Хищник", "Всеядное", "Травоядное"])
            else:
                self.entries[field] = ttk.Entry(input_frame)
            self.entries[field].grid(row=i, column=1, padx=5, pady=2)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Добавить животное", command=self.add_animal).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Удалить выбранное", command=self.delete_selected).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Первые 5 имен", command=self.show_first_five).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Последние 3 ID", command=self.show_last_three).grid(row=0, column=3, padx=5)
        
        # Кнопки для работы с файлами
        file_frame = ttk.Frame(self.root)
        file_frame.grid(row=2, column=0, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Прочитать из файла", command=self.load_from_file).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Сохранить в файл", command=self.save_to_file).grid(row=0, column=1, padx=5)
        
        # Создаем Treeview
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "type", "food"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Имя")
        self.tree.heading("type", text="Тип")
        self.tree.heading("food", text="Количество пищи")
        
        # Настраиваем ширину колонок
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("type", width=150)
        self.tree.column("food", width=150)
        
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
        # Сортируем животных по количеству пищи (по убыванию) и имени (по алфавиту)
        self.animals.sort(key=lambda x: (-x.food_amount, x.name))
        
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Заполняем таблицу
        for animal in self.animals:
            self.tree.insert("", "end", values=(
                animal.id,
                animal.name,
                animal.__class__.__name__,
                animal.calculate_food()
            ))
            
    def add_animal(self):
        try:
            # Получаем значения из полей ввода
            id = int(self.entries["id"].get())
            name = self.entries["name"].get()
            food_amount = float(self.entries["food_amount"].get())
            animal_type = self.entries["animal_type"].get()
            
            # Проверяем, что все поля заполнены
            if not all([name, animal_type]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            # Проверяем, существует ли животное с таким ID
            if any(animal.id == id for animal in self.animals):
                messagebox.showerror("Ошибка", "Животное с таким ID уже есть в списке")
                return
                
            # Создаем новое животное в зависимости от типа
            if animal_type == "Хищник":
                new_animal = Predator(id, name, food_amount)
            elif animal_type == "Всеядное":
                new_animal = Omnivore(id, name, food_amount)
            elif animal_type == "Травоядное":
                new_animal = Herbivore(id, name, food_amount)
            else:
                messagebox.showerror("Ошибка", "Неверный тип животного")
                return
                
            self.animals.append(new_animal)
            
            # Обновляем таблицу
            self.update_tree()
            
            # Очищаем поля ввода
            for entry in self.entries.values():
                if isinstance(entry, ttk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("")
                    
            messagebox.showinfo("Успех", "Животное успешно добавлено")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода числовых значений")
            
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите животное для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранное животное?"):
            # Получаем индексы выбранных элементов
            indices_to_delete = []
            for item in selected_items:
                values = self.tree.item(item)['values']
                id = values[0]  # ID находится в первой колонке
                for i, animal in enumerate(self.animals):
                    if animal.id == id:
                        indices_to_delete.append(i)
                        break
            
            # Удаляем животных в обратном порядке
            for index in sorted(indices_to_delete, reverse=True):
                del self.animals[index]
                
            # Обновляем таблицу
            self.update_tree()
            messagebox.showinfo("Успех", "Выбранное животное удалено")
            
    def show_first_five(self):
        if len(self.animals) == 0:
            messagebox.showinfo("Информация", "Список животных пуст")
            return
            
        names = [animal.name for animal in self.animals[:5]]
        messagebox.showinfo("Первые 5 имен", "\n".join(names))
        
    def show_last_three(self):
        if len(self.animals) == 0:
            messagebox.showinfo("Информация", "Список животных пуст")
            return
            
        ids = [str(animal.id) for animal in self.animals[-3:]]
        messagebox.showinfo("Последние 3 ID", "\n".join(ids))
        
    def save_to_file(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            # Преобразуем животных в словари для сохранения
            animals_data = []
            for animal in self.animals:
                animal_dict = {
                    "id": animal.id,
                    "name": animal.name,
                    "food_amount": animal.food_amount,
                    "type": animal.__class__.__name__
                }
                animals_data.append(animal_dict)
                
            # Сохраняем в файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(animals_data, f, ensure_ascii=False, indent=4)
                
            messagebox.showinfo("Успех", "Данные успешно сохранены в файл")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
            
    def load_from_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            # Читаем данные из файла
            with open(file_path, 'r', encoding='utf-8') as f:
                animals_data = json.load(f)
                
            # Очищаем текущий список животных
            self.animals.clear()
            
            # Создаем новых животных из данных
            for animal_dict in animals_data:
                if animal_dict["type"] == "Predator":
                    new_animal = Predator(animal_dict["id"], animal_dict["name"], animal_dict["food_amount"])
                elif animal_dict["type"] == "Omnivore":
                    new_animal = Omnivore(animal_dict["id"], animal_dict["name"], animal_dict["food_amount"])
                elif animal_dict["type"] == "Herbivore":
                    new_animal = Herbivore(animal_dict["id"], animal_dict["name"], animal_dict["food_amount"])
                else:
                    raise ValueError(f"Неизвестный тип животного: {animal_dict['type']}")
                    
                self.animals.append(new_animal)
                
            # Обновляем таблицу
            self.update_tree()
            messagebox.showinfo("Успех", "Данные успешно загружены из файла")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Некорректный формат файла")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZooApp(root)
    root.mainloop()
