import numpy as np
import matplotlib.pyplot as plt


def sin_r(x, r_param):
    return r_param * np.sin(np.pi * x)


def dsin_r(x, r_param):
    return r_param * np.pi * np.cos(np.pi * x)


r_min = 0.0
r_max = 1.0
r_points = 2500
r_values = np.linspace(r_min, r_max, r_points)

bifurcation_discard = 1000
points_to_plot = 250

lyapunov_discard = 1000
lyapunov_iterations = 2500

x0 = 0.5

bif_r_plot = []
bif_x_plot = []
exponents = np.zeros(r_points)

for r_idx, r_val in enumerate(r_values):
    if r_idx % (r_points // 10) == 0:
        print(f"gotuje dla r = {r_val:.2f} ({r_idx}/{r_points})")

    x_bif = x0
    for _ in range(bifurcation_discard):
        x_bif = sin_r(x_bif, r_val)

    orbit = x_bif
    for _ in range(points_to_plot):
        orbit = sin_r(orbit, r_val)
        bif_r_plot.append(r_val)
        bif_x_plot.append(orbit)

    x_lyapunov = x0
    for _ in range(lyapunov_discard):
        x_lyapunov = sin_r(x_lyapunov, r_val)

    current_sum = 0.0
    aux = x_lyapunov

    if r_val == 0:
        exponents[r_idx] = -np.inf
    else:
        valid = 0
        for _ in range(lyapunov_iterations):
            derivative = dsin_r(aux, r_val)
            log_term = np.log(np.abs(derivative) + 1e-13)

            if np.isfinite(log_term):
                current_sum += log_term
                valid += 1
            else:
                current_sum += -30
                valid += 1

            aux = sin_r(aux, r_val)
            if not np.isfinite(aux):
                exponents[r_idx] = np.nan
                break

        if valid > 0 and np.isfinite(exponents[r_idx]):
            exponents[r_idx] = current_sum / valid
        elif not np.isfinite(exponents[r_idx]):
            pass
        else:
            exponents[r_idx] = np.nan


plot_values = np.array(exponents)
indices = np.isfinite(plot_values)

# to jest przepalowane troszke
if np.any(indices):
    finite_min = np.min(plot_values[indices])
    plot_values[np.isneginf(plot_values)] = finite_min - 1.0
else:
    plot_values[np.isneginf(plot_values)] = -5.0
    finite_min = -5.0


fig, ax = plt.subplots(2, 1, sharex=True, figsize=(12, 10))

# diagram bifurkacyjny
ax[0].scatter(bif_r_plot, bif_x_plot, s=0.05, c='k', alpha=0.15)
ax[0].set_ylabel('$x_n$', fontsize=14)
ax[0].set_ylim(-0.05, 1.05)
ax[0].set_xlim(r_min, r_max)
ax[0].grid(True, linestyle=':', alpha=0.5)

# wykres wykladnika lapunowa
ax[1].plot(r_values, plot_values, 'b-', linewidth=1.5, label='$\\lambda(r)$')
ax[1].axhline(0, color='g', linestyle='dotted', linewidth=1, label='$\\lambda=0$')
ax[1].set_ylabel('$\\lambda(r)$', fontsize=14)
ax[1].set_xlabel('$r$', fontsize=14)

maximum = np.nanmax(plot_values[indices]) if np.any(indices) else 0.0
minimum = np.nanmin(plot_values)

plot_max = 0.5
if maximum > 0.0:
    plot_max = maximum + 0.1 * abs(maximum) + 0.1
elif maximum > -0.1:
    plot_max = 0.2

plot_min = max(minimum if np.isfinite(minimum) else -4.0, -4.0)

ax[1].set_ylim(plot_min, plot_max)
ax[1].grid(True, linestyle=':', alpha=0.5)
ax[1].legend(fontsize=12)

plt.tight_layout(pad=1.5)
plt.show()
