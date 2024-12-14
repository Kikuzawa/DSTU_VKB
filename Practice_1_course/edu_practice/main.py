from wheatstone import *
from Vijener import *
from verification import *

num = -1
while num != 0:
    print('[0] - Конец программы\n[1] - Шифр Виженера\n[2] - Шифр "Двойной квадрат" Уитстона')
    num = verification_Main()
    if num == 1:
        Vijener()
    elif num == 2:
        wheatstone()
    else:
        break
    print('--------------------------')