def expogo(x, y):
    # Work with positive x and y, and use symmetry property to deal
    # with other quadrants.
    flip_x = x < 0
    flip_y = y < 0
    x = abs(x)
    y = abs(y)

    moves = []

    if (x + y) % 2 == 0:
        # Exactly one of the target coordinates must be odd.
        return "IMPOSSIBLE"

    while x != 0 or y != 0:
        # Move in the current 'odd' direction.
        next_x = (x >> 1) & 1
        next_y = (y >> 1) & 1

        if x >> 1 or y >> 1:
            if x & 1:
                if next_x == next_y:
                    moves.append("E" if flip_x else "W")
                    x += 1
                else:
                    moves.append("W" if flip_x else "E")
            elif y & 1:
                if next_x == next_y:
                    moves.append("N" if flip_y else "S")
                    y += 1
                else:
                    moves.append("S" if flip_y else "N")
        else:
            # Last move. Finish now for the shortest path.
            if x & 1:
                moves.append("W" if flip_x else "E")
            else:
                moves.append("S" if flip_y else "N")

        x >>= 1
        y >>= 1

    return "".join([x for x in moves])


def main():
    num_cases = int(input())
    for i in range(num_cases):
        x, y = tuple(int(x) for x in input().split())
        print("Case #{:d}: {:s}".format(i+1, expogo(x, y)))


if __name__ == "__main__":
    main()
