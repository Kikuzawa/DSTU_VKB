import time
from Proverka import *
def z1():

    def bubble_sort(mass):
        for i in range(len(mass) - 1):
            for j in range(len(mass) - i - 1):
                if mass[j] > mass[j + 1]:
                    swap = mass[j]
                    mass[j] = mass[j + 1]
                    mass[j + 1] = swap

    def vibor_sort(mass):
        for i in range(0, len(mass) - 1):
            min = i
            for j in range(i + 1, len(mass)):
                if mass[j] < mass[min]:
                    min = j
            mass[i], mass[min] = mass[min], mass[i]

    def vstav_sort(mass):
        for i in range(1, len(mass)):
            temp = mass[i]
            j = i - 1
            while (j >= 0 and temp < mass[j]):
                mass[j + 1] = mass[j]
                j = j - 1
            mass[j + 1] = temp

    print('==========================\n| Лабораторная работа №1 |\n==========================\n\nВведите длину массива:')
    n = prov_Z()
    mass = []

    for i in range(n):
        print('Введите элемент массива:')
        digit = prov_Z()
        mass.append(digit)

    print('Неотсортированный список: ', mass)
    B = Vi = Vs = mass

    print('-----Пузырьковый метод-----')
    start_time = time.time()
    bubble_sort(B)
    print('Отсортирован: ', B)
    print('Time: ', time.time() - start_time)

    print('-----Сортировка Выборкой-----')
    start_time = time.time()
    bubble_sort(Vi)
    print('Отсортирован: ', Vi)
    print('Time: ', time.time() - start_time)

    print('-----Сортировка Вставкой-----')
    start_time = time.time()
    bubble_sort(Vs)
    print('Отсортирован: ', Vs)
    print('Time: ', time.time() - start_time)
    return ('=====================\n    КОНЕЦ ЗАДАНИЯ    \n=====================')