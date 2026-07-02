from src.models.enums import Base

class Nucleotide:
    def __init__(self, base: Base, position: int):
        self.base = base
        self.position = position

        # 为 Task2 的双向链表预留
        self.prev = None
        self.next = None