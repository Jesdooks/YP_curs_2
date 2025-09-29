import tkinter as tk
from tkinter import ttk, messagebox

class Laba_3:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def вывод_на_экран(self):
        return f"x = {self.x}, y = {self.y}"

    def изменение_переменных(self, x1, y1):
        self.x = x1
        self.y = y1
        return "Значения изменены"

    def сумма(self):
        return f'Сумма чисел: {self.x + self.y}'

    def наибольшее(self):
        if self.x > self.y:
            return f'Наибольшее число: {self.x}'
        else:
            return f'Наибольшее число: {self.y}'

class Laba3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 3")
        
        # Создаем объект класса Laba_3 с начальными значениями 0
        self.laba = Laba_3(0, 0)
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Ввод значений", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(input_frame, text="Значение x:").grid(row=0, column=0, sticky="w")
        self.x_entry = ttk.Entry(input_frame)
        self.x_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Значение y:").grid(row=1, column=0, sticky="w")
        self.y_entry = ttk.Entry(input_frame)
        self.y_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Кнопка для установки значений
        ttk.Button(input_frame, text="Установить значения", command=self.set_values).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Вывод чисел", command=self.show_values).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Наибольшее значение", command=self.show_max).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Сумма значений", command=self.show_sum).grid(row=0, column=2, padx=5)
        
        # Текстовое поле для вывода результатов
        self.result_text = tk.Text(self.root, height=5, width=40)
        self.result_text.grid(row=2, column=0, padx=10, pady=5)
        
        # Показываем начальные значения
        self.show_values()
        
    def set_values(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.laba.изменение_переменных(x, y)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Значения установлены: x={x}, y={y}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовые значения")
        
    def show_values(self):
        result = self.laba.вывод_на_экран()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
    def show_max(self):
        result = self.laba.наибольшее()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
    def show_sum(self):
        result = self.laba.сумма()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = Laba3App(root)
    root.mainloop()