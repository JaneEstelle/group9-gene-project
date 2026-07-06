class PhylogeneticGraph:
    def __init__(self):
        self.species = []
        self.edges = []

    def add_species(self, species_name):
        if species_name not in self.species:
            self.species.append(species_name)

    def remove_species(self, species_name):
        if species_name in self.species:
            self.species.remove(species_name)
            new_edges = []
            for edge in self.edges:
                if edge[0] != species_name and edge[1] != species_name:
                    new_edges.append(edge)
            self.edges = new_edges

    def add_relationship(self, species1, species2, distance):
        self.add_species(species1)
        self.add_species(species2)

        exists = False
        for edge in self.edges:
            if (edge[0] == species1 and edge[1] == species2) or \
               (edge[0] == species2 and edge[1] == species1):
                edge[2] = distance
                exists = True
                break

        if not exists:
            self.edges.append([species1, species2, distance])

    def remove_relationship(self, species1, species2):
        new_edges = []
        for edge in self.edges:
            if not ((edge[0] == species1 and edge[1] == species2) or
                    (edge[0] == species2 and edge[1] == species1)):
                new_edges.append(edge)
        self.edges = new_edges

    def get_distance(self, species1, species2):
        for edge in self.edges:
            if (edge[0] == species1 and edge[1] == species2) or \
               (edge[0] == species2 and edge[1] == species1):
                return edge[2]
        return None

    def minimum_spanning_tree(self):
        raise NotImplementedError("MST calculation is not implemented yet.")

    def get_all_species(self):
        return self.species.copy()

    def get_relationships(self):
        return [edge.copy() for edge in self.edges]