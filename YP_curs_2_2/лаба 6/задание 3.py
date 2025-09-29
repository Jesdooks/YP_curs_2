'''Добавьте к задаче №2 возможность
Уменьшить возраст всех студентов на 1'''
from tkinter import *
with open("students.csv", encoding="utf-8") as file: #эту часть взял со второго задания
    lst = file.read().split("\n")
    stud_list = [stud.split(";") for stud in lst] #формирую списки из значений в строчке, списки сохраняю в списке stud_list
    slovar = {i[0]:i[1:] for i in stud_list[1:]} #?

root = Tk() #создание основного окна
root.title("Задание 3")
root.geometry(f"600x250+500+200")

def decrease_age_by_1():
    global slovar, students #Объявляю переменные глоб, чтобы работать с этими переменными вне функции
    students.delete(0, END)
    for key, value in slovar.items():
        try:
            age = int(value[1])
            new_age = age - 1
            new_value = value[:1] + [str(new_age)] + value[2:]
            slovar[key] = new_value
        except (ValueError, IndexError):
            print(f"Ошибка обработки данных для студента {key}: {value}")
            continue
    #обновлённый список
    for key, value in slovar.items():
        students.insert(END, f"{key}: {' '.join(value[:2])}")

title = Label(root,
              text="Студенты",
              font=("Arial", 20)
              )

# Окно для отображения студентов
students = Listbox(root,
                   width=35,
                   font=("Arial", 15),
                   )

# Кнопка уменьшить возраст на 1
decreasing = Button(root,
                    text="уменьшить возраст на 1",
                    command=decrease_age_by_1,
                    font=("Arial", 20),
                    bg="yellow"  # Устанавливаем красный цвет фона кнопки
                    )

# Создание фрейма для размещения списка и кнопки рядом
frame = Frame(root)
frame.pack(pady=10)  # Отступ сверху для фрейма

# Размещение списка студентов слева и кнопки справа от него
students.pack(side=LEFT)  # Список студентов слева
decreasing.pack(side=LEFT, padx=10)  # Кнопка справа от списка с отступом

# Инициализация списка студентов в Listbox
for key, value in slovar.items():
    students.insert(END, f"{key}: {' '.join(value[:2])}")

# Отображение заголовка
title.pack()

root.mainloop()