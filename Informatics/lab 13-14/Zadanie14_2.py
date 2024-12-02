from tkinter import *
root = Tk()

root.title('Задание 2')
root.geometry('300x250')
A = Entry(width=30)
B = Entry(width=30)
C = Entry(width=30)
btn_proverka = Button(text='Проверить')



Lbl = Label(bg='white',fg='red', width=50, height=5)

def proverka(event):
    a = int(A.get())
    b = int(B.get())
    c = int(C.get())
    if (a >= b >= c) or (a <= b <= c):
        Lbl['text'] = 'Истина'
    else:
        Lbl['text'] = 'Ложь'

btn_proverka.bind('<Button-1>', proverka)

A.pack()
B.pack()
C.pack()
btn_proverka.pack()
Lbl.pack()
root.mainloop()