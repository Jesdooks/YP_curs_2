from tkinter import *
import tkinter as tk
from tkinter import messagebox, simpledialog

# Исходный список студентов
students_list = [
    [1, "Иванов Иван Иванович", 20, "БО-111111"],
    [2, "Петров Петр Петрович", 21, "БО-111111"],
    [3, "Сидоров Сидор Сидорович", 22, "БО-222222"],
    [4, "Иванова Мария Ивановна", 23, "БО-222222"],
    [5, "Иванов Алексей Иванович", 22, "БО-33333"]
]

# Преобразование списка в словарь для удобного доступа к данным студентов
students_dict = {}
for student in students_list:
    key = student[0] # Первый элемент списка студента как ключ
    value = student[1:] # Остальные элементы списка студента как значение
    students_dict[key] = value #пара ключ-значение
def update_student_info():
    # Обновляем информацию о студентах в метке
    info = "Студенты:\n"
    for key, value in students_dict.items(): #items возвращает кортежи значений
        info += f"No: {key}, ФИО: {value[0]}, Возраст: {value[1]}, Группа: {value[2]}\n"
    students_info_label.config(text=info) #отображ измен текста на виджете label


def increase_age_by_name():
    # Запрашиваем ФИО студента для увеличения возраста simpledialog.askstring - созд диалог окно для ввода
    full_name = simpledialog.askstring("Увеличить возраст", "Введите ФИО студента:")
    if full_name:
        found = False
        for key, value in students_dict.items():
            if value[0] == full_name: #если фио совпало с введённым
                '''ВАЖНО!!!'''
                value[1] += 1  # Увеличиваем возраст на 1 год
                found = True
                break
        if found:
            messagebox.showinfo("Успех", f"Возраст студента {full_name} увеличен на 1 год.")
            update_student_info()
        else:
            messagebox.showerror("Ошибка", f"Студент с ФИО '{full_name}' не найден.")


def change_name():
    # Изменяем ФИО студента simpledialog.askstring - созд диалог окно для ввода
    old_name = simpledialog.askstring("Изменить ФИО", "Введите старое ФИО студента:")
    new_name = simpledialog.askstring("Изменить ФИО", "Введите новое ФИО студента:")
    if old_name and new_name:
        found = False
        for key, value in students_dict.items():
            if value[0] == old_name:
                value[0] = new_name  # Меняем старое ФИО на новое
                found = True
                break
        if found:
            messagebox.showinfo("Успех", f"ФИО студента изменено с '{old_name}' на '{new_name}'.")
            update_student_info()
        else:
            messagebox.showerror("Ошибка", f"Студент с ФИО '{old_name}' не найден.")


def increase_age_by_no():
    # Увеличиваем возраст студента по его номеру simpledialog.askstring - созд диалог окно для ввода
    no = simpledialog.askinteger("Увеличить возраст", "Введите No студента:")
    if no is not None and no in students_dict: #не пустое
        students_dict[no][1] += 1  # Увеличиваем возраст на 1 год
        messagebox.showinfo("Успех", f"Возраст студента с No {no} увеличен на 1 год.")
        update_student_info()
    else:
        messagebox.showerror("Ошибка", f"Студент с No '{no}' не найден.")


def change_group():
    # Изменяем группу студента по его ФИО
    full_name = simpledialog.askstring("Изменить группу", "Введите ФИО студента:")
    new_group = simpledialog.askstring("Изменить группу", "Введите новую группу:")
    if full_name and new_group:
        found = False
        for key, value in students_dict.items():
            if value[0] == full_name:
                value[2] = new_group  # Меняем группу на новую
                found = True
                break
        if found:
            messagebox.showinfo("Успех", f"Группа студента {full_name} изменена на '{new_group}'.")
            update_student_info()
        else:
            messagebox.showerror("Ошибка", f"Студент с ФИО '{full_name}' не найден.")


def delete_student_by_no():
    # Удаляем запись о студенте по его номеру
    no = simpledialog.askinteger("Удалить студента", "Введите No студента для удаления:")
    if no is not None and no in students_dict:
        del students_dict[no]  # Удаляем студента из словаря
        messagebox.showinfo("Успех", f"Студент с No {no} удален.")
        update_student_info()
    else:
        messagebox.showerror("Ошибка", f"Студент с No '{no}' не найден.")


def adjust_age_conditions():
    # Корректируем возраст студентов по заданным условиям
    for key in list(students_dict.keys()):
        age = students_dict[key][1]
        '''ВАЖНО!!!!'''
        if age > 22:
            students_dict[key][1] -= 1  # Уменьшаем возраст на 1 год для студентов старше 22 лет
        elif age == 23:
            del students_dict[key]  # Удаляем студентов в возрасте 23 лет
    messagebox.showinfo("Успех", "Возраст студентов скорректирован.")
    update_student_info()


def increase_age_ivanov():
    # Увеличиваем возраст всех студентов с фамилией 'Иванов'
    for key, value in students_dict.items():
        if value[0][:7] == ("Иванов "):
            value[1] += 1  # Увеличиваем возраст на 1 год
    messagebox.showinfo("Успех", "Возраст студентов с фамилией 'Иванов' увеличен на 1 год.")
    update_student_info()


