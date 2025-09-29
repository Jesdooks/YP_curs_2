import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, scrolledtext
import math
import random
import string
from prettytable import PrettyTable
import os
import csv
import copy
import numpy as np

total_sum = 0
count = 0

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def main_menu():
    clear_window()
    lab_work_1_button = ttk.Button(root, text="Лабораторная работа 1", command=open_lab_work_1)
    lab_work_1_button.pack(pady=20)

    lab_work_2_button = ttk.Button(root, text="Лабораторная работа 2", command=open_lab_work_2)
    lab_work_2_button.pack(pady=20)

    lab_work_3_button = ttk.Button(root, text="Лабораторная работа 3", command=open_lab_work_3)
    lab_work_3_button.pack(pady=20)

    lab_work_4_button = ttk.Button(root, text="Лабораторная работа 4", command=open_lab_work_4)
    lab_work_4_button.pack(pady=20)

    lab_work_5_button = ttk.Button(root, text="Лабораторная работа 5", command=open_lab_work_5)
    lab_work_5_button.pack(pady=20)

    lab_work_6_button = ttk.Button(root, text="Лабораторная работа 6", command=open_lab_work_6)
    lab_work_6_button.pack(pady=20)

    lab_work_7_button = ttk.Button(root, text="Лабораторная работа 7", command=open_lab_work_7)
    lab_work_7_button.pack(pady=20)

    lab_work_8_button = ttk.Button(root, text="Лабораторная работа 8", command=open_lab_work_8)
    lab_work_8_button.pack(pady=20)

def open_lab_work_1():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 1", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab1).pack(pady=5)
    ttk.Button(root, text="Задание 2", command=task_2_lab1).pack(pady=5)
    ttk.Button(root, text="Задание 3", command=task_3_lab1).pack(pady=5)
    ttk.Button(root, text="Задание 4", command=task_4_lab1).pack(pady=5)
    ttk.Button(root, text="Задание 5", command=task_5_lab1).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_2():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 2", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab2).pack(pady=5)
    ttk.Button(root, text="Задание 2", command=task_2_lab2).pack(pady=5)
    ttk.Button(root, text="Задание 3", command=task_3_lab2).pack(pady=5)
    ttk.Button(root, text="Задание 4", command=task_4_lab2).pack(pady=5)
    ttk.Button(root, text="Задание 5", command=task_5_lab2).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_3():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 3", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 2", command=task_2_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 3", command=task_3_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 4", command=task_4_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 5", command=task_5_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 6", command=task_6_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 7", command=task_7_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 8", command=task_8_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 9", command=task_9_lab3).pack(pady=5)
    ttk.Button(root, text="Задание 10", command=task_10_lab3).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_4():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 4", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab4).pack(pady=5)
    ttk.Button(root, text="Задание 2", command=task_2_lab4).pack(pady=5)
    ttk.Button(root, text="Задание 3", command=task_3_lab4).pack(pady=5)
    ttk.Button(root, text="Задание 4", command=task_4_lab4).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_5():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 5", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab5).pack(pady=5)
    ttk.Button(root, text="Задание 2-3", command=task_2_lab5).pack(pady=5)


    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_6():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 6", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab6).pack(pady=5)
    ttk.Button(root, text="Задание 2-4", command=task_2_lab6).pack(pady=5)


    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_7():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 7", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1", command=task_1_lab7).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def open_lab_work_8():
    clear_window()
    lab_label = tk.Label(root, text="Лабораторная работа 8", font=("Arial", 16))
    lab_label.pack(pady=10)

    ttk.Button(root, text="Задание 1-6", command=task_1_lab8).pack(pady=5)
    ttk.Button(root, text="Задание 2", command=task_2_lab8).pack(pady=5)
    ttk.Button(root, text="Задание 3", command=task_3_lab8).pack(pady=5)

    back_button = ttk.Button(root, text="Назад", command=main_menu)
    back_button.pack(pady=5)

def task_1_lab1():
    """Задание 1: Введите информацию о себе"""
    clear_window()
    tk.Label(root, text="Введите информацию о себе", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Как Вас зовут?").pack(pady=2)
    entry_name = tk.Entry(root)
    entry_name.pack(pady=5)

    tk.Label(root, text="Название ВУЗа:").pack(pady=2)
    entry_vuz = tk.Entry(root)
    entry_vuz.pack(pady=5)

    tk.Label(root, text="Укажите номер вашей группы.").pack(pady=2)
    entry_group = tk.Entry(root)
    entry_group.pack(pady=5)

    tk.Label(root, text="Изучаемый язык:").pack(pady=2)
    entry_language = tk.Entry(root)
    entry_language.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить",
                               command=lambda: submit_student_info(entry_name.get(), entry_vuz.get(), entry_group.get(),
                                                                   entry_language.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_1)
    back_button.pack(pady=5)


def submit_student_info(name, vyz, num, yaz):
    """Обрабатывает данные студента и отображает их в сообщении"""
    message = (f"- Добрый день, {name}!\n"
               f"- Вы обучаетесь в образовательной организации {vyz} в группе {num}\n"
               f"- {name}, желаем Вам успешного обучения программированию на языке {yaz}")
    messagebox.showinfo("Результат", message)


def task_2_lab1():
    """Задание 2: Введите числа a, b, c, d и f"""
    clear_window()
    tk.Label(root, text="Введите числа a, b, c, d и f", font=("Arial", 16)).pack(pady=10)

    labels = ["a:", "b:", "c:", "d:", "f:"]
    entries = []

    for label in labels:
        tk.Label(root, text=label).pack(pady=2)
        entry = tk.Entry(root)
        entry.pack(pady=5)
        entries.append(entry)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: calculate([entry.get() for entry in entries]))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_1)
    back_button.pack(pady=5)


def calculate(inputs):
    """Выполняет вычисления на основе введенных чисел"""
    try:
        a, b, c, d, f = map(int, inputs)

        if a != 0:
            result = math.fabs(a - b * c * d ** 3 + (c ** 5 - a ** 2) / a + f ** 3 * (a - 213))
            messagebox.showinfo("Результат вычислений", f"Результат: {result}")
        else:
            messagebox.showerror("Ошибка", "Число a не может равняться нулю")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")


def task_3_lab1():
    """Задание 3: Введите список элементов"""
    clear_window()
    tk.Label(root, text="Введите список элементов", font=("Arial", 16)).pack(pady=10)

    entry_list = tk.Entry(root)
    entry_list.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: process_list(entry_list.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_1)
    back_button.pack(pady=5)


