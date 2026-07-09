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


# ===================================
# Task 3 - MST
# ===================================

    def compute_mst(self):
        
        # 创建新图存储MST
        mst = PhylogeneticGraph()
        
        for species in self.species:
            mst.add_species(species)
            
        if len(self.species) <= 1:
            return mst
        
        # 按距离从小到大排序边
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        parent = {species: species for species in self.species}
        
        # 防止成环（遍历）
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        # 防止成环（判断）
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return False
            parent[root_y] = root_x
            return True
        
        # main part of Kruskal's algorithm
        for species1, species2, distance in sorted_edges:
            if union(species1, species2):
                mst.add_relationship(species1, species2, distance)
                # 当边数达到V-1时停止
                if len(mst.edges) == len(self.species) - 1:
                    break
        
        return mst