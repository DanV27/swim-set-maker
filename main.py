#!/usr/bin/env python3
"""Simple CLI for Swimset with exact-target generation.

This script asks for a swim level and an exact yard target, then builds a swim set
using blocks from the `blocks` dictionary. The generator will use warmup and
cooldown and fill the main set to exactly match the requested yards by using
available blocks and small filler increments (50, 25, 1 yards) when necessary.
"""

from typing import Dict, List, Tuple
import random


blocks: Dict[str, List[Dict[str, int]]] = {
    "warmup": [
        {"desc": "4x50 easy swim", "dist": 200},
        {"desc": "2x100 swim + 4x50 drill", "dist": 400},
    ],
    "sprint": [
        {"desc": "8x25 all out, :30 rest", "dist": 200},
        {"desc": "12x50 race pace, :45 rest", "dist": 600},
    ],
    "endurance": [
        {"desc": "5x200 aerobic pace", "dist": 1000},
        {"desc": "3x400 steady", "dist": 1200},
    ],
    "technique": [
        {"desc": "6x50 drill/swim", "dist": 300},
        {"desc": "4x100 IM drill", "dist": 400},
    ],
    "recovery": [
        {"desc": "200 easy choice", "dist": 200},
        {"desc": "8x25 easy kick", "dist": 200},
    ],
    "cooldown": [
        {"desc": "200 easy swim", "dist": 200},
        {"desc": "100 choice", "dist": 100},
    ]
}


def parse_yard_range(s: str) -> int:
    """Parse input like "500-1500" or "1000" and return an integer target yardage.

    For a range, return the midpoint. On parse error, return 1000.
    """
    s = s.strip()
    if not s:
        return 1000
    if "-" in s:
        try:
            lo, hi = [int(x) for x in s.split("-", 1)]
            return max(1, (lo + hi) // 2)
        except ValueError:
            return 1000
    try:
        return max(1, int(s))
    except ValueError:
        return 1000


def _smallest_block_dist(blocks: Dict[str, List[Dict[str, int]]]) -> int:
    dists = [b["dist"] for opts in blocks.values() for b in opts]
    return min(dists) if dists else 25


def generate_exact_swim_set(level: str, target_yards: int, blocks: Dict[str, List[Dict[str, int]]]) -> Tuple[List[Tuple[str, str, int]], int]:
    """Generate a swim set whose total yards equal `target_yards` exactly.

    Strategy:
    - Start with smallest warmup and smallest cooldown to minimize unavoidable overhead.
    - Greedily add whole blocks that fit the remaining yards using a level-based priority.
    - When remaining yards are smaller than any block, fill with 50s and 25s (common swim increments).
    - If the target is smaller than the smallest warmup+cooldown, omit warmup/cooldown and use fillers.
    """
    lvl = level.lower()
    if lvl not in ("beginner", "intermediate", "advanced"):
        lvl = "intermediate"

    # Pick smallest warmup and cooldown to preserve yards for main set
    warm_opts = blocks.get("warmup", [])
    cooldown_opts = blocks.get("cooldown", [])
    warm_choice = min(warm_opts, key=lambda b: b["dist"]) if warm_opts else {"desc": "warmup", "dist": 0}
    cool_choice = min(cooldown_opts, key=lambda b: b["dist"]) if cooldown_opts else {"desc": "cooldown", "dist": 0}

    warm_dist = warm_choice.get("dist", 0)
    cool_dist = cool_choice.get("dist", 0)

    remaining = target_yards - warm_dist - cool_dist

    # If remaining negative, try removing warmup first, then cooldown
    if remaining < 0:
        # try no warmup
        remaining = target_yards - cool_dist
        warm_choice = None
        warm_dist = 0
    if remaining < 0:
        # try no cooldown either
        remaining = target_yards
        cool_choice = None
        cool_dist = 0

    # Build priorities
    priorities = {
        "beginner": ["technique", "endurance", "recovery", "sprint"],
        "intermediate": ["endurance", "technique", "sprint", "recovery"],
        "advanced": ["sprint", "endurance", "technique", "recovery"],
    }
    order = priorities[lvl]

    set_items: List[Tuple[str, str, int]] = []
    if warm_choice:
        set_items.append(("warmup", warm_choice["desc"], warm_choice["dist"]))

    # Greedy addition of whole blocks
    attempts = 0
    min_block = _smallest_block_dist(blocks)
    while remaining >= min_block and attempts < 200:
        added = False
        for section in order:
            opts = blocks.get(section, [])
            if not opts:
                continue
            fitting = [b for b in opts if b["dist"] <= remaining]
            if fitting:
                choice = random.choice(fitting)
                set_items.append((section, choice["desc"], choice["dist"]))
                remaining -= choice["dist"]
                added = True
                break
        if not added:
            break
        attempts += 1

    # Fill remaining with common small increments (50, then 25, then 1)
    filler_units = [50, 25, 1]
    for unit in filler_units:
        while remaining >= unit:
            desc = f"{unit} easy" if unit >= 25 else f"{unit} drill"
            set_items.append(("fill", desc, unit))
            remaining -= unit

    # Finally add cooldown if chosen
    if cool_choice:
        set_items.append(("cooldown", cool_choice["desc"], cool_choice["dist"]))

    total = sum(x[2] for x in set_items)

    # As a safeguard, if totals don't match due to rounding issues, adjust with 1-yd fillers
    if total != target_yards:
        diff = target_yards - total
        if diff > 0:
            for _ in range(diff):
                set_items.append(("fill", "1 easy", 1))
        elif diff < 0:
            # If overshot (shouldn't happen), try to remove the last fillers first
            overshoot = -diff
            new_items = []
            removed = 0
            for sec, desc, d in reversed(set_items):
                if removed >= overshoot:
                    new_items.append((sec, desc, d))
                else:
                    if sec == "fill":
                        removed += d
                    else:
                        new_items.append((sec, desc, d))
            set_items = list(reversed(new_items))
        total = sum(x[2] for x in set_items)

    return set_items, total


def prompt_swim_info():
    print("Hello welcome to swimset, please state your swim level and desired yard range")
    level = input("Swim level (beginner/intermediate/advanced): ").strip()
    yard_range = input("Desired yard range (e.g., 500-1500 or 1000): ").strip()
    print()
    print(f"Received: level='{level}', yard_range='{yard_range}'")
    return level, yard_range


def main():
    try:
        level, yard_range = prompt_swim_info()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return

    target = parse_yard_range(yard_range)
    swim_set, total = generate_exact_swim_set(level, target, blocks)

    print("\nGenerated Swim Set (exact target)")
    current_section = None
    for section, desc, dist in swim_set:
        if section != current_section:
            print(f"\n{section.upper()}")
            current_section = section
        print(f" - {desc} ({dist} yds)")

    print(f"\nTotal: {total} yds (target was {target} yds)")


if __name__ == "__main__":
    main()