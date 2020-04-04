def nesting_depth(s):
    depth = 0
    ans_elements = []
    for c in s:
        target = int(c)
        diff = target - depth
        if diff > 0:
            ans_elements.append("(" * diff)
        elif diff < 0:
            ans_elements.append(")" * -diff)
        ans_elements.append(c)
        depth = target

    if depth > 0:
        ans_elements.append(")" * depth)

    return "".join([e for e in ans_elements])


def main():
    num_cases = int(input())
    for i in range(num_cases):
        s = input()
        print("Case #{:d}: {:s}".format(i+1, nesting_depth(s)))


if __name__ == "__main__":
    main()
