import math
import random

is_deg = True
is_2nd = False

def toggle_deg(btn):
    global is_deg
    is_deg = not is_deg
    btn.config(text="deg" if is_deg else "rad")

def toggle_2nd(btns):
    global is_2nd
    is_2nd = not is_2nd
    btns["sin"].config(text="sin⁻¹" if is_2nd else "sin")
    btns["cos"].config(text="cos⁻¹" if is_2nd else "cos")
    btns["tan"].config(text="tan⁻¹" if is_2nd else "tan")

def trig_insert(fn, insert):
    if not is_2nd:
        insert(fn + "(")
    else:
        if fn == "sin": insert("asin(")
        if fn == "cos": insert("acos(")
        if fn == "tan": insert("atan(")

def factorial(n):
    if n < 0 or int(n) != n:
        return float("nan")
    return math.factorial(int(n))

def prepare(expr):
    expr = expr.replace("^", "**")
    expr = expr.replace("pi", str(math.pi))
    expr = expr.replace("e", str(math.e))

    if is_deg:
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        expr = expr.replace("asin(", "math.degrees(math.asin(")
        expr = expr.replace("acos(", "math.degrees(math.acos(")
        expr = expr.replace("atan(", "math.degrees(math.atan(")
    else:
        expr = expr.replace("sin(", "math.sin(")
        expr = expr.replace("cos(", "math.cos(")
        expr = expr.replace("tan(", "math.tan(")
        expr = expr.replace("asin(", "math.asin(")
        expr = expr.replace("acos(", "math.acos(")
        expr = expr.replace("atan(", "math.atan(")

    expr = expr.replace("ln(", "math.log(")
    expr = expr.replace("lg(", "math.log10(")
    return expr

def evaluate(expr):
    if expr.endswith("!"):
        return factorial(float(expr[:-1]))
    return eval(prepare(expr))

def rand():
    return str(random.random())