def change_surname_ivanov():
    # Изменяем фамилию всех студентов 'Иванов' на 'Сидоров'
    for key, value in students_dict.items():
        if value[0].startswith("Иванов"): #startswith начинается ли строка с указанной подстроки
            value[0] = value[0].replace("Иванов", "Сидоров")  # Заменяем фамилию
    messagebox.showinfo("Успех", "Фамилия студентов 'Иванов' изменена на 'Сидоров'.")
    update_student_info()


def swap_fio_group():
    # Меняем местами ФИО и группу у всех студентов
    for key, value in students_dict.items():
        value[0], value[2] = value[2], value[0]  # Меняем местами значения ФИО и группы
    messagebox.showinfo("Успех", "ФИО и группа студентов поменяны местами.")
    update_student_info()

'''ВАЖНО!!!!!!!! key'''
def filter_students(condition):
    # Фильтруем студентов по заданному условию и возвращаем отфильтрованный словарь
    filtered_students = {}
    for key, value in students_dict.items():
        if condition(key):
            filtered_students[key] = value
    return filtered_students


def show_filtered_students(condition):
    # Отображаем отфильтрованных студентов согласно заданному условию
    filtered_students = filter_students(condition)
    info = "Отфильтрованные студенты:\n"

    if not filtered_students:
        info += "Нет студентов по заданному критерию."

    for key, value in filtered_students.items():
        info += f"No: {key}, ФИО: {value[0]}, Возраст: {value[1]}, Группа: {value[2]}\n"

    filtered_students_label.config(text=info)


# Создаем главное окно приложения
root = tk.Tk()
root.title("Управление студентами")
root.attributes('-fullscreen', True)

# Создаем фреймы для организации интерфейса приложения
frame = Frame(borderwidth=1, relief=SOLID)
frame.grid(column=0, row=0, padx=20, pady=20, ipady=30)
frame1 = Frame(borderwidth=1, relief=SOLID)
frame1.grid(column=1, row=0, padx=20, pady=20, sticky=N)
frame2 = Frame(borderwidth=1, relief=SOLID)
frame2.grid(sticky=NE, column=2, row=0, padx=20, pady=20)

# Метка для отображения информации о студентах
students_info_label = tk.Label(frame, text="", justify=tk.LEFT, font=('Arial', 14))
students_info_label.grid(column=0, row=0, padx=20, pady=15)

# Метка для отображения отфильтрованных студентов
filtered_students_label = tk.Label(frame, text="", justify=tk.LEFT, font=('Arial', 14))
filtered_students_label.grid(column=0, row=1, padx=20, pady=15)

# Кнопки для различных операций над данными о студентах
tk.Button(root, text="Закрыть окно", command=root.destroy, font=('Arial', 14), width=15).grid(column=0, row=2)
tk.Button(frame1, text="Увеличить возраст по ФИО", width=23, command=increase_age_by_name).grid(pady=5)
tk.Button(frame1, text="Изменить ФИО студента", width=23, command=change_name).grid(pady=5)
tk.Button(frame1, text="Увеличить возраст по No", command=increase_age_by_no, width=29).grid(pady=5)
tk.Button(frame1, text="Изменить группу студента", command=change_group, width=29).grid(pady=5)
tk.Button(frame1, text="Удалить запись о студенте по No", command=delete_student_by_no, width=29).grid(pady=5)
tk.Button(frame1, text="Скорректировать возраст студентов", command=adjust_age_conditions, width=29).grid(pady=5)
tk.Button(frame1, text="Увеличить возраст 'Иванов'", command=increase_age_ivanov, width=29).grid(pady=5)
tk.Button(frame1, text="Изменить фамилию 'Иванов' на 'Сидоров'", command=change_surname_ivanov, width=36).grid(pady=5)
tk.Button(frame1, text="Поменять ФИО и Группу местами", command=swap_fio_group, width=36).grid(pady=5, padx=5)

# Кнопки для фильтрации студентов по различным критериям
tk.Button(frame2, text="Студенты группы 'A'",
          command=lambda: show_filtered_students(lambda x: x[2] == 'А'), width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с номерами 1-10",
          command=lambda: show_filtered_students(lambda x: x in range(1, 11)), width=31).grid(pady=5)
tk.Button(frame2, text="Студенты в возрасте 22 лет", command=lambda: show_filtered_students(lambda x: x[1] == 22),
          width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с фамилией 'Иванов'",
          command=lambda: show_filtered_students(lambda x: x[0][:7] == ("Иванов ")), width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с фамилиями заканчивающимися на 'а'",
          command=lambda: show_filtered_students(lambda x: x[0][-1]==('а')), width=35).grid(pady=5)
tk.Button(frame2, text="Студенты с четным возрастом", command=lambda: show_filtered_students(lambda x: x[1] % 2 == 0),
          width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с возрастом содержащим '5'",
          command=lambda: show_filtered_students(lambda x: '5' in str(x[1])), width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с четным номером", command=lambda: show_filtered_students(lambda x: x % 2 == 0),
          width=31).grid(pady=5)
tk.Button(frame2, text="Студенты с длинной группой больше 7 символов",
          command=lambda: show_filtered_students(lambda x: len(x[2]) > 7), width=43).grid(pady=5)
tk.Button(frame2, text="Студенты с номером группы заканчивающимся на '1'",
          command=lambda: show_filtered_students(lambda x: x[2].endswith('1')), width=43).grid(padx=5, pady=5)

# Инициализируем отображение информации о студентах
update_student_info()

# Запускаем главный цикл приложения
root.mainloop()