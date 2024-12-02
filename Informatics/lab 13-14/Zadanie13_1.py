print('==Введите ненулевые значения a, b==')
a = float(input('Введите значение числа a: '))
b = float(input('Введите значение числа b: '))
if a != 0 and b != 0:
    print('a =', a)
    print('b =', b)
    print('|a| + |b| =', abs(a) + abs(b))
    print('|a| - |b| =', abs(a) - abs(b))
    print('|b| - |a| =', abs(b) - abs(a))
    print('|a| * |b| =', abs(a) * abs(b))
    print('|a| / |b| = {0:.2f}'.format(abs(a) / abs(b)))
    print('|b| / |a| = {0:.2f}'.format(abs(b) / abs(a)))
else: print('==Только ненулевые значения!==')

