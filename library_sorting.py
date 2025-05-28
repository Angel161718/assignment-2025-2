import sys
import json

class SparseTable:
    def __init__(self, nn, mm, k, x):
        self.nn = nn
        self.mm = mm
        self.k = k
        self.n = 1
        self.m = int(self.nn[k - 1] * self.mm[k])
        self.table = [x] * self.m
        self.auth_keys = [x]
        self.head = 0

    def print_table(self):
        result = []
        for i in range(self.m):
            idx = (self.head + i) % self.m
            val = self.table[idx]
            if i == 0:
                result.append(f">{val}<")
            else:
                result.append(str(val))
        print(f"[{', '.join(result)}]")

    def binary_search_insert_position(self, key):
        low = 0
        high = self.n
        while low < high:
            mid = (low + high) // 2
            mid_idx = (self.head + mid) % self.m
            if self.table[mid_idx] < key:
                low = mid + 1
            else:
                high = mid
        return low

    def insert(self, key):
        if key in self.auth_keys:
            self.print_table()
            return

        pos = self.binary_search_insert_position(key)
        idx = (self.head + pos) % self.m

        if self.table[idx] == self.table[(idx - 1) % self.m]:
            self.table[idx] = key
        else:
            i = (self.head + self.m - 1) % self.m
            while i != idx:
                self.table[(i + 1) % self.m] = self.table[i]
                i = (i - 1 + self.m) % self.m
            self.table[idx] = key
            self.head = (self.head - 1 + self.m) % self.m

        self.auth_keys.append(key)
        self.auth_keys.sort()
        self.n += 1
        self.print_table()

    def lookup(self, key):
        pos = self.binary_search_insert_position(key)
        idx = (self.head + pos) % self.m

        if idx < self.m and self.table[idx] == key:
            print(f"Key {key} found at position {pos}.")
        else:
            print(f"Key {key} not found. It should be at position {pos}.")

        self.print_table()

def main():
    if len(sys.argv) != 2:
        print("Usage: python library_sorting.py <input_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"File '{input_file}' is not valid JSON.")
        sys.exit(1)

    nn = data["nn"]
    mm = data["mm"]
    k = data["k"]
    x = data["x"]
    actions = data["actions"]

    print(f"CREATE with k={k}, n_k={nn}, m_k={mm}, key={x}")
    table = SparseTable(nn, mm, k, x)
    table.print_table()

    for action in actions:
        if action["action"] == "insert":
            print(f"INSERT {action['key']}")
            table.insert(action["key"])
        elif action["action"] == "lookup":
            print(f"LOOKUP {action['key']}")
            table.lookup(action["key"])

if __name__ == "__main__":
    main()

