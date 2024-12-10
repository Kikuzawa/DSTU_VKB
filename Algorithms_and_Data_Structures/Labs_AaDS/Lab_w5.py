import heapq
from Proverka import *
def z1():
    print('==========================\n| Лабораторная работа №5 |\n==========================\nВыберите метод сортировки: свойства кучи или модуль Heapq. [1/2]:')
    w = prov_n()
    if w == 1:
        sposob_1()
    else: sposob_2()
    return ('=====================\n    КОНЕЦ ЗАДАНИЯ    \n=====================')

def print_heap(arr):
    ml = max(len(str(x)) for x in arr)
    mass = [('{:0' + str(ml) + '}').format(x) for x in arr]
    dp = len(bin(len(arr))) - 1
    print('---Двоичная куча в виде дерева---')
    for i in range(1, dp + 1):
        str_space = ' ' * max(0, 2 ** (dp - i - 2) * (ml + 1) - 1 - ml // 2)
        sep_space = ' ' * max(0, 2 ** (dp - i - 1) * (ml + 1) - ml)
        print(str_space + sep_space.join(mass[2 ** (i - 1) - 1: 2 ** i - 1]))

def sposob_1():
    def heap_build(arr, n, i, k): #преобразование в двоичную кучу поддерева с корневым узлом i - индекса массива arr, n - размер двоичной кучи
        D = i
        left_v = 2 * i + 1
        right_v = 2 * i + 2

        if k == 'max':
            if left_v < n and arr[i] < arr[left_v]:
                D = left_v

            if right_v < n and arr[D] < arr[right_v]:
                D = right_v

            if D != i:
                arr[i], arr[D] = arr[D], arr[i]
                heap_build(arr, n, D, k)
        else:
            if left_v < n and arr[i] > arr[left_v]:
                D = left_v

            if right_v < n and arr[D] > arr[right_v]:
                D = right_v

            if D != i:  # замена корня
                arr[i], arr[D] = arr[D], arr[i]
                heap_build(arr, n, D, k)  # строим следующие поддеревья (ветви)

    def heap_sort(arr, k): #сортировка массива для кучи
        n = len(arr)
        for i in range(n, -1, -1):
            heap_build(arr, n, i, k)

    print('Введите последовательность чисел для кучи:')
    arr = prov_pos()

    n = len(arr)
    print('Изначальный массив:', arr)

    arr1 = arr.copy()
    arr2 = arr.copy()

    heap_sort(arr1, k='max')
    print("Отсортированный массив для max heap", arr1)
    print_heap(arr1)

    heap_sort(arr2, k='min')
    print("Отсортированный массив для min heap", arr2)
    print_heap(arr2)

    print('=== После удаления корня -', arr1[0],'- куча Max ===')
    arr1.pop(0)
    heap_sort(arr1, k='max')
    print("Отсортированный массив для max heap", arr1)
    print_heap(arr1)

    print('=== После удаления корня -', arr2[0],'- куча Min ===')
    arr2.pop(0)
    heap_sort(arr2, k='min')
    print("Отсортированный массив для min heap", arr2)
    print_heap(arr2)

def sposob_2():

    print('Введите последовательность чисел для кучи:')
    arr = prov_pos()
    heap = []
    for i in arr:
        heapq.heappush(heap, i)
    print('Массив:', heap)
    print_heap(heap)

    print('Куча с удалением корня:', heap[0])
    heapq.heappop(heap)
    print('Массив:', heap)
    print_heap(heap)