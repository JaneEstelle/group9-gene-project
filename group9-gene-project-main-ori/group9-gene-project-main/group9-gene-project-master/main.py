# 序列链表核心类，存储 DNA 字符串、碱基链表、突变记录，生成 / 加载数据集时创建序列对象
from src.models.sequence import Sequence
# 枚举类：碱基 (A/T/G/C)、序列类型 DNA、突变类型替换，规范数据格式
from src.models.enums import Base, SequenceType, MutationType
# 突变实体类，保存突变位点、原碱基、突变碱基，加载 CSV 突变数据使用
from src.models.mutation import Mutation
# 二叉搜索树 BST，Task6 要求加载完序列后存入 BST，提供按物种查找序列功能
from src.structures.bst import SequenceLibrary
# 进化关系图，加载 distance CSV 构建物种 / 序列距离边，后续求 MST
from src.structures.graph import PhylogeneticGraph
# Part2 Task1 编辑距离（Levenshtein）专用导入
from src.analysis.edit_distance import compute_edit_distance, traceback, get_alignment_from_stack
# Part2 Task2 突变热点检测专用导入
from src.analysis.hotspot_detection import detect_hotspots, detect_hotspots_from_multiple_alignments
from src.data.dataset_generator import generate_all_datasets
from src.data.data_loader import load_all_datasets


def main():

    # ============================================================
    # 第一个 main 的原有内容（完全不变）
    # ============================================================

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
    from src.structures.bst import SequenceLibrary

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
    from src.structures.graph import PhylogeneticGraph

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


    # ============================================================
    # Part 1 Task 6: Generate and Load Dataset
    # ============================================================
    print("=" * 70)
    print("Bioinformatics Analysis Tool - Comprehensive Test")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("Part 1 Task 6: Generate and Load Dataset")
    print("=" * 70)

    generate_all_datasets()

    sequences_dict, mutations_list, graph = load_all_datasets()

    sequences = []
    for seq_id in sequences_dict:
        sequences.append(sequences_dict[seq_id])

    sequence_library = SequenceLibrary()
    i = 0
    while i < len(sequences):
        sequence_library.insert(sequences[i])
        i = i + 1

    print("\nLoaded " + str(len(sequences)) + " sequences into BST")
    print("Loaded " + str(len(graph.species)) + " species into phylogenetic graph")
    print("Loaded " + str(len(graph.edges)) + " evolutionary relationships")


    # ============================================================
    # Part 2 Task 1: Edit Distance (Levenshtein)
    # ============================================================
    print("\n" + "=" * 70)
    print("Part 2 Task 1: Edit Distance (Levenshtein)")
    print("=" * 70)

    seq1 = Sequence("seq1", "Test1", SequenceType.DNA)
    seq2 = Sequence("seq2", "Test2", SequenceType.DNA)

    bases1 = "ATGC"
    j = 0
    while j < len(bases1):
        seq1.insert_nucleotide(seq1.size, Base[bases1[j]])
        j = j + 1

    bases2 = "AAGC"
    j = 0
    while j < len(bases2):
        seq2.insert_nucleotide(seq2.size, Base[bases2[j]])
        j = j + 1

    print("\nSequence 1: " + seq1.get_sequence_string())
    print("Sequence 2: " + seq2.get_sequence_string())

    dp = compute_edit_distance(seq1, seq2)
    distance, stack = traceback(seq1, seq2, dp)
    print("\nEdit Distance: " + str(distance))

    aligned_a, aligned_b, operations = get_alignment_from_stack(stack)
    print("\nAlignment:")
    print("  " + aligned_a)

    marks = ""
    k = 0
    while k < len(operations):
        if operations[k] == 'MATCH':
            marks = marks + '|'
        else:
            marks = marks + '*'
        k = k + 1
    print("  " + marks)
    print("  " + aligned_b)

    print("\nOperations (from stack):")
    k = 0
    while k < len(operations):
        print("  Step " + str(k) + ": " + operations[k])
        k = k + 1


    # ============================================================
    # Part 2 Task 2: Mutation Hotspot Detection
    # ============================================================
    print("\n" + "=" * 70)
    print("Part 2 Task 2: Mutation Hotspot Detection")
    print("=" * 70)

    human_seqs = sequence_library.find_by_species("Homo sapiens")
    if len(human_seqs) > 0:
        hotspots = detect_hotspots_from_multiple_alignments(human_seqs, threshold=0.3)

        print("\nAnalyzing " + str(len(human_seqs)) + " sequences from Homo sapiens")
        print("Found " + str(len(hotspots)) + " mutation hotspots:")

        limit = 5
        if len(hotspots) < limit:
            limit = len(hotspots)
        k = 0
        while k < limit:
            hotspot = hotspots[k]
            print("\n  Position " + str(hotspot['position']) + ":")
            print("    Diversity: " + "{:.3f}".format(hotspot['diversity']))
            print("    Base Counts: " + str(hotspot['base_counts']))
            print("    Majority: " + hotspot['majority_base'] + ", Minority: " + hotspot['minority_base'])
            k = k + 1
    else:
        print("\nNo Homo sapiens sequences found in library")


    # ============================================================
    # PART2 TASK3
    # ============================================================
    from src.visualisation.MST_graph import PhylogeneticGraph as MSTPhyloGraph
    # ⚠️ 删除了重复的导入：from src.data.dataset_generator import generate_all_datasets
    import csv
    import os

    print("\n" + "=" * 60)
    print("Task 3: Minimum Spanning Tree (Kruskal's Algorithm)")
    print("=" * 60)

    # 1. 生成完整数据集
    print("\n[1] Generating dataset...")
    generate_all_datasets("datasets")

    # 2. 加载距离数据
    print("\n[2] Loading evolutionary distances...")
    mst_graph = MSTPhyloGraph()
    dist_path = os.path.join("datasets", "evolutionary_distances_dataset.csv")

    with open(dist_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mst_graph.add_relationship(
                row['species_a'],
                row['species_b'],
                int(row['distance'])
            )

    print(f"    Loaded {len(mst_graph.species)} species")
    print(f"    Loaded {len(mst_graph.edges)} edges")

    # 3. 计算 MST
    print("\n[3] Computing MST using Kruskal's algorithm...")
    mst = mst_graph.compute_mst()

    # 4. 显示结果
    print("\n" + "-" * 50)
    print("MST Results")
    print("-" * 50)
    print(f"  Total species: {len(mst.species)}")
    print(f"  MST edges: {len(mst.edges)}")
    print(f"  MST total weight: {sum(edge[2] for edge in mst.edges)}")
    print(f"  Original total weight: {sum(edge[2] for edge in mst_graph.edges)}")

    print("\n  MST edges (shortest evolutionary paths):")
    for u, v, w in sorted(mst.edges, key=lambda x: x[2]):
        print(f"    {u} -- {v} : {w}")

    # 5. 找出关系最近的物种对
    if len(mst.edges) > 0:
        closest = min(mst.edges, key=lambda x: x[2])
        print(f"\n  Closest relationship: {closest[0]} and {closest[1]} (distance {closest[2]})")

    print("\n" + "=" * 60)
    print(" MST computation complete!")
    print("=" * 60)


    # ============================================================
    # PART2 TASK4
    # ============================================================
    from src.analysis.benchmark import main as benchmark_main

    print("\n" + "=" * 60)
    print("Task 4: Empirical Benchmarking")
    print("=" * 60)
    print("\n[Running benchmarks...]")
    print("[This may take 1-2 minutes for L=20000]")
    print("=" * 60)

    benchmark_main()


if __name__ == "__main__":
    main()

print('程序运行成功')