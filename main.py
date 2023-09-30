import sys
from math import floor
from time import sleep
from random import randint

import mmapi

adjlist = [[] for i in range(16)]
heading = 0
# brain = []
stack = []
exit_route = []
cheese_route = []

CARDINALS = {
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3,
}
# CHEESE = randint(1, 16)
CHEESE = 6

mmapi.setColor(CHEESE - floor(CHEESE / 4) * 4, floor(CHEESE / 4), "Y")
mmapi.setText(CHEESE - floor(CHEESE / 4) * 4, floor(CHEESE / 4), "chees")

# I am going with n, e, s, w for each cell
walls = []
for y in range(4):
    for x in range(4):
        cell = {"n": None, "e": None, "s": None, "w": None}
        if y == 0:
            cell["s"] = True
        elif y == 3:
            cell["n"] = True
        if x == 0:
            cell["w"] = True
        elif x == 3:
            cell["e"] = True
        walls.append(cell)
        for k, v in cell.items():
            if v is True:
                mmapi.setWall(x, y, k)


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


# void dfs(int x) {
#     if (visited[x]) return;
#     visited[x] = true;
#     for (auto i: adjlist[x]) {
#         dfs(i);
#     }
# }


def turn_heading(target_heading):
    global heading
    # log(f"turning {target_heading} from {heading}")
    if target_heading - heading > 0:
        for _ in range(target_heading - heading):
            mmapi.turnRight()
    else:
        for _ in range(heading - target_heading):
            mmapi.turnLeft()
    heading = target_heading


def dfs(c):
    stack.append(c)
    if c == 15:
        for o in stack:
            exit_route.append(o)
        log(f"exit {exit_route}")
    if c == CHEESE:
        for o in stack:
            cheese_route.append(o)
        log(f"cheese route {cheese_route}")
    x = c - floor(c / 4) * 4
    y = floor(c / 4)
    log(f"c {c}, x {x}, y {y}")

    # Scan each wall to get the adjacent nodes
    log(f"cell {walls[y * 4 + x]}")
    unknown_walls = [k for k, v in walls[y * 4 + x].items() if v is None]
    log(f"unknown {unknown_walls}")
    for w in unknown_walls:
        target_heading = CARDINALS[w]
        log(f"idk about {w}, but imma turn to {target_heading}")
        turn_heading(target_heading)
        wall = mmapi.wallFront()
        walls[c][w] = wall
        if w == "n":
            walls[c + 4]["s"] = wall
        elif w == "s":
            walls[c - 4]["n"] = wall
        elif w == "e":
            walls[c + 1]["w"] = wall
        elif w == "w":
            walls[c - 1]["e"] = wall
        if wall:
            mmapi.setWall(x, y, w)
            log(f"now i know there is a wall at {x} {y} {w}")
        else:
            if w == "n":
                adjlist[c].append(c + 4)
            elif w == "e":
                adjlist[c].append(c + 1)
            elif w == "s":
                adjlist[c].append(c - 4)
            elif w == "w":
                adjlist[c].append(c - 1)

    wallcount = 0
    for w in walls[y * 4 + x].values():
        if w is True:
            wallcount += 1
    if wallcount == 3 and c != 0:
        log("We have reached a ded end!! Yay")
        return

    log(adjlist[c])
    for adj in adjlist[c]:
        # Go to the adjacent node
        if adj - c == 1:  # east
            target_heading = 1
        elif adj - c == -1:  # west
            target_heading = 3
        elif adj - c == 4:  # north
            target_heading = 0
        elif adj - c == -4:  # south
            target_heading = 2
        # log(f"lets go {target_heading}")
        turn_heading(target_heading)
        mmapi.moveForward()
        dfs(adj)

        # Go back to c
        if adj - c == 1:  # east
            target_heading = 3
        elif adj - c == -1:  # west
            target_heading = 1
        elif adj - c == 4:  # north
            target_heading = 2
        elif adj - c == -4:  # south
            target_heading = 0
        # log(f"lets go {target_heading}")
        turn_heading(target_heading)
        mmapi.moveForward()
        stack.pop()


# def brain_dfs(c):
#     brain.append(c)
#     for thing in adjlist[c]:
#         brain_dfs(thing)


def real_run():
    current_tile = 0
    log(exit_route)
    log(cheese_route)
    # Drive from root to cheese
    for step in cheese_route[1:]:
        if step - current_tile == 4:  # Go north
            turn_heading(0)
        elif step - current_tile == -4:  # Go south
            turn_heading(2)
        elif step - current_tile == 1:  # Go east
            turn_heading(1)
        elif step - current_tile == -1:  # Go west !!!
            turn_heading(3)
        mmapi.moveForward()
        current_tile = step

    # Do the thing with exit_route and cheese_route
    er = exit_route.copy()
    cr = cheese_route.copy()
    divergent = 0
    for a, b in zip(exit_route, cheese_route):
        # print(a, b)
        if a == b:
            er.pop(0)
            cr.pop(0)
            divergent += 1
    get_out = cr[::-1] + [exit_route[divergent - 1]] + er
    if get_out[0] == CHEESE:
        get_out.pop(0)
    log(get_out)

    for step in get_out:
        if step - current_tile == 4:  # Go north
            turn_heading(0)
        elif step - current_tile == -4:  # Go south
            turn_heading(2)
        elif step - current_tile == 1:  # Go east
            turn_heading(1)
        elif step - current_tile == -1:  # Go west !!!
            turn_heading(3)
        mmapi.moveForward()
        current_tile = step


def main():
    dfs(0)
    log("DFS done")
    turn_heading(0)
    sleep(1)
    real_run()


if __name__ == "__main__":
    main()
