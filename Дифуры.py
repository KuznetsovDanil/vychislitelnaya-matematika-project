## -*- coding: 1251 -*-
import math
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sympy as sym
import matplotlib.pyplot as plt
plt.interactive(True)

# преобразование текстового выражения в математическое
def eval_expr(s, x, y):
	allowed_names = {"x": x, "y": y, "п": sym.pi, "pi": sym.pi, "abs": math.fabs,
					 "е": math.e, "e": math.e, "sqrt": sym.sqrt, "ln": sym.ln, "log": sym.log,
					 "sin": sym.sin, "cos": sym.cos, "tg": sym.tan, "ctg": sym.cot,
					 "sh": sym.sinh, "ch": sym.cosh, "th": sym.tanh, "cth": sym.coth,
					 "arcsin": sym.asin, "arccos": sym.acos, "arctg": sym.atan, "arcctg": sym.acot,
					 "arsh": sym.asinh, "arch": sym.acosh, "arth": sym.atanh, "arcth": sym.acoth}
	try:
		s = s.replace("^", "**")
		code = compile(s, "<string>", "eval")
		for name in code.co_names:
			if name not in allowed_names:
				pass
		return eval(code, {"__builtins__": {}}, allowed_names)
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
def get_and_prepair_equation(variant):
	try:
		s = diffeq.get()
		x, y, dx, dy = sym.symbols('x y dx dy')
		s = s.replace("^", "**")
		check_eq = s.count("=")
		low = eval_expr(lower.get(), 0, 0)
		up = eval_expr(upper.get(), 0, 0)
		tau = 10**(int(spin.get()))
		x0 = eval_expr(arg.get(), 0, 0)
		y0 = eval_expr(mean.get(), 0, 0)
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
							y_new = ys_to_plus[a][m-1] + eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])*tau
						elif variant == 2:
							k = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							y_new = ys_to_plus[a][m-1] + eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2,  ys_to_plus[a][m-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/3, ys_to_plus[a][m-1] + tau/3*k1)
							k3 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau*2/3, ys_to_plus[a][m-1] + tau*2/3*k2)
							y_new = 1/4*(k1 + 3*k3)*tau + ys_to_plus[a][m-1]
						elif variant == 4:
							k1 = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k1)
							k3 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k2)
							k4 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau, ys_to_plus[a][m-1] + tau*k3)
							y_new = 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau + ys_to_plus[a][m-1]
						ys_to_plus[a].append(y_new)
				
					ys_to_minus.append([y0])
					for n in range(1, j):
						if variant == 1:
							y_new = ys_to_minus[a][n-1] - eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])*tau
						elif variant == 2:
							k = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							y_new = ys_to_minus[a][n-1] - eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2,  ys_to_minus[a][n-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/3, ys_to_minus[a][n-1] + tau/3*k1)
							k3 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau*2/3, ys_to_minus[a][n-1] + tau*2/3*k2)
							y_new = ys_to_minus[a][n-1] - 1/4*(k1 + 3*k3)*tau
						elif variant == 4:
							k1 = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k1)
							k3 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k2)
							k4 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau, ys_to_minus[a][n-1] + tau*k3)
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
							y_new = ys_to_plus[a][m-1] + eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])*tau
						elif variant == 2:
							k = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							y_new = ys_to_plus[a][m-1] + eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2,  ys_to_plus[a][m-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/3, ys_to_plus[a][m-1] + tau/3*k1)
							k3 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau*2/3, ys_to_plus[a][m-1] + tau*2/3*k2)
							y_new = 1/4*(k1 + 3*k3)*tau + ys_to_plus[a][m-1]
						elif variant == 4:
							k1 = eval_expr(my_expr[a], xs_to_plus[m-1], ys_to_plus[a][m-1])
							k2 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k1)
							k3 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau/2, ys_to_plus[a][m-1] + tau/2*k2)
							k4 = eval_expr(my_expr[a], xs_to_plus[m-1] + tau, ys_to_plus[a][m-1] + tau*k3)
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
							y_new = ys_to_minus[a][n-1] - eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])*tau
						elif variant == 2:
							k = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							y_new = ys_to_minus[a][n-1] - eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2,  ys_to_minus[a][n-1] + tau/2*k) * tau
						elif variant == 3:
							k1 = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/3, ys_to_minus[a][n-1] + tau/3*k1)
							k3 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau*2/3, ys_to_minus[a][n-1] + tau*2/3*k2)
							y_new = ys_to_minus[a][n-1] - 1/4*(k1 + 3*k3)*tau
						elif variant == 4:
							k1 = eval_expr(my_expr[a], xs_to_minus[n-1], ys_to_minus[a][n-1])
							k2 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k1)
							k3 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau/2, ys_to_minus[a][n-1] + tau/2*k2)
							k4 = eval_expr(my_expr[a], xs_to_minus[n-1] + tau, ys_to_minus[a][n-1] + tau*k3)
							y_new = ys_to_minus[a][n-1] - 1/6*(k1 + 2*k2 + 2*k3 + k4)*tau
						ys_to_minus[a].append(y_new)
					ys_to_minus[a] = list(reversed(ys_to_minus[a]))
					ys.append(ys_to_minus[a][:len(xs)])
				xs = list(reversed(xs))
				return [xs, ys]
	except Exception:
		messagebox.showerror("Внимание!", "Ошибка!")


