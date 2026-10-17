import random
import pygame
from constants import (
    ANCHO, SUELO_Y, DINO_X, VEL_INICIAL, VEL_CANGREJO,
    PAJARO_NIVELES, CANGREJO_VEL, FOSO_ANCHO, METEORO_G, METEORO_BANDAS,
    CACTUS, CACTUS_BORDE, PAJARO, PAJARO_ALA, PAJARO_PICO,
    SUELO_TIERRA2, SUELO_LINEA,
)
from utils import mezclar


class Obstaculo:
    def __init__(self, tipo, x, nivel=None, velocidad=VEL_INICIAL):
        self.tipo = tipo
        self.nivel = nivel
        self.x = float(x)
        self.cuadro = 0
        if tipo == "bajo":
            self.w, self.h = 26, 42
        elif tipo == "alto":
            self.w, self.h = 34, random.choice([62, 74])
        elif tipo == "pajaro":
            self.w, self.h = 48, 24
            self.top = PAJARO_NIVELES[nivel]
        elif tipo == "cangrejo":
            self.w, self.h = 30, 16
            self.vel_propia = CANGREJO_VEL
        elif tipo == "foso":
            self.w = random.randint(*FOSO_ANCHO)
            self.h = 26
        else:
            self.w, self.h = 22, 16
            self.y = 10.0
            self.vx_propia = random.uniform(2.5, 4.0)
            self.vy = 0.4
            destino = DINO_X - self.w
            t = max(1.0, (x - destino) / (velocidad + self.vx_propia))
            if nivel == "corto":
                t = t * random.uniform(0.55, 0.75)
                y_obj = float(SUELO_Y)
            else:
                y_obj = float(METEORO_BANDAS[nivel] - self.h)
            g = 2.0 * (y_obj - self.y - self.vy * t) / (t * t)
            self.g_propia = max(METEORO_G[0], min(METEORO_G[1], g))

    @property
    def rect(self):
        if self.tipo == "pajaro":
            return pygame.Rect(int(self.x), self.top, self.w, self.h)
        if self.tipo == "meteorito":
            return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
        if self.tipo == "foso":
            return pygame.Rect(int(self.x), SUELO_Y, self.w, self.h)
        return pygame.Rect(int(self.x), SUELO_Y - self.h, self.w, self.h)

    def actualizar(self, velocidad):
        if self.tipo == "cangrejo":
            self.x -= velocidad + self.vel_propia
        elif self.tipo == "meteorito":
            self.x -= velocidad + self.vx_propia
            self.vy += self.g_propia
            self.y += self.vy
        else:
            self.x -= velocidad
        self.cuadro += 1

    def dibujar(self, sup, luz):
        r = self.rect
        if self.tipo == "pajaro":
            cuerpo = mezclar(PAJARO, (30, 36, 60), 1 - luz)
            ala_col = mezclar(PAJARO_ALA, (40, 50, 80), 1 - luz)
            cx, cy = r.centerx, r.centery
            pygame.draw.ellipse(sup, cuerpo, (cx - 12, cy - 6, 24, 13))
            pygame.draw.polygon(
                sup, cuerpo, [(cx + 8, cy - 4), (cx + 20, cy - 2), (cx + 8, cy + 3)]
            )
            pygame.draw.polygon(
                sup, PAJARO_PICO, [(cx + 18, cy - 3), (cx + 26, cy), (cx + 18, cy + 1)]
            )
            arriba = (self.cuadro // 6) % 2 == 0
            if arriba:
                pygame.draw.polygon(
                    sup, ala_col, [(cx - 6, cy - 2), (cx + 6, cy - 2), (cx, cy - 16)]
                )
            else:
                pygame.draw.polygon(
                    sup, ala_col, [(cx - 6, cy + 2), (cx + 6, cy + 2), (cx, cy + 14)]
                )
            return
        if self.tipo == "cangrejo":
            cuerpo = mezclar((214, 96, 70), (60, 36, 40), 1 - luz)
            oscuro = mezclar((150, 58, 44), (40, 26, 30), 1 - luz)
            pygame.draw.ellipse(sup, cuerpo, (r.left, r.top + 2, r.w, r.h - 2))
            paso = (self.cuadro // 3) % 2
            for i in range(3):
                px = r.left + 6 + i * 9
                dy = 2 if (i + paso) % 2 == 0 else 5
                pygame.draw.line(
                    sup, oscuro, (px, r.bottom - 4), (px - 3, r.bottom + dy - 4), 2
                )
                pygame.draw.line(
                    sup, oscuro, (px + 3, r.bottom - 4), (px + 6, r.bottom + dy - 4), 2
                )
            for ox in (r.centerx - 5, r.centerx + 5):
                pygame.draw.line(sup, oscuro, (ox, r.top + 3), (ox, r.top - 3), 2)
                pygame.draw.circle(sup, (250, 250, 250), (ox, r.top - 4), 3)
                pygame.draw.circle(sup, (30, 30, 30), (ox, r.top - 4), 1)
            pygame.draw.circle(sup, cuerpo, (r.left - 2, r.centery), 5)
            return
        if self.tipo == "foso":
            tierra = mezclar(SUELO_TIERRA2, (34, 40, 64), 1 - luz)
            vacio = mezclar((52, 38, 26), (8, 10, 18), 1 - luz)
            pygame.draw.rect(
                sup, tierra, (r.left, SUELO_Y - 2, r.w, 6)
            )
            pygame.draw.polygon(
                sup,
                vacio,
                [
                    (r.left, SUELO_Y - 1),
                    (r.right, SUELO_Y - 1),
                    (r.right - 8, SUELO_Y + 30),
                    (r.left + 8, SUELO_Y + 30),
                ],
            )
            borde = mezclar(SUELO_LINEA, (24, 30, 52), 1 - luz)
            pygame.draw.line(
                sup, borde, (r.left, SUELO_Y - 1), (r.left + 4, SUELO_Y + 8), 2
            )
            pygame.draw.line(
                sup, borde, (r.right, SUELO_Y - 1), (r.right - 4, SUELO_Y + 8), 2
            )
            return
        if self.tipo == "meteorito":
            nucleo = mezclar((255, 150, 60), (180, 70, 30), 1 - luz)
            roca = mezclar((150, 90, 60), (70, 44, 36), 1 - luz)
            cx, cy = r.centerx, r.centery
            pygame.draw.polygon(
                sup,
                nucleo,
                [
                    (cx + 6, cy - 4),
                    (cx + 22, cy - 14),
                    (cx + 10, cy + 2),
                ],
            )
            pygame.draw.circle(sup, roca, (cx, cy), 9)
            pygame.draw.circle(sup, nucleo, (cx - 3, cy + 2), 4)
            return
        cuerpo = mezclar(CACTUS, (30, 50, 40), 1 - luz)
        borde = mezclar(CACTUS_BORDE, (22, 40, 30), 1 - luz)
        tronco = pygame.Rect(r.centerx - 6, r.top, 12, r.height)
        pygame.draw.rect(sup, cuerpo, tronco, border_radius=5)
        pygame.draw.rect(sup, borde, tronco, width=2, border_radius=5)
        if self.tipo == "alto":
            pygame.draw.rect(sup, cuerpo, (r.left, r.top + 18, 8, 18), border_radius=4)
            pygame.draw.rect(
                sup, cuerpo, (r.right - 8, r.top + 28, 8, 16), border_radius=4
            )
        else:
            pygame.draw.rect(
                sup, cuerpo, (r.right - 8, r.top + 12, 8, 14), border_radius=4
            )