def process_list(input_string):
    """Обрабатывает список элементов, выводя элементы на нечетных позициях"""
    input_list = input_string.split()
    '''ВАЖНО!!!!'''
    odd_index_elements = [input_list[i] for i in range(len(input_list)) if i % 2 == 0]

    if odd_index_elements:
        result_message = "Элементы на нечетных позициях:\n" + "\n".join(odd_index_elements)
        messagebox.showinfo("Результат обработки списка", result_message)
    else:
        messagebox.showinfo("Результат обработки списка", "Нет элементов на нечетных позициях.")


def task_4_lab1():
    """Задание 4: Введите список чисел"""
    clear_window()
    tk.Label(root, text="Введите список чисел", font=("Arial", 16)).pack(pady=10)

    entry_list = tk.Entry(root)
    entry_list.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: multiply_less_than_ten(entry_list.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_1)
    back_button.pack(pady=5)


def multiply_less_than_ten(input_string):
    """Вычисляет произведение чисел меньше 10"""
    try:
        numbers = list(map(int, input_string.split()))
        product = 1
        found = False
        for number in numbers:
            if number < 10:
                product *= number
                found = True
        if not found:
            product = 0
        messagebox.showinfo("Результат", f"Произведение чисел меньше 10: {product}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")


def task_5_lab1():
    """Задание 5: Введите список чисел"""
    clear_window()
    tk.Label(root, text="Введите список чисел", font=("Arial", 16)).pack(pady=10)

    entry_list = tk.Entry(root)
    entry_list.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: find_central_element(entry_list.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_1)
    back_button.pack(pady=5)


def find_central_element(input_string):
    """Находит центральный элемент списка"""
    try:
        numbers = min(list(map(int, input_string.split())))

        messagebox.showinfo("Минмальный элемент", f"Минимальный элемент: {numbers}")

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def task_1_lab2():
    """Задание 1: Введите число, пока не будет введено число >= 40"""
    clear_window()
    tk.Label(root, text="Введите любое число:", font=("Arial", 16)).pack(pady=10)

    entry_number = tk.Entry(root)
    entry_number.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: check_number(entry_number.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_2)
    back_button.pack(pady=5)


def check_number(user_input):
    """Проверяет введенное число"""
    try:
        user_number = int(user_input)
        my_number = 3
        if user_number < my_number:
            messagebox.showinfo("Результат", "Введите другое число.")
        else:
            messagebox.showinfo("Результат", "Вы ввели число >= 3.")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")


def task_2_lab2():
    """Задание 2: Слова меньше 10 символов'"""
    clear_window()
    tk.Label(root, text="Введите любые слова через пробел:", font=("Arial", 16)).pack(pady=10)

    entry_words = tk.Entry(root)
    entry_words.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: show_words_starting_with_r(entry_words.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_2)
    back_button.pack(pady=5)


def show_words_starting_with_r(input_string):
    """Показывает слова, меньше 10 символов'"""
    words = input_string.split()
    result = []
    for i in range(len(words)):
        if len(words[i]) < 10:
            result += [words[i]]
    if result:
        messagebox.showinfo("Результат", "Слова, меньше 10 символов:\n" + "\n".join(result))
    else:
        messagebox.showinfo("Результат", "Нет слов, меньше 10 символов.")


def task_3_lab2():
    """Задание 3: Строку размером N символов из r символов'"""
    clear_window()
    tk.Label(root, text="Введите целочисленное число N:", font=("Arial", 16)).pack(pady=10)

    entry_words = tk.Entry(root)
    entry_words.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: stoka_N(entry_words.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_2)
    back_button.pack(pady=5)


def stoka_N(input_user):
    """Задание 3: Строку размером N символов из r символов"""
    user_number = int(input_user)
    stroka = 'r' * user_number
    messagebox.showinfo("Результат", f"Cтрока длинной N символов: {stroka}")


def task_4_lab2():
    """Задание 4: Строка только из букв"""
    clear_window()
    tk.Label(root, text="Введите строку с числами и буквами:", font=("Arial", 16)).pack(pady=10)

    entry_string = tk.Entry(root)
    entry_string.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: separate_numbers_and_letters(entry_string.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_2)
    back_button.pack(pady=5)


def separate_numbers_and_letters(input_string):
    """Задание 4: Строка только из букв"""
    '''numbers = ''.join(c for c in input_string if c.isdigit())'''
    letters = ''.join(c for c in input_string if c.isalpha())
    messagebox.showinfo("Результат", f"Строка только из букв: {letters}")


def task_5_lab2():
    """Задание 5: Удалить все чётные элементы"""
    clear_window()
    tk.Label(root, text="Введите 10 любых элементов через пробел:", font=("Arial", 16)).pack(pady=10)
    entry_list1 = tk.Entry(root)
    entry_list1.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: combine_lists(entry_list1.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_2)
    back_button.pack(pady=5)


def combine_lists(list1_string):
    """Задание 5: Удалить все чётные элементы"""
    list1 = list1_string.split()
    stroka = ''
    stroka_1 = stroka.join(list1[0::2])+'k'+'l'
    messagebox.showinfo("Результат", "Строка без чётных элементов:\n" + stroka_1)

