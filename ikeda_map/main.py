import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Ikeda map
def ikeda_map(x, y, u):
    t = 0.4 - 6 / (1 + x**2 + y**2)
    x1 = 1 + u * (x * np.cos(t) - y * np.sin(t))
    y1 = u * (x * np.sin(t) + y * np.cos(t))
    return x1, y1


# Trajectory generator
def generate_trajectory(u, steps=50000, discard=1000):
    x, y = 0.0, 0.0
    points = []
    for i in range(steps):
        x, y = ikeda_map(x, y, u)
        if i >= discard:
            points.append((x, y))
    return np.array(points)


# u values
u_values = np.arange(0.6, 1.001, 0.001)

# Precompute trajectories for all u
print("Precomputing trajectories...")
trajectories = [generate_trajectory(u) for u in u_values]

# Setup plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
sc = ax.scatter([], [], s=0.1, color='black')


def update(frame):
    data = trajectories[frame]
    sc.set_offsets(data)
    ax.set_title(f"Ikeda attractor (u = {u_values[frame]:.3f})")
    return [sc]


# Animate
ani = FuncAnimation(fig, update, frames=len(u_values), interval=30, blit=True)

# Save as GIF (safe fallback)
ani.save("ikeda_attractor.gif", writer='pillow', fps=30)
