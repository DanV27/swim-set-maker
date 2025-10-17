#!/usr/bin/env python3
"""Simple CLI for Swimset.

This script asks for a swim level and a desired yard target.
"""

from data import warm_ups, cool_downs, drills, main_sets
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

def parse_args():
    p = argparse.ArgumentParser(description="Swimset CLI")
    p.add_argument("--level", choices=["beginner", "intermediate", "advanced"],
                   help="swimmer level (non-interactive)")
    p.add_argument("--yards", type=int, choices=[500, 1000, 1500, 2000],
                   help="desired total yards (non-interactive)")
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

    print(f"\nYou selected: Level = {level.capitalize()}, Yards = {yards}")
    warm, main, cool = generate_simple_set(level, yards)

    print("\nGenerated simple set:")
    print(f"\nWARMUP: {warm[1]} ({warm[0]} yds)")
    print(f"MAIN: {main[1]} ({main[0]} yds)")
    print(f"COOLDOWN: {cool[1]} ({cool[0]} yds)")

    total = (warm[0] or 0) + (main[0] or 0) + (cool[0] or 0)
    print(f"\nTotal: {total} yds")

    print("\nThank you for using Swimset!")

if __name__ == "__main__":
    main()