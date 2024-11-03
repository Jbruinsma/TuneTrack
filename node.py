class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self, start_label='start', end_label='end'):
        self.start = Node(start_label)
        self.end = Node(end_label)
        self.start.next = self.end
        self.end.prev = self.start

    def reset_ll(self):
        self.__init__(self.start.val, self.end.val)

    def add_to_end(self, val):
        new_node = Node(val)
        next_node = self.end
        prev_node = self.end.prev
        prev_node.next = new_node
        next_node.prev = new_node
        new_node.next = next_node
        new_node.prev = prev_node
