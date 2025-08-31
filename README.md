## pygame-snake

A small, Snake game written with Pygame. 
>TODO: add gif here + store in repo

---
### Requirements
- Python 3.10+
- Pygame 2.x

---
### Run it
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

---
### Controls
- ↑ ↓ ← → | move
- P | pause/resume
- Enter | start / continue
- Esc | quit

---

### How it works
#### Game loop:
Handles events, updates snake position, checks collisions, draws frame at CONFIG.FPS.

#### Snake:
Keeps a list of body segments. Grows by CONFIG.GROWTH_PER_FOOD. Boundary or self collision -> game over.

#### Food:
Spawns on random free grid cells.

#### UI:
Minimal text rendering for title, prompts  and score.

---

