import math
from math import *
import integrating
from integrating import func
from tkinter import messagebox
import matplotlib.pyplot as plt
plt.interactive(True)

def build_expr(ai, bi, i, l):
    add_expr = ""
    if ai != 0.0:
        if ai > 0.0:
            add_expr += " + " + str(round(ai, 5))
        else:
            add_expr += " - " + str(round(-ai, 5))
        if l != math.pi:
            add_expr += "*cos(" + str(round(i/l, 5)) + "*pi*x)"
        else:
            add_expr += "*cos(" + str(i) + "*x)"
    if bi != 0.0:
        if bi > 0.0:
            add_expr += " + " + str(round(bi, 5))
        else:
            add_expr += " - " + str(round(-bi, 5))
        if l != math.pi:
            add_expr += "*sin(" + str(round(i/l, 5)) + "*pi*x)"
        else:
            add_expr += "*sin(" + str(i) + "*x)"
    return add_expr

def fourier_row(s, s1, s2, a, b, h, n, variant_int, variant_row, kind_of_func):
    if kind_of_func == 1:
        if variant_row == 1:
            l = (b - a) / 2
            a0 = 1 / l * integrating.integral(s, a, b, h, variant_int)
            expr = str(round(a0/2, 12))
            an = [(1 / l * integrating.integral(s + "*cos(" + str(i / l) + "*pi*x)", a, b, h, variant_int)) for i in range(1, n)]
            bn = [(1 / l * integrating.integral(s + "*sin(" + str(i / l) + "*pi*x)", a, b, h, variant_int)) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(an[i-1], bn[i-1], i, l)
            return expr
        elif variant_row == 2:
            l = b - a
            a0 = 1 / l * integrating.integral(s, a, b, h, variant_int)
            expr = str(round(a0, 12))
            an = [(2 / l * integrating.integral(s + "*cos(" + str(i / l) + "*pi*x)", a, b, h, variant_int)) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(an[i-1], 0.0, i, l)
            return expr
        elif variant_row == 3:
            l = b - a
            expr = "0.0"
            bn = [(2 / l * integrating.integral(s + "*sin(" + str(i / l) + "*pi*x)", a, b, h, variant_int)) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(0.0, bn[i-1], i, l)
            return expr
    elif kind_of_func == 2:
        if variant_row == 1:
            l = (b - a) / 2
            a0 = 1 / l * (integrating.integral(s1, a, (a+b)/2, h, variant_int) + integrating.integral(s2, (a+b)/2, b, h, variant_int))
            expr = str(round(a0/2, 12))
            an = [(1 / l * (integrating.integral(s1 + "*cos(" + str(i / l) + "*pi*x)", a, (a+b)/2, h, variant_int) +
                            integrating.integral(s2 + "*cos(" + str(i / l) + "*pi*x)", (a+b)/2, b, h, variant_int))) for i in range(1, n)]
            bn = [(1 / l * (integrating.integral(s1 + "*sin(" + str(i / l) + "*pi*x)", a, (a+b)/2, h, variant_int) +
                            integrating.integral(s2 + "*sin(" + str(i / l) + "*pi*x)", (a+b)/2, b, h, variant_int))) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(an[i-1], bn[i-1], i, l)
            return expr
        elif variant_row == 2:
            l = b - a
            a0 = 1 / l * (integrating.integral(s1, a, (a+b)/2, h, variant_int) + integrating.integral(s2, (a+b)/2, b, h, variant_int))
            expr = str(round(a0/2, 12))
            an = [(2 / l * (integrating.integral(s1 + "*cos(" + str(i / l) + "*pi*x)", a, (a+b)/2, h, variant_int) +
                            integrating.integral(s2 + "*cos(" + str(i / l) + "*pi*x)", (a+b)/2, b, h, variant_int))) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(an[i-1], 0.0, i, l)
            return expr
        elif variant_row == 3:
            l = b - a
            expr = "0.0"
            bn = [(2 / l * (integrating.integral(s1 + "*cos(" + str(i / l) + "*pi*x)", a, (a+b)/2, h, variant_int) +
                            integrating.integral(s2 + "*cos(" + str(i / l) + "*pi*x)", (a+b)/2, b, h, variant_int))) for i in range(1, n)]
            for i in range(1, n):
                expr += build_expr(0.0, bn[i-1], i, l)
            return expr

def graphic(s, s1, s2, expr, a, b, h, n, redraw):
    xs = [(a + h*i) for i in range(int((b-a)/h+1)) if round((a + h*i), 12) < round(b, 12)]
    if not (s is None) and s1 is None and s2 is None:
        s = s.replace("**", "^")
        ys = [func(expr, xi) for xi in xs]
        fs = [func(s, xi) for xi in xs]
        if not redraw:
            plt.plot(xs, ys, label=("S"+str(n)))
            plt.plot(xs, fs, "--", label=("y = " + s[1:-1]))
        else:
            fig, ax = plt.subplots(1, 1)
            ax.plot(xs, ys, label=("S"+str(n)))
            ax.plot(xs, fs, "--", label=("y = " + s[1:-1]))
    elif s is None and not (s1 is None or s2 is None):
        s1 = s1.replace("**", "^")
        s2 = s2.replace("**", "^")
        c = (a+b)/2
        l = len(xs)
        if l % 2 != 0:
            xs.insert(l//2+1, xs[l//2])
        ys = [func(expr, xi) for xi in xs]
        fs = [func(s1, xi) for xi in xs[:l//2+1]] + [func(s2, xi) for xi in xs[l//2+1:]]
        if not redraw:
            plt.plot(xs, ys, label=("S"+str(n)))
            plt.plot(xs, fs, "--", label=("y = { " + s1[1:-1] + ", " + str(a) + "<=x<" + str(c) + ";\n" +
                                                     s2[1:-1] + ", " + str(c) + "<=x<=" + str(b) + " }"))
        else:
            fig, ax = plt.subplots(1, 1)
            ax.plot(xs, ys, label=("S"+str(n)))
            ax.plot(xs, fs, "--", label=("y = { " + s1[1:-1] + ", " + str(round(a, 5)) + "<=x<" + str(round(c, 5)) + ";\n" +
                                                     s2[1:-1] + ", " + str(round(c, 5)) + "<=x<=" + str(round(b, 5)) + " }"))
    plt.grid(True)
    plt.axis("square")
    plt.legend()
    plt.show()

def mistake(s, s1, s2, res_func, a, b, h):
    xs = [(a + h*i) for i in range(int((b-a)/h+1)) if round((a + h*i), 12) < round(b, 12)]
    l = len(xs)
    average_mistake = 0.0
    quadrum_mistake = 0.0
    if not (s is None) and s1 is None and s2 is None:
        for xi in xs:
            average_mistake += func("abs(" + s + " - (" + res_func + "))", xi)
            quadrum_mistake += func("(" + s + " - (" + res_func + "))**2", xi)
    elif s is None and not (s1 is None or s2 is None):
        if l % 2 != 0:
            xs.insert(l//2+1, xs[l//2])
        for xi in xs[:l//2+1]:
            average_mistake += func("abs(" + s1 + " - (" + res_func + "))", xi)
            quadrum_mistake += func("(" + s1 + " - (" + res_func + "))**2", xi)
        for xi in xs[l//2+1:]:
            average_mistake += func("abs(" + s2 + " - (" + res_func + "))", xi)
            quadrum_mistake += func("(" + s2 + " - (" + res_func + "))**2", xi)
    l = len(xs)
    average_mistake /= l
    quadrum_mistake = math.sqrt(quadrum_mistake / l / (l-1))
    return [average_mistake, quadrum_mistake]

# список формул
def formuls():
    messagebox.showinfo("Формулы", '''Тригонометрический ряд Фурье функции f(x) имеет следующий вид:
                        \nf(x) = a[0]/2 + Σ(a[i]*cos(ix) + b[i]*sin(ix)) | i = 1..n
                        \nЕсли f(x) раскладывается на отрезке [-π; π] по обеим функциям, то коэффициенты определяются следующим образом:
                        \na[0] = 1/π * (-π;π)∫ f(x) dx,
                        \na[n] = 1/π * (-π;π)∫ f(x)*cos(nx) dx,
                        \nb[n] = 1/π * (-π;π)∫ f(x)*sin(nx) dx.
                        \nЕсли только по косинусам (в случае чётности) на [0; π], то:
                        \na[n] = 2/π * (0;π)∫ f(x)*cos(nx) dx,
                        \nb[n] = 0.
                        \nЕсли только по синусам (в случае нечётности) на [0; π], то:
                        \na[n] = 0,
                        \nb[n] = 2/π * (0;π)∫ f(x)*sin(nx) dx.
                        \n
                        \nЕсли границы отрезка [-l; l], то коэффициенты определяются так:
                        \na[0] = 1/l * (-l;l)∫ f(x) dx,
                        \na[n] = 1/l * (-l;l)∫ f(x)*cos((n*π/l)*x) dx,
                        \nb[n] = 1/l * (-l;l)∫ f(x)*sin((n*π/l)*x) dx.
                        \nРяд в таком случае имеет вид:
                        \nf(x) = a[0]/2 + Σ(a[i]*cos((i*π/l)*x) + b[i]*sin(i*π/l)*x)) | i = 1..n''')