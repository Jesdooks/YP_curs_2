#Пусть задано некоторое число my_number. Пользователь вводит с клавиатуры свое число user_number.
#Запрашивайте у пользователя вводить число user_number до тех пор, пока оно не будет равно my_number.
user_number = int(input('Введите число: '))
my_number = 3
while user_number != my_number:
    user_number = int(input('Введите число: '))
print('Вы молодец, ввели число равное числу программы!')