from src.chair_calculator_main import chairs_per_room


def test_chairs_calculator_pass_returning_list_of_cahirs_per_room():
    floor_plan = r"""
           +-----------------------+
           |                       |
           |                     S |
           |                       |
           |  P (room W)   +-------+
           |     P         |       | 
           |               |   P   |
           | C             |       | 
           |               +-----+ |
           |                     | |
           |   +-+            PC | |
           |  /   \   W          | |
           | /  W  \     +----+  | |
           |/       \   /     +--+ |
           +         +-+           |
           |                PP     |
           |  (room P)C            |
           |                       |
           +-----------------------+ 
           """

    # fmt: off
    assert chairs_per_room(floor_plan) == (
        "total:\n"
        "W: 2, P: 6, S: 1, C: 3\n"
        "room P:\n"
        "W: 1, P: 3, S: 0, C: 1\n"
        "room W:\n"
        "W: 1, P: 3, S: 1, C: 2\n"
    )
    # fmt: on


def test_chairs_calculator_pass_returning_list_of_cahirs_for_larger_room():
    floor_plan = r"""
            +-----------+------------------------------------+
            |           |                                    |
            | (closet)  |                                    |
            |         P |                            S       |
            |         P |         (sleeping room)            |
            |         P |                                    |
            |           |                                    |
            +-----------+    W                               |
            |           |                                    |
            |        W  |                                    |
            |           |                                    |
            |           +--------------+---------------------+
            |                          |                     |
            |                          |                W W  |
            |                          |    (office)         |
            |                          |                     |
            +--------------+           |                     |
            |              |           |                     |
            | (toilet)     |           |             P       |
            |   C          |           |                     |
            |              |           |                     |
            +--------------+           +---------------------+
            |              |           |                     |
            |              |           |                     |
            |              |           |                     |
            | (bathroom)   |           |      (kitchen)      |
            |              |           |                     |
            |              |           |      W   W          |
            |              |           |      W   W          |
            |       P      +           |                     |
            |             /            +---------------------+
            |            /                                   |
            |           /                                    |
            |          /                          W    W   W |
            +---------+                                      |
            |                                                |
            | S                                   W    W   W |
            |                (living room)                   |
            | S                                              |
            |                                                |
            |                                                |
            |                                                |
            |                                                |
            +--------------------------+---------------------+
                                    |                     |
                                    |                  P  |
                                    |  (balcony)          |
                                    |                 P   |
                                    |                     |
                                    +---------------------+
           """

    # fmt: off
    assert chairs_per_room(floor_plan) == (
        "total:\n"
        "W: 14, P: 7, S: 3, C: 1\n"
        "balcony:\n"
        "W: 0, P: 2, S: 0, C: 0\n"
        "bathroom:\n"
        "W: 0, P: 1, S: 0, C: 0\n"
        "closet:\n"
        "W: 0, P: 3, S: 0, C: 0\n"
        "kitchen:\n"
        "W: 4, P: 0, S: 0, C: 0\n"
        "living room:\n"
        "W: 7, P: 0, S: 2, C: 0\n"
        "office:\n"
        "W: 2, P: 1, S: 0, C: 0\n"
        "sleeping room:\n"
        "W: 1, P: 0, S: 1, C: 0\n"
        "toilet:\n"
        "W: 0, P: 0, S: 0, C: 1\n"
    )
    # fmt: on
