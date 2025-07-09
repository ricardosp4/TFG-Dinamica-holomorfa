import colorsys
from PIL import Image
import math, cmath
import numpy as np
import os

# === Parámetros generales ===
ancho, largo = 1000, 1000  # Tamaño de la imagen
N = 100  # Máximo de iteraciones
R = 100  # Radio de escape
a = -1/0.24  # Parámetro a
theta = 0.61517321588  # Rotación irracional
lambd = cmath.exp(2j * math.pi * theta)  # λ de módulo 1

# Región del plano complejo a visualizar
z_centro = complex(-2, 0)
r = 5.7
re_min, re_max = z_centro.real - r, z_centro.real + r
im_min, im_max = z_centro.imag - r, z_centro.imag + r
print(re_min, re_max, im_min, im_max)

# === Paleta de colores ===
def generar_paleta(n_colores):
    return [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / n_colores, 1, 1))
        for i in range(n_colores)
    ]

paleta = generar_paleta(N)

# === Función racional q_lambda,a(z) ===
def q(z, a, lambd):
    den = 1 - a*z
    if abs(den) < 1e-12:
        return complex('inf')
    return lambd * z**2 * (z - a) / den

# === Crear imagen ===
img = Image.new("RGB", (ancho, largo))
pixels = img.load()

# === Iteración punto a punto para colorear basins ===
for x in range(ancho):
    for y in range(largo):
        re = re_min + (x / (ancho)) * (re_max - re_min)
        im = im_min + (y / (largo)) * (im_max - im_min)
        z = complex(re, im)

        n = 0
        escaped = False
        while n < N:
            if abs(z) > R or abs(z) < 1e-4:
                escaped = True
                break
            z = q(z, a, lambd)
            n += 1

        pixels[x, y] = paleta[n % len(paleta)] if escaped else (0, 0, 0)

# === Dibujo de órbitas invariantes (líneas del anillo) ===
num_pasos_orbita = 20000
pc1 = (a**2 - cmath.sqrt(a**4 - 10*a**2 + 9) + 3) / (4*a)
print(pc1)
pc2 = (a**2 + cmath.sqrt(a**4 - 10*a**2 + 9) + 3) / (4*a)
print(pc2)

for seed in np.linspace(pc1, pc2, 4):
    z = complex(seed, 0)
    for _ in range(num_pasos_orbita):
        # Si z no es finito (inf o nan), cortamos esta órbita
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            break

        # Mapeo de punto z a píxel
        x = int((z.real - re_min) / (re_max - re_min) * (ancho-1))
        y = int((z.imag - im_min) / (im_max - im_min) * (largo-1))

        if 0 <= x < ancho and 0 <= y < largo:
            pixels[x, y] = (255, 255, 255)

        # Iteramos
        z = q(z, a, lambd)

        # Si escapa, cortamos también
        if abs(z) > R:
            break

# === Mostrar ===
img.show()

# Guardar si se desea
filename = f"herman_ring_a_{a}.png"
os.makedirs("imagenes", exist_ok=True)
img.save(os.path.join("imagenes", filename))
print(f"Imagen guardada como: imagenes/{filename}")