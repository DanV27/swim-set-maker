#!/usr/bin/env python3
"""Simple CLI for Swimset.

Prints a welcome message and asks the user for their swim level and desired yard range.
"""

def prompt_swim_info():
	"""Prompt the user for swim level and yard range and return them.

	Returns a tuple: (level: str, yard_range: str)
	"""
	print("Hello welcome to swimset, please state your swim level and desired yard range")
	level = input("Swim level (beginner/intermediate/advanced): ").strip()
	yard_range = input("Desired yard range (e.g., 500-1500): ").strip()
	print()
	print(f"Received: level='{level}', yard_range='{yard_range}'")
	return level, yard_range


def main():
	try:
		level, yard_range = prompt_swim_info()
	except (EOFError, KeyboardInterrupt):
		print("\nInput cancelled.")
		return

	# Placeholder for further logic — currently just acknowledges input.
	print("Thank you — your swim preferences have been recorded.")


if __name__ == "__main__":
	main()



sets = {
    "sprint": [
        "8x25 all out, :30 rest",
        "12x50 @ race pace, :45 rest",
    ],
    "endurance": [
        "5x200 moderate, :20 rest",
        "3x400 aerobic pace",
    ],
    "technique": [
        "6x50 drill/swim",
        "4x100 IM drill",
    ],
    "recovery": [
        "200 easy choice",
        "8x25 easy kick",
    ]
}