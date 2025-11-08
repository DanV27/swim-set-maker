#!/usr/bin/env python3
"""Data module for Swimset: building blocks for workouts."""

# Warmups, cooldowns and drills as module-level dictionaries (keys = yards)
warm_ups = {
    "beginner": {
        100: ["100 EASY", "100 IM"],
        150: ["50 SWIM/KICK/PULL", "3x50 EZ"]
    },
    "intermediate": {
        200: ["200 EASY"],
        300: ["100 SWIM/KICK/PULL", "3x100 EZ"]
    },
    "advanced": {
        200: ["200 EASY"],
        500: ["500 EASY"],
        600: ["200 SWIM/KICK/PULL"]
    }
}

cool_downs = {
    "beginner": {
        50: ["50 COOL DOWN"],
        100: ["100 EASY"]
    },
    "intermediate": {
        100: ["100 COOL DOWN"],
        50: ["50 EASY"]
    },
    "advanced": {
        200: ["200 COOL DOWN"],
        100: ["100 EASY"]
    }
}

drills = {
    "beginner": {
        200: ["2x100 ZIPPER DRILL", "2x100 CATCH-UP DRILL", "2x100 KICKBOARD", "2x100 STREAMLINE KICK"]
    },
    "intermediate": {
        200: ["2x100 ZIPPER DRILL", "2x100 CATCH-UP DRILL", "2x100 KICKBOARD", "2x100 STREAMLINE KICK", "2x100 3-3-3"],
        400: ["4x100 FINGER-TIP DRILL", "4x100 ZIPPER DRILL", "4x100 CATCH-UP DRILL", "4x100 KICKBOARD", "4x100 STREAMLINE KICK", "4x100 3-3-3"]
    },
    "advanced": {
        400: ["4x100 FINGER-TIP DRILL", "4x100 ZIPPER DRILL", "4x100 CATCH-UP DRILL", "4x100 KICKBOARD", "4x100 STREAMLINE KICK", "4x100 3-3-3", "4x100 2KICK-1PULL", "4x100 6-KICK SWITCH"],
        500: ["5x100 FINGER-TIP DRILL", "5x100 ZIPPER DRILL", "5x100 CATCH-UP DRILL"]
    }
}

main_sets = {
    "beginner": {
        500: ["5x100 @ 2:00", "5x50 @ 1:30"],
        1000: ["10x100 @ 2:00", "10x50 @ 1:30"],
        1500: ["15x100 @ 2:00", "15x50 @ 1:30"],
        2000: ["20x100 @ 2:00", "20x50 @ 1:30"]
    },
    "intermediate": {
        500: ["5x100 @ 1:45", "5x50 @ 1:15"],
        1000: ["10x100 @ 1:45", "10x50 @ 1:15"],
        1500: ["15x100 @ 1:45", "15x50 @ 1:15"],
        2000: ["20x100 @ 1:45", "20x50 @ 1:15"]
    },
    "advanced": {
        500: ["5x100 @ 1:30", "5x50 @ 1:00"],
        1000: ["10x100 @ 1:30", "10x50 @ 1:00"],
        1500: ["15x100 @ 1:30", "15x50 @ 1:00"],
        2000: ["20x100 @ 1:30", "20x50 @ 1:00"]
    }
}

# Small building blocks to allow composing arbitrary totals
small_blocks = {
    100: ["100 SWIM"],
    50: ["50 SWIM"],
    25: ["25 SWIM"],
}