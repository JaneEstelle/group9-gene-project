#task2
from src.models.sequence import Sequence
from src.models.enums import Base, SequenceType
from src.models.mutation import Mutation
from src.models.enums import MutationType


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



# --------Task3 -----------------------------------------------------------------

    # 新建一个序列进行测试
    seq2 = Sequence("seq2", "Human", SequenceType.DNA)

    seq2.insert_nucleotide(0, Base.A)
    seq2.insert_nucleotide(1, Base.T)
    seq2.insert_nucleotide(2, Base.G)
    seq2.insert_nucleotide(3, Base.C)

    print("original:", seq2.get_sequence_string())

    # 插入突变
    m1 = Mutation(
        MutationType.INSERTION,
        2,
        new_base=Base.A
    )
    seq2.apply_mutation(m1)
    print("after insertion:", seq2.get_sequence_string())

    # 删除突变
    m2 = Mutation(
        MutationType.DELETION,
        1
    )
    seq2.apply_mutation(m2)
    print("after deletion:", seq2.get_sequence_string())

    # 替换突变
    m3 = Mutation(
        MutationType.SUBSTITUTION,
        2,
        new_base=Base.T
    )
    seq2.apply_mutation(m3)
    print("after substitution:", seq2.get_sequence_string())

    print("\nundo")

    seq2.undo_last_mutation()
    print(seq2.get_sequence_string())

    seq2.undo_last_mutation()
    print(seq2.get_sequence_string())

    seq2.undo_last_mutation()
    print(seq2.get_sequence_string())

    print("\nmutation history:")

    history = seq2.mutation_history()

    if len(history) == 0:
        print("empty")
    else:
        for mutation in history:
            print(mutation.mutation_type.value, mutation.position)




if __name__=="__main__":
    main()