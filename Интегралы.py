import math
from math import *
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.ttk import Checkbutton
import matplotlib.pyplot as plt

# преобразование текстового выражения в математическое
def eval_expr(s, x):
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

# возвращение значения функции в точке
def func(x):
    s = txt_int.get()
    try:
        return eval_expr(s, x)
    except Exception:
        pass

# вставка функции из файла
def insert_expr():
    try:
        file_name = fd.askopenfilename()
        f = open(file_name)
        s = f.read()
        txt_int.insert(1.0, s)
        f.close()
    except Exception:
        messagebox.showerror("Внимание!", "Ошибка при загрузке файла!")

# формула прямоугольников
def rectangles(a, b, m, h):
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while j < b:
            xs += [j] * 2
            j += h
        xs += [b]

        if m == 1:
            integral = (b-a) * func((a+b)/2)
            ys = [func((a+b)/2)] * 2
            return [integral, xs, ys]
        elif m in range(2, 10001):
            integral = 0
            ys = []
            x = a + h/2
            while x < b:
                y = func(x)
                integral += y
                ys += [y] * 2
                x += h
            integral *= h
            return [integral, xs, ys]
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

# формула трапеций
def trapecies(a, b, m, h):
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while j < b:
            xs += [j] * 2
            j += h
        xs += [b]

        if m == 1:
            integral = (b-a) * (func(a) + func(b)) / 2
            ys = [func(a), func(b)]
            return [integral, xs, ys]
        elif m in range (2, 10001):
            y = func(a)
            integral = y
            ys = [y]
            x = a + h
            while x < b:
                y = func(x)
                integral += 2*y 
                ys += [y] * 2
                x += h
            y = func(b)
            integral += y
            ys += [y]
            integral *= (h/2)
            return [integral, xs, ys]
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

# формула Симпсона
def simpson(a, b, m, h):
    h /= 2 # для удобства разбиваем шаг деления ещё надвое
    try:
        if m == 1:
            # значения для построения графика
            xs = []
            j = a
            while j < b:
                xs += [(j + h*i/10) for i in range (0, 21)]
                j += 2*h
            y0 = func(a)
            y1 = func((a+b)/2)
            y2 = func(b)
            integral = (b-a) / 6 * (y0 + 4*y1 + y2)
            alpha = (y0 - 2*y1 + y2) / (2 * h**2)
            beta = (y2 - y0 - 4*alpha*((a+b)/2)*h) / (2 * h)
            gamma = y1 - alpha*((a+b)/2)**2 - beta*(a+b)/2
            ys = [(alpha*i**2 + beta*i + gamma) for i in xs]
            return [integral, xs, ys]
        elif m in range (2, 10001):
            integral = 0
            xs = []
            ys = []
            x = a + h
            while x < b:
                y0 = func(x - h)
                y1 = func(x)
                y2 = func(x + h)
                integral += (y0 + 4*y1 + y2)
                alpha = (y0 - 2*y1 + y2) / (2 * h**2)
                beta = (y2 - y0 - 4*alpha*x*h) / (2 * h)
                gamma = y1 - alpha*x**2 - beta*x
                xs1 = [(x + h*i/10) for i in range(-10, 11)]
                ys += [(alpha*i**2 + beta*i + gamma) for i in xs1]
                x += 2*h
                xs += xs1
            integral *= (b-a)/(6*m)
            return [integral, xs, ys]
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

# приближённый расчёт погрешности
def mistake(a, b, h):
    m = int(spin.get()) # разбиение для подсчёта
    if m < 100:
        m = 100
    h1 = (b-a) / m
    xn = [(a + i*h1) for i in range(0, m+1)]
    variant = selected.get()
    if variant == 1:
        y2 = [((-func(x0+2*h1) + 16*func(x0+h1) - 30*func(x0) + 16*func(x0-h1) - func(x0-2*h1))/(12*h1**2)) for x0 in xn]
        y2abs = [fabs(y) for y in y2]
        return (b-a) / 24 * (h**2) * max(y2abs)
    elif variant == 2:
        y2 = [((-func(x0+2*h1) + 16*func(x0+h1) - 30*func(x0) + 16*func(x0-h1) - func(x0-2*h1))/(12*h1**2)) for x0 in xn]
        y2abs = [fabs(y) for y in y2]
        return (b-a) / 12 * (h**2) * max(y2abs)
    elif variant == 3:
        y4 = [((func(x0+4*h1) - 32*func(x0+3*h1) + 316*func(x0+2*h1) - 992*func(x0+h1) + 1414*func(x0) -
               992*func(x0-h1) + 316*func(x0-2*h1) - 32*func(x0-3*h1) + func(x0-4*h1))/(144*h1**4)) for x0 in xn]
        y4abs = [fabs(y) for y in y4]
        return (b-a) / 180 * (h**4) * max(y4abs)

