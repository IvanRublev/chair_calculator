from src.chair_calculator.floor_plan import filter_chairs, normalize_floor_plan, room_label_coordinates


def test_normalize_floor_plan_pass_when_returns_dimensions():
    _plan, dimensions = normalize_floor_plan("")
    assert (0, 0) == dimensions

    _plan, dimensions = normalize_floor_plan("   ")
    assert (3, 1) == dimensions

    _plan, dimensions = normalize_floor_plan("   \n   ")
    assert (3, 2) == dimensions

    _plan, dimensions = normalize_floor_plan("  \n          x\n ")
    assert (11, 3) == dimensions, "width should be calculated by the longest line"


def test_normalize_floor_plan_pass_when_returns_plan_filled_with_spaces_up_to_widht():
    # fmt: off
    plan, _dimensions = normalize_floor_plan(
        "  a\n"
        "          x\n"
        "b"
    )
    # fmt: on
    # fmt: off
    assert [
        "  a        ",
        "          x",
        "b          "
    ] == plan, "should fill the lines with spaces up to the width"
    # fmt: on


def test_room_label_coordinates_fails_when_floor_plan_mismatches_dimensions():
    try:
        room_label_coordinates(["     "], (2, 1))
        assert False, "ValueError should be raised when the floor plan length does not match the dimensions."
    except ValueError as e:
        assert "The floor plan length (5) does not match the dimensions (2x1=2)." == str(e)

    try:
        room_label_coordinates([""], (2, 1))
        assert False, "ValueError should be raised when the floor plan length does not match the dimensions."
    except ValueError as e:
        assert "The floor plan length (0) does not match the dimensions (2x1=2)." == str(e)


def test_room_label_coordinates_pass_when_returns_no_rooms_for_empty_floor_plan():
    assert (
        room_label_coordinates(
            [""],
            (0, 0),
        )
        == {}
    )


def test_room_label_coordinates_pass_when_ignores_labels_not_of_a_room_format_in_the_floor_plan():
    assert (
        room_label_coordinates(
            ["*+! b room"],
            (10, 1),
        )
        == {}
    )


def test_room_label_coordinates_fails_when_no_margin_around_label():
    # fmt: off
    floor_plan = [
        "            ",
        "            ",
        "    (room 1)"
    ]
    # fmt: on

    try:
        room_label_coordinates(floor_plan, (12, 3))
        assert False, "ValueError should be raised when room label is not surrounded by room markup chars."
    except ValueError as e:
        assert "The room label must have at least one space margin from each wall." == str(e)


def test_room_label_coordinates_pass_when_returns_room_coordinate_by_name():
    # fmt: off
    floor_plan = [
        "            ", 
        "   (room 1)C",
        "       W    ", 
    ]
    # fmt: on

    assert room_label_coordinates(floor_plan, (12, 3)) == {"room 1": ((3, 1), (10, 1))}


def test_room_label_coordinates_pass_when_returns_rooms_sorted_alphabetically():
    # fmt: off
    floor_plan = [
        "        ",
        " (B)(A) ", 
        "        "
    ]
    # fmt: on

    assert list(room_label_coordinates(floor_plan, (8, 3)).keys()) == ["A", "B"]


def test_room_label_coordinates_pass_when_ignores_dangling_brackets():
    # fmt: off
    floor_plan = [
        "  (     ",
        " (B)(A))", 
        "    ))  "
    ]
    # fmt: on

    assert room_label_coordinates(floor_plan, (8, 3)) == {"A": ((4, 1), (6, 1)), "B": ((1, 1), (3, 1))}


def test_filter_chairs_pass_when_returns_plan_as_is_given_no_coordinates_to_erase():
    # fmt: off
    floor_plan = [
        "+-------+", 
        "| C     |",
        "|     W |", 
        "+-------+"
    ]
    # fmt: on

    assert filter_chairs(floor_plan, label_coords=[]) == floor_plan


def test_filter_chairs_pass_when_removes_labels_at_given_coordinates():
    # fmt: off
    floor_plan = [
        "+-------+", 
        "| C(B)  |",
        "| (A) W |", 
        "+-------+"
    ]
    # fmt: on

    updated_plan = filter_chairs(floor_plan, label_coords=[((3, 5), 1), ((2, 4), 2)])

    # fmt: off
    assert [
        "+-------+", 
        "| C     |",
        "|     W |", 
        "+-------+"
    ] == updated_plan
    # fmt: on


def test_filter_chairs_fails_when_non_chair_text_left_afer_filtering():
    # fmt: off
    floor_plan = [
        "+-----------+", 
        "| C   P     |",
        "| comment W |", 
        "+-----------+"
    ]
    # fmt: on

    try:
        filter_chairs(floor_plan, label_coords=[])
        assert False, "ValueError should be raised when the floor plan has non chair character text."
    except ValueError as e:
        assert "The floor plan should have only room labels and chair characters, 'c' found." == str(e)
