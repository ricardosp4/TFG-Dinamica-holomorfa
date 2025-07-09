import cmath
import os
from PIL import Image, ImageDraw

# ============================
# PARÁMETROS DE CONFIGURACIÓN
# ============================

re_min, re_max = -2, 5
im_min, im_max = -2, 2
ancho, alto = 1400, 800
max_iter = 300
eps = 1e-3
esc = 1 / eps

# Guardado de imagen
output_path = "imagenes/espacio_parametros_criticos.png"
save_image = True  # Cambiar a True si se desea guadar

# Elegir valor de alpha
alpha = complex(2.6, 0)

# ============================
# FUNCIONES DEL MÉTODO
# ============================

def O_p(z, alpha):
    num = z ** 3 * (z - 2 * (alpha - 1))
    den = 1 - 2 * z * (alpha - 1)
    if abs(den) < 1e-10:
        return 1e6
    return num / den


def puntos_fijos_extras(alpha):
    raiz = cmath.sqrt(4 * alpha ** 2 - 12 * alpha + 5)
    s1 = (2 * alpha - 3 - raiz) / 2
    s2 = (2 * alpha - 3 + raiz) / 2
    return s1, s2


def iterar(z0, alpha):
    z = z0
    s1, s2 = puntos_fijos_extras(alpha)
    for _ in range(max_iter):
        if abs(z) < eps:
            return '0'
        elif abs(z - s1) < eps:
            return 's1'
        elif abs(z - s2) < eps:
            return 's2'
        elif abs(z) > esc:
            return 'inf'
        z = O_p(z, alpha)
    return 'none'


def color_gradiente(label):
    if label == '0':
        return 255, 40, 40  # naranja
    elif label == 's1':
        return 250, 250, 20  # amarillo
    elif label == 's2':
        return 50, 200, 50  # verde
    elif label == 'inf':
        return 80, 80, 255  # azul
    else:
        return 0, 0, 0


# ============================
# FUNCIÓN PARA DIBUJAR EL PLANO
# ============================

# Parámetros del disco D_2
center = 3
radius = 0.5


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

            label = iterar(z0, alpha)
            color = color_gradiente(label)
            img.putpixel((x, y), color)

    # Dibujar puntos fijos
    s1, s2 = puntos_fijos_extras(alpha)
    puntos_atractores = [0, s1, s2]
    puntos_repulsores = [1]

    radio = 5
    for pf in puntos_atractores:
        x_pf, y_pf = coord_a_pixel(pf, re_min, re_max, im_min, im_max, ancho, alto)
        draw.ellipse((x_pf - radio, y_pf - radio, x_pf + radio, y_pf + radio), fill=(0, 0, 0))

    for pf in puntos_repulsores:
        x_pf, y_pf = coord_a_pixel(pf, re_min, re_max, im_min, im_max, ancho, alto)
        draw.rectangle((x_pf - radio, y_pf - radio, x_pf + radio, y_pf + radio), fill=(0, 0, 0))

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
