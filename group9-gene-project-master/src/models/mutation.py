from src.models.enums import MutationType, Base

class Mutation:
    def __init__(self,
                 mutation_type: MutationType,
                 position: int,
                 original_base: Base = None,
                 new_base: Base = None):

        self.mutation_type = mutation_type
        self.position = position
        self.original_base = original_base
        self.new_base = new_base