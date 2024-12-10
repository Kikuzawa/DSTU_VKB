from Proverka import *
import math
def z1():
    def dfs_paths(graph, start, end):
        stack = [(start, [start])]  # (вершина, путь от него) # vertex - вершина
        while stack:
            (vertex, path) = stack.pop()
            for next in set(graph[vertex]) - set(path): #set - позволяет работать со множеством строк, вычитаются из графа все посещенные вершины из path
                if next == end:
                    yield path + [next] # yield - как return, но возвращает генератор различных путей, используется в итерации - подобие рекурсии, но не вызывает самого себя, Использование генератора позволяет пользователю вычислять только желаемое количество альтернативных путей.
                else:
                    stack.append((next, path + [next]))

    ##### Создание матрицы смежности #####
    print('==========================\n| Лабораторная работа №4 |\n==========================\nВведите количество вершин графа:')
    a = prov_z1()
    mass = [[0] * a for i in range(a)]
    alf = ''
    for i in range(a):
        alf += str(i + 1) + '  ' # необходим для визуализации матрицы смежности, для лучшего восприятия
    for i in range(len(mass)):  # задание матрицы смежности, где y - да, n - нет, регистр важен!
        for j in range(len(mass)):
            if i != j and i < j:
                print('Есть связь между вершиной ', i + 1, 'и', j + 1, '[y/n]? - ')
                res = str(prov_str())
                if res == 'y':
                    mass[i][j] = 1
                    mass[j][i] = 1
    print('===========================')
    print('     МАТРИЦА СМЕЖНОСТИ     ')
    print('  ', alf)
    for k in range(len(mass)):  # вывод матрицы смежности на экран, для визуального восприятия
        print(k + 1, mass[k])
    ##### Создание Графа #####
    adj_list = [[j + 1 for j in range(len(mass[i])) if mass[i][j] != 0] for i in range(len(mass))] #словарь смежности, хранит в себе вершины, являющиеся соседями опред. вершины
    graph = {}
    print('===========================')
    print('     ГРАФ     ')
    for i in range(a):
        graph[i + 1] = adj_list[i]
        print(i + 1, ':', graph[i + 1])
    print('===========================')
    ##### Задание начальной и конечной вершины в графе #####
    print('Введите номер начальной вершины:')
    start = prov_versh(a)
    print('Введите номер конечной вершины:')
    end = prov_versh(a)
    print('===========================')
    print('     ПУТИ     ')
    list_paths = list(dfs_paths(graph, start, end)) #создание списка, в каждом элементе которого будет хранится список вершин определенного пути
    for i in range(len(list_paths)):
        print('Длина:', len(list_paths[i]) - 1, '<=> ПУТЬ:', list_paths[i])
    return ('=====================\n    КОНЕЦ ЗАДАНИЯ    \n=====================')

def z2():
    def arg_min(Tabl, visited): #выбирает следующие узлы с наименьшим весом
        minimum = -1
        maximum = math.inf  # максимальное значение
        for i, t in enumerate(Tabl): #enumerate - счетчик, который возвращает кортеж, содержащий пары ('счётчик', 'элемент') для элементов последовательности.
            if t < maximum and i not in visited:
                maximum = t
                minimum = i

        return minimum

    print('==========================\n| Лабораторная работа №4 |\n==========================\nВведите количество вершин графа:')
    a = prov_z1()
    mass = [[0] * a for i in range(a)]
    matrix = [[0] * a for i in range(a)]
    alf_versh = ''

    for i in range(a):
        alf_versh += str(i + 1) + '    '
    for i in range(len(matrix)):  # задание матрицы смежности
        for j in range(len(matrix)):
            if i != j and i < j:
                print('Введите расстояние между вершинами:', i + 1, 'и', j + 1, 'Если пути между этими вершинами нет, то введите 0')
                res = prov_Z()
                if res == '0':
                    matrix[i][j] = '*'
                    matrix[j][i] = '*'
                    mass[i][j] = math.inf
                    mass[j][i] = math.inf
                else:
                    matrix[i][j] = res
                    matrix[j][i] = res
                    mass[i][j] = float(res)
                    mass[j][i] = float(res)
            if i == j:
                matrix[i][j] = '0'
                mass[j][i] = 0
    print('======================================')
    print('     МАТРИЦА ВЗВЕШАННОГО ГРАФА     ')
    print('   ', alf_versh)
    for k in range(len(matrix)):
        print(k + 1, matrix[k])
    print('======================================')

    #################################################
    #for k in range(len(mass)): #Массив, который участвует в работе кода - эквивалентен matrix, которая нужна для визуализации человеку
    #    print(k+1,mass[k])
    #################################################
    print('Введите стартовую вершину:')
    startpoint = prov_versh(a) - 1
    print('Введите конечную вершину вершину:')
    endpoint = prov_versh(a) - 1

    print('======================================')
    #################################################

    Tabl = [math.inf] * len(mass)  # последняя строка таблицы

    point = startpoint  # стартовая вершина
    visited = {point}  # множество просмотренных вершин
    Tabl[point] = 0  # нулевой вес для стартовой вершины
    optimal = [0] * len(mass)  # оптимальные связи между вершинами

    while point != -1:  # цикл, пока не просмотрим все вершины
        for j, dw in enumerate(mass[point]):  # перебираем все связанные вершины с вершиной point | enumerate - Выполняет роль счетчика элементов последовательности в циклах - типо функция генератор, формирующий совокупность таких путей с связанной вершиной
            if j not in visited:  # если вершина еще не была просмотрена, вторая проверка после генератора
                w = Tabl[point] + dw # w - вес
                if w < Tabl[j]:
                    Tabl[j] = w
                    optimal[j] = point  # связываем вершину j с вершиной point

        point = arg_min(Tabl, visited)  # выбираем следующий узел с наименьшим весом, arg_min - возвращает аргумент, т.е. вершину с мин.весом
        if point >= 0:  # выбрана очередная вершина
            visited.add(point)  # добавляем новую вершину в рассмотрение
    #print(Tabl)
    #print(optimal)
    # формирование самого оптимального маршрута
    path = [endpoint]
    while endpoint != startpoint:
        endpoint = optimal[path[-1]]
        path.append(endpoint)
    result = []
    while path: result.append(path.pop() + 1)
    print('Самый короткий путь:', result)

    leen = 0
    for i in range(len(result) - 1):
        a1 = result[i] - 1
        a2 = result[i + 1] - 1
        leen += mass[a1][a2]
    print('Длина пути:', leen)
    return ('=====================\n    КОНЕЦ ЗАДАНИЯ    \n=====================')