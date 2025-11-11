# Swim Set Maker

![Swim image](./swim.png)

Generate swim sets (warmup, drill, main, cooldown) from simple building blocks.

Features
- Simple CLI with interactive and non-interactive modes
- Two target modes: `--target-type main` (the yards apply to the MAIN only) and `--target-type total` (yards = warmup+main+cooldown)
- Optionally inject drills into the workout (`--include-drills` or the Streamlit checkbox)
- Controlled overshoot policy: small overshoots are allowed only if the final total ends in multiples of 50; the generator will also force a drill if requested and choose the composition that minimizes deviation from the target
- Streamlit demo UI (`app.py`) — UI auto-switches to Total mode when drills are requested and reports whether a drill was added
- Deterministic generation via `--seed`

Quick start

Clone and install dependencies:

```bash
git clone https://github.com/DanV27/swim-set-maker.git
cd swim-set-maker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the CLI (interactive):

```bash
python3 main.py
```

Run non-interactive (examples):

Main-target (yards apply to the main set only):
```bash
python3 main.py --level intermediate --yards 1000 --target-type main --seed 42
```

Total-target (yards apply to warmup+main+cooldown):
```bash
python3 main.py --level intermediate --yards 1000 --target-type total --seed 42
```

Force drills to be included (total-target):
```bash
python3 main.py --level beginner --yards 1000 --target-type total --include-drills --seed 7
```

Run the Streamlit UI:

```bash
streamlit run app.py
```

Notes on drills and overshoot behavior
- When `--include-drills` is used (or the Streamlit checkbox), the generator will attempt to insert a drill while keeping the total close to the requested yards. The UI will show whether a drill was added.
- The algorithm prefers not to worsen closeness to the target, but will force a drill if requested. Small overshoots are only permitted when the final total ends in a multiple of 50 (and within a conservative cap) unless forced.
- Drills are displayed immediately after the warmup in the generated output.

Files
- `main.py` - CLI and generator
- `data.py` - warmups, main sets, drills, cooldowns, and small building blocks
- `app.py` - Streamlit UI
- `requirements.txt` - Python deps for the UI

Contributing

Open an issue or PR for desired improvements (more data variants, smarter splitting, tests, CLI features).

License

MIT