def graphic(a, m, h, xs, ys):
    x = [(a + h*i/30) for i in range(0, m*30+1)]
    y = [func(i) for i in x]
    variant = selected.get()
    if variant == 1:
        plt.title("Квадратура прямоугольников")
    elif variant == 2:
        plt.title("Квадратура трапеций")
    elif variant == 3:
        plt.title("Квадратура Симпсона")
    plt.plot(x, y, xs, ys)
    plt.axis('square')
    plt.grid(True)
    plt.fill_between(xs, 0, ys, color="r", alpha=0.3)
    plt.show()

# кнопка выполнения действий
def clicked():
    variant = selected.get()
    txt1.delete(1.0, END)
    txt2.delete(1.0, END)
    try:
        a = float(eval_expr(lim_down.get(), 0))
        b = float(eval_expr(lim_up.get(), 0))
        m = int(eval_expr(spin.get(), 0))
        h = (b - a) / m
        if variant == 1:
            res = rectangles(a, b, m, h)
            result = round(res[0], 12)    # дальше этого разряда возникает ошибка округления
        elif variant == 2:
            res = trapecies(a, b, m, h)
            result = round(res[0], 12)
        elif variant == 3:
            res = simpson(a, b, m, h)
            result = round(res[0], 12)
        txt1.insert(INSERT, result)
        txt2.insert(INSERT, round(mistake(a, b, h), 19))
        # передача данных для графика
        xs = res[1]
        ys = res[2]
        if chk_state.get():
            graphic(a, m, h, xs, ys)
    except Exception:
        pass

# информация о программе
def info():
    messagebox.showinfo('О программе', '''Данная программа является учебной и предназначена для приближённого вычисления определённых собственных интегралов тремя различными способами.
                         \nФункции реализованы с помощью языка Python 3.9 на основании методических указаний в задании и могут некорректно работать при попытке вычислить интеграл иного типа.
                         \nНе рекомендуется вводить выражения, не являющиеся математическими, в том числе команды для командной строки Windows и интерпретатора Python.
                         \nВ программе реализована защита от подобных выражений, однако создатель не несёт ответственности за некорректное использование приложения.''')

# справка для пользователя
def help():
    messagebox.showinfo('Помощь', '''Чтобы вычислить интеграл, необходимо:
                         \n1) выбрать формулу для подсчёта;
                         \n2) указать точность вычисления - число частей, на которые разбивается отрезок;
                         \n3) нажать кнопку "Строить график" для вывода окна с графическим сравнением функции и выбранной квадратуры;
                         \n4) ввести функцию для интегрирования:
                         \n   a) с клавиатуры;
                         \n   б) нажать на кнопку и выбрать текстовый файл (*.txt, *.doc) для чтения;
                         \n5) ввести пределы интегрирования (числа или выражения);
                         \n6) нажать на кнопку "Вычислить".\n
                         \nО точности вычисления - см. в разделе "Формулы".
                         \nНе вводите выражения, не являющиеся математически! Это может быть небезопасны для работы программы и компьютера.
                         \nИспользуйте "**" в качестве символа возведения в степень.
                         \nПредельно доступное число шагов разбиения - 10000.\n
                         \nВнимание! Квадратуры могут давать сбои при сильном дроблении отрезка (m>100). Желательно проверять найденные значения.
                         \nВнимание! Большое количество частей отрезка может значительно увеличивать время работы программы.''')