def graphic(numbers):
	xs = numbers[0]
	ys = numbers[1]
	variant = selected.get()
	if variant == 1:
		plt.title("Метод Эйлера")
	elif variant == 2:
		plt.title("Предиктор-корректор")
	elif variant == 3:
		plt.title("Метод Рунге-Кутта 3 порядка")
	elif variant == 4:
		plt.title("Метод Рунге-Кутта 4 порядка")
	plt.grid(True)
	for a in range(len(ys)):
		plt.plot(xs, ys[a])
	plt.axis("square")
	plt.show()

if_file = 0
if_count_mistake = 0

def if_write():
	global if_file
	if chkb.get() == 0:
		if_file = 0
	elif chkb.get() == 1:
		if_file = 1

def if_mistake():
	global if_count_mistake
	if chkb1.get() == 0:
		if_count_mistake = 0
	elif chkb1.get() == 1:
		if_count_mistake = 1

def mistake(numbers):
	try:
		xs = numbers[0]
		ys_diff = numbers[1]
		ys_real = [eval_expr(analytical_solution.get(), x, 0) for x in xs]
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
			txt.insert(INSERT, average_mistake)
			txt2.insert(INSERT, quadrum_mistake)
	except ZeroDivisionError:
		txt.insert(INSERT, "nan")
		txt2.insert(INSERT, "nan")
	except Exception:
		pass

def clicked():
	variant = selected.get()
	numbers = get_and_prepair_equation(variant)

	global if_file, if_count_mistake
	if if_file == 1:
		f = open(r"numbers.txt", "a")
		f.write("x\n" + str(numbers[0]) + "\n")
		for a in range(len(numbers[1])):
			f.write("y[" + str(a) + "]\n" + str(numbers[1][a]) + "\n")
		f.close()
	txt.delete(1.0, END)
	txt2.delete(1.0, END)
	if if_count_mistake == 1:
		mistake(numbers)
	graphic(numbers)

def info():
	messagebox.showinfo("О программе", '''Данная программа является учебной и предназначена для численного решения дифференциальных уравнений 1-го порядка различными способами.
                         \nФункции реализованы с помощью языка Python 3.9 на основании методических указаний в задании и могут некорректно работать при неверно введённых данных.
                         \nНе рекомендуется вводить выражения, не являющиеся математическими, в том числе команды для командной строки Windows и интерпретатора Python.
                         \nВ программе реализована защита от подобных выражений, однако создатель не несёт ответственности за некорректное использование приложения.''')

def help():
	messagebox.showinfo("Помощь", '''Чтобы найти численное решение дифференциального уравнения (решить задачу Коши), необходимо:
	                     \n1) выбрать способ решения;
	                     \n2) настроить точность вычислений;
						 \n3) ввести уравнение (или выбрать из выпадающего списка);
						 \n4) задать отрезок для построения графика;
						 \n5) поставить задачу Коши (точку, через которую должен проходить график);
						 \n6) настроить вывод значений в текстовый файл и подсчёт погрешности;
						 \n7) нажать кнопку "Решить".
						 \nСледите, чтобы данные были введены корректно. В противном случае программа предупредит об ошибке.
						 \nЕсли на отрезке функция имеет разрыв, задайте условие задачи Коши для других промежутков и постройте график кусочно.''')

