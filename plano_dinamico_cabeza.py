import cmath
import os
from PIL import Image, ImageDraw

# ========================
# CONFIGURACIÓN GLOBAL
# ========================

# Tamaño y dominio del plano complejo
re_min, re_max = -1.7, 2.6
im_min, im_max = -1.7, 1.7
ancho, alto = int((re_max - re_min) * 400), int((im_max - im_min) * 400)

# Iteración y precisión
max_iter = 150
eps = 1e-4
esc = 1 / eps

# Guardado de imagen
output_path = "imagenes/esp_din.png"
save_image = True  # Cambiar a False si no se quiere guardar

# Elegir valor de alpha
alpha = complex(2.2, 0.2)

# ========================
# FUNCIONES
# ========================

def O_p(z, alpha):
    """Iteración del método de orden superior con parámetro alpha."""
    num = z ** 3 * (z - 2 * (alpha - 1))
    den = 1 - 2 * z * (alpha - 1)
    if abs(den) < 1e-10:
        return 1e10  # Para evitar división por cero
    return num / den


def iterar(z0, alpha):
    """Itera desde z0 y clasifica el destino: 0, 1, infinito, otro."""
    z = z0
    for _ in range(max_iter):
        if abs(z) < eps:
            return 255, 80, 80
        elif abs(z - 1) < eps:
            return 80, 255, 80
        elif abs(z) > esc:
            return 80, 80, 255
        z = O_p(z, alpha)
    return 0, 0, 0


def coord_a_pixel(z, re_min, re_max, im_min, im_max, ancho, alto):
    """Convierte coordenadas complejas a píxeles de imagen."""
    x = int((z.real - re_min) / (re_max - re_min) * ancho)
    y = int((z.imag - im_min) / (im_max - im_min) * alto)
    return x, y


def generar_imagen(alpha):
    """Genera la imagen del plano dinámico para un valor de alpha."""
    img = Image.new("RGB", (ancho, alto), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    for x in range(ancho):
        for y in range(alto):
            re = re_min + (x / ancho) * (re_max - re_min)
            im = im_min + (y / alto) * (im_max - im_min)
            z0 = complex(re, im)

            color = iterar(z0, alpha)
            img.putpixel((x, y), color)

    # Dibujar puntos fijos
    puntos = [0, 1]
    radio = 8
    for pf in puntos:
        x_pf, y_pf = coord_a_pixel(pf, re_min, re_max, im_min, im_max, ancho, alto)
        draw.ellipse((x_pf - radio, y_pf - radio, x_pf + radio, y_pf + radio), fill=(255, 255, 255))

    raiz = cmath.sqrt(4 * alpha ** 2 - 12 * alpha + 5)
    s1 = (2 * alpha - 3 - raiz) / 2
    s2 = (2 * alpha - 3 + raiz) / 2
    puntos = [s1, s2]
    radio = 5
    for pf in puntos:
        x_pf, y_pf = coord_a_pixel(pf, re_min, re_max, im_min, im_max, ancho, alto)
        draw.rectangle((x_pf - radio, y_pf - radio, x_pf + radio, y_pf + radio), fill=(255, 255, 255))

    return img


# ========================
# EJECUCIÓN
# ========================

if __name__ == "__main__":
    # Generar imagen para el valor dado
    imagen = generar_imagen(alpha)
    imagen.show()

    # Guardar imagen si está activado
    if save_image:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Cambiar el nombre de salida con el valor de alpha
        alpha_str = f"alpha_{alpha.real:.2f}_{alpha.imag:+.2f}".replace('.', 'p').replace('+', 'p').replace('-', 'm')
        filename = f"esp_din_{alpha_str}.png"
        full_path = os.path.join(os.path.dirname(output_path), filename)

        imagen.save(full_path)
        print(f"Imagen guardada en: {full_path}")

