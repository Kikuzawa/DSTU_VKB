A, B, C = map(int, input('Введите целые значения к числам A,B,C (через проблел):').split())
print('A =', A,'\nB =', B,'\nC =', C)
result = ''
if (A > B > C) or (A < B < C):
    result = 'ИСТИНА'
else:
    result = 'ЛОЖЬ'
print('Число B находится между числами A и C? -', result)