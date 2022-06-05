import math
import sympy as sym
import seaborn as sns
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
import integrals
import integrating
import diffeqs
import fourier
import mathphys
from eval_expression import eval_expr

def clicked_integral():
    variant = selected1.get()
    s = txt_int.get()
    txt1_1.delete(1.0, END)
    txt1_2.delete(1.0, END)
    a = float(eval_expr(lim_down.get(), 0, 0, 0))
    b = float(eval_expr(lim_up.get(), 0, 0, 0))
    m = int(eval_expr(spin1.get(), 0, 0, 0))
    h = (b - a) / m
    res = integrals.integral(s, a, b, h, variant)
    result = round(res[0], 12)
    txt1_1.insert(INSERT, result)
    txt1_2.insert(INSERT, round(integrals.mistake(s, a, b, m, h, variant), 19))
    # передача данных для графика
    xs = res[1]
    ys = res[2]
    redraw = chk_state1_2.get()
    if chk_state1_1.get():
        integrals.graphic(s, a, m, h, xs, ys, variant, redraw)

def clicked_differential_equation():
    s = diffeq.get()
    s = s.replace("^", "**")
    variant = selected2.get()
    low = eval_expr(lower.get(), 0, 0, 0)
    up = eval_expr(upper.get(), 0, 0, 0)
    tau = 10**(int(spin2.get()))
    x0 = eval_expr(arg.get(), 0, 0, 0)
    y0 = eval_expr(mean.get(), 0, 0, 0)
    numbers = diffeqs.solve_equation(s, low, up, tau, x0, y0, variant)
        
    if chk_state2_1.get():
        f = open(r"numbers.txt", "a")
        f.write("x\n" + str(numbers[0]) + "\n")
        for a in range(len(numbers[1])):
            f.write("y[" + str(a) + "]\n" + str(numbers[1][a]) + "\n")
        f.close()
    txt2_1.delete(1.0, END)
    txt2_2.delete(1.0, END)
    redraw = chk_state2_2.get()
    diffeqs.graphic(numbers, variant, redraw)
    if chk_state2_3.get():
            differences = diffeqs.mistake(numbers, analytical_solution.get())
            txt2_1.insert(INSERT, str(differences[0]))
            txt2_2.insert(INSERT, str(differences[1]))
            
def clicked_fourier_row():
    variant_int = selected3.get()
    variant_row = sin_or_cos.get()
    kind_of_func = kind.get()
    if kind_of_func == 1:
        s = "(" + func1.get() + ")"
        s1 = s2 = None
        a = float(eval_expr(from1.get(), 0, 0, 0))
        b = float(eval_expr(to1.get(), 0, 0, 0))
    elif kind_of_func == 2:
        s = None
        s1 = "(" + func2_1.get() + ")"
        s2 = "(" + func2_2.get() + ")"
        a = float(eval_expr(from2.get(), 0, 0, 0))
        b = float(eval_expr(to2.get(), 0, 0, 0))
    n = int(count_members.get())
    h = float(eval_expr(step.get(), 0, 0, 0))
    if a != -b and variant_row == 1:
        messagebox.showerror("Внимание!", "Отрезок не симметричный!")
    elif a == 0 and variant_row == 1:
        messagebox.showerror("Внимание!", "Такие отрезки надо раскладывать либо по sin, либо по cos!")
    elif a != 0 and (variant_row == 2 or variant_row == 3):
        messagebox.showerror("Внимание!", "Такие отрезки надо раскладывать по обеим функциям!")
    elif a >= b:
        messagebox.showerror("Внимание!", "Неверный ввод данных!")
    else:
        res_func = fourier.fourier_row(s, s1, s2, a, b, h, n, variant_int, variant_row, kind_of_func)
        redraw = chk_state3_1.get()
        fourier.graphic(s, s1, s2, res_func, a, b, h, n, redraw)
        decomposition.delete(1.0, END)
        decomposition.insert(INSERT, res_func)
        difference = fourier.mistake(s, s1, s2, res_func, a, b, h)
        txt3_1.delete(1.0, END)
        txt3_2.delete(1.0, END)
        if chk_state3_2.get():
            if kind_of_func == 1:
                txt3_1.insert(INSERT, str(integrating.integral("abs(" + s + " - (" + res_func + "))", a, b, h, variant_int) / (b-a)))
                txt3_2.insert(INSERT, str(difference[1]))
            elif kind_of_func == 2:
                txt3_1.insert(INSERT, str(integrating.integral("abs(" + s1 + " - (" + res_func + "))", a, (a+b)/2, h, variant_int) / ((b-a)/2) +
                                          integrating.integral("abs(" + s2 + " - (" + res_func + "))", (a+b)/2, b, h, variant_int) / ((b-a)/2)))
                txt3_2.insert(INSERT, str(difference[1]))

