nums = input()
'''nums = """
12345678
87654321
23456789
98765432
13579753
31532657
17597315
26351732"""'''


matrix = []
#создаю матрицу
for el in nums.split("\n")[1:]:
    matrix.append(list(map(int,el)))
#print(matrix)

#Задание 1 Напишите функцию возведения всех четных элементов в квадрат.
def mat_sq(mat):
    for row in matrix:
        for i in range(len(row)):
            if row[i] % 2 == 0:
                row[i] = row[i] ** 2
    return mat

#Задание 2 Напишите функцию сложения по столбцам.
def row_addition(*args):
    global matrix
    res = []

    for row in matrix:
        total = sum(row[col] for col in args)
        res.append(total)

    return res

#Задание 3 Напишите функцию возведения в квадрат всех элементов четных строк.

def sq_even_rows(mat):
    for i in range(len(mat)):
        if i % 2 == 0:
            for j in range(len(mat[i])):
                mat[i][j] = mat[i][j] ** 2

    return mat


#Задание 4 Напишите функцию сложения всех элементов матрицы.
def addition_by_elems(mat):
    return sum([sum(row) for row in mat]) #сначала сумм все знач в строке, добв в новый список и суммируются


#Задание 5 Пользователь вводит через консоль число. Напишите функцию, которая заменит все числа в матрице, которые меньше введенного, на введенное число.
def replace_num(num, mat):
    for row in matrix:
        for i in range(len(row)):
            if row[i] < num:
                row[i] = num

    return mat


#Задание 6 Пусть пользователь через консоль вводит число. Напишите функцию удаления столбца в матрице, чей номер равен введенному числу.
def del_column(num,mat):
    for row in matrix:
        for i in range(len(row)):
            if i == num:
                del row[i]


    return mat


#Задание 7 Напишите функцию создания матрицы любого размера, заполненного нулями (размер задается через консоль).
def create_mat(n,m):
    mat = []
    for i in range(n):
        mat.append([0] * m)
    return mat

#Задание 8 Пусть пользователь через консоль вводит число: номер строки.
#Напишите функцию, которая выведет все элементы данной строки, возведенные в квадрат.
''' #по столбцам
def sq_column(num,mat):
    sq_col = []
    for row in mat:
        sq_col.append(row[num] ** 2)
    return sq_col'''


def sq_column(num, mat):
    sq_col = []
    for value in mat[num]:
        sq_col.append(value ** 2)
    return sq_col


#1, 3
'''c = sq_even_rows(matrix)
for i in range(len(c)):
    print(c[i])'''

#2
'''print(row_addition(2, 3))'''

#4
'''print(addition_by_elems(matrix))'''

#5,6,8
'''c = del_column(2, matrix)
for i in range(len(c)):
    print(c[i])'''

#7
'''c = create_mat(2,3)
for i in range(len(c)):
    print(c[i])'''

#8
print(sq_column(0, matrix))