# pygame-snake


A small, Snake game written with Pygame. 

TODO: add gif here + store in repo
---

Requirements
- Python 3.10+ (uses match/case)
- Pygame 2.x

---
Run it

> Tip: use a virtualenv (OS/Linux)

python -m venv .venv && source .venv/bin/activate
pip install pygame
python app.py

---
Controls
↑ ↓ ← → — move
P — pause/resume
Enter — start / continue
Esc — quit

---

How it works

Game loop: handles events, updates snake position, checks collisions, draws frame at CONFIG.FPS.

Snake: keeps a list of body segments. Grows by CONFIG.GROWTH_PER_FOOD. Boundary or self collision -> game over.

Food: spawns on random free grid cells.

UI: minimal text rendering for title, prompts  and score.

---

Troubleshooting

`ModuleNotFoundError: pygame:` run pip install pygame in the same environment you use to run the game.

---

