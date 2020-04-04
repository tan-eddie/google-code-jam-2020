def trace(matrix):
    tr = 0
    for i in range(len(matrix)):
        tr += matrix[i][i]
    return tr


def duplicate_rows(matrix):
    duplicates = 0
    for row in matrix:
        prev = set()
        for e in row:
            if e in prev:
                duplicates += 1
                break
            else:
                prev.add(e)

    return duplicates


def duplicate_cols(matrix):
    duplicates = 0
    n = len(matrix)
    for c in range(n):
        prev = set()
        for r in range(n):
            if matrix[r][c] in prev:
                duplicates += 1
                break
            else:
                prev.add(matrix[r][c])

    return duplicates


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n = int(input())
        matrix = []
        for r in range(n):
            row = [int(x) for x in input().split()]
            matrix.append(row)

        print("Case #{:d}: {:d} {:d} {:d}".format(
            i+1, trace(matrix), duplicate_rows(matrix), duplicate_cols(matrix)))


if __name__ == "__main__":
    main()
