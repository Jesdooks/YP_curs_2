from tkinter import *

with open("students.csv", encoding="utf-8") as f:
    lst = f.read().split("\n")
    stud_list = [stud.split(";") for stud in lst]
    header = stud_list[0]  #заголовок
    my_dict = {i[0]: i[1:] for i in stud_list[1:]}

root = Tk()
root.title("task_3")
root.geometry(f"600x250+500+200")


def decrease_age_by_1():
    global my_dict, students
    students.delete(0, END)
    for key, value in my_dict.items():
        try:
            age = int(value[1])
            new_age =  age - 1
            new_value = value[:1] + [str(new_age)] + value[2:]
            my_dict[key] = new_value
        except (ValueError, IndexError):
            print(f"Ошибка обработки данных для студента {key}: {value}")
            continue

    for key, value in my_dict.items():
        students.insert(END, f"{key}: {' '.join(value[:2])}")


def save_to_file():
    global my_dict, header
    try:
        with open("students", "w", encoding="utf-8") as file:  # Сохраняем в исходный файл
            file.write(";".join(header) + "\n")  # Записываем заголовок
            for key, value in my_dict.items():
                file.write(f"{key};{';'.join(value)}\n")
        print("Данные успешно сохранены!")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


# Метка заголовка
title = Label(root,
              text="Студенты",
              font=("Arial", 20)
              )
title.pack(pady=10)  # Отступ сверху для заголовка

# Создание фрейма для списка студентов
frame_left = Frame(root)
frame_left.pack(side=LEFT, padx=10, pady=10)  # Размещаем слева с отступами

# Окно для отображения студентов
students = Listbox(frame_left,
                   width=35,
                   font=("Arial", 15),
                   )
students.pack()  # Размещаем список в левом фрейме

# Заполнение списка студентов
for key, value in my_dict.items():
    students.insert(END, f"{key}: {' '.join(value[:2])}")

# Создание фрейма для кнопок
frame_right = Frame(root)
frame_right.pack(side=RIGHT, padx=10, pady=10)  # Размещаем справа с отступами

# Кнопка уменьшить возраст на 1
decreasing = Button(frame_right,
                    text="Уменьшить возраст на 1",
                    command=decrease_age_by_1,
                    font=("Arial", 20)
                    )
decreasing.pack(pady=5)  # Отступ между кнопками

# Кнопка сохранить
saving = Button(frame_right,
                text="Сохранить",
                command=save_to_file,  # Добавлено command
                pady=15,
                padx=15,
                font=("Arial", 20)
                )
saving.pack(pady=5)  # Отступ между кнопками

root.mainloop()