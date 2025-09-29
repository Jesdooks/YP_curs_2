students = [
    [1, "Иванов Иван Иванович", 20, "Группа A"],
    [2, "Петров Петр Петрович", 21, "Группа B"],
    [3, "Сидоров Сидор Сидорович", 22, "Группа C"]
]

students_dict = {}
for student in students:
    key = student[0] # Первый элемент списка студента как ключ
    value = student[1:] # Остальные элементы списка студента как значение
    students_dict[key] = value #пара ключ-значение

for key, value in students_dict.items():
    print(f'{key}: {value}')
