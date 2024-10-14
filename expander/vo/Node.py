from vo.Tree import Tree


class Node(Tree):
    def __init__(self, name, order, is_block, contains):
        super().__init__(name, order)
        self.is_block = is_block
        self.contains = sorted(contains, key=lambda x: x.order)
