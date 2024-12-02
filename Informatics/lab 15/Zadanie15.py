#1 способ
s = str(input('Введите строку: '))
k = 1
for i in s:
    if i == '.':
        break
    elif i == ' ':
        k += 1
print('Количество слов:', k)

#2 способ
s = str(input('Введите строку: '))
s = s.split()
print('Количество слов:', len(s))
print(s)