# список формул
def formuls():
    messagebox.showinfo('Формулы', '''a, b - пределы интегрирования
                         \nm - количество частей отрезка интегрирования
                         \nh = (b-a) / m  - шаг интегрирования\n
                         \nКвадратура прямоугольников:
                         \nm = 1       ∫ f(x) dx ~ (b-a) * f((a+b)/2)
                         \nm > 1       ∫ f(x) dx ~ h * (f(a+h/2) + f(a+3h/2) + ... + f(a+(2m-1)h/2))\n
                         \nКвадратура трапеций:
                         \nm = 1       ∫ f(x) dx ~ (b-a)/2 * (f(a) + f(b))
                         \nm > 1       ∫ f(x) dx ~ h/2 * (f(a) + 2*f(a+h) + ... + 2*f(b-h) + f(b))\n
                         \nКвадратура Симпсона:
                         \nm = 1       ∫ f(x) dx ~ (b-a)/6 * (f(a) + 4*f((a+b)/2) + f(b))
                         \nm > 1       ∫ f(x) dx ~ h/6 * (f(a) + f(b) + 2*(f(a+h)+...+f(b-h)) + 4*(f(a+h/2)+...+f(b-h/2)))\n\n
                         \nПогрешность вычисляется приближённо по специальным формулам с указанным шагом h.
                         \nКвадратура прямоугольников:
                         \n∆ = (b-a)/24 * h^2 * |max f''(x)|
                         \nКвадратура трапеций:
                         \n∆ = (b-a)/12 * h^2 * |max f''(x)|
                         \nКвадратура Симпсона:
                         \n∆ = (b-a)/180 * h^4 * |max fIV(x)|\n
                         \nf''(x0) ~ 1/12h^2 * (-f(x0+2h) + 16f(x0+h) - 30f(x0) + 16f(x0-h) - f(x0-2h))
                         \nfIV(x0) ~ 1/144h^2 * (f(x0+4h) - 32(x0+3h) + 316f(x0+2h) - 992f(x0+h) + 1414f(x0) - 992f(x0-h) + 316f(x0-2h) - 32f(x0-3h) + f(x0-4h))''')

# выход
def away():
    exit()

# графический интерфейс
window = Tk()  
window.title("Определённые интегралы")
window.geometry('650x350')
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
spin = Spinbox(window, from_=1, to=10000, width=5, textvariable=var)  
spin.grid(column=2, row=4)
lbl4 = Label(window, text="частей", font=("Calibri", 11))  
lbl4.grid(column=3, row=4)
chk_state = BooleanVar()  
chk_state.set(True)
chk = Checkbutton(window, text='Строить график', var=chk_state)  
chk.grid(column=0, row=4)  
lbl5 = Label(window, text="(При разбиении по Симпсону отрезок автоматически делится на 2m частей.)", font=("Calibri", 8))
lbl5.grid(column=1, row=5, columnspan=4)
lbl6 = Label(window, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")  
lbl6.grid(column=0, row=6, columnspan=4)
lbl7 = Label(window, text="Интеграл:", font=("Calibri", 13))  
lbl7.grid(column=0, row=7, columnspan=4)
btn = Button(window, text="Вычислить", command=clicked)  
btn.grid(column=3, row=7)
lbl8 = Label(window, text="∫", font=("Calibri", 13))  
lbl8.grid(column=0, row=9)
lbl9 = Label(window, text=" dx = ", font=("Calibri", 13))  
lbl9.grid(column=2, row=9)
lim_up = Entry(window, width=5)
lim_up.grid(column=0, row=8, padx=5)
lim_down = Entry(window, width=5)
lim_down.grid(column=0, row=10, padx=5)
txt_int = Entry(window,width=40)  
txt_int.grid(column=1, row=9)
txt1 = scrolledtext.ScrolledText(window, width=20, height=1)
txt1.grid(column=3, row=9)
filename = Button(window, text="Выбрать файл", command=insert_expr)
filename.grid(column=0, row=11)
lbl10 = Label(window, text="Погрешность:", font=("Calibri", 12))  
lbl10.grid(column=1, row=11, columnspan=2)
txt2 = scrolledtext.ScrolledText(window, width=20, height=1)
txt2.grid(column=3, row=11)
menu = Menu(window)  
new_item = Menu(menu, tearoff=0)
new_item.add_command(label="О программе", command=info)
new_item.add_command(label="Помощь", command=help)
new_item.add_command(label="Формулы", command=formuls)
new_item.add_separator()
new_item.add_command(label="Выход", command=away)
menu.add_cascade(label='Справка', menu=new_item)
window.config(menu=menu)
window.mainloop()
