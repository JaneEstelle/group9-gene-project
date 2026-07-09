# src/analysis/benchmark.py
"""
Task 4: Empirical Benchmarking
测试 L (序列长度) 和 N (序列数量) 对性能的影响
"""

import sys
import os

# ---- 设置 matplotlib 后端为非交互式，直接保存成文件 ----
import matplotlib
matplotlib.use('Agg')

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import time
import random
import matplotlib.pyplot as plt
from src.models.sequence import Sequence
from src.models.enums import Base, SequenceType
from src.structures.bst import SequenceLibrary
from src.analysis.edit_distance import compute_edit_distance, traceback

def random_seq(length):
    """生成随机 DNA 序列"""
    bases = ['A', 'T', 'G', 'C']
    seq = Sequence(f"test_{length}", "Test", SequenceType.DNA)
    for i, b in enumerate(''.join(random.choices(bases, k=length))):
        seq.insert_nucleotide(i, Base[b])
    return seq


# ============================================================
# 测试1：insert_nucleotide 在不同位置和长度的性能
# ============================================================

def test_insertion():
    lengths = [50, 200, 1000, 5000, 20000]
    results = {'begin': [], 'middle': [], 'end': []}
    repeats = 10000

    print("\n--- Insertion Performance (averaged over 10000 ops) ---")
    for L in lengths:
        print(f"  L={L}", end="")


