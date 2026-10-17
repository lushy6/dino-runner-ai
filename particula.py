import random
import pygame
from constants import POLVO


class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2.6, -0.6)
        self.vy = random.uniform(-2.2, -0.4)
        self.vida = random.randint(14, 26)
        self.t = 0
        self.r = random.uniform(2, 4)

    @property
    def vivo(self):
        return self.t < self.vida

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.14
        self.t += 1

    def dibujar(self, sup):
        alpha = int(max(0, 200 * (1 - self.t / self.vida)))
        s = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(s, (*POLVO, alpha), (4, 4), int(self.r))
        sup.blit(s, (int(self.x) - 4, int(self.y) - 4))


