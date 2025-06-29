import cmath
import os
from PIL import Image
import colorsys

# ================================
# CONFIGURACIÓN Y PARÁMETROS
# ================================

# Tamaño y rango del plano complejo
re_min, re_max = -0.4, 4.6
im_min, im_max = -2.0, 2.0
ancho, alto = 1500, 1200

# Iteración y precisión
max_iter = 150
tol = 1e-4
tol_inf = 1 / tol

# Guardado de imagen
output_path = "imagenes/espacio_parametros_criticos.png"
save_image = True  # Cambiar a True si se desea guadar


# ================================
# FUNCIONES AUXILIARES
# ================================

def generar_paleta(n_colores):
    """Genera una paleta de colores arcoíris en HSV convertidos a RGB."""
    return [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / n_colores, 1, 1))
        for i in range(n_colores)
    ]


def c_plus(alpha):
    """Calcula el punto crítico c_2 en función del parámetro alpha."""
    try:
        num = 3 - 4 * alpha + 2 * alpha ** 2
        radicando = -6 * alpha + 19 * alpha ** 2 - 16 * alpha ** 3 + 4 * alpha ** 4
        raiz = cmath.sqrt(radicando)
        den = 3 * (alpha - 1)

        if abs(den) < 1e-12:
            return None
        return (num + raiz) / den

    except Exception:
        return None


def O_p(z, alpha):
    """Aplica una iteración del método de orden superior."""
    num = z ** 3 * (z - 2 * (alpha - 1))
    den = 1 - 2 * z * (alpha - 1)
    if abs(den) < 1e-12:
        return 1e10
    return num / den


# ================================
# GENERACIÓN DE LA IMAGEN
# ================================

def generar_imagen():
    paleta = generar_paleta(max_iter)
    img = Image.new("RGB", (ancho, alto))
    pixels = img.load()

    for x in range(ancho):
        for y in range(alto):
            re = re_min + (x / ancho) * (re_max - re_min)
            im = im_max - (y / alto) * (im_max - im_min)
            alpha = complex(re, im)

            z = c_plus(alpha)
            if z is None:
                pixels[x, y] = (0, 0, 0)
                continue

            n = 0
            while n < max_iter:
                if abs(z) < tol or abs(z) > tol_inf:
                    break
                z = O_p(z, alpha)
                n += 1

            # Color según la velocidad de escape/convergencia
            if n == max_iter:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = paleta[n % len(paleta)]

    return img


# ================================
# EJECUCIÓN
# ================================

if __name__ == "__main__":
    imagen = generar_imagen()
    imagen.show()

    if save_image:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        imagen.save(output_path)
        print(f"Imagen guardada en: {output_path}")
