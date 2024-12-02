from tkinter import *
root = Tk()

root.title('Задание 3')
root.geometry('300x250')
N = Entry(width=30)
A = Entry(width=30)
btn_proverka = Button(text='Проверить')



Lbl = Label(bg='white',fg='red', width=40)
Lbl1 = Label(bg='black',fg='white',width=10)

def proverka(event):
    n = int(N.get())
    i, k, result = 0, 0, 0
    s = A.get()
    ss = s.split()
    pos = [int(x) for x in ss]
    while pos[k] > 0 and k != n:
        result += 1
        k += 1
    Lbl['text'] = str(pos)
    Lbl1['text'] = str(result)

btn_proverka.bind('<Button-1>', proverka)

N.pack()
A.pack()
btn_proverka.pack()
Lbl.pack()
Lbl1.pack()
root.mainloop()