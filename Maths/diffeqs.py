import math
from tkinter import messagebox
from eval_expression import eval_expr
import sympy as sym
import matplotlib.pyplot as plt
plt.interactive(True)

def func(s, x, y):
	try:
		return eval_expr(s, x, y, 0)
	except Exception:
		pass

# создание списка иксов вверх от заданного
def going_up(x0, upx, tau):
	xs_to_plus = [x0]
	i = 1
	while round(x0+tau*i, 5) <= upx:
		xs_to_plus.append(round(x0+tau*i, 6))
		i += 1
	return [xs_to_plus, i]

# создание списка иксов вниз от заданного
def going_down(x0, lowx, tau):
	xs_to_minus = [x0]
	j = 1
	while round(x0-tau*j, 5) >= lowx:
		xs_to_minus.append(round(x0-tau*j, 6))
		j += 1
	return [xs_to_minus, j]

# численное решение с выбором метода внутри функции
def solve_equation(s, low, up, tau, x0, y0, variant):
	try:
		x, y, dx, dy = sym.symbols('x y dx dy')
		check_eq = s.count("=")
		if check_eq == 1 and low < up:
			if "y'" in s:
				s = s.replace("y'", "dy/dx")
			where_eq = s.find("=")
			f = sym.sympify(s[:where_eq])
			g = sym.sympify(s[(where_eq+1):])
			first_expr = sym.Eq(f, g)
			solutions = sym.solve(first_expr, (dy/dx))
			my_expr = [str(sol) for sol in solutions]

			ys_to_plus = []
			ys_to_minus = []
			ys = []

			if x0 >= low and x0 <= up:
				nums_to_plus = going_up(x0, up, tau)
				xs_to_plus = nums_to_plus[0]
				i = nums_to_plus[1]
				nums_to_minus = going_down(x0, low, tau)
				xs_to_minus = nums_to_minus[0]
				j = nums_to_minus[1]

				for a in range(len(my_expr)):
					ys_to_plus.append([y0])
					for m in range(1, i):
						if variant == 1:
							y_new = ys_to_plus[a][m-1] + func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])*tau
						elif variant == 2:
							k = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							y_new = ys_to_plus[a][m-1] + func(my_expr[a], xs_to_plus[m-1] + tau/2,  ys_to_plus[a][m-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = func(my_expr[a], xs_to_plus[m-1] + tau/3, ys_to_plus[a][m-1] + tau/3*k1)
							k3 = func(my_expr[a], xs_to_plus[m-1] + tau*2/3, ys_to_plus[a][m-1] + tau*2/3*k2)
							y_new = 1/4*(k1 + 3*k3)*tau + ys_to_plus[a][m-1]
						elif variant == 4:
							k1 = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = func(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k1)
							k3 = func(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k2)
							k4 = func(my_expr[a], xs_to_plus[m-1] + tau, ys_to_plus[a][m-1] + tau*k3)
							y_new = 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau + ys_to_plus[a][m-1]
						ys_to_plus[a].append(y_new)
				
					ys_to_minus.append([y0])
					for n in range(1, j):
						if variant == 1:
							y_new = ys_to_minus[a][n-1] - func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])*tau
						elif variant == 2:
							k = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							y_new = ys_to_minus[a][n-1] - func(my_expr[a], xs_to_minus[n-1] + tau/2,  ys_to_minus[a][n-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = func(my_expr[a], xs_to_minus[n-1] + tau/3, ys_to_minus[a][n-1] + tau/3*k1)
							k3 = func(my_expr[a], xs_to_minus[n-1] + tau*2/3, ys_to_minus[a][n-1] + tau*2/3*k2)
							y_new = ys_to_minus[a][n-1] - 1/4*(k1 + 3*k3)*tau
						elif variant == 4:
							k1 = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = func(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k1)
							k3 = func(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k2)
							k4 = func(my_expr[a], xs_to_minus[n-1] + tau, ys_to_minus[a][n-1] + tau*k3)
							y_new = ys_to_minus[a][n-1] - 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau
						ys_to_minus[a].append(y_new)
					ys_to_minus[a] = list(reversed(ys_to_minus[a][1:]))
					xs = xs_to_minus + xs_to_plus
					ys.append(ys_to_minus[a] + ys_to_plus[a])
				xs_to_minus = list(reversed(xs_to_minus[1:]))
				xs = xs_to_minus + xs_to_plus
				return [xs, ys]

			elif x0 < low:
				nums_to_plus = going_up(x0, up, tau)
				xs_to_plus = nums_to_plus[0]
				xs = [xn for xn in xs_to_plus if xn >= low]
				i = nums_to_plus[1]

				for a in range(len(my_expr)):
					ys_to_plus.append([y0])
					for m in range(1, i):
						if variant == 1:
							y_new = ys_to_plus[a][m-1] + func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])*tau
						elif variant == 2:
							k = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							y_new = ys_to_plus[a][m-1] + func(my_expr[a], xs_to_plus[m-1] + tau/2,  ys_to_plus[a][m-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = func(my_expr[a], xs_to_plus[m-1] + tau/3, ys_to_plus[a][m-1] + tau/3*k1)
							k3 = func(my_expr[a], xs_to_plus[m-1] + tau*2/3, ys_to_plus[a][m-1] + tau*2/3*k2)
							y_new = 1/4*(k1 + 3*k3)*tau + ys_to_plus[a][m-1]
						elif variant == 4:
							k1 = func(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = func(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k1)
							k3 = func(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k2)
							k4 = func(my_expr[a], xs_to_plus[m-1] + tau, ys_to_plus[a][m-1] + tau*k3)
							y_new = 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau + ys_to_plus[a][m-1]
						ys_to_plus[a].append(y_new)
					ys.append(ys_to_plus[a][-len(xs):])
				return [xs, ys]

			elif x0 > up:
				nums_to_minus = going_down(x0, low, tau)
				xs_to_minus = nums_to_minus[0]
				xs = [xn for xn in xs_to_minus if xn <= up]
				j = nums_to_minus[1]
				for a in range(len(my_expr)):
					ys_to_minus.append([y0])
					for n in range(1, j):
						if variant == 1:
							y_new = ys_to_minus[a][n-1] - func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])*tau
						elif variant == 2:
							k = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							y_new = ys_to_minus[a][n-1] - func(my_expr[a], xs_to_minus[n-1] + tau/2,  ys_to_minus[a][n-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = func(my_expr[a], xs_to_minus[n-1] + tau/3, ys_to_minus[a][n-1] + tau/3*k1)
							k3 = func(my_expr[a], xs_to_minus[n-1] + tau*2/3, ys_to_minus[a][n-1] + tau*2/3*k2)
							y_new = ys_to_minus[a][n-1] - 1/4*(k1 + 3*k3)*tau
						elif variant == 4:
							k1 = func(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = func(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k1)
							k3 = func(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k2)
							k4 = func(my_expr[a], xs_to_minus[n-1] + tau, ys_to_minus[a][n-1] + tau*k3)
							y_new = ys_to_minus[a][n-1] - 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau
						ys_to_minus[a].append(y_new)
					ys_to_minus[a] = list(reversed(ys_to_minus[a]))
					ys.append(ys_to_minus[a][:len(xs)])
				xs = list(reversed(xs))
				return [xs, ys]
	except Exception:
		pass


def graphic(numbers, variant, redraw):
	xs = numbers[0]
	ys = numbers[1]
	if variant == 1:
		plt.title("Метод Эйлера")
	elif variant == 2:
		plt.title("Предиктор-корректор")
	elif variant == 3:
		plt.title("Метод Рунге-Кутта 3 порядка")
	elif variant == 4:
		plt.title("Метод Рунге-Кутта 4 порядка")
	plt.grid(True)
	if not redraw:
		for a in range(len(ys)):
			plt.plot(xs, ys[a])
	else:
		fig, ax = plt.subplots(1, 1)
		for a in range(len(ys)):
			ax.plot(xs, ys[a])
	plt.axis("square")
	plt.show()

def mistake(numbers, an_sol):
	try:
		xs = numbers[0]
		ys_diff = numbers[1]
		ys_real = [func(an_sol, x, 0) for x in xs]
		if len(ys_diff) == 1:
			sum1 = 0.0
			sum2 = 0.0
			count = 0
			differences = []
			for i in range(len(xs)):
				if not (math.isnan(ys_diff[0][i]) or math.isnan(ys_real[i]) or
						math.isinf(ys_diff[0][i]) or math.isinf(ys_real[i]) or
						ys_diff[0][i] is None or ys_real[i] is None):
					differences.append(ys_diff[0][i] - ys_real[i])
			for d in differences:
					sum1 += math.fabs(d)
					sum2 += d**2
					count += 1
			average_mistake = sum1 / count
			quadrum_mistake = math.sqrt(sum2/count/(count-1))
			return [average_mistake, quadrum_mistake]
	except Exception:
		pass


def formuls():
	messagebox.showinfo("Формулы", '''Первым шагом из введённого уравнения явно выражается производная: dy/dx = f(x,y).
	                     \nЗатем она заменяется на разностное выражение (y[n+1] - y[n]) / τ, и дальше преобразования зависят от выбранного метода.
						 \n
	                     \nМетод Эйлера (ломаных):
	                     \n(y[n+1] - y[n]) / τ = f(x[n], y[n])
						 \n
						 \nПредиктор-корректор (один из методов Рунге-Кутта 2-го порядка):
						 \n(y[n+1] - y[n]) / τ = f(x[n] + tau/2, y[n] + (τ/2)*f(x[n], y[n]))
						 \n
						 \nМетод Рунге-Кутта 3-го порядка (разновидность):
						 \nk1 = f(x[n], y[n]);
						 \nk2 = f(x[n] + τ/3, y[n] + (τ/3)*k1);
						 \nk3 = f(x[n] + 2*τ/3, y[n] + (2*τ/3)*k2);
						 \n(y[n+1] - y[n]) / τ = 1/4 * (k1 + 3*k3)
						 \n
						 \nМетод Рунге-Кутта 4-го порядка (разновидность):
						 \nk1 = f(x[n], y[n]);
						 \nk2 = f(x[n] + τ/2, y[n] + (τ/2)*k1);
						 \nk3 = f(x[n] + τ/2, y[n] + (τ/2)*k2);
						 \nk4 = f(x[n] + τ, y[n] + τ*k3);
						 \n(y[n+1] - y[n] / τ = 1/6 * (k1 + 2*k2 + 2*k3 + k4)
						 \n
						 \nгде:
						 \nx[n], y[n] - известные текущие значения х и у;
						 \ny[n+1] - искомое значение функции в следующей точке;
						 \nτ - шаг вычислений;
						 \nk1, k2, k3, k4 - промежуточные коэффициенты.''')