import sys
import json

class SparseTable:
    def __init__(self, nn, mm, k, x):
        self.nn = nn
        self.mm = mm
        self.k = k
        self.n = 1
        self.m = int(self.nn[k - 1] * self.mm[k])
        self.table = [x] + [x] * (self.m - 1)
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
        low, high = 0, self.n
        while low < high:
            mid = (low + high) // 2
            idx = (self.head + mid) % self.m
            if self.table[idx] < key:
                low = mid + 1
            else:
                high = mid
        return low

    def rebuild(self, new_m):
        self.auth_keys.sort()
        new_table = [None] * new_m
        n = len(self.auth_keys)
        q = new_m // n
        r = new_m % n
        positions = []
        index = 0
        for i in range(n):
            positions.append(index)
            step = q + 1 if (i * r) // n < ((i + 1) * r) // n else q
            index += step
        for pos, key in zip(positions, self.auth_keys):
            new_table[pos] = key
        for i in range(new_m):
            if new_table[i] is None:
                new_table[i] = new_table[i - 1]
        self.table = new_table
        self.m = new_m
        self.n = n
        self.head = 0

    def insert(self, key):
        if key in self.auth_keys:
            self.print_table()
            return
        if self.n == self.nn[self.k]:
            self.k += 1
            new_m = int(self.nn[self.k - 1] * self.mm[self.k])
            self.rebuild(new_m)
        pos = self.binary_search_insert_position(key)
        idx = (self.head + pos) % self.m
        if (pos == 0 and self.table[idx] == self.table[(idx + 1) % self.m]) or            (pos > 0 and self.table[idx] == self.table[(idx - 1 + self.m) % self.m]):
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

    def delete(self, key):
        if key not in self.auth_keys:
            self.print_table()
            return
        pos = self.binary_search_insert_position(key)
        idx = (self.head + pos) % self.m
        count = 1
        i = (idx + 1) % self.m
        while i != self.head and self.table[i] == key:
            count += 1
            i = (i + 1) % self.m
        next_value = self.table[i] if i != self.head else key
        for j in range(count):
            self.table[(idx + j) % self.m] = next_value
        self.auth_keys.remove(key)
        self.auth_keys.sort()
        self.n -= 1
        if self.k >= 2 and self.n == self.nn[self.k - 2]:
            self.k -= 1
            new_m = int(self.nn[self.k - 1] * self.mm[self.k])
            self.rebuild(new_m)
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
        elif action["action"] == "delete":
            print(f"DELETE {action['key']}")
            table.delete(action["key"])

if __name__ == "__main__":
    main()
