import operator


class Task:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.assignee = None


def schedule(tasks):
    tasks_by_start = sorted(tasks, key=operator.attrgetter('start'))
    tasks_by_end = sorted(tasks, key=operator.attrgetter('end'))
    c_busy = False
    j_busy = False
    s = 0
    e = 0
    while s < len(tasks_by_start):
        if tasks_by_start[s].start < tasks_by_end[e].end:
            # Start a new task.
            if c_busy and j_busy:
                return "IMPOSSIBLE"
            elif not c_busy:
                tasks_by_start[s].assignee = "C"
                c_busy = True
            else:
                tasks_by_start[s].assignee = "J"
                j_busy = True
            s += 1
        else:
            # End a task and free up a resource.
            if tasks_by_end[e].assignee == "C":
                c_busy = False
            else:
                j_busy = False
            e += 1

    return "".join(task.assignee for task in tasks)


def main():
    num_cases = int(input())
    for i in range(num_cases):
        n = int(input())
        tasks = []
        for j in range(n):
            times = tuple(int(x) for x in input().split())
            tasks.append(Task(times[0], times[1]))

        print("Case #{:d}: {:s}".format(i+1, schedule(tasks)))


if __name__ == "__main__":
    main()
