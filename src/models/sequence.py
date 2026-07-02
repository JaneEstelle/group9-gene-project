from src.models.enums import Base
from src.models.nucleotide import Nucleotide
from src.models.stack import Stack

class Sequence:
    def __init__(self, sequence_id, species_name, sequence_type):
        self.sequence_id = sequence_id
        self.species_name = species_name
        self.sequence_type = sequence_type

        self.head = None
        self.tail = None
        self.size = 0

        self.mutation_stack = Stack()

    # 插入碱基
    def insert_nucleotide(self, position, base):
        if position < 0 or position > self.size:
            raise IndexError("Invalid position")

        node = Nucleotide(base, position)

        if self.head is None:
            self.head = node
            self.tail = node
        elif position == 0:
            node.next = self.head
            self.head.prev = node
            self.head = node
        elif position == self.size:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            cur = self.head
            for _ in range(position):
                cur = cur.next

            node.prev = cur.prev
            node.next = cur
            cur.prev.next = node
            cur.prev = node

        self.size += 1
        self.update_positions()

    # 删除碱基
    def delete_nucleotide(self, position):
        if position < 0 or position >= self.size:
            raise IndexError("Invalid position")

        cur = self.head
        for _ in range(position):
            cur = cur.next

        if self.size == 1:
            self.head = None
            self.tail = None
        elif cur == self.head:
            self.head = cur.next
            self.head.prev = None
        elif cur == self.tail:
            self.tail = cur.prev
            self.tail.next = None
        else:
            cur.prev.next = cur.next
            cur.next.prev = cur.prev

        self.size -= 1
        self.update_positions()

        return cur.base

    # 替换碱基
    def substitute_nucleotide(self, position, new_base):
        cur = self.head
        for _ in range(position):
            cur = cur.next

        old = cur.base
        cur.base = new_base
        return old

    # 返回序列
    def get_sequence_string(self):
        s = ""
        cur = self.head

        while cur:
            s += cur.base.value
            cur = cur.next

        return s

    # 长度
    def length(self):
        return self.size

    # 查找子序列
    def find_subsequence(self, pattern):
        return self.get_sequence_string().find(pattern)

    # 反向互补
    def reverse_complement(self):
        table = {
            Base.A: Base.T,
            Base.T: Base.A,
            Base.G: Base.C,
            Base.C: Base.G
        }

        new_seq = Sequence(
            self.sequence_id + "_rc",
            self.species_name,
            self.sequence_type
        )

        cur = self.tail
        while cur:
            new_seq.insert_nucleotide(new_seq.size, table[cur.base])
            cur = cur.prev

        return new_seq

    # 更新位置
    def update_positions(self):
        cur = self.head
        index = 0

        while cur:
            cur.position = index
            index += 1
            cur = cur.next