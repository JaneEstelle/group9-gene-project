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
    INSERTION = "INSERTION"
    DELETION = "DELETION"
    SUBSTITUTION = "SUBSTITUTION"