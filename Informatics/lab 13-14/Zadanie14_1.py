from tkinter import *
root = Tk()

root.title('Задание 1')
root.geometry('300x250')
A = Entry(width=30)
B = Entry(width=30)
btn_plus = Button(text='|a| + |b|')
btn_minus = Button(text='|a| - |b|')
btn_umn = Button(text='|a| * |b|')
btn_dell = Button(text='|a| / |b|')
btn_clear = Button(text='Clear')


Lbl = Label(bg='white',fg='red', width=50, height=5)

def plus(event):
    a = int(A.get())
    b = int(B.get())
    Lbl['text'] = str(abs(a) + abs(b))

def minus(event):
    a = int(A.get())
    b = int(B.get())
    Lbl['text'] = str(abs(a) - abs(b))

def umn(event):
    a = int(A.get())
    b = int(B.get())
    Lbl['text'] = str(abs(a) * abs(b))

def dell(event):
    a = int(A.get())
    b = int(B.get())
    Lbl['text'] = str(abs(a) / abs(b))

def clear(event):
    Lbl['text'] = ''

btn_plus.bind('<Button-1>', plus)
btn_minus.bind('<Button-1>', minus)
btn_dell.bind('<Button-1>', dell)
btn_umn.bind('<Button-1>', umn)
btn_clear.bind('<Button-1>', clear)

A.pack()
B.pack()
btn_plus.pack()
btn_minus.pack()
btn_umn.pack()
btn_dell.pack()
btn_clear.pack()
Lbl.pack()
root.mainloop()