def task_1_lab3():
    """Задание 1: Ввод чисел A, B и C и вывод минимального"""
    clear_window()
    tk.Label(root, text="Введите числа A, B и C через пробел:", font=("Arial", 16)).pack(pady=10)

    entry_numbers = tk.Entry(root)
    entry_numbers.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: find_minimum(entry_numbers.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def find_minimum(input_string):
    """Находит минимальное число из введенных"""
    try:
        numbers = list(map(int, input_string.split()))
        minimum = min(numbers)
        messagebox.showinfo("Результат", f"Минимальное число: {minimum}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")

def task_2_lab3():
    """Задание 2: Ввод времени сна и анализ"""
    clear_window()
    tk.Label(root, text="Введите время нормального сна:", font=("Arial", 16)).pack(pady=10)

    entry_normal_sleep = tk.Entry(root)
    entry_normal_sleep.pack(pady=5)

    tk.Label(root, text="Введите максимальное время сна:", font=("Arial", 16)).pack(pady=10)

    entry_max_sleep = tk.Entry(root)
    entry_max_sleep.pack(pady=5)

    tk.Label(root, text="Введите сколько вы спите:", font=("Arial", 16)).pack(pady=10)

    entry_sleep_time = tk.Entry(root)
    entry_sleep_time.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: sleep_analysis(entry_normal_sleep.get(), entry_max_sleep.get(), entry_sleep_time.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def sleep_analysis(normal_sleep_str, max_sleep_str, sleep_time_str):
    """Анализирует время сна"""
    try:
        normal_sleep = int(normal_sleep_str)
        max_sleep = int(max_sleep_str)
        sleep_time = int(sleep_time_str)

        if normal_sleep <= max_sleep:
            if normal_sleep <= sleep_time < max_sleep:
                messagebox.showinfo("Результат", "Это нормально")
            elif sleep_time < normal_sleep:
                messagebox.showinfo("Результат", "Недосып")
            else:
                messagebox.showinfo("Результат", "Пересып")
        else:
            messagebox.showerror("Ошибка", "Такого не может быть")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")

def task_3_lab3():
    """Задание 3: Проверка на високосный год"""
    clear_window()
    tk.Label(root, text="Введите год:", font=("Arial", 16)).pack(pady=10)

    entry_year = tk.Entry(root)
    entry_year.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: check_leap_year(entry_year.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def check_leap_year(year_string):
    """Проверяет, является ли год високосным"""
    try:
        year = int(year_string)
        if year % 4 != 0:
            messagebox.showinfo("Результат", "Не високосный")
        elif year % 100 == 0:
            if year % 400 == 0:
                messagebox.showinfo("Результат", "Високосный")
            else:
                messagebox.showinfo("Результат", "Не високосный")
        else:
            messagebox.showinfo("Результат", "Високосный")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректный год.")

def task_4_lab3():
    """Задание 4: Проверка диапазона числа"""
    clear_window()
    tk.Label(root, text="Введите любое число:", font=("Arial", 16)).pack(pady=10)

    entry_number = tk.Entry(root)
    entry_number.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: check_in_range(entry_number.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def check_in_range(number_string):
    """Проверяет, попадает ли число в заданные интервалы"""
    try:
        number = int(number_string)
        if -15 < number <= 12 or 14 < number < 17 or number >= 19:
            messagebox.showinfo("Результат", "True")
        else:
            messagebox.showinfo("Результат", "False")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")

def task_5_lab3():
    """Задание 5: Проверка счастливого билета"""
    clear_window()
    tk.Label(root, text="Введите 6 значный номер билета:", font=("Arial", 16)).pack(pady=10)

    entry_ticket = tk.Entry(root)
    entry_ticket.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: check_lucky_ticket(entry_ticket.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def check_lucky_ticket(ticket_string):
    """Проверяет, является ли билет счастливым"""
    try:
        ticket_numbers = list(map(int, ticket_string))
        if len(ticket_numbers) != 6:
            raise ValueError("Номер билета должен содержать 6 цифр.")
        if sum(ticket_numbers[:3]) == sum(ticket_numbers[3:]):
            messagebox.showinfo("Результат", "Счастливый билет")
        else:
            messagebox.showinfo("Результат", "Обычный")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def task_6_lab3():
    """Задание 6: Сумма введенных чисел до нуля"""
    clear_window()
    tk.Label(root, text="Введите любое число или 0 для завершения:", font=("Arial", 16)).pack(pady=10)

    entry_number = tk.Entry(root)
    entry_number.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: sum_until_zero(entry_number.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)


def sum_until_zero(first_input):
    """Суммирует числа до тех пор, пока не введено 0"""
    total_sum = 0
    try:
        num = int(first_input)
        while num != 0:
            total_sum += num
            num = int(input('Введите любое число (0 для завершения):\n'))
        messagebox.showinfo("Результат", f"Сумма всех чисел: {total_sum}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")


def task_7_lab3():
    """Задание 7: Нахождение ближайшего общего кратного"""
    clear_window()
    tk.Label(root, text="Введите 2 числа через пробел:", font=("Arial", 16)).pack(pady=10)

    entry_numbers = tk.Entry(root)
    entry_numbers.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: find_lcm(entry_numbers.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)


def find_lcm(input_string):
    """Находит ближайшее общее кратное для двух чисел"""
    try:
        a, b = map(int, input_string.split())
        d = max(a, b)
        while d % a != 0 or d % b != 0:
            d += 1
        messagebox.showinfo("Результат", f"Ближайшее общее кратное: {d}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")


def task_8_lab3():
    """Задание 8: Ввод чисел с условиями"""
    clear_window()
    tk.Label(root, text="Введите число (для выхода больше 100):", font=("Arial", 16)).pack(pady=10)

    entry_number = tk.Entry(root)
    entry_number.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: input_numbers(entry_number))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def input_numbers(entry_widget):
    """Обрабатывает ввод чисел с условиями"""
    try:
        n = int(entry_widget.get())
        entry_widget.delete(0, tk.END)  # Очищаем поле ввода

        if n < 10:
            messagebox.showinfo("Результат", "Число меньше 10. Попробуйте снова.")
        elif n > 100:
            messagebox.showinfo("Результат", "Вы вышли из программы.")
            # Здесь можно добавить логику завершения или возврата к другим заданиям
        else:
            messagebox.showinfo("Результат", f"Вы ввели: {n}")

        entry_widget.focus()  # Устанавливаем фокус на поле ввода

    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")
        entry_widget.delete(0, tk.END)  # Очищаем поле ввода

def task_9_lab3():
    """Задание 9: Цены за конфеты"""
    clear_window()
    tk.Label(root, text="Введите цену конфет за кг:", font=("Arial", 16)).pack(pady=10)

    entry_price = tk.Entry(root)
    entry_price.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: calculate_candy_prices(entry_price.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def calculate_candy_prices(price_string):
    """Выводит цены конфет за 1-10 кг"""
    try:
        price_per_kg = float(price_string)
        prices = [price_per_kg * i for i in range(1, 11)]
        messagebox.showinfo("Результат", "\n".join(f"{i} кг: {price}" for i, price in enumerate(prices, start=1)))
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректную цену.")

def task_10_lab3():
    """Задание 10: Подсчет суммы и количества чисел"""
    global total_sum, count
    total_sum = 0
    count = 0

    clear_window()
    tk.Label(root, text="Введите целое число (0 для завершения):", font=("Arial", 16)).pack(pady=10)

    entry_number = tk.Entry(root)
    entry_number.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: count_sum(entry_number.get(), entry_number))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_3)
    back_button.pack(pady=5)

def count_sum(first_input, entry_widget):
    """Суммирует введенные числа и считает их количество"""
    global total_sum, count

    try:
        num = int(first_input)
        if num == 0:
            # Если введено 0, показываем результат и сбрасываем значения
            messagebox.showinfo("Результат", f"Сумма всех чисел: {total_sum}\nКоличество всех чисел: {count}")
            total_sum = 0
            count = 0
            entry_widget.delete(0, tk.END)  # Очищаем поле ввода
            return

        # Если число не ноль, добавляем его к сумме и увеличиваем счетчик
        total_sum += num
        count += 1

        # Очищаем поле ввода для следующего числа
        entry_widget.delete(0, tk.END)
        entry_widget.focus()  # Устанавливаем фокус на поле ввода

    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")
        entry_widget.delete(0, tk.END)  # Очищаем поле ввода

def task_1_lab4():
    """Задание 1: Ввод слов с пробелами и знаками препинания"""
    clear_window()
    tk.Label(root, text="Введите слова (с пробелами и знаками препинания):", font=("Arial", 16)).pack(pady=10)
    entry_string = tk.Entry(root, width=50)
    entry_string.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: process_string(entry_string.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_4)
    back_button.pack(pady=5)

def process_string(input_string):
    """Обрабатывает строку, выводит слова, заканчивающиеся на определённые знаки"""
    s = input_string.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split()
    new_s = []
    for i in s:
        if i[0:2] == 'ли':
            new_s.append(i)
    messagebox.showinfo("Результат", f"Слова, начинающиеся на ли: {' '.join(new_s)}")

def task_2_lab4():
    """Задание 2: Формирование таблицы студентов"""
    clear_window()
    tk.Label(root, text="Данные студентов:", font=("Arial", 16)).pack(pady=10)

    # Строка с данными
    my_string = "Ф;И;О;Возраст;Категория;_Иванов;Иван;Иванович;23 года;Студент 3 курса;_Петров;Семен;Игоревич;22 года;Студент 2 курса"

    formatted_table = PrettyTable()
    formatted_table.field_names = ["ФИО", "Информация о студенте"]

    data = my_string.split(';')

    for i in range(5, len(data), 5):
        full_name = f"{data[i][1:]} {data[i + 1]} {data[i + 2]}"
        age = data[i + 3]
        category = data[i + 4]
        student_info = f"{category}, {age}"
        formatted_table.add_row([full_name, student_info])

    # Отображение таблицы в текстовом поле
    text_box = tk.Text(root, height=15, width=70)
    text_box.pack(pady=10)
    text_box.insert(tk.END, formatted_table.get_string(border=False))
    text_box.config(state=tk.DISABLED)  # Запретить редактирование текста

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_4)
    back_button.pack(pady=5)

def task_3_lab4():
    """Задание 3: Формирование таблицы с фильтрацией"""
    clear_window()
    tk.Label(root, text="Данные студентов:", font=("Arial", 16)).pack(pady=10)

    # Строка с данными
    my_string = 'ФИО;Возраст;Категория;_Иванов Иван Иванович;23 года;Студент 3 курса;_Петров Семен Игоревич;22 года;Студент 2 курса;' \
                '_Иванов Семен Игоревич;22 года;Студент 2 курса;_Акибов Ярослав Наумович;23 года;Студент 3 курса;' \
                '_Борков Станислав Максимович;21 год;Студент 1 курса;' \
                '_Петров Семен Семенович;21 год;Студент 1 курса;' \
                '_Романов Станислав Андреевич;23 года;Студент 3 курса;' \
                '_Петров Всеволод Борисович;21 год;Студент 2 курса'

    formatted_table = PrettyTable()
    formatted_table.field_names = ['ФИО', 'Возраст', 'Курс']

    data = my_string.split(';')

    for i in range(3, len(data), 3):
        full_name = data[i][1:]
        age = data[i + 1]
        category = data[i + 2]
        formatted_table.add_row([full_name, age, category])

    # Фильтрация и отображение результата
    filtered_rows = []
    for row in formatted_table.rows:
        if row[0][0] in ['А', 'Б']:
            filtered_rows.append(f"{row[0]}, {row[1]}, {row[2]}")

    if filtered_rows:
        result_message = "\n".join(filtered_rows)
        # Отображение отфильтрованных данных в текстовом поле
        text_box = tk.Text(root, height=15, width=70)
        text_box.pack(pady=10)
        text_box.insert(tk.END, result_message)
        text_box.config(state=tk.DISABLED)  # Запретить редактирование текста
    else:
        messagebox.showinfo("Результат", "Нет студентов с фамилиями на буквы 'А' или 'Б'.")

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_4)
    back_button.pack(pady=5)

def task_4_lab4():
    """Задание 4: Подсчет символов и слов"""
    clear_window()
    tk.Label(root, text="Введите вашу строку:", font=("Arial", 16)).pack(pady=10)
    entry_string = tk.Entry(root, width=50)
    entry_string.pack(pady=5)

    submit_button = ttk.Button(root, text="Подтвердить", command=lambda: count_characters_and_words(entry_string.get()))
    submit_button.pack(pady=5)

    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_4)
    back_button.pack(pady=5)

