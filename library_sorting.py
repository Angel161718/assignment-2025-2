import sys
import json

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


if __name__ == "__main__":
    main()
