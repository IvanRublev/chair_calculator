from src.chair_calculator.constants import Constants
from src.chair_calculator.validator import validate_margin


def mask_room(
    floor_plan: list[str], dimensions: tuple[int, int], seed_point: tuple[int, int], filler: str
) -> list[str]:
    """Masks a room in the floor plan with a given filler character.

    Args:
        floor_plan (list[str]): The floor plan represented as a list of strings.
        dimensions (tuple[int, int]): The dimensions of the room (width, height).
        seed_point (tuple[int, int]): The zero-based starting point for masking (x, y).
        filler (str): The character used to fill the room.

    Returns:
        list[str]: The masked floor plan with the room filled.

    Raises:
        ValueError: If the floor plan length does not match the dimensions.
        ValueError: If the filler is not a single character.
        ValueError: If the filler is one of the room markup characters.

    """
    width, height = dimensions
    floor_square = width * height
    floor_plan_len = sum(map(len, floor_plan))

    if floor_square != floor_plan_len:
        raise ValueError(f"The floor plan length ({floor_plan_len}) \
does not match the dimensions ({width}x{height}={floor_square}).")

    if len(filler) > 1:
        raise ValueError("Filler must be a single character.")

    if filler in Constants.ROOM_MARKUP_CHARS:
        raise ValueError("Filler must not be one of room markup chars.")

    masked_chars = [list(line) for line in floor_plan]

    stack = [seed_point]

    def can_fill(x, y):
        # Don't fill chars outside of the plan
        if x == -1 or x == width or y == -1 or y == height:
            return False

        # Don't fill chars that we already filled
        char = masked_chars[y][x]
        can = char in Constants.ROOM_MARKUP_CHARS and char != filler
        return can

    def find_seed_points(lx, rx, y):
        for x in range(lx, rx + 1):
            if can_fill(x, y):
                stack.append((x, y))

    while len(stack) > 0:
        x, y = stack.pop()
        lx = x

        # Fill to the left
        while can_fill(lx, y):
            masked_chars[y][lx] = filler
            lx -= 1

        # Fill to the right
        rx = x + 1
        while can_fill(rx, y):
            masked_chars[y][rx] = filler
            rx += 1

        # Find new seed points above and below.
        # We span till the edge fillable points in the current row
        # to check for a wall because we might have diagonal piece of it
        # \ or / right above or below the fillable point on the edges.
        find_seed_points(lx + 1, rx - 1, y + 1)
        find_seed_points(lx + 1, rx - 1, y - 1)

    masked_lines = list(map("".join, masked_chars))

    return masked_lines


def print_mask(mask: list[str]) -> str:
    """Prints the masked floor plan.

    Args:
        mask (list[str]): The masked floor plan represented as a list of strings.

    Returns:
        str: The masked floor plan as a single string with each line separated by the newline characters.

    """
    return "\n".join(mask)


def stats_for_masked_chairs(floor_plan: list[str], mask: list[str], filler: str) -> dict[str, int]:
    """Calculates the statistics for masked chairs in a given floor plan.

    Args:
        floor_plan (list[str]): The floor plan represented as a list of strings.
        mask (list[str]): The mask represented as a list of strings with the same dimensions as the floor plan.
        filler (str): The character used to represent masked areas in the mask.

    Returns:
        dict[str, int]: A dictionary containing the count of each chair character found in the masked areas.
            Chair characters are from Constants.CHAIR_CHARS.

    Raises:
        ValueError: If the floor plan dimensions does not match the mask dimensions.
    """

    count_by_chair: dict[str, int] = {}
    try:
        for line_idx, floor_line in enumerate(floor_plan):
            mask_line = mask[line_idx]
            for char_idx, floor_char in enumerate(floor_line):
                mask_char = mask_line[char_idx]

                if mask_char == filler and floor_char in Constants.CHAIR_CHARS:
                    validate_margin(
                        floor_plan,
                        start=(char_idx, line_idx),
                        end=(char_idx, line_idx),
                        error_text=f"The chair '{floor_char}' must have at least one space margin from each wall.",
                    )
                    count_by_chair[floor_char] = count_by_chair.get(floor_char, 0) + 1

    except IndexError as _e:
        raise ValueError("The mask and floor plan must have the same dimensions.")

    count_by_chairs = {chair_char: count_by_chair.get(chair_char, 0) for chair_char in Constants.CHAIR_CHARS}

    return count_by_chairs


def stats_totals(stats: list[dict[str, int]]) -> dict[str, int]:
    """Calculates the total number of each type of chair based on the given statistics.

    Args:
        stats (list[dict[str, int]]): A list of dictionaries representing the statistics of each room.
            Each dictionary contains the count of each chair type, where the keys are chair characters
            from Constants.CHAIR_CHARS and the values are the corresponding counts.

    Returns:
        dict[str, int]: A dictionary containing the total count of each chair type across all rooms.
            The keys are chair characters and the values are the corresponding total counts.
    """

    totals = {chair_char: 0 for chair_char in Constants.CHAIR_CHARS}

    for stat in stats:
        for chair_char in Constants.CHAIR_CHARS:
            count = stat.get(chair_char, 0)
            totals[chair_char] = totals.get(chair_char, 0) + count

    return totals


def str_stats(stats: dict[str, int]) -> str:
    """Converts the given stats dictionary into a string representation.

    Args:
        stats (dict[str, int]): A dictionary containing chair characters as keys and their counts as values.

    Returns:
        str: A string representation of the stats dictionary, with chair characters
            and their counts separated by commas.
    """
    return ", ".join([f"{chair}: {count}" for chair, count in stats.items()])
