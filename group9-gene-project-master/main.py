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


    # --------Task4 -----------------------------------------------------------------
    from src.models.bst import SequenceLibrary

    print("\n=== Task4: Sequence Library ===")
    lib = SequenceLibrary()

    seq4 = Sequence("seq001", "Human", SequenceType.DNA)
    seq4.insert_nucleotide(0, Base.A)
    seq4.insert_nucleotide(1, Base.T)

    seq5 = Sequence("seq002", "Chimp", SequenceType.DNA)
    seq5.insert_nucleotide(0, Base.G)

    lib.insert(seq4)
    lib.insert(seq5)

    found = lib.search("seq001")
    print("Search seq001:", found.species_name if found else "Not found")

    human_seqs = lib.find_by_species("Human")
    print("Human sequences count:", len(human_seqs))

    all_seqs = lib.in_order_traversal()
    print("All sequences:", [s.sequence_id for s in all_seqs])

    lib.delete("seq001")
    found = lib.search("seq001")
    print("After delete seq001:", "Found" if found else "Not found")


    # --------Task5 -----------------------------------------------------------------
    from src.models.graph import PhylogeneticGraph

    print("\n=== Task5: Phylogenetic Graph ===")
    graph = PhylogeneticGraph()

    graph.add_species("Human")
    graph.add_species("Chimp")
    graph.add_species("Gorilla")

    graph.add_relationship("Human", "Chimp", 0.01)
    graph.add_relationship("Human", "Gorilla", 0.03)
    graph.add_relationship("Chimp", "Gorilla", 0.02)

    print("All species:", graph.get_all_species())
    print("All relationships:", graph.get_relationships())
    print("Distance Human-Chimp:", graph.get_distance("Human", "Chimp"))

    graph.remove_relationship("Human", "Gorilla")
    print("\nAfter removing Human-Gorilla relationship:")
    print("All relationships:", graph.get_relationships())

    graph.remove_species("Gorilla")
    print("\nAfter removing Gorilla:")
    print("All species:", graph.get_all_species())
    print("All relationships:", graph.get_relationships())


if __name__=="__main__":
    main()