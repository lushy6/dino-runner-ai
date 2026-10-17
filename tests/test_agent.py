import os
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from ai import predecir_meteorito, procesar_ia
from benchmark import run
from constants import SUELO_Y
from dino import Dino
from obstaculo import Obstaculo


def test_clear_ground_requires_no_action():
    assert procesar_ia(Dino(), [], 8) == (False, False, False)


def test_near_ground_hazard_triggers_jump():
    dino = Dino()
    assert procesar_ia(dino, [Obstaculo("bajo", dino.rect.right + 30)], 8)[0]


def test_middle_bird_triggers_duck_instead_of_jump():
    dino = Dino()
    assert procesar_ia(dino, [Obstaculo("pajaro", dino.rect.right + 20, "medio")], 8) == (
        False, True, False
    )


def test_passed_obstacles_do_not_trigger_action():
    assert procesar_ia(Dino(), [Obstaculo("alto", -100)], 8) == (False, False, False)


def test_meteorite_that_lands_before_player_is_not_crossing():
    meteorite = SimpleNamespace(x=800, y=SUELO_Y - 20, vy=10, h=16, w=22,
                               vx_propia=3, g_propia=0.2)
    assert predecir_meteorito(meteorite, Dino().rect, 8) == ("impacto", None, None)


def test_pause_preserves_gameplay_state():
    from unittest.mock import patch
    from juego import Juego

    with patch("juego.cargar_record", return_value=0), patch("juego.guardar_record"):
        game = Juego()
        game.iniciar("ia")
        game.pausa = True
        before = (game.cuadro, game.distancia, game.puntaje)
        game.actualizar(None)
        assert (game.cuadro, game.distancia, game.puntaje) == before
        game.sonidos.detener_musica()


def test_seeded_agent_run_is_reproducible_and_survives():
    pygame.init()
    try:
        first = run(0, 60 * 30)
        assert first == run(0, 60 * 30)
        assert first["survived"]
    finally:
        pygame.quit()