def clicked_math_physics():
    try:
        du_dt = sym.sympify(du.get())
        k = sym.sympify(quot.get())
        d2u_dx2 = sym.sympify(d2u.get())
        mx = mu.get()
        h = float(step_x.get())
        tau = float(step_t.get())
        ll = float(lim_x.get())
        tt = float(lim_t.get())
        txt4.delete(1.0, END)
        data = mathphys.get_and_solve_equation(du_dt, k, d2u_dx2, mx, h, tau, ll, tt)
        sns.set_theme()
        ax = sns.heatmap(data, robust=True, xticklabels=10, yticklabels=False)
        ax.invert_yaxis()
        ax.set_xticks(range(data.shape[1]), labels=[round(i*h,   8) for i in range(int(ll/h))])
        ax.set_yticks(range(data.shape[0]), labels=[round(j*tau, 8) for j in range(int(tt/tau))])
        if chk_state4_1.get():
            real_func = real_solution.get()
            difference = mathphys.mistake(data, real_func, h, tau, ll, tt)
            txt4.insert(INSERT, str(difference))
        if chk_state4_2.get():
            f = open(r"heatmap.txt", "a")
            f.write("[")
            for n in range(data.shape[0]):
                f.write("[")
                for i in range(data.shape[1]):
                    f.write(str(data[n][i]) + " ")
                f.write("]\n")
            f.write("]\n\n")
            f.close()
    except Exception:
        pass


# информация о программе
def info():
    messagebox.showinfo("О программе", '''Данная программа является учебной и предназначена для приближённого выполнения различных математических вычислений.
                         \nФункции реализованы с помощью языка Python 3.9 и могут некорректно работать при неправильном вводе данных..
                         \nНе рекомендуется вводить выражения, не являющиеся математическими, в том числе команды для командной строки Windows и интерпретатора Python.
                         \nВ программе реализована защита от подобных выражений, однако создатель не несёт ответственности за некорректное использование приложения.''')

