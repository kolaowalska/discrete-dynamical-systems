import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def logistic_map(r, x):
    return r * x * (1 - x)


def bifurcation_diagram():
    n = 10000
    discard = n // 2

    # krok 0.001
    r_values = np.linspace(0, 4, 1001)

    r_axis = []
    x_axis = []

    for r in r_values:
        x = np.random.random()
        for i in range(n):
            x = logistic_map(r, x)
            if i >= discard:
                r_axis.append(r)
                x_axis.append(x)

    print("done")
    plt.figure(figsize=(20, 10))
    plt.plot(r_axis, x_axis, ',k', alpha=0.25)
    plt.xlabel('r')
    plt.ylabel('x')
    plt.title('diagram bifurkacyjny')
    plt.show()


bifurcation_diagram()
