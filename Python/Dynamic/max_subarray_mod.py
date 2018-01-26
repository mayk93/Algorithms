import sys

class Tree():
    def __init__(self):
        self.tree = []

    def add(self, element):
        # ToDo: Turn this into a propper tree
        self.tree.append(element)
        self.tree.sort()

    def min_above(self, lowest):
        for _ in self.tree:
            print "Now looking at %s, need to be immediatly above %s" % (
                _, lowest
            )
            if _ >= lowest:
                return _
        print "This is not right!"
        print self.tree
        return self.tree[0]

def main(array, mod):
    prefix = [array[0]]  # Here we keep the prefix sums
    tree = Tree()
    tree.add(prefix[0])
    result = prefix[0]
    index = 0
    for element in array[1:]:
        prefix.append((prefix[index] + element) % mod)
        min_above = tree.min_above(prefix[index])
        result = max((prefix[index] - min_above) % mod, result)
        tree.add(prefix[index])
    return result


if __name__ == "__main__":
    try:
        array = [int(_) for _ in sys.argv[1:]]
        mod = int(sys.argv[len(sys.argv) - 1])
    except Exception as e:
        print e
        sys.exit()
    _ = main(array, mod)
    print _


'''
int[] sum;
sum[0] = A[0];
Tree tree;
tree.add(sum[0]);
int result = sum[0];
for(int i = 1; i < n; i++){
    sum[i] = sum[i - 1] + A[i];
    sum[i] %= M;
    int a = tree.getMinimumValueLargerThan(sum[i]);
    result = max((sum[i] - a + M) % M, result);
    tree.add(sum[i]);
}
print result;
'''
