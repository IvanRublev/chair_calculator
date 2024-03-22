from src.chair_calculator.floor_plan import filter_chairs, normalize_floor_plan, room_label_coordinates
from src.chair_calculator.room import mask_room, stats_for_masked_chairs, stats_totals, str_stats


def chairs_per_room(plan_content: str) -> str:
    """Calculates the number of chairs for appartment and per each room based on the given floor plan.

    Args:
        plan_content (str): The floor plan containing room labels and chair characters.

    Returns:
        str: The output text containing the chair statistics total for apartment and per each room.

    """
    floor_plan: list[str]
    dimensions: tuple[int, int]
    floor_plan, dimensions = normalize_floor_plan(plan_content)

    # The following function will crash for room labels having no margin from walls
    coords_by_room = room_label_coordinates(floor_plan, dimensions=dimensions)

    # Remove labels from the plan so they don't interfere with the chair counting
    # because labels might containt chair characters.
    label_coords = []
    for _room, (label_start, label_end) in coords_by_room.items():
        label_start_x, label_start_y = label_start
        label_end_x, _label_end_y = label_end
        label_coords.append(((label_start_x, label_end_x), label_start_y))

    # The following function will remove labels by given coords,
    # it will crash for text characters left which are not chair characters, spaces, or walls.
    unlabeled_plan = filter_chairs(floor_plan, label_coords=label_coords)

    # Aggregate chair stats for each room
    stats_by_room = {}

    for room, (label_start, _label_end) in coords_by_room.items():
        mask = mask_room(unlabeled_plan, dimensions=dimensions, seed_point=label_start, filler="*")
        # The following function will crash for chair characters having no margin from walls
        stats = stats_for_masked_chairs(unlabeled_plan, mask=mask, filler="*")
        stats_by_room[room] = stats

    # Aggregate output text
    output = ""
    # Totals
    totals = stats_totals(list(stats_by_room.values()))
    output += f"total:\n{str_stats(totals)}\n"

    # Stats
    for room, stats in stats_by_room.items():
        output += f"{room}:\n{str_stats(stats)}\n"

    return output
