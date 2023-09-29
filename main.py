import sys
from math import floor

import mmapi

adjlist = [[] for i in range(16)]
heading = 0

cardinals = {
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3,
}

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


def dfs(c):
    x = c - floor(c / 4) * 4
    y = floor(c / 4)
    log(f"c {c}, x {x}, y {y}")
    global heading
    log(f"h {heading}")

    # Scan each wall to get the adjacent nodes
    log(f"cell {walls[y * 4 + x]}")

    for k, v in walls[y * 4 + x].items():
        if v is None:
            target_heading = cardinals[k]
            log(f"idk about {k}, but imma turn to {target_heading}")
            if target_heading - heading > 0:
                for i in range(target_heading - heading):
                    mmapi.turnRight()
            else:
                for i in range(heading - target_heading):
                    mmapi.turnLeft()
            wall = mmapi.wallFront()
            walls[c][k] = wall
            if k == "n":
                walls[c + 4]["s"] = wall
            elif k == "s":
                walls[c - 4]["n"] = wall
            elif k == "e":
                walls[c + 1]["w"] = wall
            elif k == "w":
                walls[c - 1]["e"] = wall

            if wall:
                mmapi.setWall(x, y, k)
                log(f"now i know there is a wall at {x} {y} {k}")
            else:
                if k == "n":
                    adjlist[c].append(c + 4)
                elif k == "e":
                    adjlist[c].append(c + 1)
                elif k == "s":
                    adjlist[c].append(c - 4)
                elif k == "w":
                    adjlist[c].append(c - 1)

            heading = target_heading

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
        if target_heading - heading > 0:
            for i in range(target_heading - heading):
                mmapi.turnRight()
        else:
            for i in range(heading - target_heading):
                mmapi.turnLeft()
        heading = target_heading
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
        if target_heading - heading > 0:
            for i in range(target_heading - heading):
                mmapi.turnRight()
        else:
            for i in range(heading - target_heading):
                mmapi.turnLeft()
        heading = target_heading
        mmapi.moveForward()


def main():
    dfs(0)
    log("LET'S GOOOOO")
    log(adjlist)


if __name__ == "__main__":
    main()
