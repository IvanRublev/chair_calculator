class Constants:
    # Characters that are used to markup the room names.
    ROOM_LABEL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"

    # Characters that are used to markup the chairs.
    # Defines the order of chairs in the output line.
    CHAIR_CHARS = "WPSC"

    # Character which is used to markup the floor.
    FLOOR_CHAR = " "

    # Characters that can be used to markup the room names, chairs, and floor.
    # Every character that is not a wall.
    ROOM_MARKUP_CHARS = ROOM_LABEL_CHARS + CHAIR_CHARS + FLOOR_CHAR
