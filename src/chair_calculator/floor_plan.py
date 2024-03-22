from src.chair_calculator.validator import validate_margin, validate_non_chair_chars


def normalize_floor_plan(floor_plan: str) -> tuple[list[str], tuple[int, int]]:
    """Normalizes the given floor plan by padding each line with spaces to make them equal in length.

    Args:
        floor_plan (str): The original floor plan as a string.

    Returns:
        tuple[list[str], tuple[int, int]]: A tuple containing (normalized_lines, dimensions)
               The normalized_lines are a list of strings, where each string represents a padded line of the floor plan.
               The dimensions are represented as a tuple (width, height), where width is the maximum line length
               and height is the number of lines.
    """

    lines = floor_plan.split("\n")

    height = 0
    width = 0
    if lines != [""]:
        height = len(lines)
        width = max(map(len, lines))

    normalized_lines = [line.ljust(width) for line in lines]

    return normalized_lines, (width, height)


def room_label_coordinates(
    floor_plan: list[str], dimensions: tuple[int, int]
) -> dict[str, tuple[tuple[int, int], tuple[int, int]]]:
    """Extracts the room labels and their coordinates from a given floor plan.

    Args:
        floor_plan (list[str]): The floor plan represented as a list of strings.
        dimensions (tuple[int, int]): The dimensions of the floor plan (width, height).

    Returns:
        dict[str, tuple[tuple[int, int], tuple[int, int]]]: A dictionary mapping room names to their label coordinates.
            Each room name is associated with a tuple of two tuples representing the starting
            and ending coordinates of the label.

    Raises:
        ValueError: If the length of the floor plan does not match the specified dimensions.

    """

    # Iterate over the floor plan character by character,
    # detect the room name and its coordinates
    width, height = dimensions
    floor_square = width * height
    floor_plan_len = sum(map(len, floor_plan))
    if floor_square != floor_plan_len:
        raise ValueError(f"The floor plan length ({floor_plan_len}) \
does not match the dimensions ({width}x{height}={floor_square}).")

    coords_by_room = {}
    room_started = False
    name = ""
    label_start: tuple[int, int]
    for row, line in enumerate(floor_plan):
        for col, char in enumerate(line):
            if char == "(":
                room_started = True
                name = ""
                label_start = (col, row)
            elif char == ")" and room_started:
                room_started = False
                label_end = (col, row)
                validate_margin(
                    floor_plan,
                    start=label_start,
                    end=label_end,
                    error_text="The room label must have at least one space margin from each wall.",
                )
                coords_by_room[name] = (label_start, label_end)
            elif room_started:
                name += char

    coords_by_room = {k: coords_by_room[k] for k in sorted(coords_by_room)}

    return coords_by_room


def filter_chairs(floor_plan: list[str], label_coords: list[tuple[tuple[int, int], int]]) -> list[str]:
    """Filters chair characters and walls for calculation.

    Erases labels from a floor plan based on the given coordinates.

    Args:
        floor_plan (list[str]): The original floor plan as a list of strings.
        label_coords (list[tuple[tuple[int, int], int]]): The coordinates of the labels to be erased.
            Each label's coordinate is a tuple of two tuples (start_x, end_x) and y.

    Returns:
        list[str]: The updated floor plan without room labels.

    """
    plan_chars = [list(line) for line in floor_plan]

    for (start_x, end_x), y in label_coords:
        plan_chars[y][start_x : end_x + 1] = " " * (end_x - start_x + 1)

    updated_plan = ["".join(line) for line in plan_chars]

    validate_non_chair_chars(
        updated_plan, lambda char: f"The floor plan should have only room labels and chair characters, '{char}' found."
    )

    return updated_plan
