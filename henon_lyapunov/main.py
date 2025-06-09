import numpy as np
import matplotlib.pyplot as plt


def henon(x, y, a=1.4, b=0.3):
    x_next = 1 - a * x**2 + y
    y_next = b * x
    return x_next, y_next


def henon_jacobian(x, a=1.4, b=0.3):
    return np.array([[-2 * a * x, 1], [b, 0]])


def max_lyapunov_exponent(x0, y0, a=1.4, b=0.3, iterations=10000, discard=1000):
    x, y = x0, y0
    v = np.array([1.0, 0.0])
    lyapunov_sum = 0.0
    count = 0

    for i in range(iterations):
        x_next, y_next = henon(x, y, a, b)

        if abs(x_next) > 1e6 or abs(y_next) > 1e6:
            return np.nan

        if i >= discard:
            J = henon_jacobian(x, a, b)
            v_next = J @ v
            norm_v_next = np.linalg.norm(v_next)

            if norm_v_next > 0:
                lyapunov_sum += np.log(norm_v_next)
                v = v_next / norm_v_next
                count += 1
            else:
                return 0.0

        x, y = x_next, y_next

    if count == 0:
        return np.nan

    return lyapunov_sum / count


x_min, x_max, num_x = -1.25, 1.25, 400
y_min, y_max, num_y = -0.45, 0.45, 300

x_vals = np.linspace(x_min, x_max, num_x)
y_vals = np.linspace(y_min, y_max, num_y)
lyapunov_map = np.zeros((num_y, num_x))

print("program dziala, ale licze na liczydle... prosze o cierpliwosc")
for i, y_val in enumerate(y_vals):
    for j, x_val in enumerate(x_vals):
        lyapunov_map[i, j] = max_lyapunov_exponent(x_val, y_val, iterations=1500, discard=500)
    if (i+1) % (num_y // 10) == 0:
      print(f"status zamowienia: {((i+1)/num_y)*100:.0f}%")


attractor_x = []
attractor_y = []
x_attr, y_attr = 0.1, 0.1
attractor_pts = 50000
attractor_discard = 1000

for _ in range(attractor_pts + attractor_discard):
    x_attr, y_attr = henon(x_attr, y_attr)
    if _ >= attractor_discard:
        attractor_x.append(x_attr)
        attractor_y.append(y_attr)


plt.figure(figsize=(10, 8))

plt.imshow(np.flipud(lyapunov_map), extent=[x_min, x_max, y_min, y_max],
           aspect='auto', cmap='plasma', vmin=0.25, vmax=0.55)

cbar = plt.colorbar(label='najwiekszy wykladnik lapunowa ($\\lambda_{max}$)')
# cbar.set_ticks(np.linspace(0, np.nanmax(lyapunov_map[lyapunov_map > 0]), 6))
cbar.set_ticks(np.arange(0.30, 0.60, 0.05))

plt.scatter(attractor_x, attractor_y, s=0.1, color='black', alpha=0.5, label='pan henon')
# plt.plot(attractor_x, attractor_y, 'ko', markersize=0.02, alpha=0.3, label='pan henon')

plt.xlabel('$x$')
plt.ylabel('$y$')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.legend()
# plt.grid(True, linestyle=':', alpha=0.5)
plt.grid(False)
plt.show()
