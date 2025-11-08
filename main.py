#!/usr/bin/env python3
"""Simple CLI for Swimset.

This script asks for a swim level and a desired yard target.
"""

from data import warm_ups, cool_downs, drills, main_sets, small_blocks
import random
import argparse


def generate_simple_set(level: str, yards: int):
    """Return a tuple (warmup_desc, main_desc, cooldown_desc) for the given level and yards.

    - warmup: pick the smallest warmup available for level
    - main: pick the main_sets[level][yards] first entry if present, else choose closest smaller key
    - cooldown: pick the smallest cooldown available for level
    """
    lvl = level.lower()
    # Warmup
    warm_options = warm_ups.get(lvl, {})
    if warm_options:
        warm_key = min(warm_options.keys())
        warm_desc = random.choice(warm_options[warm_key])
    else:
        warm_key = 0
        warm_desc = "200 easy"

    # Main set selection
    mains = main_sets.get(lvl, {})
    if yards in mains:
        key = yards
        main_desc = random.choice(mains[yards])
    else:
        # pick the largest main key <= yards, otherwise pick the smallest available
        smaller_keys = [k for k in mains.keys() if k <= yards]
        if smaller_keys:
            key = max(smaller_keys)
        elif mains:
            key = min(mains.keys())
        else:
            key = yards
        main_desc = random.choice(mains[key]) if mains else f"{yards} swim"

    # Cooldown
    cool_options = cool_downs.get(lvl, {})
    if cool_options:
        cool_key = min(cool_options.keys())
        cool_desc = random.choice(cool_options[cool_key])
    else:
        cool_key = 0
        cool_desc = "100 easy"

    return (warm_key, warm_desc), (key, main_desc), (cool_key, cool_desc)

def prompt_swim_info():
    print("Welcome to Swimset!")
    level = input("Are you a beginner, intermediate, or advanced swimmer? ").strip().lower()
    while level not in ("beginner", "intermediate", "advanced"):
        print("Invalid input. Please choose from beginner, intermediate, or advanced.")
        level = input("Are you a beginner, intermediate, or advanced swimmer? ").strip().lower()

    print("\nChoose your desired swim yards:")
    print("Options: 500, 1000, 1500, 2000")
    try:
        yards = int(input("Enter your desired swim yards: ").strip())
        while yards not in (500, 1000, 1500, 2000):
            print("Invalid input. Please choose from 500, 1000, 1500, or 2000.")
            yards = int(input("Enter your desired swim yards: ").strip())
    except ValueError:
        print("Invalid input. Defaulting to 1000 yards.")
        yards = 1000

    return level, yards


def generate_total_matched_set(level: str, target_total: int, include_drills: bool = False):
    """Generate a set where the total (warm+main+cool) attempts to match target_total.

    Returns (warm, main, cool) where main is (yards, [descriptions...])
    """
    lvl = level.lower()
    # pick smallest warm and cooldown to minimize overhead
    warm_options = warm_ups.get(lvl, {})
    cool_options = cool_downs.get(lvl, {})
    warm_key = min(warm_options.keys()) if warm_options else 0
    warm_desc = random.choice(warm_options[warm_key]) if warm_options else ""
    cool_key = min(cool_options.keys()) if cool_options else 0
    cool_desc = random.choice(cool_options[cool_key]) if cool_options else ""

    warm_dist = warm_key
    cool_dist = cool_key

    remaining = target_total - warm_dist - cool_dist

    # If negative, try removing warm then cooldown
    if remaining < 0:
        # drop warm
        warm_key = 0
        warm_desc = ""
        warm_dist = 0
        remaining = target_total - warm_dist - cool_dist
    if remaining < 0:
        # drop cooldown too
        cool_key = 0
        cool_desc = ""
        cool_dist = 0
        remaining = target_total

    mains = main_sets.get(lvl, {})
    main_items = []  # list of (size, desc)
    main_total = 0

    # Greedy: use largest available main blocks first
    main_sizes = sorted(mains.keys(), reverse=True) if mains else []
    while remaining > 0:
        picked = None
        # try mains first
        for s in main_sizes:
            if s <= remaining:
                picked = s
                break
        if picked:
            desc = random.choice(mains[picked])
            main_items.append((picked, desc))
            remaining -= picked
            main_total += picked
            continue

        # fall back to small blocks
        small_sizes = sorted(small_blocks.keys(), reverse=True)
        for u in small_sizes:
            if u <= remaining:
                main_items.append((u, small_blocks[u][0]))
                remaining -= u
                main_total += u
                picked = u
                break
        if not picked:
            # cannot represent remaining (less than smallest block)
            # as last resort, break (will produce total less than target)
            break

    # After greedy assembly, try to append a small block that may overshoot
    # only if the resulting total ends in a multiple of 50 (user-tolerated overshoot)
    current_total = (warm_key or 0) + main_total + (cool_key or 0)
    if current_total < target_total:
        # try small blocks and pick the one that reaches or minimally overshoots the target
        small_sizes_asc = sorted(small_blocks.keys())
        candidates = []
        for u in small_sizes_asc:
            candidate = current_total + u
            if candidate >= target_total and candidate % 50 == 0:
                candidates.append((candidate - target_total, u, candidate))
        if candidates:
            # pick minimal overshoot
            candidates.sort()
            _, u, candidate = candidates[0]
            main_items.append((u, small_blocks[u][0]))
            main_total += u
            current_total = candidate

    # Optionally try to insert drills while keeping total close to target
    if include_drills:
        warm, (main_total, main_items), cool = try_insert_drills(level, (warm_key, warm_desc), (main_total, main_items), (cool_key, cool_desc), target_total)

    return (warm_key, warm_desc), (main_total, main_items), (cool_key, cool_desc)


