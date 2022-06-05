import numpy as np
import sympy as sym
from tkinter import messagebox
from eval_expression import eval_expr

def func(s, x, t):
	try:
		return eval_expr(s, x, 0, t)
	except Exception:
		pass

def get_and_solve_equation(du_dt, k, d2u_dx2, mx, h, tau, ll, tt):
	x, t = sym.symbols("x t")
	fxt = str(du_dt - k**2 * d2u_dx2)

	xs = [(i*h)   for i in range(int(ll/h))   if round(i*h,   12) <= ll]
	ts = [(j*tau) for j in range(int(tt/tau)) if round(j*tau, 12) <= tt]
		
	ys = np.empty([len(ts), len(xs)])
	ys[0] = [func(mx, xs[i], 0.0) for i in range(len(xs))]
	for n in range(len(ts)):
		ys[n][0], ys[n][-1] = 0.0, 0.0

	for n in range(1, len(ts)):
		for i in range(1, len(xs)-1):
			ys[n][i] = ys[n-1][i] + tau * (ys[n-1][i+1] - 2*ys[n-1][i] + ys[n-1][i-1]) / h**2 + tau * func(fxt, xs[i], ts[n])
	return ys

def mistake(ys, real_func, h, tau, ll, tt):
	xs = [(i*h)   for i in range(int(ll/h))   if round(i*h,   12) <= ll]
	ts = [(j*tau) for j in range(int(tt/tau)) if round(j*tau, 12) <= tt]
	diff = 0.0

	us = np.empty([len(ts), len(xs)])
	for n in range(len(ts)):
		for i in range(len(xs)):
			us[n][i] = func(real_func, xs[i], ts[n])
			if us[n][i] != 0:
				diff += (us[n][i] - ys[n][i]) / us[n][i]
	
	return diff*100/len(ts)/len(xs)

# список формул
def formuls():
    messagebox.showinfo("Формулы", '''Явная схема предполагает итеративное разложение исходного ДУ 2-го порядка по числовым значениям:
	                    \ny[n+1][i] = y[n][i] + τ * (y[n][i+1] - 2*y[n][i] + y[n][i-1]) / h^2 + τ * f(x[i], t[n]),
						\nгде y[n][...] - уже вычисленные значения для x[n], t[...], τ и h - шаги для вычисления по времени и по координате.
						\n
						\nЧтобы разложение сходилось, требуется соблюдение спектрального признака устойчивости: τ/h^2 <= 1/2.''')