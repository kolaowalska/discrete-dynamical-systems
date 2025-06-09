import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def garfield_map(img, iterations):
    N = img.shape[0]
    assert img.shape[0] == img.shape[1]

    result = img.copy()
    for _ in range(iterations):
        new_img = np.zeros_like(result)
        for y in range(N):
            for x in range(N):
                x_new = (x + y) % N
                y_new = (x + 2 * y) % N
                new_img[x_new, y_new] = result[y, x]
        result = new_img
    return result


image_path = "gafielf.png"
# image_path = "garfiels.png"
image = Image.open(image_path).resize((200, 200)).convert('RGB')
image_np = np.array(image)

iterations = 150
transformed_image = garfield_map(image_np, iterations)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("garfield przed:")
plt.imshow(image_np)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title(f"garfield po {iterations} iteracjach:")
plt.imshow(transformed_image)
plt.axis('off')
plt.show()
