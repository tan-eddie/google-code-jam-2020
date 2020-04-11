class Node:
    def __init__(self, skill):
        self.skill = skill
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.deleted = False

    def neighbours(self):
        return [n for n in [self.north, self.east, self.south, self.west] if n is not None]

    def neighbour_avg(self):
        sum = 0
        neighbours = self.neighbours()
        for n in neighbours:
            sum += n.skill
        avg = 0
        if len(neighbours) > 0:
            avg = sum / len(neighbours)
        return avg

    def delete(self):
        if self.north is not None:
            self.north.south = self.south
        if self.east is not None:
            self.east.west = self.west
        if self.south is not None:
            self.south.north = self.north
        if self.west is not None:
            self.west.east = self.east


def init_graph(mat, r, c):
    nodes = []
    total_skill = 0
    for i in range(r):
        row = []
        for j in range(c):
            node = Node(mat[i][j])
            total_skill += mat[i][j]
            row.append(node)
            if i > 0:
                node.north = nodes[i-1][j]
                nodes[i-1][j].south = node
            if j > 0:
                node.west = row[j-1]
                row[j-1].east = node
        nodes.append(row)
    return nodes, total_skill


def interest_level(mat, r, c):
    nodes, round_interest = init_graph(mat, r, c)
    nodes_to_check = set([node for row in nodes for node in row])
    total_interest = round_interest
    while nodes_to_check:
        nodes_to_delete = []
        for node in nodes_to_check:
            avg = node.neighbour_avg()
            if node.skill < avg:
                nodes_to_delete.append(node)
                node.deleted = True

        nodes_to_check.clear()
        for node in nodes_to_delete:
            node.delete()
            for n in node.neighbours():
                if not n.deleted:
                    nodes_to_check.add(n)
            round_interest -= node.skill

        if nodes_to_delete:
            total_interest += round_interest

    return total_interest


def main():
    num_cases = int(input())
    for i in range(num_cases):
        r, c = tuple(int(x) for x in input().split())
        mat = []
        for j in range(r):
            row = [int(x) for x in input().split()]
            mat.append(row)
        print("Case #{:d}: {:d}".format(i+1, interest_level(mat, r, c)))


if __name__ == "__main__":
    main()
