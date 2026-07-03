from enum import Enum


class Base(Enum):
    A = "A"
    T = "T"
    G = "G"
    C = "C"


class SequenceType(Enum):
    DNA = "DNA"
    RNA = "RNA"


class MutationType(Enum):
    INSERTION = "INSERTION"        # 插入碱基
    DELETION = "DELETION"       # 删除碱基
    SUBSTITUTION = "SUBSTITUTION"     #替换碱基