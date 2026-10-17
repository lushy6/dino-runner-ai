# Dino Runner with AI Agent

A Python/Pygame remake of the Chrome dinosaur game, with an AI mode that plays the game by itself.

Built as the final project for Data Structures & Algorithms II (IDS344L) at Instituto Tecnológico de Santo Domingo (INTEC).

**Authors:** Matias Birbuet · José Emilio García

## Features

- **Two modes:** play it yourself, or watch the AI play
- **Six hazard types** that unlock as the game speeds up: short cacti, tall cacti, birds at three heights, crabs that walk toward you, pits, and falling meteorites
- **AI agent** that decides each frame whether to jump, duck, or fast-fall
- **All sound generated in code:** sound effects and chiptune music are synthesized at runtime, with no audio files
- **Day/night sky,** parallax hills, particles, and screen shake
- **High score** saved between sessions

## How the AI works

The agent looks at the nearest obstacle and reacts using simple rules (a greedy strategy):

- **Ground obstacles** (cacti, crabs, pits): jump when the gap is small enough, based on the current speed. For crabs, the AI also adds the crab's own speed, since it is walking toward the dino.
- **Birds:** duck under mid-height birds and jump over low ones.
- **Meteorites:** the AI simulates the meteorite's fall frame by frame (up to 240 frames ahead) to predict whether it will cross the dino's position and at what height. Then it decides to jump, duck, or wait.
- **Fast-fall:** when the dino is in the air and the path ahead is clear, it drops faster to land sooner.

The logic lives in [`ai.py`](ai.py).

**Results:** in 8 headless test runs of 10 minutes each (36,000 frames at 60 FPS), the AI never crashed and reached the game's top speed. In one run it cleared 701 obstacles, covering all six hazard types.

## Run it

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| `1` | Start in player mode |
| `2` | Start in AI mode |
| `Space` / `↑` / `W` | Jump |
| `↓` / `S` | Duck (fast-fall in the air) |
| `P` | Pause |
| `R` | Restart after game over |
| `M` | Back to menu |
| `N` | Mute / unmute |
| `Esc` | Quit |

## Project structure

| File | What it does |
| --- | --- |
| `main.py` | Entry point and game loop |
| `juego.py` | Game state, obstacle spawning, collisions, scoring, screens |
| `ai.py` | AI agent and meteorite trajectory prediction |
| `dino.py` | Player character physics and animation |
| `obstaculo.py` | Obstacle types and their movement |
| `fondo.py` / `suelo.py` | Sky, hills, and ground drawing |
| `sonidos.py` | Procedural sound effects and music |
| `particula.py` | Dust particles |
| `record.py` | Saving and loading the high score |
| `constants.py` / `utils.py` | Settings, colors, and drawing helpers |

The code uses Spanish names (for example, `saltar` = jump, `agachar` = duck).
