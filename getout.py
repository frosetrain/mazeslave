testcases = [
    [
        [0, 4, 5, 9, 10, 11, 15],
        [0, 4, 5, 9, 10, 11, 7, 3, 2, 6],
        [2, 3, 7, 11, 15]
    ],
    [
        [0, 1, 5, 9, 10, 14, 15],
        [0, 1, 5, 9, 10, 14, 15, 11, 7, 3, 2, 6],
        [2, 3, 7, 11, 15],
    ],
    [
        [0, 4, 8, 9, 10, 14, 15],
        [0, 1, 5, 6],
        [5, 1, 0, 4, 8, 9, 10, 14, 15]
    ],
    [
        [0, 1, 2, 3, 7, 6, 5, 4, 8, 12, 13, 9, 10, 14, 15],
        [0, 1, 2, 3, 7, 6],
        [5, 4, 8, 12, 13, 9, 10, 14, 15],
    ],
]

CHEESE = 6

for e in testcases:
    exit_route = e[0]
    cheese_route = e[1]

    er = exit_route.copy()
    cr = cheese_route.copy()
    # print(er, cr)

    divergent = 0
    for a, b in zip(exit_route, cheese_route):
        # print(a, b)
        if a == b:
            er.pop(0)
            cr.pop(0)
            divergent += 1
    # print(divergent, er, cr)

    get_out = cr[::-1] + [exit_route[divergent - 1]] + er
    if get_out[0] == CHEESE:
        get_out.pop(0)

    if get_out == e[2]:
        print("AC")
    else:
        print("WA")
    print(">>>>>>>", get_out)
    print("correct", e[2])
    print()
    print()
