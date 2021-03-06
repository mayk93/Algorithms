import sys

def main(array):
    global_max, current_max = 0, 0

    for element in array:
        current_max = max(current_max + element, 0)
        global_max = max(global_max, current_max)

    return global_max

if __name__ == "__main__":
    try:
        array = [int(_) for _ in sys.argv[1:]]
    except Exception as e:
        print e
        sys.exit()
    _ = main(array)
    print _
