
with open('students.csv') as file: #открывание файла
    baza_stud = []
    s = file.readline() #чтение названия столбиков в переменную (25ст лекции)
    for i in file.readlines(): #считывает до конца файл
        new_line = i.replace('\n', '').split(';')
        lst = i.split(';')
        baza_stud.append(new_line)

#print(baza_stud)
#сортировка по возрасту
a = sorted(baza_stud, key=lambda x: x[2])
for j in a:
    print(' '.join(map(str, j)))
