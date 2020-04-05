"""
NOTE: THIS IS WIP, UNTESTED AND PROBABLY DOESN'T WORK.
"""

def trace(sq):
    tr = 0
    for i in range(len(sq)):
        tr += sq[i][i]
    return tr


def diag_counts(sq):
    """
    Return counts of diagonal elements.
    """
    n = len(sq)
    counts = [0] * n
    for i in range(n):
        counts[sq[i][i] - 1] += 1
    return counts


def diag_counts_trace(diag_counts, mapping):
    tr = 0
    for i, count in enumerate(diag_counts):
        tr += mapping[i] * count
    return tr


def mapping_for_trace(diag_counts, trace, elements):
    """
    Return a mapping for getting trace from diag_counts.
    Returns None if no mapping found.
    """
    n = len(diag_counts)
    nonzero_counts = [count for count in diag_counts if count > 0]
    tr = diag_counts_trace(diag_counts, mapping)

    return None


def swap_rows(sq, r1, r2):
    sq[r1], sq[r2] = sq[r2], sq[r1]


def basic_latin_square(n):
    """
    Generate the basic natural latin square by shifting the elements
    at each row.
    """
    sq = []
    for r in range(n):
        col = []
        for c in range(n):
            col.append((r + c) % n + 1)
        sq.append(col)
    return sq


def substitute(sq, mapping):
    """
    Map [1, 2, 3, 4, ...] in sq to mapping.
    """
    n = len(sq)
    for r in n:
        for c in n:
            sq[r][c] = mapping[sq[r][c] - 1]


def latin_square(n, k):
    """
    Attempt to generate a nxn natural latin square with trace k.
    """
    sq = basic_latin_square(n)
    diag = diag_counts(sq)
    mapping = mapping_for_trace(diag, k, list(range(1, n+1)))

    if mapping is None:
        for r1 in range(n):
            for r2 in range(r1+1, n):
                swap_rows(sq, r1, r2)
                diag = diag_counts(sq)
                mapping = mapping_for_trace(diag, k, list(range(1, n+1)))
                if mapping is not None:
                    break

    if mapping is not None:
        substitute(sq, mapping)
        return matrix_to_str(sq)
    else:
        return "IMPOSSIBLE"


def matrix_to_str(m):
    return "\n".join([" ".join([str(x) for x in row]) for row in m])


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n, k = tuple([int(x) for x in input().split()])
        print("Case #{:d}: {:s}".format(i+1, latin_square(n, k)))


if __name__ == "__main__":
    main()
