from tkinter import *
#прин каждый элемент из baza_stud и возв 3 эл
'''def year():

    download_label.config(text="Изначальные данные: \n-" +)
    upload_label.config(text="Изменённые данные: \n-" + )
root = Tk() #пользовательское окно

root.title('Название программы') #Название окна
root.geometry('300x300')

button = Button(root, text="Увеличить возраст", font=("Arial", 20), command=year)
button.pack()
button.pack(side=BOTTOM, pady=30)

download_label = Label(root, text="Изначальные данные: \n-", font=("Arial", 20, "bold"))
download_label.pack(pady=(50, 0))
upload_label = Label(root, text="Изменённые данные: \n-", font=("Arial", 20, "bold"))
upload_label.pack(pady=(10, 0))

root.mainloop() #постоянный цикл, чтобы работала программа
'''
with open('students.csv') as file: #открывание файла
    baza_stud = []
    s = file.readline() #чтение названия столбиков в переменную (25ст лекции)
    for i in file.readlines(): #считывает до конца файл, а .readline() до \n
        new_line = i.replace('\n', '').split(';')
        lst = i.split(';')
        baza_stud.append(new_line)

#print(baza_stud)
students_sorted = sorted(baza_stud, key=lambda x: x[2]) #сортировка студентов по возрасту (reverse=True)
#print(students_sorted)

#вывод студентов по возрасту
'''for j in students_sorted:
    print(' '.join(map(str, j)))'''

for student in students_sorted:
    student[2] = str(int(student[2]) - 1)

#вывод студентов по возрасту - 1
for student in students_sorted:
    print(' '.join(map(str, student)))
