"""Repeatable, offline evaluation of the rule-based agent (no wall-clock delay)."""

import argparse
import json
import os
import random
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from constants import FPS, VEL_MAX
from juego import Juego


def run(seed, frames):
    """Run actual game physics and collisions without touching the high score."""
    random.seed(seed)
    with patch("juego.cargar_record", return_value=0), patch("juego.guardar_record"):
        game = Juego()
        game.iniciar("ia")
        spawned = set()
        hazards = 0
        original = game._generar_obstaculo

        def track_spawn():
            nonlocal hazards
            before = {id(ob) for ob in game.obstaculos}
            original()
            for obstacle in game.obstaculos:
                if id(obstacle) not in before:
                    spawned.add(obstacle.tipo)
                    hazards += 1

        game._generar_obstaculo = track_spawn
        completed = 0
        for _ in range(frames):
            game.actualizar(None)
            completed += 1
            if game.fase == "game_over":
                break
        game.sonidos.detener_musica()
        return {
            "seed": seed,
            "frames": completed,
            "simulated_seconds": completed / FPS,
            "survived": game.fase == "jugando",
            "score": game.puntaje,
            "reached_top_speed": game.velocidad == VEL_MAX,
            "hazards_spawned": hazards,
            "hazard_types": sorted(spawned),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=8)
    parser.add_argument("--seconds", type=int, default=600)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.runs < 1 or args.seconds < 1:
        parser.error("runs and seconds must be positive")
    pygame.init()
    try:
        results = [run(args.seed + index, args.seconds * FPS) for index in range(args.runs)]
    finally:
        pygame.quit()
    report = {
        "protocol": "Actual game update/collision loop; 60 simulated FPS; seeds recorded; no rendering.",
        "pygame_version": pygame.version.ver,
        "requested_seconds_per_run": args.seconds,
        "survived_runs": sum(result["survived"] for result in results),
        "total_runs": len(results),
        "runs": results,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if all(result["survived"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
