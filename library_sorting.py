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

if __name__ == "__main__":
    main()
