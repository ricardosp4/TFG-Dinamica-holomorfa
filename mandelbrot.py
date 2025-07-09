import colorsys
from PIL import Image, ImageDraw
import math
import os

def generar_paleta(n_colores):
    paleta = []
    for i in range(n_colores):
        hue = i / n_colores
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        paleta.append((int(r * 255), int(g * 255), int(b * 255)))
    return paleta

# Parámetros de la imagen
ancho, alto = 1600, 1200
N = 75     # Máximo número de iteraciones
R = 2.5    # Radio de escape estándar para Mandelbrot

# Crear imagen
img = Image.new("RGB", (ancho, alto))
pixels = img.load()

# Dominio: rectángulo que contiene M

z_centro = complex(-0.62, 0)
r = 1.75

re_min, re_max = z_centro.real - r, z_centro.real + r
im_min, im_max = z_centro.imag - r * (alto/ancho), z_centro.imag + r * (alto/ancho)

paleta = generar_paleta(N)

for x in range(ancho):
    for y in range(alto):
        # Convertir coordenadas de píxel a número complejo c
        re = re_min + (x / ancho) * (re_max - re_min)
        im = im_max - (y / alto) * (im_max - im_min)
        c = complex(re, im)

        z = 0
        n = 0
        while abs(z) <= R and n < N:
            z = z**2 + c
            n += 1

        if n == N:
            pixels[x, y] = (0, 0, 0)  # Pertenece a M (negro)
        else:
            pixels[x, y] = paleta[n % len(paleta)]  # Escapó (coloreado)

img.show()

# Guardar imagen
os.makedirs("imagenes", exist_ok=True)
img.save("imagenes/mandelbrot.png")