def try_insert_drills(level: str, warm, main, cool, target_total: int):
    """Attempt to insert a drill block into the main items without exceeding target_total.

    - main is (main_total, main_items) where main_items is list of (size, desc)
    - returns updated (warm, main, cool)
    """
    lvl = level.lower()
    drill_options = drills.get(lvl, {})
    if not drill_options:
        return warm, main, cool

    main_total, main_items = main
    current_total = (warm[0] or 0) + main_total + (cool[0] or 0)
    base_distance = abs(current_total - target_total)

    # Try drill sizes and choose an append/replace that minimizes overshoot while keeping
    # any overshoot <= max_overshoot. Prefer append if it fits under target.
    max_overshoot = 100
    best_choice = None  # tuple (overshoot, action, details)
    # consider appends
    for d in drill_options.keys():
        candidate_total = current_total + d
        new_distance = abs(candidate_total - target_total)
        if candidate_total <= target_total and new_distance <= base_distance:
            # perfect fit under target and not worse than current: choose immediately
            desc = random.choice(drill_options[d])
            main_items.append((d, desc))
            main_total += d
            current_total += d
            return warm, (main_total, main_items), cool
        else:
            overshoot = candidate_total - target_total
            if candidate_total % 50 == 0 and overshoot <= max_overshoot and new_distance <= base_distance:
                # candidate append is allowed; track as a possible choice
                if best_choice is None or overshoot < best_choice[0]:
                    best_choice = (overshoot, 'append', d)

    # consider replacements (try suffixes)
    for d in drill_options.keys():
        for start in range(len(main_items) - 1, -1, -1):
            suffix = main_items[start:]
            suffix_sum = sum(s for s, _ in suffix)
            if suffix_sum < d:
                continue
            new_total = current_total - suffix_sum + d
            new_distance = abs(new_total - target_total)
            if new_total <= target_total and new_distance <= base_distance:
                # accept replacement immediately
                desc = random.choice(drill_options[d])
                main_items = main_items[:start] + [(d, desc)]
                main_total = main_total - suffix_sum + d
                return warm, (main_total, main_items), cool
            else:
                overshoot = new_total - target_total
                if new_total % 50 == 0 and overshoot <= max_overshoot and new_distance <= base_distance:
                    if best_choice is None or overshoot < best_choice[0]:
                        best_choice = (overshoot, 'replace', d, start, suffix_sum)

    # perform best tracked allowed choice if any
    if best_choice:
        if best_choice[1] == 'append':
            _, _, d = best_choice
            desc = random.choice(drill_options[d])
            main_items.append((d, desc))
            main_total += d
            current_total += d
            return warm, (main_total, main_items), cool
        else:
            _, _, d, start, suffix_sum = best_choice
            desc = random.choice(drill_options[d])
            main_items = main_items[:start] + [(d, desc)]
            main_total = main_total - suffix_sum + d
            return warm, (main_total, main_items), cool

    # nothing fit without exceeding target; don't change
    return warm, (main_total, main_items), cool

def parse_args():
    p = argparse.ArgumentParser(description="Swimset CLI")
    p.add_argument("--level", choices=["beginner", "intermediate", "advanced"],
                   help="swimmer level (non-interactive)")
    p.add_argument("--yards", type=int, choices=[500, 1000, 1500, 2000],
                   help="desired total yards (non-interactive)")
    p.add_argument("--target-type", choices=["main", "total"], default="main",
                   help="whether the yards value refers to main-only or total (warm+main+cool)")
    p.add_argument("--include-drills", action="store_true",
                   help="include drills in the generated workout (only applied for total-target)")
    p.add_argument("--seed", type=int, help="random seed for deterministic output")
    p.add_argument("--no-input", action="store_true",
                   help="fail if required flags are not provided (no interactive prompts)")
    return p.parse_args()


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    if args.level and args.yards:
        level, yards = args.level, args.yards
    elif args.no_input:
        print("Non-interactive mode requires --level and --yards")
        return
    else:
        try:
            level, yards = prompt_swim_info()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            return

    print(f"\nYou selected: Level = {level.capitalize()}, Yards = {yards} (target-type={args.target_type})")
    if args.target_type == "main":
        warm, main, cool = generate_simple_set(level, yards)
    else:
        # target refers to total yards; attempt to build warm+main+cool ~= yards
        warm, main, cool = generate_total_matched_set(level, yards, include_drills=args.include_drills)

    print("\nGenerated simple set:")
    print(f"\nWARMUP: {warm[1]} ({warm[0]} yds)")
    # main[1] may be a string or a list of descriptions
    if isinstance(main[1], list):
        print("MAIN:")
        for item in main[1]:
            if isinstance(item, tuple):
                print(f" - {item[1]}")
            else:
                print(f" - {item}")
        print(f"  ({main[0]} yds)")
    else:
        print(f"MAIN: {main[1]} ({main[0]} yds)")
    print(f"COOLDOWN: {cool[1]} ({cool[0]} yds)")

    total = (warm[0] or 0) + (main[0] or 0) + (cool[0] or 0)
    print(f"\nTotal: {total} yds")

    print("\nThank you for using Swimset!")

if __name__ == "__main__":
    main()