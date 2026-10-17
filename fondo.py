import random
import math
import pygame
from constants import ANCHO, SUELO_Y, ALTO
from utils import mezclar, color_cielo, dibujar_gradiente
from constants import HILLS_FAR, HILLS_NEAR, SOL, LUNA


class Fondo:
    def __init__(self):
        self.t_dia = 0.05
        self.cuadro = 0
        self.estrellas = [
            (
                random.randint(0, ANCHO),
                random.randint(0, SUELO_Y - 90),
                random.uniform(0, math.tau),
            )
            for _ in range(60)
        ]
        self.nubes = []
        for _ in range(5):
            self.nubes.append(
                [
                    random.randint(0, ANCHO),
                    random.randint(30, 130),
                    random.uniform(0.7, 1.4),
                    random.uniform(0.2, 0.5),
                ]
            )
        self.off_lejos = 0.0
        self.off_cerca = 0.0
        self._cielo = pygame.Surface((ANCHO, SUELO_Y))
        self._cielo_clave = -1
        self.perfil_lejos = [random.randint(55, 95) for _ in range(7)]
        self.perfil_cerca = [random.randint(35, 70) for _ in range(10)]

    @property
    def luz(self):
        return (math.cos(self.t_dia * math.tau) + 1) / 2

    def actualizar(self, velocidad):
        self.cuadro += 1
        self.t_dia = (self.t_dia + 0.00010) % 1.0
        for nube in self.nubes:
            nube[0] -= nube[3]
            if nube[0] < -120:
                nube[0] = ANCHO + 60
                nube[1] = random.randint(30, 130)
                nube[2] = random.uniform(0.7, 1.4)
        self.off_lejos = (self.off_lejos + velocidad * 0.10) % (ANCHO + 200)
        self.off_cerca = (self.off_cerca + velocidad * 0.28) % (ANCHO + 200)

    def _dibujar_montanas(self, sup, perfil, offset, base_y, color):
        ancho_seg = (ANCHO + 200) / len(perfil)
        puntos = [(-200, base_y)]
        for repeticion in range(2):
            for i, alto in enumerate(perfil):
                cx = -offset + repeticion * (ANCHO + 200) + i * ancho_seg
                puntos.append((cx, base_y - alto))
        puntos.append((ANCHO + 200, base_y))
        puntos.append((ANCHO + 200, ALTO))
        puntos.append((-200, ALTO))
        pygame.draw.polygon(sup, color, puntos)

    def _dibujar_nube(self, sup, x, y, escala, alpha):
        w, h = int(90 * escala), int(46 * escala)
        nube = pygame.Surface((w, h), pygame.SRCALPHA)
        col = (255, 255, 255, alpha)
        pygame.draw.ellipse(nube, col, (0, h * 0.4, w * 0.6, h * 0.6))
        pygame.draw.ellipse(nube, col, (w * 0.25, h * 0.15, w * 0.5, h * 0.7))
        pygame.draw.ellipse(nube, col, (w * 0.45, h * 0.35, w * 0.55, h * 0.6))
        sup.blit(nube, (x, y))

    def dibujar(self, sup):
        clave = int(self.t_dia * 400)
        if clave != self._cielo_clave:
            self._cielo_clave = clave
            arriba, abajo = color_cielo(self.t_dia)
            dibujar_gradiente(self._cielo, arriba, abajo, (0, 0, ANCHO, SUELO_Y))
        sup.blit(self._cielo, (0, 0))

        if self.luz < 0.55:
            intensidad = (0.55 - self.luz) / 0.55
            for ex, ey, fase in self.estrellas:
                brillo = 0.5 + 0.5 * math.sin(self.cuadro * 0.05 + fase)
                v = int(255 * intensidad * brillo)
                if v > 12:
                    pygame.draw.circle(sup, (v, v, v), (ex, ey), 1)

        dd = (self.t_dia + 0.25) % 1.0
        if dd < 0.5:
            f = dd / 0.5
            sx = int(-40 + (ANCHO + 80) * f)
            sy = int((SUELO_Y - 40) - math.sin(math.pi * f) * 150)
            glow = pygame.Surface((140, 140), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 244, 200, 70), (70, 70), 70)
            sup.blit(glow, (sx - 70, sy - 70))
            pygame.draw.circle(sup, SOL, (sx, sy), 26)
        else:
            f = (dd - 0.5) / 0.5
            mx = int(-40 + (ANCHO + 80) * f)
            my = int((SUELO_Y - 40) - math.sin(math.pi * f) * 150)
            pygame.draw.circle(sup, LUNA, (mx, my), 22)
            pygame.draw.circle(
                sup, mezclar(LUNA, (40, 50, 90), 0.5), (mx + 8, my - 6), 18
            )

        far = mezclar(HILLS_FAR, (40, 48, 80), 1 - self.luz)
        near = mezclar(HILLS_NEAR, (32, 44, 70), 1 - self.luz)
        self._dibujar_montanas(sup, self.perfil_lejos, self.off_lejos, SUELO_Y + 6, far)
        self._dibujar_montanas(
            sup, self.perfil_cerca, self.off_cerca, SUELO_Y + 12, near
        )

        alpha = int(70 + 150 * self.luz)
        for x, y, escala, _ in self.nubes:
            self._dibujar_nube(sup, x, y, escala, alpha)


