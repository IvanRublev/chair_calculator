from src.chair_calculator.constants import Constants
from src.chair_calculator.validator import validate_margin, validate_non_chair_chars


def test_validate_margin_fails_when_no_margin_from_plan_border():
    # fmt: off
    floor_plan = [
        "            ",
        "    (room 1)",
        "            "
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(4, 1), end=(11, 1), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "            ",
        "            ",
        "  (room 1)  "
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(3, 3), end=(10, 3), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "            ",
        "(room 1)    ",
        "            "
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(1, 2), end=(8, 2), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "  (room 1)  ",
        "            ",
        "            "
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(2, 0), end=(9, 0), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)


def test_validate_margin_fails_when_no_margin_from_room_walls():
    # fmt: off
    floor_plan = [
        "+----------+",
        "|          |",
        "|  (room 1)|",
        "|          |",
        "+----------+"
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(3, 2), end=(10, 2), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "+----------+",
        "|          |",
        "| (room 1) |",
        "+----------+",        
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(2, 2), end=(9, 2), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "+----------+",
        "|          |",
        "|(room 1)  |",
        "|          |",
        "+----------+"
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(1, 2), end=(8, 2), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)

    # fmt: off
    floor_plan = [
        "+----------+",
        "| (room 1) |",
        "|          |",
        "+----------+"
    ]
    # fmt: on

    try:
        validate_margin(floor_plan, start=(2, 1), end=(9, 1), error_text="No margin.")
        assert False, "ValueError should be raised when label is not surrounded by room markup chars."
    except ValueError as e:
        assert "No margin." == str(e)


def test_validate_non_chair_char_passes_given_spaces_chairs_walls():
    floor_plan = [f"{Constants.CHAIR_CHARS}" r" +/\|-   "]

    validate_non_chair_chars(floor_plan, lambda _c: "Non chair chars error.")


def test_validate_non_chair_char_failes_given_text():
    floor_plan = ["hello"]

    try:
        validate_non_chair_chars(floor_plan, lambda c: f"Non chair chars error '{c}'.")
        assert False, "ValueError should be raised when given non spaces, chair, or wall character text."
    except ValueError as e:
        assert "Non chair chars error 'h'." == str(e)