def help():
    messagebox.showinfo("Справка", '''I. Чтобы вычислить интеграл, необходимо:
                         \n1) выбрать формулу для подсчёта и указать точность вычисления - число частей, на которые разбивается отрезок;
                         \n2) нажать кнопку "Строить график" для вывода окна с графическим сравнением функции и выбранной квадратуры;
                         \n3) ввести функцию и пределы интегрирования;
                         \n4) нажать на кнопку "Вычислить".
                         \nО точности вычисления - см. в разделе "Формулы". Не вводите выражения, не являющиеся математическими! Это может быть небезопасно для работы программы и компьютера.
                         \nВнимание! Квадратуры могут давать сбои при сильном дроблении отрезка (m>100). Желательно проверять найденные значения. Большое количество частей отрезка может значительно замедлять работу программы.
                         \n
                         \nII. Чтобы найти численное решение дифференциального уравнения (решить задачу Коши), необходимо:
	                     \n1) выбрать способ решения и настроить точность вычислений;
						 \n2) ввести уравнение (или выбрать из выпадающего списка) и задать отрезок для построения графика;
						 \n3) поставить задачу Коши (точку, через которую должен проходить график);
						 \n4) настроить вывод значений в текстовый файл "numbers.txt" и подсчёт погрешности;
						 \n5) нажать кнопку "Решить".
						 \nСледите, чтобы данные были введены корректно. Если на отрезке функция имеет разрыв, задайте условие задачи Коши для других промежутков и постройте график кусочно.
                         \n
                         \nIII. Чтобы разложить произвольную функцию в тригонометрический ряд Фурье, необходимо:
                         \n1) выбрать метод вычисления интегралов и вид функции (целый или кусочный);
                         \n2) ввести границы отрезка, уравнение функции и значение шага для вычисления;
                         \n3) настроить перерисовку графика и вычисление погрешностей.
                         \nВ результате выведется выражение для функции через sin и cos, а также сравнение графиков исходной функции и разложения.
                         \nДля полного разложения отрезок должен быть симметричным относительно 0, для cos или sin - начинаться с 0. Раскладывать по косинусам лучше чётные функции, по синусам - нечётные.
                         \n
                         \nIV. Чтобы составить тепловую карту уравнения теплопроводности с производными функции u(x, t), необходимо:
                         \n1) ввести уравнения для первой производной по времени (∂u/∂t) и второй производной по координате (∂2u/∂x2);
                         \n2) задать коэффициент k, начальные условия вида μ(x) = u(x, 0), задать шаги и пределы вычислений по координате и по времени;
                         \n3) если вы хотите проверить тепловую карту на погрешность, введите точное решение и настройте вычисление с помощью кнопки;
                         \n4) для получения массива значений в файле "heatmap.txt" нажмите кнопку "Выводить в файл".
                         \nШаги подбирайте так, чтобы соблюдался спектральный признак устойчивости τ/h^2 <= 1/2, так как для решения используется явная схема.''')

# выход
def away():
    exit()


window = Tk()
window.title("Высшая математика")
window.geometry("650x360")
tab_control = ttk.Notebook(window)
color_style = ttk.Style()
color_style.configure("TFrame", background="#FFFFE0")
tab1 = ttk.Frame(tab_control, style="TFrame")  
tab2 = ttk.Frame(tab_control, style="TFrame")
tab3 = ttk.Frame(tab_control, style="TFrame")
tab4 = ttk.Frame(tab_control, style="TFrame")
tab_control.add(tab1, text="Интегралы")  
tab_control.add(tab2, text="Диффуры")
tab_control.add(tab3, text="Ряд Фурье")  
tab_control.add(tab4, text="Теплопроводность")

