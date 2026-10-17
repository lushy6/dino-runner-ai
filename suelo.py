import random
import pygame
from constants import ANCHO, ALTO, SUELO_Y
from utils import mezclar
from constants import SUELO_TIERRA, SUELO_TIERRA2, SUELO_LINEA, GRASS, PIEDRA


class Suelo:
    def __init__(self):
        self.scroll = 0.0
        self.decor = []
        x = 0
        while x < ANCHO + 100:
            self.decor.append([x, random.choice(["pasto", "piedra", "pasto"])])
            x += random.randint(70, 150)

    def actualizar(self, velocidad):
        self.scroll = (self.scroll + velocidad) % 36
        for d in self.decor:
            d[0] -= velocidad
        self.decor = [d for d in self.decor if d[0] > -30]
        ultimo = max((d[0] for d in self.decor), default=0)
        while ultimo < ANCHO + 60:
            ultimo += random.randint(70, 150)
            self.decor.append([ultimo, random.choice(["pasto", "piedra", "pasto"])])

    def dibujar(self, sup, luz):
        pygame.draw.rect(
            sup,
            mezclar(SUELO_TIERRA, (40, 46, 70), 1 - luz),
            (0, SUELO_Y, ANCHO, ALTO - SUELO_Y),
        )
        pygame.draw.rect(
            sup,
            mezclar(SUELO_TIERRA2, (34, 40, 64), 1 - luz),
            (0, SUELO_Y + 26, ANCHO, ALTO - SUELO_Y - 26),
        )
        pygame.draw.line(
            sup,
            mezclar(SUELO_LINEA, (24, 30, 52), 1 - luz),
            (0, SUELO_Y),
            (ANCHO, SUELO_Y),
            3,
        )
        col_marca = mezclar(SUELO_LINEA, (30, 36, 58), 1 - luz)
        for i in range(-1, ANCHO // 36 + 2):
            x = int(i * 36 + self.scroll)
            pygame.draw.line(
                sup, col_marca, (x, SUELO_Y + 14), (x + 12, SUELO_Y + 14), 2
            )
        for x, tipo in self.decor:
            xi = int(x)
            if tipo == "pasto":
                c = mezclar(GRASS, (30, 50, 60), 1 - luz)
                for dx in (-3, 0, 3):
                    pygame.draw.line(
                        sup, c, (xi + dx, SUELO_Y), (xi + dx, SUELO_Y - 8), 2
                    )
            else:
                c = mezclar(PIEDRA, (50, 56, 74), 1 - luz)
                pygame.draw.ellipse(sup, c, (xi, SUELO_Y - 5, 12, 7))


