from Proverka import *
def z2():
    print('==========================\n| Лабораторная работа №3 |\n==========================\nВведите скобочную последовательность:')
    s = prov_sk()
    stek = []
    flag = True
    for i in s:
        if i in '({[':
            stek.append(i)
        elif i in ')}]':
            if not stek:
                flag = False
                break
            open_brack = stek.pop()
            if open_brack == '(' and i == ')':
                continue
            if open_brack == '[' and i == ']':
                continue
            if open_brack == '{' and i == '}':
                continue
            flag = False
            break
    if flag and len(stek) == 0:
        print('YES: правильная скобочная последовательсноть')
    else:
        print('NO: НЕправильная скобочная последовательность')
    return ('=====================\n    КОНЕЦ ЗАДАНИЯ    \n=====================')
def z3():
    print('==========================\n| Лабораторная работа №3 |\n==========================\n')
    def resh():
        try:
            def rpn(mass):
                stek = []
                for x in mass:
                    if (x == '+'):
                        e1 = int(stek.pop())
                        e2 = int(stek.pop())
                        oper = e2 + e1
                        stek.append(oper)
                    elif (x == '-'):
                        e1 = int(stek.pop())
                        e2 = int(stek.pop())
                        oper = e2 - e1
                        stek.append(oper)
                    elif (x == '*'):
                        e1 = int(stek.pop())
                        e2 = int(stek.pop())
                        oper = e2 * e1
                        stek.append(oper)
                    elif (x == '/'):
                        e1 = int(stek.pop())
                        e2 = int(stek.pop())
                        oper = e2 / e1
                        stek.append(oper)
                    elif (x == '^'):
                        e1 = int(stek.pop())
                        e2 = int(stek.pop())
                        oper = e2 ** e1
                        stek.append(oper)
                    else:
                        stek.append(x)
                return stek[0] # (2 + 3) * 2 / 5
            print('Введите выражение в обратной польской нотации, используя операции *, /, +, - и ^')
            primer = input()
            print(rpn(primer.split()))
        except IndexError:
            print('НЕПРАВИЛЬНАЯ ЗАПИСЬ!!!')
            return resh()
        return ''
    resh()
    print(('=====================\n    КОНЕЦ ЗАДАНИЯ    \n====================='))
    return ''