lbl1_1 = Label(tab1, text="Формула для вычисления:", font=("Calibri", 11), bg="#FFFFE0")  
lbl1_1.grid(column=0, row=1, columnspan=4)
selected1 = IntVar()
rad1_1 = Radiobutton(tab1, text="прямоугольников", font=("Calibri", 11), value=1, variable=selected1, bg="#FFFFE0")  
rad1_2 = Radiobutton(tab1, text="трапеций",        font=("Calibri", 11), value=2, variable=selected1, bg="#FFFFE0")  
rad1_3 = Radiobutton(tab1, text="Симпсона",        font=("Calibri", 11), value=3, variable=selected1, bg="#FFFFE0")  
rad1_1.grid(column=1, row=2)  
rad1_2.grid(column=2, row=2)  
rad1_3.grid(column=3, row=2)
lbl1_2 = Label(tab1, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", bg="#FFFFE0")  
lbl1_2.grid(column=0, row=3, columnspan=4)
lbl1_3 = Label(tab1, text="Разбиение на ", font=("Calibri", 11), bg="#FFFFE0")  
lbl1_3.grid(column=1, row=4)
var1 = IntVar()
var1.set(1)
spin1 = Spinbox(tab1, from_=1, to=10000, width=5, textvariable=var1)  
spin1.grid(column=2, row=4)
lbl1_4 = Label(tab1, text="частей", font=("Calibri", 11), bg="#FFFFE0")  
lbl1_4.grid(column=3, row=4)
chk_state1_1 = BooleanVar()  
chk_state1_1.set(True)
chk1 = Checkbutton(tab1, text="Строить график", var=chk_state1_1, bg="#FFFFE0")  
chk1.grid(column=0, row=4)
chk_state1_2 = BooleanVar()  
chk_state1_2.set(True)
chk1_2 = Checkbutton(tab1, text="Рисовать заново", var=chk_state1_2, bg="#FFFFE0")  
chk1_2.grid(column=0, row=5) 
lbl1_5 = Label(tab1, text="(При разбиении по Симпсону отрезок автоматически делится на 2m частей.)", font=("Calibri", 8), bg="#FFFFE0")
lbl1_5.grid(column=1, row=5, columnspan=4)
lbl1_6 = Label(tab1, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", bg="#FFFFE0")  
lbl1_6.grid(column=0, row=6, columnspan=4)
lbl1_7 = Label(tab1, text="Интеграл:", font=("Calibri", 13), bg="#FFFFE0")  
lbl1_7.grid(column=0, row=7, columnspan=4)
btn1 = Button(tab1, text="Вычислить", command=clicked_integral, bg="#C9FFC9")  
btn1.grid(column=3, row=7)
lbl1_8 = Label(tab1, text="∫", font=("Calibri", 13), bg="#FFFFE0")  
lbl1_8.grid(column=0, row=9)
lbl1_9 = Label(tab1, text=" dx = ", font=("Calibri", 13), bg="#FFFFE0")  
lbl1_9.grid(column=2, row=9)
lim_up = Entry(tab1, width=5)
lim_up.grid(column=0, row=8, padx=5)
lim_down = Entry(tab1, width=5)
lim_down.grid(column=0, row=10, padx=5)
txt_int = Entry(tab1, width=40)  
txt_int.grid(column=1, row=9)
txt1_1 = Text(tab1, width=20, height=1)
txt1_1.grid(column=3, row=9) 
lbl1_10 = Label(tab1, text="Погрешность:", font=("Calibri", 12), bg="#FFFFE0")  
lbl1_10.grid(column=1, row=11, columnspan=2)
txt1_2 = Text(tab1, width=20, height=1)
txt1_2.grid(column=3, row=11)

lbl2_1 = Label(tab2, text="Метод численного решения: ", font=("Calibri", 11), padx=5, bg="#FFFFE0")
lbl2_1.grid(column=0, row=0)
selected2 = IntVar()
rad2_1 = Radiobutton(tab2, text="Эйлера (ломаных)       ", font=("Calibri", 11), value=1, variable=selected2, justify="left", bg="#FFFFE0")
rad2_2 = Radiobutton(tab2, text="предиктор-корректор", font=("Calibri", 11), value=2, variable=selected2, justify="left", bg="#FFFFE0")
rad2_3 = Radiobutton(tab2, text="Рунге-Кутта 3 порядка", font=("Calibri", 11), value=3, variable=selected2, justify="left", bg="#FFFFE0")
rad2_4 = Radiobutton(tab2, text="Рунге-Кутта 4 порядка ", font=("Calibri", 11), value=4, variable=selected2, justify="left", bg="#FFFFE0")
rad2_1.grid(column=1, row=0, columnspan=4)
rad2_2.grid(column=5, row=0, columnspan=2)
rad2_3.grid(column=1, row=1, columnspan=4)
rad2_4.grid(column=5, row=1, columnspan=2)
lbl2_2 = Label(tab2, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", justify="left", bg="#FFFFE0", fg="#FFFFE0")
lbl2_2.grid(column=0, row=2, columnspan=8)
lbl2_3 = Label(tab2, text="Точность решения: ", font=("Calibri", 11), bg="#FFFFE0")
lbl2_3.grid(column=0, row=3)
lbl2_4 = Label(tab2, text="10 ^ ", font=("Calibri", 11), bg="#FFFFE0")
lbl2_4.grid(column=1, row=3)
var2 = IntVar()
var2.set(-2)
spin2 = Spinbox(tab2, from_=-5, to=-2, width=5, textvariable=var2, justify="left")  
spin2.grid(column=2, row=3)
btn2 = Button(tab2, text="Решить", bg="#C9FFC9", command=clicked_differential_equation)
btn2.grid(column=6, row=3)
lbl2_5 = Label(tab2, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", justify="left", bg="#FFFFE0", fg="#FFFFE0")
lbl2_5.grid(column=0, row=4, columnspan=7)
lbl2_6 = Label(tab2, text="Уравнение: ", font=("Calibri", 11), padx=5, bg="#FFFFE0")
lbl2_6.grid(column=0, row=5)
diffeq = Combobox(tab2, width=35, justify="left")
diffeq["values"] = (" ", "x*y' + x^2 + x*y - y = 0", "2*x*y' + y^2 = 1", "(2*x*y^2 - y)*dx + x*dy = 0",
					"y - y' = y^2 + x*y'", "(x + 2*y^3)*y' = y", "(y')^3 - (y')*e^(2*x) = 0", "x^2*y' = y*(x+y)",
					"(1-x^2)*dy + x*y*dx = 0", "(y')*2 + 2*(x-1)*y' - 2*y = 0", "y + (y')*(ln(y))^2 = (x + 2*ln(y))*y'",
					"x^2*y' - 2*x*y = 3*y", "y' = 1 / (x - y^2)",
					"(y')^3 + (3*x-6)*y' = 3*y", "x - y/y' = 2/y", "2*(y')^3 - 3*(y')^2 + x = y", "((x+y)^2) * y' = 1",
					"2*x^3*y*y' + 3*x^2*y^2 + 7 = 0", "dx/x = (1/y - 2*x)*dy", "x*y' = e^y + 2*y'", "2*(x - y^2)*dy = y*dx",
					"x^2*(y')^2 + y^2 = 2*x*(2 - y*y')", "dy + (x*y - x*y^3)*dx = 0", "2*x^2*y' = (y^2)*(2*x*y' - y)",
					"(y - x*y')/(x + y*y') = 2", "x*(x-1)*y' + 2*x*y = 1", "(1-x^2)*y' - 2*x*y^2 = x*y")
diffeq.grid(column=1, row=5, columnspan=5)
lbl2_7 = Label(tab2, text="Задача Коши: ", font=("Calibri", 11), bg="#FFFFE0")
lbl2_7.grid(column=0, row=6)
lbl2_8 = Label(tab2, text="у(", font=("Calibri", 11), bg="#FFFFE0")
lbl2_8.grid(column=1, row=6)
arg = Entry(tab2, width=5)
arg.grid(column=2, row=6)
lbl2_9 = Label(tab2, text=") = ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl2_9.grid(column=3, row=6)
mean = Entry(tab2, width=5)
mean.grid(column=4, row=6)
lbl2_10 = Label(tab2, text="Отрезок: ", font=("Calibri", 11), bg="#FFFFE0")
lbl2_10.grid(column=0, row=7)
lbl2_11 = Label(tab2, text="от", font=("Calibri", 11), bg="#FFFFE0")
lbl2_11.grid(column=1, row=7)
lower = Entry(tab2, width=10)
lower.grid(column=2, row=7)
lbl2_12 = Label(tab2, text="до", font=("Calibri", 11), bg="#FFFFE0")
lbl2_12.grid(column=3, row=7)
upper = Entry(tab2, width=10)
upper.grid(column=4, row=7)
chk_state2_1 = BooleanVar()
chk_state2_1.set(True)
chk_state2_2 = BooleanVar()
chk_state2_2.set(True)
chk_state2_3 = BooleanVar()
chk_state2_3.set(True)
chk2_1 = Checkbutton(tab2, text="Вывод в файл значений", variable=chk_state2_1, bg="#FFFFE0")
chk2_1.grid(column=0, row=8, pady=20)
chk2_2 = Checkbutton(tab2, text="Рисовать заново", variable=chk_state2_2, bg="#FFFFE0")
chk2_2.grid(column=1, row=8, columnspan=3)
chk2_3 = Checkbutton(tab2, text="Расчёт погрешности", variable=chk_state2_3, bg="#FFFFE0", justify="right")
chk2_3.grid(column=4, row=8, columnspan=3)
lbl2_13 = Label(tab2, text="Введите решение уравнения в явном виде:", font=("Calibri", 11), bg="#FFFFE0")
lbl2_13.grid(column=0, row=9, columnspan=3)
lbl2_14 = Label(tab2, text="y = ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl2_14.grid(column=3, row=9)
analytical_solution = Entry(tab2, width=30)
analytical_solution.grid(column=4, row=9, columnspan=3)
lbl2_15 = Label(tab2, text="Погрешность решения: ", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl2_15.grid(column=0, row=11, columnspan=3)
lbl2_16 = Label(tab2, text="средняя", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl2_16.grid(column=3, row=10, columnspan=2)
lbl2_17 = Label(tab2, text="среднекв.", font=("Calibri", 11), bg="#FFFFE0", justify="center")
lbl2_17.grid(column=5, row=10, columnspan=2)
txt2_1 = Text(tab2, width=15, height=1)  
txt2_1.grid(column=3, row=11, columnspan=2)
txt2_2 = Text(tab2, width=15, height=1)  
txt2_2.grid(column=5, row=11, columnspan=2)

lbl3_1 = Label(tab3, text="Интегрирование:", font=("Calibri", 11), bg="#FFFFE0")
lbl3_1.grid(column=0, row=0)
selected3 = IntVar()
rad3_1 = Radiobutton(tab3, text="прямоугольники",            font=("Calibri", 11), value=1, variable=selected3, justify="left", bg="#FFFFE0")
rad3_2 = Radiobutton(tab3, text="трапеции                ",  font=("Calibri", 11), value=2, variable=selected3, justify="left", bg="#FFFFE0")
rad3_3 = Radiobutton(tab3, text="Симпсон                  ", font=("Calibri", 11), value=3, variable=selected3, justify="left", bg="#FFFFE0")
rad3_1.grid(column=0, row=1)
rad3_2.grid(column=0, row=2)
rad3_3.grid(column=0, row=3)
lbl3_2 = Label(tab3, text="Отрезок:", font=("Calibri", 11), bg="#FFFFE0")
lbl3_2.grid(column=1, row=0, padx=10)
kind = IntVar()
rad3_4 = Radiobutton(tab3, text="целый      ", font=("Calibri", 11), value=1, variable=kind, justify="left", bg="#FFFFE0")
rad3_5 = Radiobutton(tab3, text="кусочный",    font=("Calibri", 11), value=2, variable=kind, justify="left", bg="#FFFFE0")
rad3_4.grid(column=1, row=1, padx=10)
rad3_5.grid(column=1, row=2, padx=10)
lbl3_3 = Label(tab3, text="от", font=("Calibri", 11), bg="#FFFFE0")
lbl3_4 = Label(tab3, text="до", font=("Calibri", 11), bg="#FFFFE0")
lbl3_3.grid(column=2, row=0, padx=20)
lbl3_4.grid(column=3, row=0, padx=5)
from1 = Entry(tab3, width=5)
from2 = Entry(tab3, width=5)
to1   = Entry(tab3, width=5)
to2   = Entry(tab3, width=5)
from1.grid(column=2, row=1, padx=20)
from2.grid(column=2, row=2, padx=20)
to1.grid(column=3, row=1, padx=5)
to2.grid(column=3, row=2, padx=5)
lbl3_5 = Label(tab3, text="f(x)", font=("Calibri", 11), bg="#FFFFE0")
lbl3_5.grid(column=4, row=0, padx=15, columnspan=2)
func1   = Entry(tab3, width=32)
func2_1 = Entry(tab3, width=15)
func2_2 = Entry(tab3, width=15)
func1.grid(column=4, row=1, padx=15, columnspan=2)
func2_1.grid(column=4, row=2, padx=15)
func2_2.grid(column=5, row=2)
sin_or_cos = IntVar()
row1 = Radiobutton(tab3, text="cos+sin", font=("Calibri", 11), value=1, variable=sin_or_cos, bg="#FFFFE0")
row2 = Radiobutton(tab3, text="cos    ", font=("Calibri", 11), value=2, variable=sin_or_cos, bg="#FFFFE0")
row3 = Radiobutton(tab3, text="sin    ", font=("Calibri", 11), value=3, variable=sin_or_cos, bg="#FFFFE0")
row1.grid(column=2, row=3, columnspan=2)
row2.grid(column=4, row=3)
row3.grid(column=5, row=3)
lbl3_6 = Label(tab3, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", fg="#FFFFE0", bg="#FFFFE0")
lbl3_6.grid(column=0, row=4, columnspan=6)
lbl3_7 = Label(tab3, text="Число членов ряда Фурье:", font=("Calibri", 11), bg="#FFFFE0")
lbl3_7.grid(column=0, row=5, columnspan=2)
members = IntVar()
members.set(2)
count_members = Spinbox(tab3, from_=2, to=15, width=5, textvariable=members)
count_members.grid(column=2, row=5)
lbl3_8 = Label(tab3, text="                Шаг:", font=("Calibri", 11), justify="right", bg="#FFFFE0")
lbl3_8.grid(column=4, row=5)
step = Entry(tab3, width=10, justify="left")
step.grid(column=5, row=5)
lbl3_9 = Label(tab3, text="                          f(x) ~", font=("Calibri", 11), justify="right", bg="#FFFFE0")
lbl3_9.grid(column=0, row=6)
decomposition = Text(tab3, width=45, height=4, font=('Calibri', 10))
decomposition.grid(column=1, row=6, padx=5, pady=10, columnspan=4)
btn3 = Button(tab3, text="Разложение", bg="#C9FFC9", command=clicked_fourier_row)
btn3.grid(column=5, row=6, pady=10)
chk_state3_1 = BooleanVar()  
chk_state3_1.set(True)
chk3_1 = Checkbutton(tab3, text="Рисовать заново", font=("Calibri", 11), variable=chk_state3_1, bg="#FFFFE0")  
chk3_1.grid(column=0, row=8, columnspan=2)
chk_state3_2 = BooleanVar()  
chk_state3_2.set(True)
chk3_2 = Checkbutton(tab3, text="Погрешности:", font=("Calibri", 11), variable=chk_state3_2, bg="#FFFFE0")
chk3_2.grid(column=2, row=8, columnspan=2)
lbl3_10 = Label(tab3, text="средняя", font=("Calibri", 11), bg="#FFFFE0")
lbl3_10.grid(column=4, row=7)
lbl3_11 = Label(tab3, text="ср.-квадр.", font=("Calibri", 11), bg="#FFFFE0")
lbl3_11.grid(column=5, row=7)
txt3_1 = Text(tab3, width=12, height=1)  
txt3_1.grid(column=4, row=8)
txt3_2 = Text(tab3, width=12, height=1)  
txt3_2.grid(column=5, row=8)

lbl4_1 = Label(tab4, text="Решение уравнений вида: ∂u/∂t = k^2 * ∂2u/∂x2 + f(x, t)", font=("Calibri, 11"), bg="#FFFFE0")
lbl4_1.grid(column=0, row=0, columnspan=8)
lbl4_2 = Label(tab4, text=". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", fg="#FFFFE0", bg="#FFFFE0")
lbl4_2.grid(column=0, row=1, columnspan=5)
lbl4_3 = Label(tab4, text="     ∂u/∂t = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_3.grid(column=0, row=2)
du = Entry(tab4, width=30)
du.grid(column=1, row=2, columnspan=2)
lbl4_4 = Label(tab4, text="∂2u/∂x2 = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_4.grid(column=0, row=3)
d2u = Entry(tab4, width=30)
d2u.grid(column=1, row=3, columnspan=2)
lbl4_5 = Label(tab4, text="                    k = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_5.grid(column=3, row=2)
quot = Entry(tab4, width=20)
quot.grid(column=4, row=2, columnspan=2)
lbl4_6 = Label(tab4, text="μ(x) = u(x, 0) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_6.grid(column=3, row=3)
mu = Entry(tab4, width=20)
mu.grid(column=4, row=3, columnspan=2)
lbl4_7 = Label(tab4, text="    f(x, t) = ", font=("Calibri, 11"), bg="#FFFFE0")
lbl4_7.grid(column=0, row=4)
lbl4_8 = Label(tab4, text="        ∂u/∂t - k^2 * ∂2u/∂x2", font=("Calibri, 11"), bg="#FFFFE0")
lbl4_8.grid(column=1, row=4)
lbl4_9 = Label(tab4, text="u(0, t) = u(l, t) = 0", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_9.grid(column=3, row=4)
lbl4_10 = Label(tab4, text="Шаги:", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_10.grid(column=0, row=5, rowspan=2, pady=12)
lbl4_11 = Label(tab4, text="h(x) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_11.grid(column=1, row=5, pady=12)
lbl4_12 = Label(tab4, text="τ(t) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_12.grid(column=1, row=6)
step_x = Entry(tab4, width=10, justify="left")
step_x.grid(column=2, row=5, pady=12)
step_t = Entry(tab4, width=10, justify="left")
step_t.grid(column=2, row=6)
lbl4_13 = Label(tab4, text="Пределы:", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_13.grid(column=3, row=5, rowspan=2, pady=12)
lbl4_14 = Label(tab4, text="l(x) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_14.grid(column=4, row=5, pady=12)
lbl4_15 = Label(tab4, text="T(t) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="center")
lbl4_15.grid(column=4, row=6)
lim_x = Entry(tab4, width=10, justify="center")
lim_x.grid(column=5, row=5, pady=12)
lim_t = Entry(tab4, width=10, justify="center")
lim_t.grid(column=5, row=6)
lbl4_16 = Label(tab4, text="Точное решение: u(x, t) = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_16.grid(column=0, row=7, columnspan=2, pady=25)
real_solution = Entry(tab4, width=35)
real_solution.grid(column=2, row=7, columnspan=2, pady=25)
btn4 = Button(tab4, text="Построить", font=("Calibri, 11"), bg="#C9FFC9", command=clicked_math_physics)
btn4.grid(column=5, row=7)
chk_state4_1 = BooleanVar()  
chk_state4_1.set(True)
chk4_1 = Checkbutton(tab4, text="Считать погрешность", font=("Calibri, 11"), bg="#FFFFE0")
chk4_1.grid(column=0, row=8, columnspan=2)
lbl4_17 = Label(tab4, text="        δ = ", font=("Calibri, 11"), bg="#FFFFE0", justify="right")
lbl4_17.grid(column=2, row=8)
txt4 = Text(tab4, width=20, height=1)
txt4.grid(column=3, row=8)
lbl4_18 = Label(tab4, text="%        ", font=("Calibri, 11"), bg="#FFFFE0", justify="left")
lbl4_18.grid(column=4, row=8)
chk_state4_2 = BooleanVar()  
chk_state4_2.set(True)
chk4_2 = Checkbutton(tab4, text="       Выводить в файл", font=("Calibri, 11"), bg="#FFFFE0")
chk4_2.grid(column=0, row=9, columnspan=2)

menu = Menu(window)  
new_item1 = Menu(menu, tearoff=0)  
new_item1.add_command(label="О программе", command=info)
new_item1.add_command(label="Справка", command=help)
new_item1.add_separator()
new_item1.add_command(label="Выход", command=away)
menu.add_cascade(label="Помощь", menu=new_item1)
new_item2 = Menu(menu, tearoff=0)  
new_item2.add_command(label="Интегралы", command=integrals.formuls)
new_item2.add_command(label="Дифференциальные уравнения", command=diffeqs.formuls)
new_item2.add_command(label="Ряды Фурье", command=fourier.formuls)
new_item2.add_command(label="Уравнения теплопроводности", command=mathphys.formuls)
menu.add_cascade(label="Формулы", menu=new_item2)
window.config(menu=menu)  

tab_control.pack(expand=1, fill="both")  
window.mainloop()