#!/usr/bin/env python3
"""Simple CLI for Swimset.

This script asks for a swim level and a desired yard target.
"""

# Redo warm_ups dictionary to match the structure of main_sets
def warm_ups():
    return {
        "beginner": {
            100: ["100 EASY", "100 IM"],
            150: ["50 SWIM/KICK/PULL"],
            
        },
        "intermediate": {
            300: ["100 SWIM/KICK/PULL"],
            200: ["200 EASY"],
        },
        "advanced": {
            200: ["200 EASY"],
            500: ["500 EASY"],
            600: ["200 SWIM/KICK/PULL"],
            
\
        }
    }

# Redo cool_downs dictionary to match the structure of main_sets
def cool_downs():
    return {
        "beginner": {
            50: ["50 COOL DOWN"],
        },
        "intermediate": {
            100: ["100 COOL DOWN"],
        },
        "advanced": {
            200: ["200 COOL DOWN"],
        }
    }

# Redo drills dictionary to match the structure of main_sets
def drills():
    return {
        "beginner": {
            500: ["ZIPPER DRILL"],
            1000: ["ZIPPER DRILL", "CATCH-UP DRILL"],
            1500: ["ZIPPER DRILL", "CATCH-UP DRILL", "ZIPPER DRILL"],
            2000: ["ZIPPER DRILL", "CATCH-UP DRILL", "ZIPPER DRILL", "CATCH-UP DRILL"]
        },
        "intermediate": {
            500: ["FINGER-TIP DRILL"],
            1000: ["FINGER-TIP DRILL", "3-3-3"],
            1500: ["FINGER-TIP DRILL", "3-3-3", "FINGER-TIP DRILL"],
            2000: ["FINGER-TIP DRILL", "3-3-3", "FINGER-TIP DRILL", "3-3-3"]
        },
        "advanced": {
            500: ["FINGER-TIP DRILL"],
            1000: ["FINGER-TIP DRILL", "3-3-3"],
            1500: ["FINGER-TIP DRILL", "3-3-3", "2 Kick 1 Pull"],
            2000: ["FINGER-TIP DRILL", "3-3-3", "2 Kick 1 Pull", "6 Kick Switch"]
        }
    }

# Add a dictionary to store main sets categorized by levels and yard targets
main_sets = {
    "beginner": {
        500: ["5x100 @ 2:00", "5x50 @ 1:15"],
        1000: ["10x100 @ 2:00", "10x50 @ 1:15"],
        1500: ["15x100 @ 2:00", "15x50 @ 1:15"],
        2000: ["20x100 @ 2:00", "20x50 @ 1:15"]
    },
    "intermediate": {
        500: ["5x100 @ 1:45", "5x50 @ 1:10"],
        1000: ["10x100 @ 1:45", "10x50 @ 1:10"],
        1500: ["15x100 @ 1:45", "15x50 @ 1:10"],
        2000: ["20x100 @ 1:45", "20x50 @ 1:10"]
    },
    "advanced": {
        500: ["5x100 @ 1:30", "5x50 @ :55"],
        1000: ["10x100 @ 1:30", "10x50 @ :55"],
        1500: ["15x100 @ 1:30", "15x50 @ :55"],
        2000: ["20x100 @ 1:30", "20x50 @ :55"]
    }
}

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

def main():
    try:
        level, yards = prompt_swim_info()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return

    print(f"\nYou selected: Level = {level.capitalize()}, Yards = {yards}")
    print("Thank you for using Swimset!")

if __name__ == "__main__":
    main()