def formuls():
	messagebox.showinfo("Формулы", '''Первым шагом из введённого уравнения явно выражается производная: dy/dx = f(x,y).
	                     \nЗатем она заменяется на разностное выражение (y[n+1] - y[n]) / tau, и дальше преобразования зависят от выбранного метода.
						 \n
	                     \nМетод Эйлера (ломаных):
	                     \n(y[n+1] - y[n]) / tau = f(x[n], y[n])
						 \n
						 \nПредиктор-корректор (один из методов Рунге-Кутта 2-го порядка):
						 \n(y[n+1] - y[n]) / tau = f(x[n] + tau/2, y[n] + (tau/2)*f(x[n], y[n]))
						 \n
						 \nМетод Рунге-Кутта 3-го порядка (разновидность):
						 \nk1 = f(x[n], y[n]);
						 \nk2 = f(x[n] + tau/3, y[n] + (tau/3)*k1);
						 \nk3 = f(x[n] + 2*tau/3, y[n] + (2*tau/3)*k2);
						 \n(y[n+1] - y[n]) / tau = 1/4 * (k1 + 3*k3)
						 \n
						 \nМетод Рунге-Кутта 4-го порядка (разновидность):
						 \nk1 = f(x[n], y[n]);
						 \nk2 = f(x[n] + tau/2, y[n] + (tau/2)*k1);
						 \nk3 = f(x[n] + tau/2, y[n] + (tau/2)*k2);
						 \nk4 = f(x[n] + tau, y[n] + tau*k3);
						 \n(y[n+1] - y[n] / tau = 1/6 * (k1 + 2*k2 + 2*k3 + k4)
						 \n
						 \nгде:
						 \nx[n], y[n] - известные текущие значения х и у;
						 \ny[n+1] - искомое значение функции в следующей точке;
						 \ntau - шаг вычислений;
						 \nk1, k2, k3, k4 - промежуточные коэффициенты.''')

# выход
def away():
    exit()


window = Tk()
window.title("Дифференциальные уравнения")
window.geometry("600x350")
window.configure(bg="#FFFFE0")

lbl1 = Label(text="Метод численного решения: ", font=("Calibri", 11), padx=5, bg="#FFFFE0")
lbl1.grid(column=0, row=0)

selected = IntVar()
rad1 = Radiobutton(window, text="Эйлера (ломаных)   ", font=("Calibri", 11), value=1, variable=selected, justify="left", bg="#FFFFE0")
rad2 = Radiobutton(window, text="предиктор-корректор", font=("Calibri", 11), value=2, variable=selected, justify="left", bg="#FFFFE0")
rad3 = Radiobutton(window, text="Рунге-Кутта 3 пор. ", font=("Calibri", 11), value=3, variable=selected, justify="left", bg="#FFFFE0")
rad4 = Radiobutton(window, text="Рунге-Кутта 4 пор. ", font=("Calibri", 11), value=4, variable=selected, justify="left", bg="#FFFFE0")
rad1.grid(column=1, row=0, columnspan=4)
rad2.grid(column=5, row=0, columnspan=2)
rad3.grid(column=1, row=1, columnspan=4)
rad4.grid(column=5, row=1, columnspan=2)

