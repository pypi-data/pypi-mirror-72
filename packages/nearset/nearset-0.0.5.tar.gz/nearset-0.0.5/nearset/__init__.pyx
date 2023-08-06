from collections import defaultdict
from bisect import bisect_left
from blist import blist


cdef class Node(object):
    cpdef public object value
    cpdef public object key
    cpdef public float order

    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def __repr__(self):
        return f"<{self.key}>{self.value}"


cdef class Nearset(object):
    cpdef public object cmp
    cpdef public object _keys
    cpdef public Node start_value
    cpdef public object nodes
    cpdef public object orders
    cpdef public int max_size

    def __init__(self, cmp, max_size=-1):
        self.cmp = cmp
        self._keys = blist()
        self.nodes = blist()
        self.orders = blist()
        self.max_size = max_size

    def __len__(self):
        return len(self._keys)
    
    def __setitem__(self, key, value):
        self.add(key, value)

    cpdef add(self, object key, object value=None):
        cpdef Node node

        # if no key is provided, key is the value
        if value is None:
            value = key

        # if element already exists, ignore
        if key in self._keys:
            return

        # create Node element and compute sort value
        node = Node(key, value)
        node.order = self.cmp(node.value)

        if self.max_size > 0 \
                and len(self._keys) >= self.max_size \
                and node.order > self.nodes[self.max_size - 1].order:
            return

        # if the node is the first element to be inserted, insert immediately
        if len(self._keys) == 0:
            # isometrically insert data in nodes, indices and keys
            self.nodes.append(node)
            self._keys.append(key)
            self.orders.append(node.order)
        else:
            # insert node using the standard method
            self.insert(node)

    cpdef insert(self, Node node):
        # get insertion index
        idx = bisect_left(self.orders, node.order)

        # isometrically insert data in nodes, indices and keys
        self.nodes.insert(idx, node)
        self._keys.insert(idx, node.key)
        self.orders.insert(idx, node.order)

        if self.max_size > 0 and len(self.nodes) > self.max_size:
            self.nodes = self.nodes[:self.max_size]
            self._keys = self._keys[:self.max_size]
            self.orders = self.orders[:self.max_size]

    cpdef pop(self):
        self.orders.pop()
        node = self.nodes.pop()
        self._keys.remove(node.key)
        return node

    cpdef lpop(self):
        self.orders.pop(0)
        node = self.nodes.pop(0)
        self._keys.remove(node.key)
        return node

    cpdef items(self):
        return [(item.key, item.value) for item in self.nodes]
    
    def __iter__(self):
        for node in self.nodes:
            yield node.key, node.value, node.order

    def __repr__(self):
        return str([item.value for item in self.nodes])

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nodes[key].value
        elif isinstance(key, slice):
            return [item.value for item in self.nodes[key]]
        raise KeyError(key)
