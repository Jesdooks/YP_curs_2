'''Добавьте к задаче 2 пользовательский интерфейс
Добавьте к пользовательскому интерфейсу из задачи 3 возможность сохранения новых данных обратно в файл.'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv

with open('students.csv', 'w', encoding='utf-8') as file:
    file.write('№;ФИО;Возраст;Группа\n')
    file.write('1;Иванов Иван Иванович;23;БО-111111\n')
    file.write('2;Сидоров Семен Семенович;23;БО-111111\n')
    file.write('3;Яшков Илья Петрович;24;БО-222222\n')


# функция для чтения студентов из файла
def read_students():
    students = []
    with open('students.csv', mode='r', encoding='utf-8') as files:
        reader = csv.reader(files, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) == 4:
                students.append(row)
    return students


# функция для отображения студентов в таблице
def display_students(students):
    for row in tree.get_children():
        tree.delete(row)

    for student in students:
        tree.insert('', tk.END, values=student)


# Функция для сортировки студентов по возрасту и отображения результата
def sort_students_by_age():
    students = read_students()
    sorted_students = sorted(students, key=lambda x: int(x[2]))
    display_students(sorted_students)


# Функция для увеличения возраста всех студентов на 1 и обновления таблицы
def decrease_age():
    students = read_students()
    for student in students:
        age = int(student[2])
        student[2] = str(age - 1)

    display_students(students)


def add_student():
    # Открываем диалоговое окно для ввода данных студента
    fio = simpledialog.askstring("Ввод ФИО", "Введите ФИО студента:")
    age = simpledialog.askinteger("Ввод возраста", "Введите возраст студента:")
    group = simpledialog.askstring("Ввод группы", "Введите группу студента:")

    if fio and age is not None and group:
        # Генерируем номер студента (количество строк в файле + 1)
        students = read_students()
        student_number = len(students) + 1

        # Записываем нового студента в файл
        with open('students.csv', 'a', encoding='utf-8') as files:
            writer = csv.writer(files, delimiter=';')
            writer.writerow([student_number, fio, age, group])

        # Обновляем таблицу
        display_students(read_students())
    else:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")


# Функция для сохранения данных в файле
def save_to_new_file():
    new_file_name = simpledialog.askstring("Сохранение", "Введите имя нового файла (с расширением .csv):")

    if new_file_name:
        students = read_students()
        with open(new_file_name, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['№', 'ФИО', 'Возраст', 'Группа'])  # Записываем заголовок
            writer.writerows(students)  # Записываем данные студентов

        messagebox.showinfo("Сохранение", f"Данные успешно сохранены в файл {new_file_name}")
    else:
        messagebox.showwarning("Ошибка", "Имя файла не может быть пустым!")


# Создание основного окна Tkinter
root = tk.Tk()
root.title("Таблица студентов")

# Создание виджета Treeview
tree = ttk.Treeview(root, columns=('№', 'ФИО', 'Возраст', 'Группа'), show='headings')
tree.heading('№', text='№')
tree.heading('ФИО', text='ФИО')
tree.heading('Возраст', text='Возраст')
tree.heading('Группа', text='Группа')

tree.column('№', width=50)
tree.column('ФИО', width=200)
tree.column('Возраст', width=100)
tree.column('Группа', width=100)

tree.pack(fill=tk.BOTH, expand=True)

# Создание кнопок
btn_sort_age = tk.Button(root, text="Сортировать по возрасту", command=sort_students_by_age)
btn_sort_age.pack(pady=5)

btn_decrease_age = tk.Button(root, text="Уменьшить возраст на 1", command=decrease_age)
btn_decrease_age.pack(pady=5)

btn_add_student = tk.Button(root, text="Добавить студента", command=add_student)
btn_add_student.pack(pady=5)

save_button = tk.Button(root, text="Сохранить данные", command=save_to_new_file)
save_button.pack(pady=10)

# Изначально отображаем студентов в таблице
display_students(read_students())

root.mainloop()
