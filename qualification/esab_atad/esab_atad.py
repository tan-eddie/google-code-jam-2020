import sys


class Batch:
    MUTATION_NONE = 0
    MUTATION_COMP = 1
    MUTATION_REV = 2
    MUTATION_REVCOMP = 3

    def __init__(self, num, length, start_offset):
        self.num = num
        self.length = length
        self.start_offset = start_offset
        self.comp = Batch.comp(num, length)
        self.rev = Batch.rev(num, length)
        self.revcomp = Batch.revcomp(num, length)

    def mutate(self, mutation):
        if mutation == Batch.MUTATION_COMP:
            self.num, self.comp = self.comp, self.num
            self.rev, self.revcomp = self.revcomp, self.rev
        elif mutation == Batch.MUTATION_REV:
            self.num, self.rev = self.rev, self.num
            self.comp, self.revcomp = self.revcomp, self.comp
        elif mutation == Batch.MUTATION_REVCOMP:
            self.num, self.revcomp = self.revcomp, self.num
            self.comp, self.rev = self.rev, self.comp

    def get_bit(self, bit):
        return (self.num >> bit) & 1

    def get_bit_string(self, end_half):
        string = ""
        offset = 0
        if end_half:
            offset = self.length // 2
        for i in range(self.length // 2):
            string += str(self.get_bit(offset + i))
        return string

    def get_mapped_bit_idx(self, bit, total_bits):
        """
        Map index of a bit in this batch to its index in the remote array.
        """
        is_start = bit < self.length // 2
        if is_start:
            return 1 + self.start_offset + bit
        else:
            return 1 + total_bits - self.start_offset - self.length + bit

    def get_rev_bit_idx(self):
        """
        Get the bit index to find mutation with ambiguity between
        num <-> rev and comp <-> revcomp
        """
        bit = 0
        mask = 1
        while (bit < self.length) and ((self.num & mask) != (self.rev & mask)):
            bit += 1
            mask <<= 1
        return bit

    def get_revcomp_bit_idx(self):
        """
        Get the bit index to find mutation with ambiguity between
        num <-> revcomp and comp <-> rev
        """
        bit = 0
        mask = 1
        while (bit < self.length) and ((self.num & mask) != (self.revcomp & mask)):
            bit += 1
            mask <<= 1
        return bit

    @staticmethod
    def comp(bits, length):
        return ~bits & ((1 << length) - 1)

    @staticmethod
    def rev(bits, length):
        before = bits
        result = 0
        for i in range(length):
            result = (result << 1) | (before & 1)
            before >>= 1
        return result

    @staticmethod
    def revcomp(bits, length):
        return Batch.rev(Batch.comp(bits, length), length)


def query(p):
    print(p)
    sys.stdout.flush()
    return int(input())


def send_answer(ans):
    print(ans)
    sys.stdout.flush()


def find_mutation(batches, total_bits):
    possible_mutations = set([Batch.MUTATION_NONE,
                              Batch.MUTATION_COMP,
                              Batch.MUTATION_REV,
                              Batch.MUTATION_REVCOMP])

    rev_queried = False
    revcomp_queried = False
    i = len(batches) - 1
    while i >= 0 and len(possible_mutations) > 1:
        batch = batches[i]
        rev_bit = batch.get_rev_bit_idx()
        revcomp_bit = batch.get_revcomp_bit_idx()

        if rev_bit < batch.length and not rev_queried:
            bit = query(batch.get_mapped_bit_idx(rev_bit, total_bits))
            rev_queried = True
            if bit == batch.get_bit(rev_bit):
                possible_mutations.discard(Batch.MUTATION_COMP)
                possible_mutations.discard(Batch.MUTATION_REVCOMP)
            else:
                possible_mutations.discard(Batch.MUTATION_NONE)
                possible_mutations.discard(Batch.MUTATION_REV)

        if revcomp_bit < batch.length and not revcomp_queried:
            bit = query(batch.get_mapped_bit_idx(revcomp_bit, total_bits))
            revcomp_queried = True
            if bit == batch.get_bit(revcomp_bit):
                possible_mutations.discard(Batch.MUTATION_COMP)
                possible_mutations.discard(Batch.MUTATION_REV)
            else:
                possible_mutations.discard(Batch.MUTATION_NONE)
                possible_mutations.discard(Batch.MUTATION_REVCOMP)

        i -= 1

    # We only made one query. So we need to do a dummy query to keep things in sync.
    if not rev_queried or not revcomp_queried:
        query(1)

    # All remaining mutations in possible_mutations are applicable
    # to all batches. So just return an arbitrary one.
    return possible_mutations.pop()


def read_batch(length, total_bits, read):
    # Note: we don't properly handle odd lengths here...
    # Odd lengths won't happen with the Code Jam test sets, but it is possible
    # to make this algorithm work for arbitrary lengths.
    num = 0
    offset = read // 2
    actual_length = min(length, total_bits - read)
    cont_length = actual_length // 2

    # Read from start (queries are 1-indexed).
    for i in range(cont_length):
        bit = query(1 + offset + i)
        num = num | (bit << i)

    # Read from end.
    for i in range(cont_length, actual_length):
        bit = query(1 + total_bits - offset - actual_length + i)
        num = num | (bit << i)

    return Batch(num, actual_length, offset)


def process_test_case(b):
    batches = []
    read = 0

    # Do two dummy queries before first batch so every batch is 8 bits.
    # Note this is unnecessary, I've only done it to simplify things.
    query(1)
    query(1)

    while read < b:
        if batches:
            # Determine new mutation using previous batches (uses two queries).
            mutation = find_mutation(batches, b)
            # Apply this mutation to the previous batches.
            for batch in batches:
                batch.mutate(mutation)

        # Read at most 8 bits (8 queries) for the next batch.
        # If less than 8 bits were read, then we have read all b bits.
        batch = read_batch(8, b, read)
        batches.append(batch)
        read += batch.length

    # Build and send answer.
    bit_strings = [""] * (len(batches) * 2)
    for i, batch in enumerate(batches):
        bit_strings[i] = batch.get_bit_string(False)
        bit_strings[len(bit_strings) - i - 1] = batch.get_bit_string(True)
    send_answer("".join([s for s in bit_strings]))


def main():
    num_cases, b = tuple(int(x) for x in input().split())
    for i in range(num_cases):
        process_test_case(b)
        result = input()
        if result == "N":
            return


if __name__ == "__main__":
    main()