lbl2 = Label(text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", justify="left", bg="#FFFFE0", fg="#FFFFE0")
lbl2.grid(column=0, row=2, columnspan=8)
lbl3 = Label(text="Точность решения: ", font=("Calibri", 11), bg="#FFFFE0")
lbl3.grid(column=0, row=3)
lbl4 = Label(text="10 ^ ", font=("Calibri", 11), bg="#FFFFE0")
lbl4.grid(column=1, row=3)

var = IntVar()
var.set(-2)
spin = Spinbox(window, from_=-5, to=-2, width=5, textvariable=var, justify="left")  
spin.grid(column=2, row=3)

btn = Button(window, text="Решить", bg="#C9FFC9", command=clicked)
btn.grid(column=6, row=3)

lbl5 = Label(text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", justify="left", bg="#FFFFE0", fg="#FFFFE0")
lbl5.grid(column=0, row=4, columnspan=7)
lbl6 = Label(text="Уравнение: ", font=("Calibri", 11), padx=5, bg="#FFFFE0")
lbl6.grid(column=0, row=5)

diffeq = Combobox(window, width=35, justify="left")
diffeq["values"] = (" ", "x*y' + x^2 + x*y - y = 0", "2*x*y' + y^2 = 1", "(2*x*y^2 - y)*dx + x*dy = 0",
					"y - y' = y^2 + x*y'", "(x + 2*y^3)*y' = y", "(y')^3 - (y')*e^(2*x) = 0", "x^2*y' = y*(x+y)",
					"(1-x^2)*dy + x*y*dx = 0", "(y')*2 + 2*(x-1)*y' - 2*y = 0", "y + (y')*(ln(y))^2 = (x + 2*ln(y))*y'",
					"x^2*y' - 2*x*y = 3*y", "y' = 1 / (x - y^2)",
					"(y')^3 + (3*x-6)*y' = 3*y", "x - y/y' = 2/y", "2*(y')^3 - 3*(y')^2 + x = y", "((x+y)^2) * y' = 1",
					"2*x^3*y*y' + 3*x^2*y^2 + 7 = 0", "dx/x = (1/y - 2*x)*dy", "x*y' = e^y + 2*y'", "2*(x - y^2)*dy = y*dx",
					"x^2*(y')^2 + y^2 = 2*x*(2 - y*y')", "dy + (x*y - x*y^3)*dx = 0", "2*x^2*y' = (y^2)*(2*x*y' - y)",
					"(y - x*y')/(x + y*y') = 2", "x*(x-1)*y' + 2*x*y = 1", "(1-x^2)*y' - 2*x*y^2 = x*y")
diffeq.grid(column=1, row=5, columnspan=5)

lbl7 = Label(text="Задача Коши: ", font=("Calibri", 11), bg="#FFFFE0")
lbl7.grid(column=0, row=6)
lbl8 = Label(text="у(", font=("Calibri", 11), bg="#FFFFE0")
lbl8.grid(column=1, row=6)
arg = Entry(window, width=5)
arg.grid(column=2, row=6)
lbl9 = Label(text=") = ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl9.grid(column=3, row=6)
mean = Entry(window, width=5)
mean.grid(column=4, row=6)

lbl10 = Label(text="Отрезок: ", font=("Calibri", 11), bg="#FFFFE0")
lbl10.grid(column=0, row=7)
lbl11 = Label(text="от", font=("Calibri", 11), bg="#FFFFE0")
lbl11.grid(column=1, row=7)
lower = Entry(window, width=10)
lower.grid(column=2, row=7)
lbl12 = Label(text="до", font=("Calibri", 11), bg="#FFFFE0")
lbl12.grid(column=3, row=7)
upper = Entry(window, width=10)
upper.grid(column=4, row=7)

chkb = IntVar()
chkb.set(0)
chk = Checkbutton(window, text="Вывод в файл значений", variable=chkb, onvalue=1, offvalue=0, command=if_write, bg="#FFFFE0")
chk.grid(column=0, row=8, pady=20)

chkb1 = IntVar()
chkb1.set(0)
chk1 = Checkbutton(window, text="Расчёт погрешности", variable=chkb1, onvalue=1, offvalue=0, command=if_mistake, bg="#FFFFE0", justify="right")
chk1.grid(column=4, row=8, columnspan=3)

lbl13 = Label(text="Введите решение уравнения в явном виде:", font=("Calibri", 11), bg="#FFFFE0")
lbl13.grid(column=0, row=9, columnspan=3)
lbl14 = Label(text="y = ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl14.grid(column=3, row=9)
analytical_solution = Entry(window, width=30)
analytical_solution.grid(column=4, row=9, columnspan=3)

lbl15 = Label(window, text="Погрешность решения: ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl15.grid(column=0, row=11, columnspan=3)
lbl16 = Label(window, text="средняя", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl16.grid(column=3, row=10, columnspan=2)
lbl17 = Label(window, text="среднекв.", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl17.grid(column=5, row=10, columnspan=2)
txt = Text(window, width=15, height=1)  
txt.grid(column=3, row=11, columnspan=2)
txt2 = Text(window, width=15, height=1)  
txt2.grid(column=5, row=11, columnspan=2)

menu = Menu(window)  
new_item = Menu(menu, tearoff=0)
new_item.add_command(label="О программе")
new_item.add_command(label="Помощь")
new_item.add_command(label="Формулы")
new_item.add_separator()
new_item.add_command(label="Выход", command=away)
menu.add_cascade(label="Справка", menu=new_item)
window.config(menu=menu)

window.mainloop()