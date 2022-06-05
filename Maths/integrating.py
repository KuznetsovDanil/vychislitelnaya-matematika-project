import math
from eval_expression import eval_expr
import matplotlib.pyplot as plt

# возвращение значения функции в точке
def func(s, x):
    try:
        return eval_expr(s, x, 0, 0)
    except Exception:
        pass

# формула прямоугольников
def rectangles(s, a, b, h):
    if h == b - a:
        return (b-a) * func(s, (a+b)/2)
    else:
        integral = 0
        x = a + h/2
        while x < b:
            integral += func(s, x)
            x += h
        return integral * h

# формула трапеций
def trapecies(s, a, b, h):
    if h == b - a:
        return (b-a) * (func(s, a) + func(s, b)) / 2
    else:
        integral = func(s, a)
        x = a + h
        while x < b:
            integral += 2*func(s, x)
            x += h
        integral += func(s, b)
        return integral * (h/2)

# формула Симпсона
def simpson(s, a, b, h):
    h /= 2 # для удобства разбиваем шаг деления ещё надвое
    if h*2 == b - a:
        return (b-a) / 6 * (func(s, a) + 4*func(s, (a+b)/2) + func(s, b))
    else:
        m = int((b - a) / (2*h))
        integral = 0
        xs = [(a + h + 2*h*i) for i in range(m+1)]
        for x in xs:
            integral += (func(s, x - h) + 4*func(s, x) + func(s, x + h))
        return integral * (h/3)

def integral(s, a, b, h, variant):
    if variant == 1:
        return rectangles(s, a, b, h)
    elif variant == 2:
        return trapecies(s, a, b, h)
    elif variant == 3:
        return simpson(s, a, b, h)