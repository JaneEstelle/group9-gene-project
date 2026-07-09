import sys
from pathlib import Path
# 自动添加项目根目录，解决 No module named 'src'
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

from src.structures.stack import Stack
from src.models.sequence import Sequence


def compute_edit_distance(seq_a, seq_b):
    s1 = seq_a.get_sequence_string()
    s2 = seq_b.get_sequence_string()
    
    m = len(s1)  # 序列a长度
    n = len(s2)  # 序列b长度
    
    dp = []
    i = 0
    while i < m + 1:
        row = []
        j = 0
        while j < n + 1:
            row.append(0)
            j = j + 1
        dp.append(row)
        i = i + 1  # 修复：原代码错误写为 i = i + 14
    
    # 初始化第一列
    i = 0
    while i < m + 1:
        dp[i][0] = i
        i = i + 1
    # 初始化第一行
    j = 0
    while j < n + 1:
        dp[0][j] = j
        j = j + 1
    
    # 填充dp表
    i = 1
    while i < m + 1:
        j = 1
        while j < n + 1:
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            option1 = dp[i-1][j] + 1
            option2 = dp[i][j-1] + 1
            option3 = dp[i-1][j-1] + cost
            dp[i][j] = min(option1, option2, option3)
            j = j + 1
        i = i + 1
    
    return dp


# 回溯函数
def traceback(seq_a, seq_b, dp):
    s1 = seq_a.get_sequence_string()
    s2 = seq_b.get_sequence_string()
    
    m = len(s1)
    n = len(s2)
    alignment_stack = Stack()
    
    i = m
    j = n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            alignment_stack.push(('MATCH', s1[i-1], s2[j-1]))
            i = i - 1
            j = j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            alignment_stack.push(('SUBSTITUTE', s1[i-1], s2[j-1]))
            i = i - 1
            j = j - 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            alignment_stack.push(('INSERT', '-', s2[j-1]))
            j = j - 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            alignment_stack.push(('DELETE', s1[i-1], '-'))
            i = i - 1
    
    return dp[m][n], alignment_stack


def get_alignment_from_stack(stack):
    aligned_a = []
    aligned_b = []
    operations = []
    
    items = stack.get_all()
    i = len(items) - 1
    while i >= 0:
        item = items[i]
        op = item[0]
        char_a = item[1]
        char_b = item[2]
        aligned_a.append(char_a)
        aligned_b.append(char_b)
        operations.append(op)
        i = i - 1
    
    str_a = ''
    j = 0
    while j < len(aligned_a):
        str_a = str_a + aligned_a[j]
        j = j + 1
    
    str_b = ''
    j = 0
    while j < len(aligned_b):
        str_b = str_b + aligned_b[j]
        j = j + 1
    
    return str_a, str_b, operations