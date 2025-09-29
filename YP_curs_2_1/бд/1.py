'''
внешний
CREAT - создание чего либо
INSERT INTO ... VALUES - дабавление в табл
SELECT - выборка данных

.fetchall() - получение всех записей список из кортежей
.fetchmany() - позволяет выбрать определённое кол-во зааписей список из кортежей
.fetchone() - выбирает отду запись кортеж
'''

import tkinter as tk
from tkinter import scrolledtext
import sqlite3

def выполнить_запрос_1():
    # Соединение с базой данных
    connect = sqlite3.connect('laba_1.db')
    cursor = connect.cursor()

    # ЗАДАНИЕ 1: Вывести все страны, начинающиеся на 'А'
    cursor.execute("SELECT Название_Страны FROM Страна")
    value = cursor.fetchall()
    # x[0] - fetchall() возвращ список кортеж, обращ к первому элементу кортежа
    spis_stran_A = [x[0] for x in value if x[0][0] == 'А']

    # Вывод результатов в текстовое поле
    result_text.delete("1.0", tk.END)  # очитска поля: имееи вид строка.символ (1-строка, 0-символ) tk.END - конец текст поля
    result_text.insert(tk.END, '\n'.join(spis_stran_A)) # tk.END - позиция вставки в конец

    # Закрытие соединения
    connect.close()

def выполнить_запрос_2():
    # Соединение с базой данных
    connect = sqlite3.connect('laba_1.db')
    cursor = connect.cursor()

    # ЗАДАНИЕ 2: Вывести все улицы, встречающиеся более чем в пяти городах
    cursor.execute("SELECT Название_Улицы FROM Улица")
    value_1 = cursor.fetchall()
    spis_street_5 = set(x[0] for x in value_1 if value_1.count(x) > 5)

    # Вывод результатов в текстовое поле
    result_text.delete("1.0", tk.END)  # Очистить поле
    result_text.insert(tk.END, '\n'.join(spis_street_5))

    # Закрытие соединения
    connect.close()

def выполнить_запрос_3():
    # Соединение с базой данных
    connect = sqlite3.connect('laba_1.db')
    cursor = connect.cursor()

    # ЗАДАНИЕ 3: Вывести все улицы РФ (ID страны РФ = 15)
    cursor.execute("SELECT * FROM Улица")
    value_2 = cursor.fetchall()

    # кортеж (id, наз_ул, id_город, id_страны)
    spis_street_Russia = set(x[1] for x in value_2 if x[3] == 15)

    # Вывод результатов в текстовое поле
    result_text.delete("1.0", tk.END)  # Очистить поле
    result_text.insert(tk.END, '\n'.join(spis_street_Russia))

    # Закрытие соединения
    connect.close()

# Создание основного окна
root = tk.Tk()
root.title("Запросы к базе данных")

# Кнопки для выполнения запросов
button_1 = tk.Button(root, text="Страны на 'A'", command=выполнить_запрос_1)
button_1.pack(pady=5)

button_2 = tk.Button(root, text="Улицы > 5 городах", command=выполнить_запрос_2)
button_2.pack(pady=5)

button_3 = tk.Button(root, text="Улицы в РФ", command=выполнить_запрос_3)
button_3.pack(pady=5)

# Текстовое поле для вывода результатов

#виджет который объединяет в себе текстовое поле и полосу прокрутки
#tk.WORD перенос на нов str будет осуществляться по словам
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
result_text.pack(pady=10)

# Запуск основного цикла обработки событий
root.mainloop()


