import random
import pygame
from constants import (
    ANCHO, ALTO, SUELO_Y, VEL_INICIAL, VEL_MAX, VEL_MENU,
    VEL_CANGREJO, VEL_PELIGROS, VEL_GRUPO_2, VEL_GRUPO_3,
    GAP_MIN, GAP_MAX, FACTOR_GAP, FACTOR_VEL,
    ALTO_DINO, ALTO_AGACHADO,
    TEXTO_CLARO, TEXTO_DORADO,
)
from fondo import Fondo
from suelo import Suelo
from dino import Dino
from obstaculo import Obstaculo
from particula import Particula
from sonidos import Sonidos
from record import cargar_record, guardar_record
from utils import texto_con_sombra
from ai import procesar_ia


class Juego:
    def __init__(self):
        self.fondo = Fondo()
        self.suelo = Suelo()
        self.dino = Dino()
        self.sonidos = Sonidos()
        self.sonidos.iniciar_musica()
        self.fase = "menu"
        self.modo = "manual"
        self.record = cargar_record()
        self.reiniciar()

    def reiniciar(self):
        self.dino = Dino()
        self.obstaculos = []
        self.particulas = []
        self.puntaje = 0
        self.distancia = 0.0
        self.velocidad = VEL_INICIAL
        self.dist_spawn = random.randint(GAP_MIN, GAP_MAX)
        self.cuadro = 0
        self.pausa = False
        self.nuevo_record = False
        self.flash = 0
        self.shake = 0

    def iniciar(self, modo):
        self.modo = modo
        self.reiniciar()
        self.fase = "jugando"

    def manejar_evento(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return "salir"
            if e.key == pygame.K_n:
                self.sonidos.silencio = not self.sonidos.silencio
                if self.sonidos.silencio:
                    self.sonidos.detener_musica()
                else:
                    self.sonidos.iniciar_musica()
                    self.sonidos.pausar_musica(self.fase == "jugando" and self.pausa)
                    self.sonidos.tocar("menu")
            if self.fase == "menu":
                if e.key == pygame.K_1:
                    self.sonidos.tocar("menu")
                    self.iniciar("manual")
                elif e.key == pygame.K_2:
                    self.sonidos.tocar("menu")
                    self.iniciar("ia")
            elif self.fase == "jugando":
                if e.key == pygame.K_p:
                    self.pausa = not self.pausa
                    self.sonidos.pausar_musica(self.pausa)
                    self.sonidos.tocar("menu")
                elif (
                    not self.pausa
                    and self.modo == "manual"
                    and e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w)
                ):
                    if self.dino.saltar():
                        self.sonidos.tocar("saltar")
                        self._polvo(6)
            elif self.fase == "game_over":
                if e.key == pygame.K_r:
                    self.sonidos.tocar("menu")
                    self.iniciar(self.modo)
                elif e.key == pygame.K_m:
                    self.sonidos.tocar("menu")
                    self.obstaculos = []
                    self.fase = "menu"
        return None

    def _polvo(self, cantidad):
        r = self.dino.rect
        for _ in range(cantidad):
            self.particulas.append(
                Particula(
                    r.left + random.randint(0, r.width // 2),
                    SUELO_Y - random.randint(0, 4),
                )
            )

    def _generar_obstaculo(self):
        tipos = ["bajo", "alto", "pajaro"]
        pesos = [5, 3, 3]
        if self.velocidad >= VEL_CANGREJO:
            tipos.append("cangrejo")
            pesos.append(2)
        if self.velocidad >= VEL_PELIGROS:
            tipos.append("foso")
            pesos.append(2)
            tipos.append("meteorito")
            pesos.append(2)
        tipo = random.choices(tipos, weights=pesos)[0]
        extra = 0
        if tipo == "pajaro":
            nivel = random.choices(("bajo", "medio", "alto"), weights=(1, 2, 1))[0]
            self.obstaculos.append(Obstaculo("pajaro", ANCHO + 20, nivel))
        elif tipo == "meteorito":
            banda = random.choices(
                ("alto", "cabeza", "bajo", "corto"), weights=(2, 3, 2, 2)
            )[0]
            self.obstaculos.append(
                Obstaculo("meteorito", ANCHO, banda, velocidad=self.velocidad)
            )
            extra = 220
        elif tipo == "foso":
            self.obstaculos.append(Obstaculo("foso", ANCHO + 20))
        elif tipo == "cangrejo":
            self.obstaculos.append(Obstaculo("cangrejo", ANCHO + 20))
        elif (
            tipo == "bajo" and self.velocidad >= VEL_GRUPO_2 and random.random() < 0.35
        ):
            tam = 2
            if self.velocidad >= VEL_GRUPO_3:
                tam = random.choice((2, 2, 3))
            for i in range(tam):
                self.obstaculos.append(Obstaculo("bajo", ANCHO + 20 + i * 29))
            extra = (tam - 1) * 29
        else:
            self.obstaculos.append(Obstaculo(tipo, ANCHO + 20))
        self.dist_spawn = (
            random.randint(GAP_MIN, GAP_MAX) + int(self.velocidad * FACTOR_GAP) + extra
        )

    def actualizar(self, teclas):
        if self.shake > 0:
            self.shake -= 1
        if self.flash > 0:
            self.flash -= 1

        if self.fase == "jugando" and self.pausa:
            return

        if self.fase == "jugando":
            vel_fondo = self.velocidad
        elif self.fase == "menu":
            vel_fondo = VEL_MENU
        else:
            vel_fondo = 0.0
        self.fondo.actualizar(vel_fondo)
        self.suelo.actualizar(vel_fondo)

        if self.fase != "jugando":
            for p in self.particulas:
                p.actualizar()
            self.particulas = [p for p in self.particulas if p.vivo]
            if self.fase == "menu":
                self.dino.cuadro += 1
            return

        if self.modo == "ia":
            saltar_ia, agachar, rapida = procesar_ia(
                self.dino, self.obstaculos, self.velocidad
            )
            sostener = True
            if saltar_ia and self.dino.saltar():
                self.sonidos.tocar("saltar")
                self._polvo(6)
        else:
            abajo = bool(teclas and (teclas[pygame.K_DOWN] or teclas[pygame.K_s]))
            sostener = bool(
                teclas
                and (
                    teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]
                )
            )
            agachar = abajo
            rapida = abajo
            if agachar and self.dino.en_suelo and not self.dino.agachado:
                self.sonidos.tocar("agachar")
            if sostener and not agachar and self.dino.saltar():
                self.sonidos.tocar("saltar")
                self._polvo(6)

        estaba_en_aire = not self.dino.en_suelo
        self.dino.actualizar(agachar, sostener, rapida)
        if estaba_en_aire and self.dino.en_suelo:
            self._polvo(8)
        if self.dino.en_suelo and self.cuadro % 7 == 0:
            self._polvo(1)

        self.dist_spawn -= self.velocidad
        if self.dist_spawn <= 0:
            self._generar_obstaculo()
        for ob in self.obstaculos:
            ob.actualizar(self.velocidad)
            if ob.tipo == "meteorito" and ob.cuadro % 3 == 0:
                self.particulas.append(
                    Particula(ob.rect.centerx + 8, ob.rect.centery - 2)
                )
        vivos = []
        for ob in self.obstaculos:
            if (
                ob.tipo == "meteorito"
                and ob.rect.bottom >= SUELO_Y
                and not ob.rect.colliderect(self.dino.rect)
            ):
                for _ in range(10):
                    self.particulas.append(Particula(ob.rect.centerx, SUELO_Y - 2))
                continue
            if ob.x + ob.w > -10:
                vivos.append(ob)
        self.obstaculos = vivos

        for p in self.particulas:
            p.actualizar()
        self.particulas = [p for p in self.particulas if p.vivo]

        self.distancia += self.velocidad
        puntaje_nuevo = int(self.distancia / 10)
        if puntaje_nuevo // 100 > self.puntaje // 100:
            self.sonidos.tocar("punto")
            self.flash = 24
        self.puntaje = puntaje_nuevo
        if self.puntaje > self.record:
            self.record = self.puntaje
            if not self.nuevo_record:
                self.nuevo_record = True
                self.sonidos.tocar("punto")
                self.flash = 24
        self.velocidad = min(VEL_MAX, VEL_INICIAL + self.puntaje * FACTOR_VEL)
        self.cuadro += 1

        dr = self.dino.rect.inflate(-10, -6)
        for ob in self.obstaculos:
            if ob.tipo == "foso":
                choca = (
                    self.dino.en_suelo
                    and dr.right > ob.x + 4
                    and dr.left < ob.x + ob.w - 4
                )
            else:
                choca = dr.colliderect(ob.rect.inflate(-6, -4))
            if choca:
                self.fase = "game_over"
                self.sonidos.tocar("morir")
                self.shake = 18
                self._polvo(14)
                if self.nuevo_record:
                    guardar_record(self.record)
                break

    def dibujar(self, sup, fuentes):
        luz = self.fondo.luz
        self.fondo.dibujar(sup)
        self.suelo.dibujar(sup, luz)
        for ob in self.obstaculos:
            ob.dibujar(sup, luz)
        self.dino.dibujar(sup)
        for p in self.particulas:
            p.dibujar(sup)

        oscuridad = int((1 - luz) ** 1.3 * 140)
        if oscuridad > 4:
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((10, 16, 46, oscuridad))
            sup.blit(velo, (0, 0))

        if self.fase == "menu":
            self._dibujar_menu(sup, fuentes)
        elif self.fase == "jugando":
            self._dibujar_hud(sup, fuentes)
            if self.pausa:
                self._dibujar_pausa(sup, fuentes)
        else:
            self._dibujar_hud(sup, fuentes)
            self._dibujar_game_over(sup, fuentes)

    def _dibujar_hud(self, sup, fuentes):
        f_chica, f_media, f_grande = fuentes
        if self.flash == 0 or (self.flash // 4) % 2 == 0:
            texto_con_sombra(
                sup,
                f_media,
                "{:05d}".format(self.puntaje),
                ANCHO - 110,
                14,
                TEXTO_CLARO,
            )
        col_rec = TEXTO_DORADO if self.nuevo_record else TEXTO_CLARO
        texto_con_sombra(
            sup, f_chica, "RECORD {:05d}".format(self.record), ANCHO - 150, 44, col_rec
        )
        etiqueta = "IA (auto)" if self.modo == "ia" else "Jugador"
        texto_con_sombra(sup, f_chica, etiqueta, 16, 14, TEXTO_CLARO)
        if self.sonidos.silencio:
            texto_con_sombra(sup, f_chica, "SONIDO OFF", 16, 44, TEXTO_DORADO)
        if self.modo == "manual":
            ayuda = "ESPACIO saltar | S/abajo agachar o caer | P pausa | N sonido"
        else:
            ayuda = "La IA juega sola | P pausa | N sonido"
        texto_con_sombra(sup, f_chica, ayuda, 16, ALTO - 26, TEXTO_CLARO)

    def _dibujar_pausa(self, sup, fuentes):
        f_chica, f_media, f_grande = fuentes
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 120))
        sup.blit(velo, (0, 0))
        texto_con_sombra(
            sup, f_grande, "PAUSA", ANCHO // 2, 120, TEXTO_CLARO, centrado=True
        )
        texto_con_sombra(
            sup,
            f_chica,
            "[P] continuar      [ESC] salir",
            ANCHO // 2,
            186,
            TEXTO_CLARO,
            centrado=True,
        )

    def _dibujar_menu(self, sup, fuentes):
        f_chica, f_media, f_grande = fuentes
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 70))
        sup.blit(velo, (0, 0))
        texto_con_sombra(
            sup, f_grande, "DINO RUNNER", ANCHO // 2, 58, TEXTO_CLARO, centrado=True
        )
        texto_con_sombra(
            sup,
            f_chica,
            "Cactus, pajaros, cangrejos, fosos y meteoritos te esperan",
            ANCHO // 2,
            110,
            TEXTO_CLARO,
            centrado=True,
        )
        texto_con_sombra(
            sup,
            f_media,
            "[1]  Jugar tu mismo",
            ANCHO // 2,
            152,
            TEXTO_CLARO,
            centrado=True,
        )
        texto_con_sombra(
            sup,
            f_media,
            "[2]  Que juegue la IA",
            ANCHO // 2,
            186,
            TEXTO_CLARO,
            centrado=True,
        )
        texto_con_sombra(
            sup,
            f_chica,
            "RECORD  {:05d}".format(self.record),
            ANCHO // 2,
            228,
            TEXTO_DORADO,
            centrado=True,
        )
        texto_con_sombra(
            sup, f_chica, "ESC para salir", ANCHO // 2, 254, TEXTO_CLARO, centrado=True
        )

    def _dibujar_game_over(self, sup, fuentes):
        f_chica, f_media, f_grande = fuentes
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 110))
        sup.blit(velo, (0, 0))
        texto_con_sombra(
            sup, f_grande, "GAME OVER", ANCHO // 2, 84, TEXTO_CLARO, centrado=True
        )
        texto_con_sombra(
            sup,
            f_media,
            "Puntaje  {:05d}".format(self.puntaje),
            ANCHO // 2,
            142,
            TEXTO_CLARO,
            centrado=True,
        )
        if self.nuevo_record:
            texto_con_sombra(
                sup,
                f_media,
                "NUEVO RECORD!",
                ANCHO // 2,
                176,
                TEXTO_DORADO,
                centrado=True,
            )
        texto_con_sombra(
            sup,
            f_chica,
            "[R] reiniciar     [M] menu",
            ANCHO // 2,
            216,
            TEXTO_CLARO,
            centrado=True,
        )


