#Пусть задан список, содержащий строки
#Выведите построчно все строки размером менее 10 символов
#f ff fff ffffffffff
a = input().split()
for i in range(len(a)):
    if len(a[i]) < 10:
        print(a[i])