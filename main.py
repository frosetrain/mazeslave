from math import floor
from time import sleep

import event
import mbot2
from cyberpi import console, quad_rgb_sensor, stop_all, ultrasonic2

adjlist = [[] for i in range(16)]
heading = 0
current_tile = 0
stack = []
exit_route = []
cheese_route = []
cheese_x = None
cheese_y = None
end_x = None
end_y = None
cheese = None
end = None
end_opening = None

dfs_done = False

CARDINALS = {
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3,
}

# n, e, s, w for each cell
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


def linetrack_forward(stop_at_junction=True):
    quad_rgb_sensor.set_led(color="white")
    while True:
        r1 = (100 - quad_rgb_sensor.get_light(1)) / 100
        r2 = (100 - quad_rgb_sensor.get_light(2)) / 100
        r3 = (100 - quad_rgb_sensor.get_light(3)) / 100
        r4 = (100 - quad_rgb_sensor.get_light(4)) / 100
        oof = (r1 * -2.5 + r2 * -1 + r3 * 1 + r4 * 2.5) / 4
        # if quad_rgb_sensor.get_line_sta() == 0:
        blacks = 0
        for val in (r1, r2, r3, r4):
            if val > 0.4:
                blacks += 1
        if blacks >= 3:
            if stop_at_junction:
                mbot2.EM_stop()
                # log("JUNCTION")
                mbot2.straight(8)
                mbot2.EM_stop()
            else:
                mbot2.straight(5)
            return
        mbot2.drive_speed(oof * -15 + 50, oof * -15 - 50)


def log(thing):
    console.println(thing)


def turn_heading(target_heading):
    global adjlist
    global heading
    global current_tile
    global stack
    global exit_route
    global cheese_route
    global walls
    # log("turning " + str(target_heading) + " from " + str(heading))
    real_heading = target_heading
    if real_heading - heading >= 3:
        real_heading -= 4
    if heading - real_heading >= 3:
        real_heading += 4
    if real_heading - heading > 0:
        for _ in range(real_heading - heading):
            mbot2.turn(90)
    else:
        for _ in range(heading - real_heading):
            mbot2.turn(-90)
    heading = target_heading


def follow_path(path):
    global adjlist
    global heading
    global current_tile
    global stack
    global exit_route
    global cheese_route
    global walls

    log("following" + str(path))
    # log(current_tile)
    for step in path:
        new_heading = None
        if step - current_tile == 4:  # Go north
            # log("go north")
            new_heading = 0
        elif step - current_tile == -4:  # Go south
            # log("go south")
            new_heading = 2
        elif step - current_tile == 1:  # Go east
            # log("go east")
            new_heading = 1
        elif step - current_tile == -1:  # Go west !!!
            # log("go west")
            new_heading = 3
        else:
            current_tile = step
            continue
        if heading != new_heading:
            turn_heading(new_heading)
            heading = new_heading
            linetrack_forward()
        else:
            linetrack_forward(False)
        current_tile = step


def fake_dfs(c):
    log("asddsjfdsklsdjlfdjfklasjfd")
    global cheese_route
    global exit_route
    global dfs_done
    cheese_route = [1, 2, 3]
    exit_route = [4, 5, 6, 7, 11, 15]
    dfs_done = True


