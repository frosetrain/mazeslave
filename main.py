wall_horizontal = "─"
wall_vertial = "│"
wall_topleft = "┌"
wall_topright = "┐"
wall_bottomleft = "└"
wall_bottomright = "┘"


def cardinal_order(directions):
    d = ""
    if "n" in directions:
        d += "n"
    if "e" in directions:
        d += "e"
    if "s" in directions:
        d += "s"
    if "w" in directions:
        d += "w"
    return d


def get_box_char(directions):
    cardinals = cardinal_order(directions)
    if cardinals == "n":
        return "╵"
    elif cardinals == "e":
        return "╶"
    elif cardinals == "s":
        return "╷"
    elif cardinals == "w":
        return "╴"
    elif cardinals == "ne":
        return "└"
    elif cardinals == "ns":
        return "│"
    elif cardinals == "nw":
        return "┘"
    elif cardinals == "es":
        return "┌"
    elif cardinals == "ew":
        return "─"
    elif cardinals == "sw":
        return "┐"
    elif cardinals == "nes":
        return "├"
    elif cardinals == "new":
        return "┴"
    elif cardinals == "nsw":
        return "┤"
    elif cardinals == "esw":
        return "┬"
    elif cardinals == "nesw":
        return "┼"
    else:
        raise KeyError


walls = [
    ["es", "ew", "ew", "sw", "s"],
    ["ns", "es", "w", "n", "ns"],
    ["nes", "nw", "es", "sw", "ns"],
    ["ns", "e", "nsw", "n", "ns"],
    ["n", "e", "new", "ew", "nw"],
]
for row in walls:
    for x in row:
        print(get_box_char(x), end="")
    print()
