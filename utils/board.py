"""
Monopoly Board Configuration
Defines all spaces, their names, types, and color groups.
"""

# Board spaces with their names
BOARD_SPACES = {
    0: "GO",
    1: "Mediterranean Avenue",
    2: "Community Chest",
    3: "Baltic Avenue",
    4: "Income Tax",
    5: "Reading Railroad",
    6: "Oriental Avenue",
    7: "Chance",
    8: "Vermont Avenue",
    9: "Connecticut Avenue",
    10: "Jail (Just Visiting)",
    11: "St. Charles Place",
    12: "Electric Company",
    13: "States Avenue",
    14: "Virginia Avenue",
    15: "Pennsylvania Railroad",
    16: "St. James Place",
    17: "Community Chest",
    18: "Tennessee Avenue",
    19: "New York Avenue",
    20: "Free Parking",
    21: "Kentucky Avenue",
    22: "Chance",
    23: "Indiana Avenue",
    24: "Illinois Avenue",
    25: "B&O Railroad",
    26: "Atlantic Avenue",
    27: "Ventnor Avenue",
    28: "Water Works",
    29: "Marvin Gardens",
    30: "Go to Jail",
    31: "Pacific Avenue",
    32: "North Carolina Avenue",
    33: "Community Chest",
    34: "Pennsylvania Avenue",
    35: "Short Line Railroad",
    36: "Chance",
    37: "Park Place",
    38: "Luxury Tax",
    39: "Boardwalk"
}

# Identify special space types
CHANCE_SPACES = [7, 22, 36]
COMMUNITY_CHEST_SPACES = [2, 17, 33]
RAILROAD_SPACES = [5, 15, 25, 35]
UTILITY_SPACES = [12, 28]
GO_TO_JAIL_SPACE = 30
JAIL_SPACE = 10
GO_SPACE = 0

# Color groups for analysis
COLOR_GROUPS = {
    "Brown": [1, 3],
    "Light Blue": [6, 8, 9],
    "Pink": [11, 13, 14],
    "Orange": [16, 18, 19],
    "Red": [21, 23, 24],
    "Yellow": [26, 27, 29],
    "Green": [31, 32, 34],
    "Dark Blue": [37, 39],
    "Railroads": [5, 15, 25, 35],
    "Utilities": [12, 28]
}

def get_space_name(space_number):
    """Return the name of a space given its number."""
    return BOARD_SPACES.get(space_number, f"Unknown Space {space_number}")

def is_chance(space):
    """Check if a space is a Chance space."""
    return space in CHANCE_SPACES

def is_community_chest(space):
    """Check if a space is a Community Chest space."""
    return space in COMMUNITY_CHEST_SPACES

def get_color_group(space):
    """Return the color group name for a given space, or None if not in a group."""
    for group_name, spaces in COLOR_GROUPS.items():
        if space in spaces:
            return group_name
    return None
