def transform(color):
    """ Transform color name to RGB value""" 
    if color == "red":
        return (233, 0, 45)
    elif color == "green":
        return (0, 255, 0)
    elif color == "blue":
        return (0, 0, 255)
    elif color == "orange":
        return (254, 130, 0)
    elif color == "yellow":
        return (255, 234, 0)
    elif color == "purple":
        return (128, 0, 128)
    elif color == "pink":
        return (255, 192, 203)
    elif color == "brown":
        return (165, 42, 42)
    elif color == "gray":
        return (128, 128, 128)
    elif color == "cyan":
        return (0, 255, 255)
    elif color == "magenta":
        return (255, 0, 255)
    elif color == "white":
        return (255, 255, 255)
    elif color == "light blue":
        return (0, 120, 203)
    elif color == "dark purple":
        return (63, 0, 151)
    elif color == "light green":
        return (58, 172, 0)
    elif color == "black":
        return (0, 0, 0)
    else:
        return (0, 0, 0)