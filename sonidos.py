import pygame
from array import array
from constants import NOTAS


class Sonidos:
    FREC = 22050

    def __init__(self):
        self.activo = False
        self.silencio = False
        self.banco = {}
        self.musica = None
        self.canal_musica = None
        try:
            if pygame.mixer.get_init() != (self.FREC, -16, 1):
                pygame.mixer.quit()
                pygame.mixer.init(self.FREC, -16, 1, 512)
            self.banco["saltar"] = self._tono([(220, 460, 0.09)])
            self.banco["agachar"] = self._tono([(170, 120, 0.05)])
            self.banco["punto"] = self._tono(
                [(660, 660, 0.06), (0, 0, 0.025), (880, 880, 0.08)]
            )
            self.banco["morir"] = self._tono([(300, 80, 0.35)], vol=0.30)
            self.banco["menu"] = self._tono([(520, 520, 0.06)])
            self.musica = self._cancion()
            self.activo = True
        except Exception:
            self.activo = False

    def _tono(self, segmentos, vol=0.22):
        datos = array("h")
        amp = int(32767 * vol)
        for f0, f1, dur in segmentos:
            n = max(1, int(self.FREC * dur))
            fase = 0.0
            ataque = max(1, int(0.005 * self.FREC))
            cola = max(1, int(0.15 * n))
            for i in range(n):
                if f0 <= 0:
                    datos.append(0)
                    continue
                f = f0 + (f1 - f0) * (i / n)
                fase += f / self.FREC
                env = 1.0
                if i < ataque:
                    env = i / ataque
                if i > n - cola:
                    env = (n - i) / cola
                v = amp if (fase % 1.0) < 0.5 else -amp
                datos.append(int(v * env))
        return pygame.mixer.Sound(buffer=datos.tobytes())

    def _cancion(self):
        melodia = (
            ["A4", "C5", "E5", "C5", "A4", "C5", "E5", "C5"]
            + ["F4", "A4", "C5", "A4", "F4", "A4", "C5", "A4"]
            + ["E4", "G4", "C5", "G4", "E4", "G4", "C5", "G4"]
            + ["D4", "G4", "B4", "G4", "D4", "G4", "B4", "G4"]
            + ["E5", "C5", "A4", "C5", "E5", "C5", "A4", "C5"]
            + ["C5", "A4", "F4", "A4", "C5", "A4", "F4", "A4"]
            + ["B4", "G4", "D4", "G4", "B4", "D5", "B4", "G4"]
            + ["A4", "-", "E4", "G4", "A4", "-", "-", "-"]
        )
        bajo = (
            ["A2", "A3"] * 4 + ["F2", "F3"] * 4 + ["C3", "C4"] * 4 + ["G2", "G3"] * 4
        ) * 2
        n = int(self.FREC * 0.2)
        datos = array("h", [0] * (n * len(melodia)))
        self._voz(datos, melodia, n, 0.085)
        self._voz(datos, bajo, n, 0.060)
        return pygame.mixer.Sound(buffer=datos.tobytes())

    def _voz(self, datos, notas, n, vol):
        amp = int(32767 * vol)
        borde = max(1, int(0.008 * self.FREC))
        idx = 0
        for nombre in notas:
            f = NOTAS[nombre]
            if f <= 0:
                idx += n
                continue
            fase = 0.0
            for i in range(n):
                fase += f / self.FREC
                env = 1.0
                if i < borde:
                    env = i / borde
                elif i > n - borde:
                    env = (n - i) / borde
                v = amp if (fase % 1.0) < 0.5 else -amp
                datos[idx] += int(v * env)
                idx += 1

    def tocar(self, nombre):
        if self.activo and not self.silencio and nombre in self.banco:
            self.banco[nombre].play()

    def iniciar_musica(self):
        if self.activo and not self.silencio and self.musica is not None:
            if self.canal_musica is None or not self.canal_musica.get_busy():
                self.canal_musica = self.musica.play(loops=-1)

    def detener_musica(self):
        if self.canal_musica is not None:
            self.canal_musica.stop()
            self.canal_musica = None

    def pausar_musica(self, en_pausa):
        if self.canal_musica is not None:
            if en_pausa:
                self.canal_musica.pause()
            else:
                self.canal_musica.unpause()


