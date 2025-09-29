import tkinter as tk
from tkinter import ttk, messagebox

class home_library:
    def __init__(self):
        self.spis_books = []

    def вывод_в_консоль(self):
        return [f"Название: {book['Название']}, Автор: {book['Автор']}, Год: {book['Год']}" for book in self.spis_books]

    def добавление_книги(self, name_book, author, year):
        new_book = {'Название': name_book, 'Автор': author, 'Год': year}
        self.spis_books.append(new_book)
        return "Книга успешно добавлена"

    def удаление_книги_по_названию(self, user_book):
        for i in self.spis_books:
            if i['Название'] == user_book:
                self.spis_books.remove(i)
                return "Книга успешно удалена"
        return "Книга с таким названием не найдена"

    def найти_книгу_по_автору(self, user_author):
        search_author = [x for x in self.spis_books if x['Автор'].lower() == user_author.lower()]
        if search_author:
            return [f"Название: {book['Название']}, Автор: {book['Автор']}, Год: {book['Год']}" for book in search_author]
        return ["Такого автора нет в библиотеке"]

    def найти_книгу_по_году(self, user_year):
        search_year = [x for x in self.spis_books if x['Год'] == user_year]
        if search_year:
            return [f"Название: {book['Название']}, Автор: {book['Автор']}, Год: {book['Год']}" for book in search_year]
        return [f"Книга с таким {user_year} годом издания отсутствует в библиотеке"]

    def сортировка_по_названиям(self):
        self.spis_books = sorted(self.spis_books, key=lambda x: x['Название'])
        return self.вывод_в_консоль()

    def сортировка_по_авторам(self):
        self.spis_books = sorted(self.spis_books, key=lambda x: x['Автор'])
        return self.вывод_в_консоль()

    def сортировка_по_году(self):
        self.spis_books = sorted(self.spis_books, key=lambda x: x['Год'])
        return self.вывод_в_консоль()

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Домашняя библиотека")
        
        # Создаем объект библиотеки
        self.library = home_library()
        
        # Добавляем тестовые книги
        self.library.добавление_книги("Мастер и Маргарита", "Михаил Булгаков", 1967)
        self.library.добавление_книги("Война и мир", "Лев Толстой", 1869)
        self.library.добавление_книги("1984", "Джордж Оруэлл", 1949)
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление книги", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = ttk.Entry(input_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Год:").grid(row=2, column=0, sticky="w")
        self.year_entry = ttk.Entry(input_frame)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Добавить книгу", command=self.add_book).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Удалить книгу", command=self.delete_book).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Поиск по автору", command=self.search_by_author).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Поиск по году", command=self.search_by_year).grid(row=0, column=3, padx=5)
        
        # Кнопки сортировки
        sort_frame = ttk.Frame(self.root)
        sort_frame.grid(row=2, column=0, padx=10, pady=5)
        
        ttk.Button(sort_frame, text="Сортировка по названию", command=self.sort_by_name).grid(row=0, column=0, padx=5)
        ttk.Button(sort_frame, text="Сортировка по автору", command=self.sort_by_author).grid(row=0, column=1, padx=5)
        ttk.Button(sort_frame, text="Сортировка по году", command=self.sort_by_year).grid(row=0, column=2, padx=5)
        
        # Текстовое поле для вывода результатов
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=3, column=0, padx=10, pady=5)
        
        # Показываем начальный список книг
        self.show_books()
        
    def show_books(self):
        books = self.library.вывод_в_консоль()
        self.result_text.delete(1.0, tk.END)
        for book in books:
            self.result_text.insert(tk.END, book + "\n")
            
    def add_book(self):
        try:
            name = self.name_entry.get()
            author = self.author_entry.get()
            year = int(self.year_entry.get())
            
            if not name or not author:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            result = self.library.добавление_книги(name, author, year)
            messagebox.showinfo("Успех", result)
            self.show_books()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            
    def delete_book(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Ошибка", "Введите название книги для удаления")
            return
            
        result = self.library.удаление_книги_по_названию(name)
        messagebox.showinfo("Результат", result)
        self.show_books()
        self.clear_entries()
        
    def search_by_author(self):
        author = self.author_entry.get()
        if not author:
            messagebox.showerror("Ошибка", "Введите автора для поиска")
            return
            
        results = self.library.найти_книгу_по_автору(author)
        self.result_text.delete(1.0, tk.END)
        for result in results:
            self.result_text.insert(tk.END, result + "\n")
            
    def search_by_year(self):
        try:
            year = int(self.year_entry.get())
            results = self.library.найти_книгу_по_году(year)
            self.result_text.delete(1.0, tk.END)
            for result in results:
                self.result_text.insert(tk.END, result + "\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный год")
            
    def sort_by_name(self):
        results = self.library.сортировка_по_названиям()
        self.result_text.delete(1.0, tk.END)
        for result in results:
            self.result_text.insert(tk.END, result + "\n")
            
    def sort_by_author(self):
        results = self.library.сортировка_по_авторам()
        self.result_text.delete(1.0, tk.END)
        for result in results:
            self.result_text.insert(tk.END, result + "\n")
            
    def sort_by_year(self):
        results = self.library.сортировка_по_году()
        self.result_text.delete(1.0, tk.END)
        for result in results:
            self.result_text.insert(tk.END, result + "\n")
            
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()



