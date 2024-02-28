

def color_to_rgb(color: str):
    """
    Transform color name to RGB value
    """

    return {
        "red": (235, 15, 67),
        "green": (97, 190, 46),
        "blue": (13, 132, 207),
        "orange": (252, 137, 8),
        "yellow": (255, 237, 56),
        "purple": (95, 37, 170),
        "pink": (255, 192, 203),
        "brown": (165, 42, 42),
        "gray": (128, 128, 128),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
        "light blue": (0, 120, 203),
        "dark purple": (63, 0, 151),
        "light green": (58, 172, 0),
        "black": (0, 0, 0)
    }.get(color, (0, 0, 0))