def count_characters_and_words(input_string):
    """Считает количество символов и слов"""
    words = input_string.split()
    char_count = len(input_string) - input_string.count(' ')
    word_count = len(words)

    messagebox.showinfo("Результат", f'Количество символов = {char_count}\nКоличество слов = {word_count}')

def task_1_lab5():
    """Задание 1: Подсчитать количество файлов в указанной директории."""
    clear_window()

    # Заранее заданный путь к директории
    file_path = r'/Users/nikitaurovsky/Desktop/учеба/2 курс/языки программирования/лаба 5'
    tk.Label(root, text=f"Путь к директории: {file_path}", font=("Arial", 14)).pack(pady=10)

    def count_files():
        if os.path.isdir(file_path):
            file_count = sum(len(files) for r, d, files in os.walk(file_path))
            messagebox.showinfo("Результат", f"Количество файлов в директории: {file_count}")
        else:
            messagebox.showerror("Ошибка", "Указанная директория не найдена.")

    ttk.Button(root, text="Подсчитать файлы", command=count_files).pack(pady=5)
    ttk.Button(root, text="Назад к заданиям", command=open_lab_work_5).pack(pady=5)

def task_2_lab5():
    """Задание 2: Открыть CSV файл, обработать данные о студентах."""
    clear_window()

    # Заранее заданный путь к файлу CSV
    file_path = r"/Users/nikitaurovsky/Desktop/учеба/2 курс/языки программирования/лаба 5/students.csv"

    tk.Label(root, text=f"Путь к файлу CSV: {file_path}", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Введите группу студента:").pack(pady=5)
    entry_group = tk.Entry(root, width=20)
    entry_group.pack(pady=5)

    tk.Label(root, text="Увеличить или уменьшить возраст? (увеличить/уменьшить)").pack(pady=5)
    entry_age_change = tk.Entry(root, width=20)
    entry_age_change.pack(pady=5)

    # Текстовое поле для отображения списка студентов
    text_box = tk.Text(root, height=15, width=70)
    text_box.pack(pady=10)

    # Переменные для хранения данных
    original_students = []
    modified_students = []

    def load_students():
        nonlocal original_students  # Позволяет изменять переменную из внешней функции

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    if row[0] == '№':
                        continue
                    no = int(row[0])
                    fio = row[1]
                    age = int(row[2])
                    group = row[3]
                    original_students.append([no, fio, age, group])

            # Отображение первоначального списка студентов в текстовом поле
            update_text_box(original_students)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_text_box(students):
        """Обновляет содержимое текстового поля."""
        text_box.delete(1.0, tk.END)  # Очистка текстового поля
        for student in students:
            text_box.insert(tk.END, f"{student}\n")

    def process_students():
        nonlocal modified_students  # Позволяет изменять переменную из внешней функции
        modified_students = copy.deepcopy(original_students)  # Создаем копию оригинальных данных

        user_gr = entry_group.get()
        age_changes = entry_age_change.get().strip().lower()

        for student in modified_students:
            if student[3].lower() == user_gr.lower():
                if age_changes == "увеличить":
                    student[2] += 1
                elif age_changes == "уменьшить":
                    student[2] -= 1

        # Обновление текстового поля с новыми данными
        update_text_box(modified_students)

        # Сохранение изменений в файл
        save_changes = messagebox.askyesno("Сохранение изменений", "Хотите сохранить изменения в файл?")
        if save_changes:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['№', 'ФИО', 'Возраст', 'Группа'])
                for student in modified_students:
                    writer.writerow(student)
            messagebox.showinfo("Результат", "Изменения успешно сохранены.")
        else:
            # Если изменения не сохранены, возвращаем к оригинальному списку и обновляем текстовое поле
            update_text_box(original_students)
            messagebox.showinfo("Результат", "Изменения не сохранены.")

    load_students()  # Загружаем студентов из файла

    ttk.Button(root, text="Обработать студентов", command=process_students).pack(pady=5)
    ttk.Button(root, text="Назад к заданиям", command=open_lab_work_5).pack(pady=5)

