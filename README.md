# Swim Project

Small CLI to generate swim sets (warmup, main, cooldown) based on swimmer level and yard target.

Files
- `main.py` - CLI and simple set generator.
- `data.py` - workout building blocks (warmups, main sets, drills, cooldowns).

Quick start

Run interactively:

```bash
python3 main.py
```

Example session:

```
Welcome to Swimset!
Are you a beginner, intermediate, or advanced swimmer? intermediate
Choose your desired swim yards:
Options: 500, 1000, 1500, 2000
Enter your desired swim yards: 1000

Generated simple set:

WARMUP: 200 EASY (200 yds)
MAIN: 10x100 @ 1:45 (1000 yds)
COOLDOWN: 50 EASY (50 yds)
```

Next steps
- Add unit tests for the generator.
- Make generation deterministic / seedable or add CLI flags (`--level`, `--yards`).
- Improve matching logic (split main sets to better fit targets).

License: MIT