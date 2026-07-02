#task2
from src.models.sequence import Sequence
from src.models.enums import Base, SequenceType


def main():
    # 创建一个 DNA 序列
    seq = Sequence("seq1", "Human", SequenceType.DNA)

    # 插入一些碱基
    seq.insert_nucleotide(0, Base.A)
    seq.insert_nucleotide(1, Base.T)
    seq.insert_nucleotide(2, Base.G)
    seq.insert_nucleotide(3, Base.C)

    print("original-sequence:", seq.get_sequence_string())

    # 删除
    seq.delete_nucleotide(1)
    print("delete:", seq.get_sequence_string())

    # 替换
    seq.substitute_nucleotide(1, Base.T)
    print("replace:", seq.get_sequence_string())

    # 反向互补
    rc = seq.reverse_complement()
    print("suppletion:", rc.get_sequence_string())


if __name__=="__main__":
    main()