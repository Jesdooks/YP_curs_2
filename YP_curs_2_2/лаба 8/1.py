num = list(map(int, input().split()))
i = int(input())
matrix = []
matrix += [num]
'''print(matrix)'''
for j in range(i):
    matrix += [num]
print(matrix)