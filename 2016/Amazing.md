#Amazing

> An important step towards the strong AI is the ability of an
> artificial agent to solve a well-defined problem. A project by the
> name 'amazing' was one of such test problems. It's still up...
> 
> **nc amazing.2016.volgactf.ru 45678**

***Scouting phase***

Use BFS to find all hidden cells reachable from current position. Add them to the stack. Repeat until stack is not empty or until there are no hidden cells on the map.

***Solving phase***

When we scouted all maze, use BFS to find the path to the very right/bottom cell.
Go there and make move to the right.

***Repeat until you get flag***


```
from pprint import pprint
import re
from pwn import *
from time import sleep

MOVES = {
    (-2, 0): "u",
    (2, 0): "d",
    (0, -4): "l",
    (0, 4): "r",
}

MOVES_INV = {v: k for k, v in MOVES.items()}

PLAYER = "*"
EMPTY = " "
WALLS = ["|", "+", "-"]
HIDDEN = "#"
ERROR = "?"
ROUND = 100
SYMBOLS = [PLAYER, EMPTY, HIDDEN] + WALLS


# returns tuple -- position of the first occurrence of 'item' element on the map
def position_of(M, item):
    for i, row in enumerate(M):
        for j, col in enumerate(row):
            if col == item:
                return i, j


# Make one step in one of 4 directions. s - delta from current position pos
def delta(pos, s):
    a, b = pos
    c, d = s
    return a + c, b + d


# Returns list of reachable neighbour positions
def reachable(M, p):
    assert len(p) == 2
    r = set()
    for k in MOVES:
        a, b = delta(p, k)
        c, d = p
        r.add((a, b))
        # check intersections with walls
        if {x[d] for x in M[a:c]}.intersection(WALLS) \
                or {x[d] for x in M[c:a]}.intersection(WALLS) \
                or set(M[c][b:d]).intersection(WALLS) \
                or set(M[c][d:b]).intersection(WALLS):
            r.remove((a, b))

    return r


# map M value in position pos
def map_at_pos(M, pos):
    assert len(pos) == 2, "len != 2"

    if pos[0] < 0 or pos[0] > len(M):
        return None
    if pos[1] < 0 or pos[1] > len(M[0]):
        return None

    return M[pos[0]][pos[1]]


# Returns path (moves) to reach 'to' cell
def get_path(M, to):
    visited = set()
    to = tuple(to)
    player = position_of(M, PLAYER)
    queue = [player]
    path = {}
    while queue:
        p = queue.pop(0)

        # reached final position
        if p == to:
            break

        if p in visited:
            continue

        visited.add(p)

        # find reachable neighbours (empty cells)
        for s in reachable(M, p):
            if map_at_pos(M, s) == EMPTY or s == to:
                if s in visited:
                    continue
                path[s] = p
                queue.append(s)

    P = ""
    pos = to
    while True:
        d = diff(path[pos], pos)
        P = MOVES[d] + P
        pos = path[pos]
        if pos == player:
            return P


# returns difference between 2 positions
def diff(p, s):
    a, b = p
    c, d = s
    return c-a, d-b


# Find all occurrences of 'target' in the map
def bfs_search(M, target):
    targets = set()
    visited = set()
    queue = [position_of(M, PLAYER)]
    while queue:
        p = queue.pop(0)

        if p in visited:
            continue

        visited.add(p)

        # find reachable neighbours (empty cells)
        for s in reachable(M, p):
            if map_at_pos(M, s) == EMPTY:
                queue.append(s)
            elif map_at_pos(M, s) == target:
                targets.add(s)

    return list(targets)

def recv_field(r):
    data = {
        'map':[],
        'other':[]
    }

    while True:
        line = r.recvline().split("\n")
        line = [x for x in line if len(x) > 0]
        if len(line) == 0:
            continue

        line = "".join(line)
        print line

        if re.match("Round number (\d+)", line):
            data['round'] = int(re.match("Round number (\d+)", line).groups()[0])
        elif len(line) >= 120:
            data['map'].append(line)
        else:
            data['other'].append(line)

        if len(data['map']) == 41:
            return data

# MAIN
r = remote("amazing.2016.volgactf.ru", 45678)
r.recvuntil("Good luck!")

while True:
    data = recv_field(r)
    MAP = data['map']

    # SCOUTING
    stack = [] + bfs_search(MAP, HIDDEN)
    while stack:
        h = stack.pop(0)
        P = get_path(MAP, h)


        if all([HIDDEN not in x for x in MAP]):
            break
        
        print P

        r.send(P[:-1] + "\n")
        
        data = recv_field(r)
        MAP = data['map']

        stack = bfs_search(MAP, HIDDEN) + stack


    # REACH FINISH
    a, b = len(MAP)-2, len(MAP[0])-3
    P = get_path(MAP, (a, b))
    r.send(P + "r" + "\n") # Make final move ('r')
```



[First round in bot's eyes](http://pastebin.com/RQmP1EDr)

After 30 rounds I got the flag: 

> VolgaCTF{eurisco!}
