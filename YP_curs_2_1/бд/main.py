import sqlite3

#соединение с бд
connect = sqlite3.connect('laba_1.db')

#курсор чтобы делать запросы и получать ответы
cursor = connect.cursor()


#ЗАДАНИЕ 1: ВЫВЕСТИ ВСЕ СТРАНЫ НАЧИНАЮЩИЕСЯ НА А

cursor.execute("SELECT Название_Страны FROM Страна")

value = cursor.fetchall()

#x[0] - fetchall() возв список кортеж, обращ к первому элементу кортежа
spis_stran_A = [x[0] for x in value if x[0][0] == 'А']
print('\n'.join(spis_stran_A))


#ЗАДАНИЕ 2: ВЫВЕСТИ ВСЕ УЛИЦЫ ВСТРЕЧАЮЩИЕСЯ БОЛЕЕ ЧЕМ В ПЯТИ ГОРОДАХ

cursor.execute("SELECT Название_Улицы FROM Улица")

value_1 = cursor.fetchall()

spis_street_5 = set(x[0] for x in value_1 if value_1.count(x) > 5)
print('\n'.join(spis_street_5))


#ЗАДАНИЕ 3: ВЫВЕСТИ ВСЕ УЛИЦЫ РФ

cursor.execute("SELECT * FROM Улица")

value_2 = cursor.fetchall()

#кортеж (id, наз_ул, id_город, id_страны)
spis_street_Russia = set(x[1] for x in value_2 if x[3] == 15)
print('\n'.join(spis_street_Russia))


connect.close()


'''
CREAT - создание чего либо
INSERT INTO ... VALUES - дабавление в табл
SELECT - выборка данных

.fetchall() - получение всех записей список из кортежей
.fetchmany() - позволяет выбрать определённое кол-во зааписей список из кортежей
.fetchone() - выбирает отду запись кортеж
'''

'''
cursor.execute("SELECT Название_Страны FROM Страна WHERE Название_Страны LIKE 'А%'")
spis_stran_A = [x[0] for x in cursor.fetchall()]
print('\n'.join(spis_stran_A))

# Задание 2
cursor.execute("""
SELECT Название_Улицы 
FROM Улица 
GROUP BY Название_Улицы 
HAVING COUNT(*) > 5
""")
spis_street_5 = [x[0] for x in cursor.fetchall()]
print('\n'.join(spis_street_5))

# Задание 3
cursor.execute("SELECT Название_Улицы FROM Улица WHERE id_страны = 15")
spis_street_Russia = [x[0] for x in cursor.fetchall()]
print('\n'.join(spis_street_Russia))'''