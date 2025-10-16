R, C = map(int, input().split())
grid = [input().strip() for _ in range(R)]
seq = input().strip()

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

end_coords = set()
# print(R, C)
# print(grid)
# print(seq)

# up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def simple_move(r, c, dir):
    for move in seq:
        if move == "L":
            dir = (dir - 1) % 4
        elif move == "R":
            dir = (dir + 1) % 4
        else:  # 'S'
            r += dr[dir]
            c += dc[dir]
            # Edge check: r and c should be in range
            if not (0 <= r < R and 0 <= c < C):
                return None
            # Check if the cell is open
            if grid[r][c] == "#":
                return None
    return (r, c)


if __name__ == "__main__":
    # actual code
    for r in range(R):
        for c in range(C):
            if grid[r][c] == ".":
                for d in range(4):
                    result = simple_move(r, c, d)
                    if result:
                        end_coords.add(result)
    if end_coords:
        print(len(end_coords))
    else:
        print("Impossible")
