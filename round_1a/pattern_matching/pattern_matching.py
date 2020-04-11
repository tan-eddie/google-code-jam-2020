def head_match(a, b):
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] != b[j]:
            return False
        else:
            i += 1
            j += 1
    return True


def tail_match(a, b):
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 and j >= 0:
        if a[i] != b[j]:
            return False
        else:
            i -= 1
            j -= 1
    return True


def get_subpatterns(pattern):
    """
    Get subpattern such that there is always a head and tail.
    E.g. A*B*C gives ["A", "B", "C"],
    *ABC gives ["", "ABC"]
    ABC* gives ["ABC", ""]
    A*BC* gives ["A", "BC", ""] 
    """
    subpatterns = []
    curr = ""
    for c in pattern:
        if c == "*":
            subpatterns.append(curr)
            curr = ""
        else:
            curr += c
    subpatterns.append(curr)
    return subpatterns


def match_all(patterns):
    subpatterns = []
    for p in patterns:
        subpatterns.append(get_subpatterns(p))

    # Build head.
    head = subpatterns[0][0]
    for s in subpatterns:
        if len(s[0]) > len(head):
            head = s[0]
    for s in subpatterns:
        if not head_match(head, s[0]):
            return "*"

    # Build tail.
    tail = subpatterns[0][-1]
    for s in subpatterns:
        if len(s[-1]) > len(tail):
            tail = s[-1]
    for s in subpatterns:
        if not tail_match(tail, s[-1]):
            return "*"

    # Build middle (can be in any order).
    middle = []
    for s in subpatterns:
        middle.extend(s[1:-1])

    # Build the string.
    return head + "".join([x for x in middle]) + tail


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n = int(input())
        patterns = []
        for j in range(n):
            patterns.append(input())
        answer = match_all(patterns)
        print("Case #{:d}: {:s}".format(i+1, answer))


if __name__ == "__main__":
    main()
