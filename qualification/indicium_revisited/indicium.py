"""
Solved this after reading analyses after the round was over. Based on Errichto's analysis.
https://youtu.be/VayKvCg4vvQ
"""


def find_triplet(n, k):
    for a in range(1, n+1):
        for b in range(1, n+1):
            for c in range(1, n+1):
                if ((n-2)*a + b + c == k and
                    ((a == b and a == c) or
                     (n == 3 and a != b and a != c and b != c) or
                     (n > 3 and a != b and a != c))):
                    return (a, b, c)
    return (0, 0, 0)


def fill_matrix(mat, a, b, c, n):
    # Fill the diagonal.
    for i in range(n-2):
        mat[i][i] = a
    mat[-2][-2] = b
    mat[-1][-1] = c

    # Fill remaining a's, b's and c's using a defined strategy.
    if not (a == b and a == c):
        mat[-2][-1] = a
        mat[-1][-2] = a
        if b == c:
            # 2 distinct numbers.
            for i in range(n-3):
                mat[i][i+1] = b
            mat[-3][0] = b
        else:
            # 3 distnct numbers.
            if n == 3:
                mat[0][1] = c
                mat[1][0] = c
                mat[0][2] = b
                mat[2][0] = b
            elif n == 4:
                mat[0][1] = c
                mat[1][2] = c
                mat[2][0] = c
                mat[0][3] = b
                mat[1][0] = b
                mat[3][1] = b
            else:
                for i in range(n-2):
                    mat[i][i+1] = c
                mat[-2][0] = c
                mat[0][-1] = b
                for i in range(1, n-2):
                    mat[i][i-1] = b
                mat[-1][-3] = b


def find_match(graph, row, matching, seen):
    for col in range(len(matching)):
        if graph[row][col] and not seen[col]:
            seen[col] = True
            if matching[col] == -1 or find_match(graph, matching[col], matching, seen):
                matching[col] = row
                return True
    return False


def bipartite_match(graph):
    """
    Find maximum bipartite match using same concept as Ford-Fulkerson algorithm.
    """
    # Value of matching[i] is the row index in graph that is matched with column i.
    matching = [-1] * len(graph)
    for i in range(len(graph)):
        seen = [False] * len(graph)
        find_match(graph, i, matching, seen)
    return matching


def latin_square(n, k):
    impossible = (False, [])

    # Impossible cases, because the only way to form these traces is with
    # 2 distinct numbers on the diagonal, a and b; (n-1) of a and 1 of b.
    # We cannot form a latin square with this diagonal.
    if k == n+1 or k == n*n-1:
        return impossible

    # Special case n == 2.
    if n == 2:
        if k == 2:
            return (True, [[1, 2], [2, 1]])
        elif k == 4:
            return (True, [[2, 1], [1, 2]])
        else:
            return impossible

    # If we have 3 numbers on the diagonal, a, b and c, where we have
    # (n-2) a, 1 b and 1 c, and a != b and a != c, then we can always form a
    # latin square. This can be proven using bipartite matching + Hall's
    # marriage theorem. Note we need to be careful about n == 3.
    # So work out what a, b, c we need to get k. It can be proven that there
    # exists an a, b and c for all n <= k <= n*n, except for k == n + 1 and
    # k == n*n - 1.
    a, b, c = find_triplet(n, k)
    if a == 0:
        return impossible

    mat = [[0] * n for i in range(n)]
    fill_matrix(mat, a, b, c, n)

    # Fill remaining numbers by finding maximum bipartite matching,
    # where left set is rows, right set is columns, and edges represent
    # valid cells where we can put the current number.
    for num in range(1, n+1):
        if num != a and num != b and num != c:
            bipartite_graph = [[1 if x == 0 else 0 for x in row]
                               for row in mat]
            matching = bipartite_match(bipartite_graph)
            for col, row in enumerate(matching):
                mat[row][col] = num

    return (True, mat)


def matrix_to_str(m):
    return "\n".join([" ".join([str(x) for x in row]) for row in m])


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n, k = tuple([int(x) for x in input().split()])
        possible, mat = latin_square(n, k)
        print("Case #{:d}: {:s}".format(
            i+1, "POSSIBLE" if possible else "IMPOSSIBLE"))
        print(matrix_to_str(mat))


if __name__ == "__main__":
    main()
