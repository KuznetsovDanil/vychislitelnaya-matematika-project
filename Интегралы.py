# -*- coding: cp1251 -*-
import math
from math import *
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox

def eval_expression(s, x):
    allowed_names = {"x": x, "п": math.pi, "pi": math.pi,
                     "е": math.e, "e": math.e, "sqrt": sqrt,
                     "ln": log, "lg": log10, "log": log,
                     "sin": sin, "cos": cos, "tg": tan,             # ctg = 1 / tg
                     "sh": sinh, "ch": cosh, "th": tanh,            # cth = 1 / th
                     "arcsin": asin, "arccos": acos, "arctg": atan, # arcctg = pi / 2 - arctg
                     "arsh": asinh, "arch": acosh, "arth": atanh}
    code = compile(s, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            messagebox.showerror('Внимание!', 'Ошибка при вводе данных!')
    return eval(code, {"__builtins__": {}}, allowed_names)

def rectangles(a, b, m, h):
    s = txt_int.get()
    try:
        if m == 1:
            return (b-a) * eval_expression(s, (a+b)/2)
        elif m in range(2, 1001):
            integral = 0
            x = a + h/2
            while x < b:
                integral += eval_expression(s, x)
                x += h
            integral *= h
            return integral
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')


def trapecies(a, b, m, h):
    s = txt_int.get()
    try:
        if m == 1:
            fa = eval_expression(s, a)
            fb = eval_expression(s, b)
            return (b-a) * (fb-fa) / 2
        elif m in range (2, 1001):
            integral = eval_expression(s, a) + eval_expression(s, b)
            x = a + h
            while x < b:
                integral += 2*eval_expression(s, x)
                x += h
            integral *= (h/2)
            return integral
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

def simpson(a, b, m, h):
    s = txt_int.get()
    try:
        if m == 1:
            return (b-a) / 6 * (eval_expression(s, a) + 4*eval_expression(s, (a+b)/2) + eval_expression(s, b))
        elif m in range (2, 1001):
            integral = eval_expression(s, a) + eval_expression(s, b)
            x = a + h
            while x < b:
                integral += (2*eval_expression(s, x) + 4*eval_expression(s, x - h/2))
                x += h
            integral += 4*eval_expression(s, b - h/2)
            integral *= (h / 6)
            return integral
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

def mistake(h):
    variant = selected.get()
    if variant == 1 or variant == 2:
        return h ** 2
    elif variant == 3:
        return h ** 4

def clicked():
    variant = selected.get()
    txt1.delete(1.0, END)
    txt2.delete(1.0, END)
    try:
        a = float(eval_expression(lim_down.get(), 0))
        b = float(eval_expression(lim_up.get(), 0))
        m = int(eval_expression(spin.get(), 0))
        h = (b - a) / m
        result = "xxxxxxxxxxxx"
        if variant == 1:
            result = '{:.7f}'.format(rectangles(a, b, m, h))
        elif variant == 2:
            result = '{:.7f}'.format(trapecies(a, b, m, h))
        elif variant == 3:
            result = '{:.7f}'.format(simpson(a, b, m, h))
        txt1.insert(INSERT, result)
        txt2.insert(INSERT, '{:.10g}'.format(mistake(h)))
    except Exception:
        pass

window = Tk()  
window.title("Определённые интегралы")
window.geometry('530x350')
lbl1 = Label(window, text="Формула для вычисления:", font=("Calibri", 11))  
lbl1.grid(column=0, row=1, columnspan=4)
selected = IntVar()
rad1 = Radiobutton(window, text='прямоугольников', font=("Calibri", 11), value=1, variable=selected)  
rad2 = Radiobutton(window, text='трапеций', font=("Calibri", 11), value=2, variable=selected)  
rad3 = Radiobutton(window, text='Симпсона', font=("Calibri", 11), value=3, variable=selected)  
rad1.grid(column=1, row=2)  
rad2.grid(column=2, row=2)  
rad3.grid(column=3, row=2)
lbl2 = Label(window, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")  
lbl2.grid(column=0, row=3, columnspan=4)
lbl3 = Label(window, text="Разбиение на ", font=("Calibri", 11))  
lbl3.grid(column=1, row=4)
var = IntVar()
var.set(1)
spin = Spinbox(window, from_=1, to=1000, width=5, textvariable=var)  
spin.grid(column=2, row=4)
lbl4 = Label(window, text="частей", font=("Calibri", 11))  
lbl4.grid(column=3, row=4)
lbl5 = Label(window, text="(При разбиении по Симпсону отрезок автоматически делится на 2m частей.)", font=("Calibri", 8))
lbl5.grid(column=1, row=5, columnspan=4)
lbl6 = Label(window, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")  
lbl6.grid(column=0, row=6, columnspan=4)
lbl7 = Label(window, text="Интеграл:", font=("Calibri", 13))  
lbl7.grid(column=0, row=7, columnspan=4)
btn = Button(window, text="Вычислить", command=clicked)  
btn.grid(column=3, row=7)
lbl8 = Label(window, text="S", font=("Calibri", 13))  
lbl8.grid(column=0, row=9)
lbl9 = Label(window, text=" dx = ", font=("Calibri", 13))  
lbl9.grid(column=2, row=9)
lim_up = Entry(window, width=5)
lim_up.grid(column=0, row=8, padx=5)
lim_down = Entry(window, width=5)
lim_down.grid(column=0, row=10, padx=5)
txt_int = Entry(window,width=40)  
txt_int.grid(column=1, row=9)
txt1 = scrolledtext.ScrolledText(window, width=15, height=1)
txt1.grid(column=3, row=9)
lbl10 = Label(window, text="Порядок погрешности:", font=("Calibri", 12))  
lbl10.grid(column=1, row=11, columnspan=2)
txt2 = scrolledtext.ScrolledText(window, width=15, height=1)
txt2.grid(column=3, row=11)
menu = Menu(window)  
new_item = Menu(menu, tearoff=0)
menu.add_cascade(label='О программе', menu=new_item)  
window.config(menu=menu)
window.mainloop()
