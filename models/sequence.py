from models.enums import SequenceType

class Sequence:
    def __init__(self,
                 sequence_id: str,
                 species_name: str,
                 sequence_type: SequenceType):

        self.sequence_id = sequence_id
        self.species_name = species_name
        self.sequence_type = sequence_type

        # 双向链表的头尾
        self.head = None
        self.tail = None