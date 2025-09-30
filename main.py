#!/usr/bin/env python3
"""Simple CLI for Swimset.

This script asks for a swim level and a desired yard target.
"""

# Add a dictionary to store warm-ups categorized by levels
warm_ups = {
    "beginner": [],
    "intermediate": [],
    "advanced": []
}

# Add a dictionary to store cool-downs categorized by levels
cool_downs = {
    "beginner": [],
    "intermediate": [],
    "advanced": []
}

# Add a dictionary to store drills categorized by levels
drills = {
    "beginner": [],
    "intermediate": [],
    "advanced": []

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