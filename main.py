from models.enums import Base
from models.enums import SequenceType
from models.enums import MutationType

from models.sequence import Sequence
from models.nucleotide import Nucleotide
from models.mutation import Mutation

sequence = Sequence(
    "SEQ001",
    "Human",
    SequenceType.DNA
)

nucleotide = Nucleotide(
    Base.A,
    1
)

mutation = Mutation(
    MutationType.SUBSTITUTION,
    1,
    Base.A,
    Base.G
)

print(sequence.sequence_id)
print(sequence.species_name)
print(nucleotide.base)
print(mutation.mutation_type)