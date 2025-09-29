'''Пусть дана некоторая директория (папка). Посчитайте количество файлов
в данной директории (папке) и выведите на экран. '''
import os

dir_path = r'/Users/nikitaurovsky/Desktop/учеба/языки программирования/лаба 5' #метод r открытие файла для чтения
files = []

for f in os.listdir(dir_path): #эл (поддиректорий и файлов) в моей папке
    if os.path.isfile(os.path.join(dir_path, f)): #Установления факта существования файла и находится ли этот файл в директории
        files.append(f)

print(f"Кол-во файлов: {len(files)}")

for f in files:
    print(f'- {f}')
