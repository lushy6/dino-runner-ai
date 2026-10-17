import random
import pygame
from constants import (
    DINO_X, SUELO_Y, ALTO_DINO, ANCHO_DINO,
    ALTO_AGACHADO, ANCHO_AGACHADO,
    SALTO_VEL, GRAVEDAD, GRAVEDAD_EXTRA, CORTE_SALTO,
    COLOR_DINO, COLOR_DINO_BORDE, COLOR_DINO_PANZA,
    COLOR_OJO, COLOR_PUPILA,
)


class Dino:
    def __init__(self):
        self.altura = 0.0
        self.vel = 0.0
        self.en_suelo = True
        self.agachado = False
        self.cuadro = 0
        self.parpadeo = 0

    @property
    def rect(self):
        if self.agachado and self.en_suelo:
            return pygame.Rect(
                DINO_X, SUELO_Y - ALTO_AGACHADO, ANCHO_AGACHADO, ALTO_AGACHADO
            )
        y = SUELO_Y - ALTO_DINO - int(self.altura)
        return pygame.Rect(DINO_X, y, ANCHO_DINO, ALTO_DINO)

    def saltar(self):
        if self.en_suelo:
            self.vel = SALTO_VEL
            self.en_suelo = False
            return True
        return False

    def actualizar(self, agachar, sostener_salto, caida_rapida):
        self.cuadro += 1
        self.agachado = agachar and self.en_suelo

        if (not self.en_suelo) and (not sostener_salto) and self.vel > CORTE_SALTO:
            self.vel = CORTE_SALTO

        extra = GRAVEDAD_EXTRA if (caida_rapida and not self.en_suelo) else 0.0

        self.altura += self.vel
        self.vel -= GRAVEDAD + extra
        if self.altura <= 0:
            self.altura = 0.0
            self.vel = 0.0
            self.en_suelo = True

        if self.parpadeo > 0:
            self.parpadeo -= 1
        elif random.random() < 0.012:
            self.parpadeo = 6

    def _ojo(self, sup, ox, oy):
        if self.parpadeo > 0:
            pygame.draw.line(sup, COLOR_PUPILA, (ox - 3, oy), (ox + 3, oy), 2)
        else:
            pygame.draw.circle(sup, COLOR_OJO, (ox, oy), 4)
            pygame.draw.circle(sup, COLOR_PUPILA, (ox + 1, oy), 2)

    def dibujar(self, sup):
        r = self.rect
        if self.agachado and self.en_suelo:
            pygame.draw.rect(sup, COLOR_DINO, r, border_radius=11)
            pygame.draw.rect(
                sup,
                COLOR_DINO_PANZA,
                (r.left + 6, r.bottom - 9, r.width - 30, 6),
                border_radius=4,
            )
            cab = pygame.Rect(r.right - 20, r.top - 4, 22, 18)
            pygame.draw.rect(sup, COLOR_DINO, cab, border_radius=6)
            pygame.draw.rect(
                sup, COLOR_DINO, (r.right - 2, r.top + 2, 9, 8), border_radius=3
            )
            self._ojo(sup, r.right - 6, r.top + 4)
            paso = (self.cuadro // 4) % 2
            pygame.draw.rect(
                sup, COLOR_DINO_BORDE, (r.left + 14 + paso * 4, r.bottom - 4, 7, 5)
            )
            pygame.draw.rect(
                sup, COLOR_DINO_BORDE, (r.left + 30 - paso * 4, r.bottom - 4, 7, 5)
            )
            return

        pygame.draw.polygon(
            sup,
            COLOR_DINO,
            [
                (r.left - 10, r.top + 18),
                (r.left + 8, r.top + 12),
                (r.left + 8, r.top + 34),
            ],
        )
        cuerpo = pygame.Rect(r.left + 2, r.top + 10, 30, 30)
        pygame.draw.rect(sup, COLOR_DINO, cuerpo, border_radius=10)
        pygame.draw.rect(
            sup, COLOR_DINO_PANZA, (r.left + 8, r.top + 28, 18, 9), border_radius=4
        )
        cabeza = pygame.Rect(r.left + 18, r.top - 2, 24, 22)
        pygame.draw.rect(sup, COLOR_DINO, cabeza, border_radius=8)
        pygame.draw.rect(
            sup, COLOR_DINO, (r.right - 4, r.top + 4, 10, 9), border_radius=3
        )
        self._ojo(sup, r.right - 4, r.top + 6)
        pygame.draw.rect(
            sup, COLOR_DINO_BORDE, (r.left + 22, r.top + 22, 8, 5), border_radius=2
        )
        if not self.en_suelo:
            pygame.draw.rect(
                sup, COLOR_DINO_BORDE, (r.left + 8, r.top + 38, 9, 7), border_radius=2
            )
            pygame.draw.rect(
                sup, COLOR_DINO_BORDE, (r.left + 22, r.top + 38, 9, 7), border_radius=2
            )
        else:
            paso = (self.cuadro // 4) % 2
            if paso == 0:
                pygame.draw.rect(sup, COLOR_DINO_BORDE, (r.left + 8, r.top + 38, 7, 8))
                pygame.draw.rect(sup, COLOR_DINO_BORDE, (r.left + 22, r.top + 40, 7, 6))
            else:
                pygame.draw.rect(sup, COLOR_DINO_BORDE, (r.left + 8, r.top + 40, 7, 6))
                pygame.draw.rect(sup, COLOR_DINO_BORDE, (r.left + 22, r.top + 38, 7, 8))

