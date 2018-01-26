import sys

def main(array, mod):
    prefix = []
    global_max, current_max = 0, 0

    for element in array:
        current_max = max(current_max + element, 0)
        global_max = max(global_max, current_max)
        prefix.append(global_max)

    return global_max, prefix

if __name__ == "__main__":
    try:
        array = [int(_) for _ in sys.argv[1:-1]]
        mod = int(sys.argv[len(sys.argv) - 1])
    except Exception as e:
        print e
        sys.exit()

    print "Array: %s" % array
    print "Mod: %s" % mod

    '''
    This is not good, because, we are making the maximum sums regularily and
    then calculating the mod for each. But we don't want that. We want the
    prefix array it's self to hold the mod sums
    '''

    _ = main(array, mod)
    print _
    print map(lambda _: _ % mod, _[1])

'''
If sum[i] - sum[start] is -1 and M=7, we have (-1 + 7) % 7 which is 6

'''
