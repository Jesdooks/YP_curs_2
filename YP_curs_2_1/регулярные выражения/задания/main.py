'''
^ - нач ст
% - кон ст
'''


import re

#основаня строка
str1 = "abcdefghijklmnopqrstuv18340"

#примеры
str2 = "abcdefghijklmnoasdfasdpqrstuv18340"
str3 = "abcdefghijklmnopqrstuv18340abc"

шаблон = r"^abcdefghijklmnopqrstuv18340$"

#возвращает объект совпадения, если строка соответствует шаблону в начале
совпадение1 = re.match(шаблон, str1)
совпадение2 = re.match(шаблон, str2)
совпадение3 = re.match(шаблон, str3)

print(f"Строка '{str1}' является 'abcdefghijklmnopqrstuv18340': {bool(совпадение1)}")
print(f"Строка '{str2}' является 'abcdefghijklmnopqrstuv18340': {bool(совпадение2)}")
print(f"Строка '{str3}' является 'abcdefghijklmnopqrstuv18340': {bool(совпадение3)}")
