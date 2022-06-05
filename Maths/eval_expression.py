## -*- coding: 1251 -*-
import math
import sympy as sym

def eval_expr(s, x, y, t):
	allowed_names = {"x": x, "y": y, "t": t, "п": sym.pi, "pi": sym.pi, "abs": math.fabs,
					 "е": math.e, "e": math.e, "sqrt": sym.sqrt, "ln": sym.ln, "log": sym.log,
					 "sin": sym.sin, "cos": sym.cos, "tg": sym.tan, "ctg": sym.cot, "sec": sym.sec, "cosec": sym.csc,
					 "sh": sym.sinh, "ch": sym.cosh, "th": sym.tanh, "cth": sym.coth, "sech": sym.sech, "cosech": sym.csch,
					 "arcsin": sym.asin, "arccos": sym.acos, "arctg": sym.atan, "arcctg": sym.acot, "arcsec": sym.asec, "arccosec": sym.acsc,
					 "arsh": sym.asinh, "arch": sym.acosh, "arth": sym.atanh, "arcth": sym.acoth, "arsech": sym.asech, "arcosech": sym.acsch}
	try:
		s = s.replace("^", "**")
		code = compile(s, "<string>", "eval")
		for name in code.co_names:
			if name not in allowed_names:
				pass
		return eval(code, {"__builtins__": {}}, allowed_names)
	except Exception:
		pass
