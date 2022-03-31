import math
from math import *
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.ttk import Checkbutton
import matplotlib.pyplot as plt

# преобразование текстового выражения в математическое
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

# вставка функции из файла
def insert_expression():
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
    s = txt_int.get()
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while j < b:
            xs += [j] * 2
            j += h
        xs += [b]

        if m == 1:
            integral = (b-a) * eval_expression(s, (a+b)/2)
            ys = [eval_expression(s, (a+b)/2)] * 2
            return [integral, xs, ys]
        elif m in range(2, 10001):
            integral = 0
            ys = []
            x = a + h/2
            while x < b:
                y = eval_expression(s, x)
                integral += y
                ys += [y] * 2
                x += h
            integral *= h
            return [integral, xs, ys]
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

# формула трапеций
def trapecies(a, b, m, h):
    s = txt_int.get()
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while j < b:
            xs += [j] * 2
            j += h
        xs += [b]

        if m == 1:
            fa = eval_expression(s, a)
            fb = eval_expression(s, b)
            integral = (b-a) * (fa + fb) / 2
            ys = [fa, fb]
            return [integral, xs, ys]
        elif m in range (2, 10001):
            y = eval_expression(s, a)
            integral = y
            ys = [y]
            x = a + h
            while x < b:
                y = eval_expression(s, x)
                integral += 2*y 
                ys += [y] * 2
                x += h
            y = eval_expression(s, b)
            integral += y
            ys += [y]
            integral *= (h/2)
            return [integral, xs, ys]
    except Exception:
        messagebox.showerror('Внимание!', 'Ошибка при вычислении!')

# формула Симпсона
def simpson(a, b, m, h):
    s = txt_int.get()
    h /= 2 # для удобства разбиваем шаг деления ещё надвое
    try:
        if m == 1:
            # значения для построения графика
            xs = []
            j = a
            while j < b:
                xs += [(j + h*i/10) for i in range (0, 21)]
                j += 2*h
            y0 = eval_expression(s, a)
            y1 = eval_expression(s, (a+b)/2)
            y2 = eval_expression(s, b)
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
                y0 = eval_expression(s, x - h)
                y1 = eval_expression(s, x)
                y2 = eval_expression(s, x + h)
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

# порядок погрешности
def mistake(a, b, h):
    variant = selected.get()
    if variant == 1:
        return (b-a) / 24 * (h**2)
    elif variant == 2:
        return (b-a) / 12 * (h**2)
    elif variant == 3:
        return (b-a) / 180 * (h**4)

def graphic(a, b, m, xs, ys):
    s = txt_int.get()
    h = (b-a) / m
    x = [(a + h*i/30) for i in range(0, m*30+1)]
    y = [eval_expression(s, i) for i in x]
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
        a = float(eval_expression(lim_down.get(), 0))
        b = float(eval_expression(lim_up.get(), 0))
        m = int(eval_expression(spin.get(), 0))
        h = (b - a) / m
        if variant == 1:
            res = rectangles(a, b, m, h)
            result = '{:.10f}'.format(res[0])
        elif variant == 2:
            res = trapecies(a, b, m, h)
            result = '{:.10f}'.format(res[0])
        elif variant == 3:
            res = simpson(a, b, m, h)
            result = '{:.10f}'.format(res[0])
        txt1.insert(INSERT, result)
        txt2.insert(INSERT, '{:.10g}'.format(mistake(a, b, h)))
        # передача данных для графика
        xs = res[1]
        ys = res[2]
        if chk_state:
            graphic(a, b, m, xs, ys)
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
                         \nПредельно доступное число шагов разбиения - 10000.''')

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
                         \nm > 1       ∫ f(x) dx ~ h/6 * (f(a) + f(b) + 2*(f(a+h)+...+f(b-h)) + 4*(f(a+h/2)+...+f(b-h/2)))\n
                         \nПорядок погрешности - выражение, позволяющее оценить возможное отклонение значения от точного. В данном приложении равен:
                         \nпрямоугольники: (b-a) / 24  * h^2
                         \nтрапеции:       (b-a) / 12  * h^2
                         \nСимпсон:        (b-a) / 180 * h^4\n
                         \nТочное значение погрешности можно получить, если домножить порядок на max|f''(x)| для формул прямоугольников и трапеций или на max|f(IV) (x)| для квадратуры Симпсона. Значение x при этом лежит на отрезке [a;b].''')

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
filename = Button(window, text="Выбрать файл", command=insert_expression)
filename.grid(column=0, row=11)
lbl10 = Label(window, text="Порядок погрешности:", font=("Calibri", 12))  
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