def dfs(c):
    global adjlist
    global heading
    global current_tile
    global stack
    global exit_route
    global cheese_route
    global walls
    global cheese
    global end
    global end_opening
    global end_x
    global end_y
    global dfs_done
    stack.append(c)
    if c == end:
        possible_ends = {"s": False, "n": False, "w": False, "e": False}
        if end_y == 0:
            cell["s"] = True
        elif end_y == 3:
            cell["n"] = True
        if end_x == 0:
            cell["w"] = True
        elif end_x == 3:
            cell["e"] = True
        for direction, possible in possible_ends.items():
            if possible:
                target_heading = CARDINALS[direction]
                turn_heading(target_heading)
                mbot2.straight(-2)
                wall = ultrasonic2.get() < 10
                if not wall:
                    end_opening = direction
                    log("opening at " + end_opening)
                mbot2.straight(2)

        walls.append(cell)

        for o in stack:
            exit_route.append(o)
        # log(f"exit {exit_route}")
        if exit_route and cheese_route:  # Go back to the start immediately
            current_tile = c
            dfs_done = True
            log("dfs done")
            # follow_path(exit_route[-2::-1])
            return 69  # An exit code the exits the entire recursive dfs stack
    if c == cheese:
        for o in stack:
            current_tile = c
            cheese_route.append(o)
        # log(f"cheese route {cheese_route}")
        if exit_route and cheese_route:  # Go back to the start immediately
            follow_path(cheese_route[-2::-1])
            return 69  # An exit code the exits the entire recursive dfs stack
    x = c - floor(c / 4) * 4
    y = floor(c / 4)
    # log(f"c {c}, x {x}, y {y}")

    # Scan each wall to get the adjacent nodes
    # log(f"cell {walls[y * 4 + x]}")
    unknown_walls = [k for k, v in walls[y * 4 + x].items() if v is None]
    # log(f"unknown {unknown_walls}")
    for w in unknown_walls:
        target_heading = CARDINALS[w]
        # log(f"idk about {w}, but imma turn to {target_heading}")
        turn_heading(target_heading)
        mbot2.straight(-2)
        wall = ultrasonic2.get() < 10
        walls[c][w] = wall
        if w == "n":
            walls[c + 4]["s"] = wall
        elif w == "s":
            walls[c - 4]["n"] = wall
        elif w == "e":
            walls[c + 1]["w"] = wall
        elif w == "w":
            walls[c - 1]["e"] = wall
        if not wall:
            if w == "n":
                adjlist[c].append(c + 4)
            elif w == "e":
                adjlist[c].append(c + 1)
            elif w == "s":
                adjlist[c].append(c - 4)
            elif w == "w":
                adjlist[c].append(c - 1)
        mbot2.straight(2)

    wallcount = 0
    for w in walls[y * 4 + x].values():
        if w is True:
            wallcount += 1
    if wallcount == 3 and c != 0:
        # log("We have reached a ded end!! Yay")
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
        linetrack_forward()
        rc = dfs(adj)
        if rc == 69:
            return 69

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
        linetrack_forward()
        stack.pop()


def real_run():
    global adjlist
    global heading
    global current_tile
    global stack
    global exit_route
    global cheese_route
    global walls
    global end_opening
    current_tile = 0
    heading = 0

    log("final er" + str(exit_route))
    log("final cr" + str(cheese_route))
    # Drive from root to cheese
    follow_path(cheese_route[1:])

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
    if get_out[0] == cheese:
        get_out.pop(0)
    log("GET out: " + str(get_out))
    follow_path(get_out)
    log(end_opening)
    turn_heading(CARDINALS[end_opening])
    mbot2.straight(50)


def enter_value(val):
    global cheese_x
    global cheese_y
    global cheese
    global end_x
    global end_y
    global end
    log(str(val))
    if cheese is None:
        if cheese_x is None:
            cheese_x = val
        elif cheese_y is None:
            cheese_y = val
            cheese = cheese_y * 4 + cheese_x
            log("cheese " + str(cheese))
    elif end is None:
        if end_x is None:
            end_x = val
        elif end_y is None:
            end_y = val
            end = end_y * 4 + end_x
            log("end " + str(end))


@event.is_press("up")
def on_press_up():
    enter_value(0)


@event.is_press("right")
def on_press_up():
    enter_value(1)


@event.is_press("down")
def on_press_up():
    enter_value(2)


@event.is_press("left")
def on_press_up():
    enter_value(3)


@event.is_press("a")
def main():
    global dfs_done
    global cheese_route
    global exit_route
    global end_opening
    # end_opening = "n"
    quad_rgb_sensor.set_led(color="white")
    if cheese is None or end is None:
        log("SPECIFY CHEESE AND/OR END!!! you idiot")
    # cheese_route = [0, 1]
    # exit_route = [0, 1, 5, 4, 8, 12]
    # real_run()
    if not dfs_done:
        dfs(0)
        turn_heading(0)
    else:
        real_run()


@event.is_press("b")
def on_press_b():
    global dfs_done
    mbot2.EM_stop()
    stop_all()
