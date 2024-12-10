def prov_n():
    try:
        num = int(input())
    except ValueError:
        print('ERROR: Выберете 1 или 2!')
        return prov_n()
    if num != 1 and num != 2:
        print('ERROR: Выберете 1 или 2!')
        return prov_n()
    else:
        return num

def prov_z1():
        try:
            num = int(input())
        except ValueError:
            print('ERROR: Натуральное число, начиная с 1!')
            return prov_z1()
        if num < 1:
            print('ERROR: Натуральное число, начиная с 1!')
            return prov_z1()
        else:
            return num

def prov_pos():
        try:
            num = list(map(int, input().split()))
        except ValueError:
            print('ERROR: Последовательность должна состоять только из целых чисел больших 0')
            return prov_pos()
        for i in num:
            if i < 1:
                print('ERROR: Последовательность должна состоять только из целых чисел больших 0')
                return prov_pos()
        return num

def prov_Z():
    try:
        num = int(input())
    except ValueError:
        print('ERROR: Только целые числа!')
        return prov_Z()
    else:
        return num

def prov_sk():
    num = str(input())
    for x in num:
        if x in '([{}])':
            continue
        else:
            print('Только скобочная последовательность!')
            return prov_sk()
    return num

def prov_str():
    try:
        num = input()
    except ValueError:
        print('ERROR: Только y или n!')
        return prov()
    if num != 'y' and num != 'n':
        print('ERROR: Только y или n!')
        return prov_str()
    else:
        return num

def prov_versh(a):
    try:
        num = int(input())
    except ValueError:
        print('ERROR: Только целые числа!')
        return prov_versh(a)
    if (num <= 0) or (num > a):
        print('ERROR: Не существует такой вершины!')
        return prov_versh(a)
    else:
        return num

