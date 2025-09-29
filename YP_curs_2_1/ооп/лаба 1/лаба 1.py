import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont

class Student:
    def __init__(self, surname, initials, group_number, progress):
        self.surname = surname
        self.initials = initials
        self.group_number = group_number
        self.progress = progress

    def средний_балл(self):
        return sum(self.progress) / len(self.progress)

    def отличники(self):
        return all(x in [4, 5] for x in self.progress)

students = [
    Student("Иванов", "И.И.", 101, [4, 5, 3, 4, 5]),
    Student("Петров", "П.П.", 102, [5, 5, 5, 5, 5]),
    Student("Сидоров", "С.С.", 103, [3, 4, 3, 4, 3]),
    Student("Кузнецов", "К.К.", 101, [4, 4, 4, 4, 4]),
    Student("Николаев", "Н.Н.", 102, [5, 4, 5, 4, 5]),
    Student("Смирнов", "С.С.", 103, [3, 3, 3, 3, 3]),
    Student("Павлов", "П.П.", 101, [4, 5, 4, 5, 4]),
    Student("Михайлов", "М.М.", 102, [5, 5, 4, 5, 5]),
    Student("Андреев", "А.А.", 103, [3, 4, 3, 4, 3]),
    Student("Васильев", "В.В.", 101, [4, 4, 4, 4, 4]),
]

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информация о студентах")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Создаем стиль
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Создаем фрейм для выбора студента
        select_frame = tk.Frame(root, bg="#f0f0f0")
        select_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Метка для выбора студента
        tk.Label(select_frame, text="Выберите студента:", bg="#f0f0f0", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Выпадающий список для выбора студента
        self.student_var = tk.StringVar()
        student_names = [f"{s.surname} {s.initials}" for s in students]
        self.student_dropdown = ttk.Combobox(select_frame, textvariable=self.student_var, values=student_names, width=30)
        self.student_dropdown.pack(side=tk.LEFT, padx=5)
        self.student_dropdown.current(0)
        
        # Создаем фрейм для кнопок
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопки
        tk.Button(button_frame, text="Посчитать средний балл студента", command=self.calculate_average, 
                 bg="grey", fg="black", font=('Arial', 12, 'bold'), width=30, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Вывод учеников с оценками 4 и 5", command=self.show_good_students, 
                 bg="grey", fg="black", font=('Arial', 12, 'bold'), width=30, height=2).pack(side=tk.LEFT, padx=5)
        
        # Создаем таблицу
        self.tree = ttk.Treeview(root, columns=("Фамилия", "Инициалы", "Группа", "Средний балл", "Оценки"), show="headings")
        
        # Настраиваем заголовки
        self.tree.heading("Фамилия", text="Фамилия")
        self.tree.heading("Инициалы", text="Инициалы")
        self.tree.heading("Группа", text="Группа")
        self.tree.heading("Средний балл", text="Средний балл")
        self.tree.heading("Оценки", text="Оценки")
        
        # Настраиваем ширину столбцов
        self.tree.column("Фамилия", width=150)
        self.tree.column("Инициалы", width=100)
        self.tree.column("Группа", width=100)
        self.tree.column("Средний балл", width=120)
        self.tree.column("Оценки", width=200)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем таблицу и скроллбар
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Отображаем всех студентов при запуске
        self.show_all_students()
    
    def show_all_students(self):
        self.tree.delete(*self.tree.get_children())
        for student in students:
            self.tree.insert("", tk.END, values=(
                student.surname,
                student.initials,
                student.group_number,
                f"{student.средний_балл():.2f}",
                ", ".join(map(str, student.progress))
            ))
    
    def calculate_average(self):
        selected_student = self.student_var.get()
        for student in students:
            if f"{student.surname} {student.initials}" == selected_student:
                average = student.средний_балл()
                messagebox.showinfo("Средний балл", f"Средний балл студента {student.surname} {student.initials}: {average:.2f}")
                return
    
    def show_good_students(self):
        self.tree.delete(*self.tree.get_children())
        for student in students:
            if student.отличники():
                self.tree.insert("", tk.END, values=(
                    student.surname,
                    student.initials,
                    student.group_number,
                    f"{student.средний_балл():.2f}",
                    ", ".join(map(str, student.progress))
                ))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