####说一下update_pos我改的部分，关闭 update_positions()，避免遍历整个链表的干扰，测的是纯粹的指针操作时间。


        # 开头插入
        seq = random_seq(L)
        t = time.perf_counter()
        for _ in range(repeats):
            seq.insert_nucleotide(0, Base['A'], update_pos=False)
        avg_begin = (time.perf_counter() - t) / repeats
        results['begin'].append(avg_begin)

        # 中间插入
        seq = random_seq(L)
        t = time.perf_counter()
        for _ in range(repeats):
            seq.insert_nucleotide(L // 2, Base['A'], update_pos=False)
        avg_middle = (time.perf_counter() - t) / repeats
        results['middle'].append(avg_middle)

        # 末尾插入（修正：使用动态 seq.size）
        seq = random_seq(L)
        t = time.perf_counter()
        for _ in range(repeats):
            seq.insert_nucleotide(seq.size, Base['A'], update_pos=False)
        avg_end = (time.perf_counter() - t) / repeats
        results['end'].append(avg_end)

        print(f"  begin:{avg_begin:.6f}s  middle:{avg_middle:.6f}s  end:{avg_end:.6f}s")

    return lengths, results


# ============================================================
# 测试2：find_subsequence 在不同位置和长度的性能
# ============================================================

def test_search():
    """测试 find_subsequence 在开头/末尾的性能"""
    lengths = [50, 200, 1000, 5000, 20000]
    results = {'begin': [], 'end': []}
    pattern = "AAAA"
    
    print("\n--- Search Performance ---")
    for L in lengths:
        print(f"  L={L}", end="")
        # 开头
        seq = random_seq(L)
        for i, b in enumerate(pattern):
            seq.insert_nucleotide(i, Base[b], update_pos=False)
        t = time.perf_counter()
        seq.find_subsequence(pattern)
        results['begin'].append(time.perf_counter() - t)
        
        # 末尾
        seq = random_seq(L)
        for i, b in enumerate(pattern):
            seq.insert_nucleotide(L + i, Base[b], update_pos=False)
        t = time.perf_counter()
        seq.find_subsequence(pattern)
        results['end'].append(time.perf_counter() - t)
        
        print(f"  begin:{results['begin'][-1]:.6f}s  end:{results['end'][-1]:.6f}s")
    
    return lengths, results


# ============================================================
# 测试3：Edit Distance 在不同长度的性能
# ============================================================

def test_edit_distance():
    """测试编辑距离在不同 L 的性能"""
    lengths = [50, 200, 1000, 5000, 20000]
    results = []
    
    print("\n--- Edit Distance Performance ---")
    for L in lengths:
        print(f"  L={L}", end="")
        seq1 = random_seq(L)
        seq2 = random_seq(L)
        t = time.perf_counter()
        dp = compute_edit_distance(seq1, seq2)
        dist, _ = traceback(seq1, seq2, dp)
        elapsed = time.perf_counter() - t
        results.append(elapsed)
        print(f"  dist={dist}  time:{elapsed:.4f}s")
    
    return lengths, results


# ============================================================
# 测试4：不同序列数量 N 对 BST 插入的影响
# ============================================================

def test_collection_size():
    """测试不同 N (序列数量) 下的 BST 插入性能"""
    n_values = [10, 50, 200]
    results = []
    
    print("\n--- Collection Size Performance (BST insert) ---")
    for n in n_values:
        print(f"  N={n}", end="")
        bst = SequenceLibrary()
        t = time.perf_counter()
        for i in range(n):
            seq = Sequence(f"seq_{i}", "Test", SequenceType.DNA)
            for j, b in enumerate(''.join(random.choices(['A','T','G','C'], k=100))):
                seq.insert_nucleotide(j, Base[b], update_pos=False)
            bst.insert(seq)
        elapsed = time.perf_counter() - t
        results.append(elapsed)
        print(f"  time:{elapsed:.4f}s")
    
    return n_values, results


# ============================================================
# 绘图（保存为文件，不弹出窗口）
# ============================================================

def plot_results(lengths, ins, search, edit, n_values, n_times, filename="benchmark_results.png"):
    """绘制所有图表并保存为图片"""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    
    # 图1：插入性能
    ax = axes[0,0]
    ax.plot(lengths, ins['begin'], 'o-', label='Beginning', color='red')
    ax.plot(lengths, ins['middle'], 's-', label='Middle', color='blue')
    ax.plot(lengths, ins['end'], '^-', label='End', color='green')
    ax.set_xlabel('Sequence Length (L)')
    ax.set_ylabel('Time (s)')
    ax.set_title('Insertion Performance (Pure Pointer Ops)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图2：查找性能
    ax = axes[0,1]
    ax.plot(lengths, search['begin'], 'o-', label='Pattern at Beginning', color='orange')
    ax.plot(lengths, search['end'], 's-', label='Pattern at End', color='purple')
    ax.set_xlabel('Sequence Length (L)')
    ax.set_ylabel('Time (s)')
    ax.set_title('Search Performance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图3：编辑距离 + O(n^2) 验证
    ax = axes[1,0]
    ax.plot(lengths, edit, 'o-', color='red', label='Actual')
    if len(edit) > 0 and edit[0] > 0:
        theoretical = [edit[0] * (L / lengths[0]) ** 2 for L in lengths]
        ax.plot(lengths, theoretical, 'r--', label='O(n^2) Theoretical', alpha=0.6)
    ax.set_xlabel('Sequence Length (L)')
    ax.set_ylabel('Time (s)')
    ax.set_title('Edit Distance vs O(n^2)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图4：序列数量 N 对性能的影响
    ax = axes[1,1]
    ax.bar([str(n) for n in n_values], n_times, color='skyblue')
    ax.set_xlabel('Number of Sequences (N)')
    ax.set_ylabel('Time (s)')
    ax.set_title('BST Insert Performance (N sequences)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"\n[Plot saved] {filename}")


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 60)
    print("Task 4: Empirical Benchmarking")
    print("=" * 60)
    print("\n[Testing sequence lengths L = 50, 200, 1000, 5000, 20000]")
    print("[Testing collection sizes N = 10, 50, 200]")
    print("\nNote: L=20000 may take 1-2 minutes\n")
    
    # 运行所有测试
    L, ins = test_insertion()
    _, search = test_search()
    _, edit = test_edit_distance()
    N, n_times = test_collection_size()
    
    # 总结
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Edit distance at L=20000: {edit[-1]:.4f}s")
    print(f"  BST insert N=200: {n_times[-1]:.4f}s")
    
    # O(n^2) 验证
    if len(edit) >= 3:
        ratios = []
        for i in range(1, len(edit)):
            ratios.append((edit[i] / edit[i-1]) / ((L[i] / L[i-1]) ** 2))
        avg = sum(ratios) / len(ratios)
        print(f"\n  O(n^2) verification: average ratio = {avg:.2f}")
        if 0.5 < avg < 2.0:
            print("  -> [OK] Confirms O(n^2)")
        else:
            print("  -> [WARNING] Check implementation")
        # 判断明显变慢的长度
        for i, t in enumerate(edit):
            if t > 1.0:
                print(f"  -> Noticeably slow at L >= {L[i]}")
                break
        else:
            print("  -> Not noticeably slow up to L=20000")
    
    # 绘图保存
    plot_results(L, ins, search, edit, N, n_times, "benchmark_results.png")
    print("\n[OK] Done! Check benchmark_results.png in current folder.")


if __name__ == "__main__":
    main()