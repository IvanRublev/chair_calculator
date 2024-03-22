from src.chair_calculator.room import stats_for_masked_chairs, stats_totals, str_stats


def test_stats_for_masked_chairs_fail_given_mask_smaller_than_floor_plan():
    try:
        stats_for_masked_chairs([" "], mask=[""], filler="*")
        assert False, "ValueError should be raised when mask has less dimensions than floor plan."
    except ValueError as e:
        assert "The mask and floor plan must have the same dimensions." == str(e)


def test_stats_for_masked_chairs_pass_return_zero_stats_for_empty_floor_plan():
    assert stats_for_masked_chairs([], mask=[], filler="*") == {"W": 0, "P": 0, "S": 0, "C": 0}


def test_stats_for_masked_chairs_fails_when_no_margin_around_chair():
    # fmt: off
    floor_plan = [
       r"+----------+", 
       r"|  C       |",
       r"|          |",
       r"+----------+"
    ]
    # fmt: on

    try:
        stats_for_masked_chairs(floor_plan, mask=floor_plan, filler="C")
        assert False, "ValueError should be raised when chair label is not surrounded by room markup chars."
    except ValueError as e:
        assert "The chair 'C' must have at least one space margin from each wall." == str(e)


def test_stats_for_masked_chairs_pass_when_returns_chairs_stats_for_masked_room():
    # fmt: off
    floor_plan = [
       r"+----------+", 
       r"|  S     C |",
       r"|  +-+   + |",
       r"| /   \ / \|",
       r"|/  C  +   +",
       r"+  W       |",
       r"|  SS P  S |",
       r"|          |",
       r"+----------+"
    ]
    # fmt: on

    # fmt: off
    mask = [
        r"+----------+",
        r"|          |",
        r"|  +-+   + |",
        r"| /***\ /*\|",
        r"|/*****+***+",
        r"+**********|",
        r"|**********|",
        r"|**********|",
        r"+----------+"
    ]
    # fmt: on

    assert stats_for_masked_chairs(floor_plan, mask=mask, filler="*") == {"W": 1, "P": 1, "S": 3, "C": 1}


def test_stats_totals_pass_when_return_zeroes_for_no_stats():
    assert stats_totals([]) == {"W": 0, "P": 0, "S": 0, "C": 0}


def test_stats_totals_pass_when_aggregate_totals_for_chairs_stats():
    stats = [
        {"W": 1, "P": 1, "S": 3, "C": 1},
        {"W": 1, "P": 1, "S": 3, "C": 1},
        {"W": 1, "P": 1, "S": 3, "C": 3},
    ]

    assert stats_totals(stats) == {"W": 3, "P": 3, "S": 9, "C": 5}


def test_str_stats_pass_when_returns_empty_string_for_no_stats():
    assert str_stats({}) == ""


def test_str_stats_pass_when_returns_formatted_stats_string():
    stats = {"W": 3, "P": 3, "S": 9, "C": 5}

    assert str_stats(stats) == "W: 3, P: 3, S: 9, C: 5"
