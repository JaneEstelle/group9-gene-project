Part1

task2:
- Why is a linked list natural for representing mutations?
    A linked list is a linear data structure made of nodes, where each node stores data and a pointer (reference) to the next node. Linked list elements are connected by pointers. This is famailar to mutations. DNA often requires insertions or deletions at positions in the middle of the sequence. A linked list can modify node connections directly without shifting large numbers of elements, making it highly suitable for modeling mutations.

DNA sequences are naturally modelled as linked lists of nucleotides (enabling efficient insertions and deletions that represent mutations)


- What is the cost of `insert_nucleotide` at position k in a linked list vs. in a Python string?
    链表想访问第 k 个核苷酸，必须从头开始走到第 k 个节点，后插入；python字符串是不可以改变的，需要先索引位置，再复制前半部分插入新字符，然后复制后半部分。链表的代价主要是遍历，字符串的代价主要是复制。
A linked list must traverse from the head to reach the k‑th nucleotide before performing an insertion at that position.
A Python string is immutable, so you must first locate the index, then copy the prefix, insert the new character, and finally copy the suffix.
The cost for a linked list comes mainly from traversal, while the cost for a string comes mainly from copying.

- When does the linked list underperform？
    当整体长度超长，需要频繁寻找靠后的指定位置时
    When the overall sequence becomes very long and you frequently need to access positions near the end.

task3:
- What information must a Mutation object store to be undoable?
    把序列恢复到突变之前的状态，需要储存突变位置，突变类型，突变前的碱基和突变后的碱基
To restore the sequence to its state before the mutation, you need to store the mutation position, the mutation type, the original base, and the mutated base.

- Is it sufficient to store the mutation type and position, or do you need more?
    Not enough. if we only store the mutation type and position, the program don't know what base should recover or delete.