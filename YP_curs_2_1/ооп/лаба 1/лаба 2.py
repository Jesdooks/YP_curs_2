class Train:
    def __init__(self, name_punkta, number_train, time_out):
        self.name_punkta = name_punkta
        self.number_train = number_train
        self.time_out = time_out

def ввод_данных_поезд(kol_vo):
    trains = []
    for i in range(kol_vo):
        name_punkta = input('Введите пункт назначения: ')

        while True:
            try:
                number_train = int(input('Введите номер поезда: '))
                break
            except ValueError:
                print("Ошибка: введите номер поезда (число).")

        time_out = input('Введите время отправления: ')
        trains.append(Train(name_punkta, number_train, time_out)) #экз

    for i in trains:
        print(f"Пункт назначения: {i.name_punkta}, Номер поезда: {i.number_train}, Время отправления: {i.time_out}")

    return trains

def сортировка_по_номеру_поезда(trains):
    train_sorted = sorted(trains, key=lambda x: x.number_train)
    for i in train_sorted:
        print(f"Пункт назначения: {i.name_punkta}, Номер поезда: {i.number_train}, Время отправления: {i.time_out}")


def вывод_инф_о_поезде(trains):
    namber_user = int(input('Введите номер поезда (число): '))
    flag = False
    for i in trains:
        if i.number_train == namber_user:
            print(f"Пункт назначения: {i.name_punkta}, Номер поезда: {i.number_train}, Время отправления: {i.time_out}")
            flag = True
            break
    if flag == False:
        print('Поезд с таким номером не найден')


def сортировка_по_пункту(trains):
    train_sorted = sorted(trains, key=lambda x: (x.name_punkta, x.time_out))
    for i in train_sorted:
        print(f"Пункт назначения: {i.name_punkta}, Номер поезда: {i.number_train}, Время отправления: {i.time_out}")

if __name__ == "__main__":
    trains = ввод_данных_поезд(3)  # Получаем список поездов
    вывод_инф_о_поезде(trains)
    print('\n')
    сортировка_по_пункту(trains)

'''
Москва - Санкт-Петербург
123
10:00

Казань - Нижний Новгород
456
14:30

Екатеринбург - Челябинск
789
18:15
'''