def task_1_lab6():
    """Задание 1: Подсчитать количество ключей в словаре."""
    slovar = {
        "key1": "строка",
        "key2": True,
        "key3": 36474,
        "key4": {"nested_key": "nested_value"},
        "key5": [1, 'Привет', True],
        "key6": 47474.998,
    }

    number_of_keys = len(slovar)

    # Отображение результата в текстовом поле
    text_box = tk.Text(root, height=5, width=70)
    text_box.pack(pady=10)
    text_box.insert(tk.END, f"Количество ключей в словаре: {number_of_keys}\nСловарь:\n{slovar}")
    text_box.config(state=tk.DISABLED)  # Запретить редактирование текста

    ttk.Button(root, text="Назад к заданиям", command=open_lab_work_6).pack(pady=5)

def task_2_lab6():
    """Задание 2: Открыть CSV файл, обработать данные о студентах."""
    clear_window()

    # Заранее заданный путь к файлу CSV
    file_path = r"/Users/nikitaurovsky/Desktop/учеба/2 курс/языки программирования/лаба 6/students.csv"

    tk.Label(root, text=f"Путь к файлу CSV: {file_path}", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Введите группу студента:").pack(pady=5)
    entry_group = tk.Entry(root, width=20)
    entry_group.pack(pady=5)



    # Текстовое поле для отображения списка студентов
    text_box = tk.Text(root, height=15, width=70)
    text_box.pack(pady=10)

    # Переменные для хранения данных
    students_dict = {}

    def load_students():
        nonlocal students_dict  # Позволяет изменять переменную из внешней функции

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    if row[0] == '№':
                        continue
                    no = int(row[0])
                    fio = row[1]
                    age = int(row[2])
                    group = row[3]
                    students_dict[no] = [fio, age, group]

            # Отображение первоначального списка студентов в текстовом поле
            update_text_box(students_dict)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_text_box(students):
        """Обновляет содержимое текстового поля."""
        text_box.delete(1.0, tk.END)  # Очистка текстового поля
        for no, info in students.items():
            text_box.insert(tk.END, f"{no}: {info}\n")

    def process_students():
        nonlocal students_dict  # Позволяет изменять переменную из внешней функции
        modified_students_dict = copy.deepcopy(students_dict)  # Создаем копию оригинальных данных

        user_gr = entry_group.get()
        age_changes = "уменьшить"

        for no, info in modified_students_dict.items():
            if info[2].lower() == user_gr.lower():
                if age_changes == "уменьшить":
                    info[1] -= 1

        # Обновление текстового поля с новыми данными
        update_text_box(modified_students_dict)

        # Сохранение изменений в файл
        save_changes = messagebox.askyesno("Сохранение изменений", "Хотите сохранить изменения в файл?")
        if save_changes:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(['№', 'ФИО', 'Возраст', 'Группа'])
                    for no, info in modified_students_dict.items():
                        writer.writerow([no] + info)
                messagebox.showinfo("Результат", "Изменения успешно сохранены.")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            # Если изменения не сохранены, возвращаем к оригинальному списку и обновляем текстовое поле
            update_text_box(students_dict)
            messagebox.showinfo("Результат", "Изменения не сохранены.")

    load_students()  # Загружаем студентов из файла
    ttk.Button(root, text="Уменьшить возраст", command=process_students).pack(pady=5)
    ttk.Button(root, text="Обработать студентов", command=process_students).pack(pady=5)
    ttk.Button(root, text="Назад к заданиям", command=open_lab_work_6).pack(pady=5)

def task_1_lab7():
    spisok = [
        'No', 'ФИО', 'Возраст', 'Группа',
        '1', 'Иванов Иван Иванович', '23', 'БО-111111',
        '2', 'Петров Семен Игоревич', '27', 'БО-222222',
        '3', 'Сидоров Сидор Сидорович', '22', 'БО-222222',
        '4', 'Акибов Ярослав Наумович', '23', 'БО-444444',
        '5', 'Борков Станислав Максимович', '21', 'БО-555555',
        '6', 'Петров Семен Семенович', '21', 'БО-666666',
        '7', 'Романов Станислав Андреевич', '23', 'БО-777777',
        '8', 'Петров Всеволод Борисович', '21', 'БО-888888',
        '9', 'Сидоров Алексей Владимирович', '22', 'БО-999999',
        '10', 'Кузнецова Анна Сергеевна', '20', 'БО-101010',
        '11', 'Михайлов Сергей Николаевич', '24', 'БО-111222',
        '12', 'Федорова Екатерина Александровна', '22', 'БО-121212',
        '13', 'Семенова Мария Петровна', '23', 'БО-131313',
        '14', 'Григорьев Игорь Васильевич', '25', 'БО-141414'
    ]

    student_slov = {}
    students_spisok = []

    # Подготовка данных студентов
    for i in range(0, len(spisok), 4):
        if spisok[i] == 'No':
            continue
        no = int(spisok[i])
        fio = spisok[i + 1]
        age = int(spisok[i + 2])
        gr = spisok[i + 3]
        students_spisok.append([no, fio, age, gr])

    for student in students_spisok:
        no = student[0]
        fio = student[1]
        age = student[2]
        gr = student[3]
        student_slov[no] = [fio, age, gr]

    # Создание основного окна
    root = tk.Tk()
    root.title("Управление студентами")

    # Создание текстового поля с прокруткой
    text_frame = tk.Frame(root)
    text_frame.pack(pady=5)

    text_area = tk.Text(text_frame, wrap=tk.WORD, width=80, height=30)
    text_area.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area.config(yscrollcommand=scrollbar.set)

    def display_students():
        text_area.delete(1.0, tk.END)  # Очистка текстового поля

        for no, info in student_slov.items():
            line = f"№: {no}, ФИО: {info[0]}, Возраст: {info[1]}, Группа: {info[2]}\n"
            text_area.insert(tk.END, line)

    def task_1_lab7_inner():
        poisk = simpledialog.askstring("Выбор способа поиска",
                                       "Для обращения к определенному студенту выберите удобный способ: "
                                       "'Номер'/'ФИО'").strip().lower()

        if poisk == 'номер':
            try:
                user_no = simpledialog.askinteger("Введите номер студента", "Введите номер студента:")
                if user_no in student_slov:
                    info = student_slov[user_no]
                    commands = simpledialog.askstring(
                        "Выбор действия",
                        "Для изменения возраста введите: 'Увеличить'/'Уменьшить'\n"
                        "Для изменения ФИО студента введите: 'ФИО'\n"
                        "Для удаления записи о студенте введите: 'Удалить'\n"
                        "Для изменения группы студента введите: 'Группа'\n"
                        "Выберите одно из действий:"
                    ).strip().lower()

                    if commands == 'увеличить':
                        info[1] += 1
                    elif commands == 'уменьшить':
                        if info[1] > 0:
                            info[1] -= 1
                        else:
                            messagebox.showerror("Ошибка", "Возраст не может быть отрицательным.")
                    elif commands == 'фио':
                        new_fio = simpledialog.askstring("Введите новое ФИО", "Введите новое ФИО:")
                        info[0] = new_fio
                    elif commands == 'удалить':
                        del student_slov[user_no]
                    elif commands == 'группа':
                        new_group = simpledialog.askstring("Введите новую группу", "Введите новую группу:")
                        info[2] = new_group
                    else:
                        messagebox.showerror("Ошибка", f'Команда: {commands}, является некорректной.')
                else:
                    messagebox.showerror("Ошибка", f'Студент с номером {user_no} не найден.')

            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный ввод номера студента.")

        elif poisk == 'фио':
            user_fio = simpledialog.askstring("Введите ФИО студента", "Введите ФИО студента:").strip()

            student_found = False
            for no, info in student_slov.items():
                if info[0].lower() == user_fio.lower():
                    student_found = True

                    commands = simpledialog.askstring(
                        "Выбор действия",
                        "Для изменения возраста введите: 'Увеличить'/'Уменьшить'\n"
                        "Для изменения ФИО студента введите: 'ФИО'\n"
                        "Для удаления записи о студенте введите: 'Удалить'\n"
                        "Для изменения группы студента введите: 'Группа'\n"
                        "Выберите одно из действий:"
                    ).strip().lower()

                    if commands == 'увеличить':
                        info[1] += 1
                    elif commands == 'уменьшить':
                        if info[1] > 0:
                            info[1] -= 1
                        else:
                            messagebox.showerror("Ошибка", "Возраст не может быть отрицательным.")
                    elif commands == 'фио':
                        new_fio = simpledialog.askstring("Введите новое ФИО", "Введите новое ФИО:")
                        info[0] = new_fio
                    elif commands == 'удалить':
                        del student_slov[no]
                    elif commands == 'группа':
                        new_group = simpledialog.askstring("Введите новую группу", "Введите новую группу:")
                        info[2] = new_group
                    else:
                        messagebox.showerror("Ошибка", f'Команда: {commands}, является некорректной.')

                    break

            if not student_found:
                messagebox.showerror("Ошибка", f'Студент с ФИО "{user_fio}" не найден. Пожалуйста, попробуйте снова.')

        # Обновляем отображение студентов после изменений
        display_students()

    def perform_additional_tasks():
        nonlocal text_area

        # Сохраняем оригинальные данные студентов для выполнения дополнительных заданий
        original_students_slov = copy.deepcopy(student_slov)

        # Задание 1: Уменьшение возраста студентов старше 22 лет на 1.
        f_students_slov = copy.deepcopy(original_students_slov)

        text_area.insert(tk.END, '\nЕсли возраст студента больше 22 уменьшаем его на 1\n')

        for no, info in f_students_slov.items():
            if info[1] > 22:
                info[1] -= 1

        text_area.insert(tk.END, f'Словарь где у студентов старше 22 убавляется возраст на 1:\n{f_students_slov}\n')

        # Задание 2: Удаление студентов с возрастом 23.
        g_students_slov = copy.deepcopy(f_students_slov)

        text_area.insert(tk.END, '\nЕсли возраст студента равен 23, удаляем его из списка\n')

        keys_to_delete = []

        for no, info in g_students_slov.items():
            if info[1] == 23:
                keys_to_delete.append(no)

        for key in keys_to_delete:
            del g_students_slov[key]

        text_area.insert(tk.END,
                         f'Обновленный словарь из студентов после удаления студентов с возрастом 23:\n{g_students_slov}\n')

        # Задание 3: Увеличение возраста студентов с фамилией «Иванов» на 1.
        h_students_slov = copy.deepcopy(g_students_slov)

        text_area.insert(tk.END, '\nУ всех студентов с фамилией «Иванов» увеличиваем возраст на 1\n')

        for no, info in h_students_slov.items():
            if "Иванов" in info[0]:
                info[1] += 1

        text_area.insert(tk.END,
                         f'Словарь где у студентов с фамилией Иванов возраст увеличен на 1:\n{h_students_slov}\n')

        # Задание 4: Замена фамилии «Иванов» на «Сидоров».
        i_students_slov = copy.deepcopy(h_students_slov)

        text_area.insert(tk.END, '\nУ студентов с фамилией «Иванов» изменить фамилию на «Сидоров».\n')

        for no, info in i_students_slov.items():
            if "Иванов" in info[0]:
                info[0] = info[0].replace('Иванов', 'Сидоров')

        text_area.insert(tk.END, f'Словарь с замененными фамилиями:\n{i_students_slov}\n')

        # Задание 5: Поменять «ФИО» и «Группа» местами.
        j_students_slov = copy.deepcopy(i_students_slov)

        text_area.insert(tk.END, '\nПоменять «ФИО» и «Группа» местами.\n')

        for no, info in j_students_slov.items():
            info[0], info[2] = info[2], info[0]

        text_area.insert(tk.END, f'Обновленный словарь:\n{j_students_slov}\n')

        # Дополнительные задания...
        ff_students_slov = copy.deepcopy(
            original_students_slov)  # Используем оригинальный словарь для дополнительных заданий

        grypa = 'БО-111111'
        text_area.insert(tk.END, '\nИнформация о студентах чья группа БО-111111\n')
        for no, info in ff_students_slov.items():
            if info[2].lower() == grypa.lower():
                text_area.insert(tk.END, f'№: {no}, ФИО: {info[0]}, Возраст: {info[1]}, Группа: {info[2]}\n')

        text_area.insert(tk.END, '\nИнформация о студентах чья фамилия Иванов\n')
        for no, info in ff_students_slov.items():
            if 'Иванов' in info[0]:
                text_area.insert(tk.END, f'№: {no}, ФИО: {info[0]}, Возраст: {info[1]}, Группа: {info[2]}\n')

        text_area.insert(tk.END, '\nИнформация о студентах чья фамилия заканчивается на букву "а":\n')
        for no, info in ff_students_slov.items():
            surname = info[0].split()[0]
            if surname.endswith('а'):
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \n')

        text_area.insert(tk.END, '\nИнформация о студентах чей возраст является четным числом\n')
        for no, info in ff_students_slov.items():
            if info[1] % 2 == 0:
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \н')

        text_area.insert(tk.END, '\nИнформация о студентах если в их возрасте встречается цифра 5\n')
        for no, info in ff_students_slov.items():
            age_str = str(info[1])
            if '5' in age_str:
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \n')

        text_area.insert(tk.END, '\nИнформация о студентах если их группа длиннее 7 символов\n')
        for no, info in ff_students_slov.items():
            if len(info[2]) > 7:
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \n')

        text_area.insert(tk.END, '\nИнформация о студентах если их номер является четным числом\n')
        for no, info in ff_students_slov.items():
            if no % 2 == 0:
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \n')

        text_area.insert(tk.END, '\nИнформация о студентах если номер их группы заканчивается на 1\n')
        for no, info in ff_students_slov.items():
            if info[2].endswith('1'):
                text_area.insert(tk.END, f'№:{no}, ФИО:{info[0]}, Возраст:{info[1]}, Группа:{info[2]} \n')

    search_button_main_part = ttk.Button(root, text="Поиск студента", command=task_1_lab7_inner)
    search_button_main_part.pack(pady=5)

    search_button_additional_tasks = ttk.Button(root, text="Выполнить дополнительные задания",
                                                command=perform_additional_tasks)
    search_button_additional_tasks.pack(pady=5)

    ttk.Button(root, text="Назад к заданиям", command=open_lab_work_7).pack(pady=5)

    display_students()  # Отображаем студентов при запуске приложения

def task_1_lab8():
    """Задание 1: Выполнение всех заданий лабораторной работы 8."""
    clear_window()

    # Исходная матрица
    matrix = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2],
        [1, 3, 5, 7, 9, 7, 5, 3],
        [3, 1, 5, 3, 2, 6, 5, 7],
        [1, 7 ,5 ,9 ,7 ,3 ,1 ,5],
        [2 ,6 ,3 ,5 ,1 ,7 ,3 ,2]
    ])

    # Функция для суммирования четных чисел по столбцам
    def summa(matrix):
        counter = np.zeros(matrix.shape[1])
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i][j] % 2 == 0:
                    counter[j] += matrix[i][j]
        return counter

    # Выполнение всех заданий
    results = []

    # Задание 1: Возведение в квадрат первых четырех строк
    double_matrix = matrix.copy()
    for i in range(min(4, matrix.shape[0])):
        double_matrix[i] = double_matrix[i] ** 2
    results.append("Результат задания 1 (возведенные в квадрат первые четыре строки):\n" + str(double_matrix))

    # Задание 2: Суммирование четных чисел по столбцам
    summa_matrix = summa(matrix)
    summa_matrix_reshaped = summa_matrix.reshape(1,-1)
    results.append("\nРезультат задания 2 (сумма четных чисел по столбцам):\n" + str(summa_matrix_reshaped))

    # Задание 3: Суммирование четных чисел по строкам
    summa_rows_matrix = np.sum(np.where(matrix % 2 == 0, matrix, np.zeros_like(matrix)), axis=1)
    results.append("\nРезультат задания 3 (сумма четных чисел по строкам):\n" + str(summa_rows_matrix))

    # Задание 4: Замена всех элементов матрицы на нули
    zeros_matrix = np.zeros_like(matrix)
    results.append("\nРезультат задания 4 (матрица из нулей):\n" + str(zeros_matrix))

    # Задание 5: Удаление последних четырех строк матрицы
    delit_matrix = matrix[:-4] if matrix.shape[0] > 4 else matrix
    results.append("\nРезультат задания 5 (матрица без последних четырех строк):\n" + str(delit_matrix))

    # Задание 6: Замена первого и последнего элемента каждой строки местами
    replaced_matrix = matrix.copy()
    for row in replaced_matrix:
        row[0], row[-1] = row[-1], row[0]
    results.append("\nРезультат задания 6 (замена первого и последнего элемента каждой строки):\n" + str(replaced_matrix))

    # Отображение результатов в текстовом поле
    text_box = tk.Text(root, height=40, width=80)
    text_box.pack(pady=10)
    text_box.insert(tk.END, "\n".join(results))
    text_box.config(state=tk.DISABLED)

    # Кнопка "Назад", которая возвращает к окну лабораторной работы
    back_button = ttk.Button(root,text="Назад",command=open_lab_work_8)
    back_button.pack(pady=5)

