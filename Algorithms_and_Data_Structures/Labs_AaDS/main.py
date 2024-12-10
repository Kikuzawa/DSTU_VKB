import Lab_w1
import Lab_w2
import Lab_w3
import Lab_w4
import Lab_w5
from Proverka import *

def lab(n, z):
    if n == 1:
        if z == 1:
            return Lab_w1.z1()
        else: return ('Задача не найдена!')
    elif n == 2:
        if z == 1:
            return Lab_w2.z1()
        elif z == 2:
            return Lab_w2.z2()
        elif z == 3:
            return Lab_w2.z3()
        else:
            return ('Задача не найдена!')
    elif n == 3:
        if z == 2:
            return Lab_w3.z2()
        elif z == 3:
            return Lab_w3.z3()
        else:
            return ('Задача не найдена!')
    elif n == 4:
        if z == 1:
            return Lab_w4.z1()
        elif z == 2:
            return Lab_w4.z2()
        else:
            return ('Задача не найдена!')
    elif n == 5:
        if z == 1:
            return Lab_w5.z1()
        else:
            return ('Задача не найдена!')
    else:
        return ('Не существует такой лабораторной работы')

print('------------Для завершения программы введите 0------------')
num = -1
while num != 0:
    print('Введите номер лабораторной работы [1-5]:')
    num = prov_Z()
    if num != 0:
        print('Введите номер задания [Натуральное число, начиная с 1]:')
        zadanie = prov_Z()
        k = lab(num,zadanie)
        print(k)
    else: break

print('Конец программы')


