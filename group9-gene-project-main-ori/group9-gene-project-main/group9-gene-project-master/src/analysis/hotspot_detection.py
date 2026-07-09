# from src.models.sequence import Sequence
import sys
from pathlib import Path

# 获取当前文件所在目录往上两层，即项目根目录
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

# 再导入
from src.models.sequence import Sequence

def detect_hotspots(sequences, threshold=0.3):
    if len(sequences) == 0:
        return []
    
    max_length = 0
    i = 0
    while i < len(sequences):
        length = sequences[i].length()
        if length > max_length:
            max_length = length
        i = i + 1
    
    if max_length == 0:
        return []
    
    mutation_counts = []
    i = 0
    while i < max_length:
        mutation_counts.append(0)
        i = i + 1
    
    i = 0
    while i < len(sequences):
        seq = sequences[i]
        current = seq.head
        pos = 0
        while current is not None:
            mutations = seq.mutation_history()
            j = 0
            while j < len(mutations):
                mutation = mutations[j]
                if mutation.position == pos:
                    mutation_counts[pos] = mutation_counts[pos] + 1
                    break
                j = j + 1
            current = current.next
            pos = pos + 1
        i = i + 1
    
    num_sequences = len(sequences)
    hotspots = []
    
    i = 0
    while i < max_length:
        if num_sequences > 0:
            frequency = mutation_counts[i] / num_sequences
            if frequency > threshold:
                hotspot = {}
                hotspot['position'] = i
                hotspot['mutation_count'] = mutation_counts[i]
                hotspot['frequency'] = frequency
                hotspots.append(hotspot)
        i = i + 1
    
    i = 0
    while i < len(hotspots) - 1:
        j = i + 1
        while j < len(hotspots):
            if hotspots[i]['frequency'] < hotspots[j]['frequency']:
                temp = hotspots[i]
                hotspots[i] = hotspots[j]
                hotspots[j] = temp
            j = j + 1
        i = i + 1
    
    return hotspots


def detect_hotspots_from_multiple_alignments(sequences, threshold=0.3):
    if len(sequences) == 0:
        return []
    
    max_length = 0
    i = 0
    while i < len(sequences):
        length = sequences[i].length()
        if length > max_length:
            max_length = length
        i = i + 1
    
    if max_length == 0:
        return []
    
    base_counts = []
    i = 0
    while i < max_length:
        base_counts.append({'A': 0, 'T': 0, 'G': 0, 'C': 0})
        i = i + 1
    
    i = 0
    while i < len(sequences):
        seq = sequences[i]
        current = seq.head
        pos = 0
        while current is not None and pos < max_length:
            base = current.base.value
            if base in base_counts[pos]:
                base_counts[pos][base] = base_counts[pos][base] + 1
            current = current.next
            pos = pos + 1
        i = i + 1
    
    num_sequences = len(sequences)
    hotspots = []
    
    i = 0
    while i < max_length:
        counts = base_counts[i]
        max_count = 0
        bases_list = ['A', 'T', 'G', 'C']
        j = 0
        while j < len(bases_list):
            base = bases_list[j]
            if counts[base] > max_count:
                max_count = counts[base]
            j = j + 1
        
        if num_sequences > 0:
            max_freq = max_count / num_sequences
            diversity = 1 - max_freq
            
            if diversity > threshold:
                hotspot = {}
                hotspot['position'] = i
                hotspot['base_counts'] = counts
                hotspot['diversity'] = diversity
                
                majority_base = 'A'
                minority_base = 'A'
                max_val = 0
                min_val = 99999
                j = 0
                while j < len(bases_list):
                    base = bases_list[j]
                    if counts[base] > max_val:
                        max_val = counts[base]
                        majority_base = base
                    if counts[base] < min_val:
                        min_val = counts[base]
                        minority_base = base
                    j = j + 1
                
                hotspot['majority_base'] = majority_base
                hotspot['minority_base'] = minority_base
                hotspots.append(hotspot)
        i = i + 1
    
    i = 0
    while i < len(hotspots) - 1:
        j = i + 1
        while j < len(hotspots):
            if hotspots[i]['diversity'] < hotspots[j]['diversity']:
                temp = hotspots[i]
                hotspots[i] = hotspots[j]
                hotspots[j] = temp
            j = j + 1
        i = i + 1
    
    return hotspots