def task_2_lab8():
    """Задание 2: Суммирование элементов в указанной строке матрицы."""
    clear_window()  # Очищаем текущее окно

    # Исходная матрица
    matrix = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2],
        [1, 3, 5, 7, 9, 7, 5, 3],
        [3, 1, 5, 3, 2, 6, 5, 7],
        [1, 7, 5, 9, 7, 3, 1, 5],
        [2, 6, 3, 5, 1, 7, 3, 2]
    ])

    # Отображение матрицы в текстовом поле
    matrix_text = tk.Text(root, height=10, width=50)
    matrix_text.pack(pady=10)

    # Форматирование и вставка матрицы
    matrix_text.insert(tk.END, "Исходная матрица:\n")
    for row in matrix:
        matrix_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

    matrix_text.config(state=tk.DISABLED)  # Запретить редактирование текста

    # Ввод номера строки от пользователя
    tk.Label(root, text="Введите номер строки от 1 до {}:".format(matrix.shape[0]), font=("Arial", 14)).pack(pady=10)
    entry_row = tk.Entry(root)
    entry_row.pack(pady=5)

    def summ_elements(matrix, row_number):
        """Суммирует элементы в указанной строке матрицы."""
        counter = 0
        if 1 <= row_number <= matrix.shape[0]:
            row_number -= 1
            counter = np.sum(matrix[row_number])
        else:
            messagebox.showerror("Ошибка", "Номер строки должен быть от {} до {}".format(1, matrix.shape[0]))
            return None
        return counter

    def calculate_sum():
        """Обрабатывает ввод и выводит сумму элементов указанной строки."""
        try:
            row_number = int(entry_row.get())
            summa = summ_elements(matrix, row_number)
            if summa is not None:
                messagebox.showinfo("Результат", f"Сумма элементов в строке {row_number}: {summa}")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста введите корректный номер строки.")

    submit_button = ttk.Button(root, text="Подсчитать сумму", command=calculate_sum)
    submit_button.pack(pady=5)

    # Кнопка "Назад" для возврата к списку лабораторных работ
    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_8)
    back_button.pack(pady=5)

