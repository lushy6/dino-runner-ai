import pygame
from constants import CLAVES_CIELO, SOMBRA_TEXTO


def mezclar(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def color_cielo(t_dia):
    for i in range(len(CLAVES_CIELO) - 1):
        t0, a0, b0 = CLAVES_CIELO[i]
        t1, a1, b1 = CLAVES_CIELO[i + 1]
        if t0 <= t_dia <= t1:
            f = (t_dia - t0) / (t1 - t0)
            return mezclar(a0, a1, f), mezclar(b0, b1, f)
    return CLAVES_CIELO[0][1], CLAVES_CIELO[0][2]


def dibujar_gradiente(sup, arriba, abajo, rect):
    x, y, w, h = rect
    pasos = h // 2
    for i in range(pasos):
        f = i / max(1, pasos - 1)
        pygame.draw.rect(sup, mezclar(arriba, abajo, f), (x, y + i * 2, w, 2))


def texto_con_sombra(sup, fuente, texto, x, y, color, centrado=False):
    sombra = fuente.render(texto, True, SOMBRA_TEXTO)
    frente = fuente.render(texto, True, color)
    if centrado:
        x -= frente.get_width() // 2
    sup.blit(sombra, (x + 2, y + 2))
    sup.blit(frente, (x, y))


