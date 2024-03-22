from typing import Callable

from src.chair_calculator.constants import Constants


def validate_margin(floor_plan: list[str], start: tuple[int, int], end: tuple[int, int], error_text: str) -> None:
    """Validates the margin of a given label within the specified start and end coordinates.

    Can validate the margin around chair charecter when start tuple equals end one.

    Margin is one character wide line around the given label line.
    In the following example the `*` character depicts the margin for the label:
    ```
    *************
    *(room name)*
    *************
    ```
    and for the chair character:
    ```
    ***
    *P*
    ***
    ```

    Args:
        floor_plan (list[str]): The floor plan represented as a list of strings.
        start (tuple[int, int]): The starting coordinates (x, y) of the label.
        end (tuple[int, int]): The ending coordinates (x, y) of the label.
        error_text (str): The error message to be raised if the margin is invalid.

    Raises:
        ValueError: If the margin is invalid.

    Returns:
        None
    """
    start_x, start_y = start
    end_x, _end_y = end

    try:
        if start_x == 0 or start_y == 0:
            raise ValueError

        margin = floor_plan[start_y][start_x - 1]
        margin += floor_plan[start_y + 1][start_x - 1 : end_x + 2]
        margin += floor_plan[start_y][end_x + 1]
        margin += floor_plan[start_y - 1][start_x - 1 : end_x + 2]
        for char in margin:
            if char not in Constants.ROOM_MARKUP_CHARS:
                raise ValueError

    except Exception as _e:
        raise ValueError(error_text)


def validate_non_chair_chars(floor_plan: list[str], error_message_fun: Callable[[str], str]) -> None:
    """Validates the non-chair characters in the given floor plan.

    Args:
        floor_plan (list[str]): The floor plan represented as a list of strings without room labels.
        error_message_fun (Callable[[str], str]): A function that takes a non-chair character as input
            and returns an error message.

    Raises:
        ValueError: If a non-chair character is found in the floor plan.

    Returns:
        None
    """
    non_chair_floor_wall_chars = [
        char
        for char in Constants.ROOM_MARKUP_CHARS
        if char != Constants.FLOOR_CHAR and char not in Constants.CHAIR_CHARS
    ]

    for line in floor_plan:
        for char in line:
            if char in non_chair_floor_wall_chars:
                raise ValueError(error_message_fun(char))
