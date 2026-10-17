import sys
import random
import pygame
from constants import ANCHO, ALTO, FPS
from juego import Juego
from record import guardar_record


def main():
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Dino Runner - Pygame")
    reloj = pygame.time.Clock()

    fuentes = (
        pygame.font.SysFont("consolas", 18, bold=True),
        pygame.font.SysFont("consolas", 26, bold=True),
        pygame.font.SysFont("consolas", 52, bold=True),
    )

    juego = Juego()
    escena = pygame.Surface((ANCHO, ALTO))

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif juego.manejar_evento(evento) == "salir":
                corriendo = False

        teclas = pygame.key.get_pressed()
        juego.actualizar(teclas)
        juego.dibujar(escena, fuentes)

        dx = dy = 0
        if juego.shake > 0:
            dx = random.randint(-4, 4)
            dy = random.randint(-3, 3)
            pantalla.fill((0, 0, 0))
        pantalla.blit(escena, (dx, dy))
        pygame.display.flip()
        reloj.tick(FPS)

    guardar_record(juego.record)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


