import colorsys
from PIL import Image
import os
import math, cmath
import numpy as np


def generar_paleta(n_colores):
    paleta = []
    for i in range(n_colores):
        hue = i / n_colores  # Valor entre 0.0 y 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)  # Saturación y valor al máximo
        paleta.append((int(r * 255), int(g * 255), int(b * 255)))
    return paleta


# Parámetros del conjunto de Julia
ancho, largo = 1000, 1000
N = 100

theta = (1 + math.sqrt(5)) / 2
lambd = cmath.exp(2j * math.pi * theta)


def f(z):
    return lambd * z + z ** 2


# Radio de escape
R = 100

# Crear imagen
img = Image.new("RGB", (ancho, largo))
pixels = img.load()

# Punto alrededor del cual centrar la imagen
z_centro = complex(0.4, 0.2)

# Tamaño del recuadro que quieres mostrar (zoom)
r = 1.5

# Ajustar límites del plano complejo
re_min, re_max = z_centro.real - r, z_centro.real + r
im_min, im_max = z_centro.imag - r, z_centro.imag + r
print(re_min, re_max, im_min, im_max)

paleta = (generar_paleta(N))

# Algoritmo de escape
for x in range(ancho):
    for y in range(largo):
        re = re_min + (x / ancho) * (re_max - re_min)
        im = im_min + (y / largo) * (im_max - im_min)
        z = complex(re, im)

        n = 0
        while abs(z) <= R and n < N:
            z = f(z)
            n += 1

        if n == N:  # Negro si no escapa
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = paleta[n % len(paleta)]


# Punto crítico
pc = -lambd / 2
for z in np.linspace(0, pc, 5):
    for i in range(10000):
        re, im = z.real, z.imag
        x = int((re - re_min) / (re_max - re_min) * ancho)
        y = int((im - im_min) / (im_max - im_min) * largo)

        if 0 <= x < ancho and 0 <= y < largo:
            pixels[x, y] = (255, 255, 255)

        z = f(z)

img.show()

filename = f"siegel_disk.png"
os.makedirs("imagenes", exist_ok=True)
img.save(os.path.join("imagenes", filename))

print(f"Imagen guardada como: imagenes/{filename}")
