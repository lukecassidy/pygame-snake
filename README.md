## pygame-snake

A small, Snake game written with Pygame.

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

---

![pygame-snake](https://github.com/user-attachments/assets/752b9311-f24d-412f-aa08-a41d373b2ba9)

---
### Controls

| Key     | Action           |
| ------- | ---------------- |
| ↑ ↓ ← → | move             |
| P       | pause/resume     |
| Enter   | start / continue |
| Esc     | quit             |

---

### How it works
- Game loop: Handles events, updates snake position, checks collisions, draws frame at CONFIG.FPS.
- Snake: Keeps a list of body segments. Grows by CONFIG.GROWTH_PER_FOOD. Boundary or self collision -> game over.
- Food: Spawns on random free grid cells.
- UI: Minimal text rendering for title, prompts  and score.

---

