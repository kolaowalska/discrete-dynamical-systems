from matplotlib import pyplot as plt
import numpy as np


def cobweb(f_str, x0, n, a, b):
    f_str = f_str.replace('^', '**')
    # f = lambda x: eval(f_str, {"x": x, "np": np})
    allowed_f = {"np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                     "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "abs": np.abs}
    try:
        f = lambda x: eval(f_str, {"__builtins__": {}}, {**allowed_f, "x": x})
    except Exception as e:
        print(f"obrzydliwa funkcja! blad parsowania: {e}")
        return

    x = np.linspace(a, b, 1000)
    try:
        y = f(x)
    except Exception as e:
        print(f"blad obliczen dla f(x): {e}")
        return

    plt.figure(figsize=(8, 8), facecolor='thistle')
    plt.plot(x, y, color='darkorchid', label=r'$f(x)$')
    plt.plot(x, x, color='lightpink', linestyle='dashed', label=r'$y = x$')

    xvals = [x0]
    yvals = [a]

    for i in range(n):
        try:
            xnew = f(xvals[-1])
            if not np.isfinite(xnew):
                print(f"bomba w {i}: wywalilo w kosmos ({xnew}). ABORT EVALUATION!!!")
                break
        except Exception as e:
            print(f"upsii w {i}: mathematica is running... {e} - ???. quit kernel!!")
            break
        xvals.extend([xvals[-1], xnew])
        yvals.extend([xnew, xnew])

    plt.plot(xvals, yvals, color='mediumvioletred', linestyle='dotted', alpha=0.7)

    plt.scatter([x0], [a], color='indigo', zorder=5)
    plt.annotate(r'$x_0$', (x0, a), textcoords="offset points", xytext=(5, 5), fontsize=12)

    plt.xlim([a, b])
    plt.ylim([a, b])
    plt.legend()
    plt.show()


# cobweb("3.5 * x * (1 - x)", 0.2, 250, 0, 1)

f_str = input("wpisuj funkcje!!!! ")
a = float(input("a = "))
b = float(input("b = "))
n = int(input("liczba iteracji n = "))
x0 = float(input("x0 = "))

cobweb(f_str, x0, n, a, b)
