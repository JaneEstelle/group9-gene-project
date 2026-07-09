import csv
from src.models.sequence import Sequence
from src.models.mutation import Mutation
from src.models.enums import Base, SequenceType, MutationType
from src.structures.graph import PhylogeneticGraph


def load_sequences(csv_path):
    sequences = {}
    
    f = open(csv_path, 'r')
    reader = csv.DictReader(f)
    
    rows = []
    for row in reader:
        rows.append(row)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        seq_id = row['sequence_id']
        species_name = row['species_name']
        seq_type = row['sequence_type']
        
        seq = Sequence(seq_id, species_name, SequenceType[seq_type])
        
        seq_str = row['sequence_string']
        j = 0
        while j < len(seq_str):
            base_char = seq_str[j]
            seq.insert_nucleotide(j, Base[base_char])
            j = j + 1
        
        sequences[seq_id] = seq
        i = i + 1
    
    f.close()
    return sequences


def load_mutations(csv_path):
    mutations = []
    
    f = open(csv_path, 'r')
    reader = csv.DictReader(f)
    
    rows = []
    for row in reader:
        rows.append(row)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        mutation_type = MutationType[row['mutation_type']]
        position = int(row['position'])
        original_base = Base[row['original_base']]
        new_base = Base[row['new_base']]
        
        mutation = Mutation(mutation_type, position, original_base, new_base)
        
        mut_item = {}
        mut_item['sequence_id'] = row['sequence_id']
        mut_item['mutation'] = mutation
        mutations.append(mut_item)
        
        i = i + 1
    
    f.close()
    return mutations


def load_distances(csv_path):
    graph = PhylogeneticGraph()
    
    f = open(csv_path, 'r')
    reader = csv.DictReader(f)
    
    rows = []
    for row in reader:
        rows.append(row)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        species_a = row['species_a']
        species_b = row['species_b']
        distance = int(row['distance'])
        
        graph.add_relationship(species_a, species_b, distance)
        
        i = i + 1
    
    f.close()
    return graph


def load_all_datasets(input_dir='datasets'):
    seq_file = input_dir + '/sequences_dataset.csv'
    mut_file = input_dir + '/mutations_dataset.csv'
    dist_file = input_dir + '/evolutionary_distances_dataset.csv'
    
    sequences = load_sequences(seq_file)
    mutations = load_mutations(mut_file)
    graph = load_distances(dist_file)
    
    i = 0
    while i < len(mutations):
        mut_data = mutations[i]
        seq_id = mut_data['sequence_id']
        if seq_id in sequences:
            sequences[seq_id].apply_mutation(mut_data['mutation'])
        i = i + 1
    
    return sequences, mutations, graph