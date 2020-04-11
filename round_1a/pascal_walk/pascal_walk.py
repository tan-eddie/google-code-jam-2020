def pascal_walk(n):
    """
    Print pascal walk of S <= 500 positions
    such that we sum to n.
    """
    # Each row of the Pascal's triangle sums to 2^r, where r >= 0 is the row.
    # To sum to 1 <= n <= 10^9, we'll need at most 29 rows since sum of all
    # these rows = 2^30 - 1 > 10^9

    # Strategy: get binary representation of n - 29, and sum rows corresponding to
    # a set bit. To 'skip' a row, just traverse down edge of 1's. Then, at the end
    # we will traverse down edge of 1's to reach n.

    # To handle cases n <= 29, we will just traverse down edge of 1's.
    if n <= 29:
        for r in range(n):
            print("{:d} {:d}".format(r+1, 1))
        return

    n_less = n - 29
    r = 1
    k = 1
    sum = 0
    while n_less > 0:
        bit = n_less & 1
        if bit == 0:
            print("{:d} {:d}".format(r, k))
            sum += 1
        else:
            forward = k == 1
            print("{:d} {:d}".format(r, k))
            for i in range(r - 1):
                if forward:
                    k += 1
                else:
                    k -= 1
                print("{:d} {:d}".format(r, k))
            sum += 1 << r - 1

        r += 1
        if k > 1:
            k += 1
        n_less >>= 1

    while sum < n:
        print("{:d} {:d}".format(r, k))
        sum += 1
        r += 1
        if k > 1:
            k += 1


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n = int(input())
        print("Case #{:d}:".format(i+1))
        pascal_walk(n)


if __name__ == "__main__":
    main()
