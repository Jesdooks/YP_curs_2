import re


def task1(string):
    regex = re.compile('^abcdefghijklmnopqrstuv18340$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task2(string):
    regex = re.compile(r'^[{]?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}[}]?$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task3(string):
    regex = re.compile(r'^[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task4(string):
    regex = re.compile(r'^(http://|https://)?'
                       r'([a-zA-Z0-9-]{2}\.)+'  # Поддомены
                       r'[a-zA-Z]{2,}'  # Домен 
                       r'(:[0-9]+)?'  # Порт
                       r'([a-zA-Z0-9-._~:/?#@$&\'()*+,;%=]*)?'  # Путь, параметры, якорь (опционально)
                       r'$')

    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task5(string):
    regex = re.compile(r'^#[A-Fa-f\d]{6}$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


#Переделать
def task6(string):
    pattern = r"""
    ^                                  # Начало строки
    (?:                                # Группа для всех вариантов дат
        (0[1-9]|[12]\d|3[01])          # День: 01–31
        /                             
        (0[13578]|1[02])               # Месяцы с 31 днем: 01, 03, 05, 07, 08, 10, 12
        /                              
        (1[6-9]|[2-9]\d)\d{2}          # Год: 1600–9999
    |                             
        (0[1-9]|[12]\d|30)             # День: 01–30
        /                             
        (0[469]|11)                    # Месяцы с 30 днями: 04, 06, 09, 11
        /                             
        (1[6-9]|[2-9]\d)\d{2}          # Год: 1600–9999
    |                              
        (0[1-9]|1\d|2[0-8])            # День: 01–28
        /                            
        02                             # Февраль
        /                           
        (1[6-9]|[2-9]\d)\d{2}          # Год: 1600–9999
    |                               
        29                             # День: 29
        /                             
        02                             # Февраль
        /                         
        (?:                            # Группа для високосных лет
            (?:                        # Годы, которые делятся на 4, но не на 100
                (1[6-9]|[2-9]\d)(?:0[48]|[2468][048]|[13579][26])
            |                          # Годы, которые делятся на 400
                (16|[2468][048]|[3579][26])00
            )
        )
    )
    $                                  # Конец строки
"""
    result = re.match(pattern, string, re.VERBOSE)

    if result:
        print(True)
    else:
        print(False)
#29/02/2000, 30/04/2003, 01/01/2003
#29/02/2001, 30-04-2003, 1/1/1899
task6('29/02/2023')


def task7(string):
    regex = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z\d]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})?$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task8(string):
    regex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)



def task9(string):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d_]{8,}$') #есть ли хотя бы один символ впереди.
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)


def task10(string):
    regex = re.compile(r'^[1-9]{1}[0-9]{5}$')
    result = re.match(regex, string)

    if result:
        print(True)
    else:
        print(False)

#скатать у Егора
def task11(user_text):

    regex = re.compile('[1-9][0-9].[0-9][0-9]|[0].[0-9][0-9] USD|RUR|EU')

    if re.match(regex, user_text):
        print(True)
    else:
        print(False)


#скатать у Егора
def task12(string):
    regex = re.compile(r'\d(?=\s\+)')
    result = re.search(regex, string)

    if result:
        print(True)
    else:
        print(False)

##Переделать количество открытых и закрытых скобок должно быть одинаково
#группирует элементы, но не создает отдельную группу для захвата
#(3 + 5) – 9 × 4
#((3 + 5) – 9 × 4
def task13(user_text):
    regex = re.compile(r'[^()]*\((?:[^()]*|\([^()]*\))*\)[^()]*')
    if re.match(regex, user_text):
        return True
    else:
        return False

