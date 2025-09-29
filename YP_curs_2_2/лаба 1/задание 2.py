#вариант 2

import math
a = int(input())
b = int(input())
c = int(input())
d = int(input())
k = int(input())


if b != 0 and a != 0:
    s = abs(((a**2 - b**3 - c**3 * a**2) * (b-c+c*(k-d/b**3)) - (k/b - k/a)*c)**2 - 20000)
    print(s)
else:
    print('Проверь чему равно значение b и a')