def task_3_lab8():
    """Задание 3: Замена элемента в матрице."""
    clear_window()  # Очищаем текущее окно

    # Исходная матрица
    matrix = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2],
        [1, 3, 5, 7, 9, 7, 5, 3],
        [3, 1, 5, 3, 2, 6, 5, 7],
        [1, 7, 5, 9, 7, 3, 1, 5],
        [2, 6, 3, 5, 1, 7, 3, 2]
    ])

    # Отображение матрицы в текстовом поле
    matrix_text = tk.Text(root, height=10, width=50)
    matrix_text.pack(pady=10)

    # Форматирование и вставка матрицы
    matrix_text.insert(tk.END, "Исходная матрица:\n")
    for row in matrix:
        matrix_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

    matrix_text.config(state=tk.DISABLED)  # Запретить редактирование текста

    # Ввод номера строки и столбца от пользователя
    tk.Label(root, text="Введите номер строки от 1 до {}:".format(matrix.shape[0]), font=("Arial", 14)).pack(pady=10)
    entry_row = tk.Entry(root)
    entry_row.pack(pady=5)

    tk.Label(root, text="Введите номер столбца от 1 до {}:".format(matrix.shape[1]), font=("Arial", 14)).pack(pady=10)
    entry_column = tk.Entry(root)
    entry_column.pack(pady=5)

    tk.Label(root, text="Введите новое значение:", font=("Arial", 14)).pack(pady=10)
    entry_value = tk.Entry(root)
    entry_value.pack(pady=5)

    def replacing(matrix, row_number, col_number, new_value):
        """Заменяет элемент в указанной строке и столбце на новое значение."""
        counter = matrix.copy()
        if (1 <= row_number <= counter.shape[0]) and (1 <= col_number <= counter.shape[1]):
            counter[row_number - 1][col_number - 1] = new_value
        else:
            messagebox.showerror("Ошибка",
                                 "Неверный номер строки или столбца. Значения должны быть от {} до {}.".format(1,
                                                                                                               matrix.shape[
                                                                                                                   0]))
            return None
        return counter

    def update_matrix():
        """Обновляет матрицу на основе ввода пользователя."""
        try:
            row_number = int(entry_row.get())
            col_number = int(entry_column.get())
            new_value = int(entry_value.get())
            updated_matrix = replacing(matrix.copy(), row_number, col_number, new_value)

            if updated_matrix is not None:
                # Отображение обновленной матрицы
                matrix_text.config(state=tk.NORMAL)  # Разрешить редактирование
                matrix_text.delete(1.0, tk.END)  # Очистить текстовое поле
                matrix_text.insert(tk.END, "Обновленная матрица:\n")
                for row in updated_matrix:
                    matrix_text.insert(tk.END, ' '.join(map(str, row)) + '\n')
                matrix_text.config(state=tk.DISABLED)  # Запретить редактирование текста

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста введите корректные числа.")

    submit_button = ttk.Button(root, text="Обновить элемент", command=update_matrix)
    submit_button.pack(pady=5)

    # Кнопка "Назад" для возврата к списку лабораторных работ
    back_button = ttk.Button(root, text="Назад к заданиям", command=open_lab_work_8)
    back_button.pack(pady=5)

# Основное окно приложения
root = tk.Tk()
root.title("Лабораторные работы")
root.geometry("600x600")

# Запуск основного меню
main_menu()
root.mainloop()