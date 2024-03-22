from src.chair_calculator.room import mask_room, print_mask


def test_mask_room_fails_when_floor_plan_mismatch_dimensions():
    try:
        mask_room(["     "], dimensions=(2, 1), seed_point=(1, 1), filler="*")
        assert False, "ValueError should be raised when the floor plan length does not match the dimensions."
    except ValueError as e:
        assert "The floor plan length (5) does not match the dimensions (2x1=2)." == str(e)


def test_mask_room_fails_if_filler_is_longer_than_one_character():
    try:
        mask_room([" "], dimensions=(1, 1), seed_point=(1, 1), filler="**")
        assert False, "ValueError should be raised when the filler is longer than one character."
    except ValueError as e:
        assert "Filler must be a single character." == str(e)


def test_mask_room_fails_if_filler_is_one_of_ROOM_MARKUP_CHARS():
    try:
        mask_room([" "], dimensions=(1, 1), seed_point=(1, 1), filler="W")
        assert False, "ValueError should be raised when the filler is one of room characters."
    except ValueError as e:
        assert "Filler must not be one of room markup chars." == str(e)


def test_mask_room_passes_when_fills_empty_plan():
    # fmt: off
    floor_plan = [
        "     ",
        "     ", 
        "     "
    ]
    # fmt: on

    mask = mask_room(
        floor_plan,
        dimensions=(5, 3),
        seed_point=(1, 1),
        filler="*",
    )

    # fmt: off
    assert [
        "*****",
        "*****",
        "*****"
    ] == mask
    # fmt: on


def test_mask_room_passes_when_overwrites_room_names():
    # fmt: off
    floor_plan = [
        " (A) ",
        "  (B)",
        "     "
    ]
    # fmt: on

    mask = mask_room(floor_plan, dimensions=(5, 3), seed_point=(1, 1), filler="*")

    # fmt: off
    assert [
        "*****",
        "*****",
        "*****",
    ] == mask
    # fmt: on


def test_mask_room_passes_when_fills_room_of_square_shape():
    # fmt: off
    floor_plan = [
        "        ",
        " +----+ ",
        " |    | ",
        " +----+ ",
        "        "
    ]
    # fmt: on

    mask = mask_room(floor_plan, dimensions=(8, 5), seed_point=(2, 2), filler="*")

    # fmt: off
    assert [
        "        ",
        " +----+ ",
        " |****| ",
        " +----+ ",
        "        "
    ] == mask
    # fmt: on


def test_mask_room_passes_when_fills_room_with_a_hall():
    # fmt: off
    floor_plan = [
        "  +-------+",
        "  | P     |",
        "  +-----+ |",
        "+----+  | |",
        "|    |  | |",
        "|    +--+ |",
        "|         |",
        "+---------+"
    ]
    # fmt: on

    mask = mask_room(floor_plan, dimensions=(11, 8), seed_point=(1, 4), filler="*")

    # fmt: off
    assert [
        "  +-------+",
        "  |*******|",
        "  +-----+*|",
        "+----+  |*|",
        "|****|  |*|",
        "|****+--+*|",
        "|*********|",
        "+---------+"
    ] == mask
    # fmt: on


def test_mask_room_passes_when_fills_room_of_polygonal_shape():
    # fmt: off
    floor_plan = [
       r"+----------+", 
       r"|          |",
       r"|  +-+   + |",
       r"| /   \ / \|",
       r"|/     +   +",
       r"+  W       |",
       r"|          |",
       r"+----------+"
    ]
    # fmt: on

    mask = mask_room(floor_plan, dimensions=(12, 8), seed_point=(4, 6), filler="*")

    # fmt: off
    assert [
        r"+----------+", 
        r"|          |",
        r"|  +-+   + |",
        r"| /***\ /*\|",
        r"|/*****+***+",
        r"+**********|",
        r"|**********|",
        r"+----------+"
    ] == mask
    # fmt: on


def test_print_mask_pass_when_returns_mask_as_str():
    assert print_mask(["*", " "]) == "*\n "
