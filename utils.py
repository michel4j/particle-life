

def color_to_rgb(color: str):
    """
    Transform color name to RGB value
    """

    return {
        "red": (233, 0, 45),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "orange": (254, 130, 0),
        "yellow": (255, 234, 0),
        "purple": (128, 0, 128),
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