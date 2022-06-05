import math
from tkinter import messagebox
import matplotlib.pyplot as plt
from eval_expression import eval_expr

# возвращение значения функции в точке
def func(s, x):
    try:
        return eval_expr(s, x, 0, 0)
    except Exception:
        pass

# формула прямоугольников
def rectangles(s, a, b, h):
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while round(j, 12) < round(b, 12):
            xs += [j] * 2
            j += h
        xs += [b]

        if h == b - a:
            integral = (b-a) * func(s, (a+b)/2)
            ys = [func(s, (a+b)/2)] * 2
            return [integral, xs, ys]
        else:
            integral = 0
            ys = []
            x = a + h/2
            while x < b:
                y = func(s, x)
                integral += y
                ys += [y] * 2
                x += h
            integral *= h
            return [integral, xs, ys]
    except Exception:
        pass

# формула трапеций
def trapecies(s, a, b, h):
    try:
        # значения для построения графика
        xs = [a]
        j = a + h
        while j < b:
            xs += [j] * 2
            j += h
        xs += [b]

        if h == b - a:
            integral = (b-a) * (func(s, a) + func(s, b)) / 2
            ys = [func(s, a), func(s, b)]
            return [integral, xs, ys]
        else:
            y = func(s, a)
            integral = y
            ys = [y]
            x = a + h
            while x < b:
                y = func(s, x)
                integral += 2*y 
                ys += [y] * 2
                x += h
            y = func(s, b)
            integral += y
            ys += [y]
            integral *= (h/2)
            return [integral, xs, ys]
    except Exception:
        pass

# формула Симпсона
def simpson(s, a, b, h):
    h /= 2 # для удобства разбиваем шаг деления ещё надвое
    try:
        if h == b - a:
            # значения для построения графика
            xs = []
            j = a
            while j < b:
                xs += [(j + h*i/10) for i in range (0, 21)]
                j += 2*h
            y0 = func(s, a)
            y1 = func(s, (a+b)/2)
            y2 = func(s, b)
            integral = (b-a) / 6 * (y0 + 4*y1 + y2)
            alpha = (y0 - 2*y1 + y2) / (2 * h**2)
            beta = (y2 - y0 - 4*alpha*((a+b)/2)*h) / (2 * h)
            gamma = y1 - alpha*((a+b)/2)**2 - beta*(a+b)/2
            ys = [(alpha*i**2 + beta*i + gamma) for i in xs]
            return [integral, xs, ys]
        else:
            integral = 0
            xs = []
            ys = []
            x = a + h
            while x < b:
                y0 = func(s, x - h)
                y1 = func(s, x)
                y2 = func(s, x + h)
                integral += (y0 + 4*y1 + y2)
                alpha = (y0 - 2*y1 + y2) / (2 * h**2)
                beta = (y2 - y0 - 4*alpha*x*h) / (2 * h)
                gamma = y1 - alpha*x**2 - beta*x
                xs1 = [(x + h*i/10) for i in range(-10, 11)]
                ys += [(alpha*i**2 + beta*i + gamma) for i in xs1]
                x += 2*h
                xs += xs1
            integral *= (h/3)
            return [integral, xs, ys]
    except Exception:
        pass

# приближённый расчёт погрешности
def mistake(s, a, b, m, h, variant):
    if m < 100:
        m = 100
    h1 = (b-a) / m
    xn = [(a + i*h1) for i in range(0, m+1)]
    if variant == 1:
        y2 = [((-func(s, x0+2*h1) + 16*func(s, x0+h1) - 30*func(s, x0) + 16*func(s, x0-h1) - func(s, x0-2*h1))/(12*h1**2)) for x0 in xn]
        y2abs = [math.fabs(y) for y in y2]
        return (b-a) / 24 * (h**2) * max(y2abs)
    elif variant == 2:
        y2 = [((-func(s, x0+2*h1) + 16*func(s, x0+h1) - 30*func(s, x0) + 16*func(s, x0-h1) - func(s, x0-2*h1))/(12*h1**2)) for x0 in xn]
        y2abs = [math.fabs(y) for y in y2]
        return (b-a) / 12 * (h**2) * max(y2abs)
    elif variant == 3:
        y4 = [((func(s, x0+4*h1) - 32*func(s, x0+3*h1) + 316*func(s, x0+2*h1) - 992*func(s, x0+h1) + 1414*func(s, x0) -
               992*func(s, x0-h1) + 316*func(s, x0-2*h1) - 32*func(s, x0-3*h1) + func(s, x0-4*h1))/(144*h1**4)) for x0 in xn]
        y4abs = [math.fabs(y) for y in y4]
        return (b-a) / 180 * (h**4) * max(y4abs)

def graphic(s, a, m, h, xs, ys, variant, redraw):
    x = [(a + h*i/30) for i in range(0, m*30+1)]
    y = [func(s, i) for i in x]
    if not redraw:
        plt.plot(x, y, xs, ys)
    else:
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, y, xs, ys)
    if variant == 1:
        plt.title("Квадратура прямоугольников")
    elif variant == 2:
        plt.title("Квадратура трапеций")
    elif variant == 3:
        plt.title("Квадратура Симпсона")
    plt.axis('square')
    plt.grid(True)
    plt.fill_between(xs, 0, ys, color="r", alpha=0.3)
    plt.show()

def integral(s, a, b, h, variant):
    if variant == 1:
        return rectangles(s, a, b, h)
    elif variant == 2:
        return trapecies(s, a, b, h)
    elif variant == 3:
        return simpson(s, a, b, h)

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