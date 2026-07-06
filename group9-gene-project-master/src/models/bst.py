from src.models.sequence import Sequence


class BSTNode:
    def __init__(self, sequence):
        self.sequence = sequence
        self.left = None
        self.right = None


class SequenceLibrary:
    def __init__(self):
        self.root = None

    def insert(self, sequence):
        if self.root is None:
            self.root = BSTNode(sequence)
        else:
            self._insert_helper(self.root, sequence)

    def _insert_helper(self, node, sequence):
        if sequence.sequence_id < node.sequence.sequence_id:
            if node.left is None:
                node.left = BSTNode(sequence)
            else:
                self._insert_helper(node.left, sequence)
        elif sequence.sequence_id > node.sequence.sequence_id:
            if node.right is None:
                node.right = BSTNode(sequence)
            else:
                self._insert_helper(node.right, sequence)
        else:
            print("Error: Sequence ID already exists!")

    def search(self, sequence_id):
        return self._search_helper(self.root, sequence_id)

    def _search_helper(self, node, sequence_id):
        if node is None:
            return None
        if sequence_id == node.sequence.sequence_id:
            return node.sequence
        elif sequence_id < node.sequence.sequence_id:
            return self._search_helper(node.left, sequence_id)
        else:
            return self._search_helper(node.right, sequence_id)

    def delete(self, sequence_id):
        self.root = self._delete_helper(self.root, sequence_id)

    def _delete_helper(self, node, sequence_id):
        if node is None:
            return None

        if sequence_id < node.sequence.sequence_id:
            node.left = self._delete_helper(node.left, sequence_id)
        elif sequence_id > node.sequence.sequence_id:
            node.right = self._delete_helper(node.right, sequence_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_node = self._find_min(node.right)
            node.sequence = min_node.sequence
            node.right = self._delete_helper(node.right, min_node.sequence.sequence_id)

        return node

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def find_by_species(self, species_name):
        result = []
        self._find_by_species_helper(self.root, species_name, result)
        return result

    def _find_by_species_helper(self, node, species_name, result):
        if node is None:
            return
        self._find_by_species_helper(node.left, species_name, result)
        if node.sequence.species_name == species_name:
            result.append(node.sequence)
        self._find_by_species_helper(node.right, species_name, result)

    def in_order_traversal(self):
        result = []
        self._in_order_helper(self.root, result)
        return result

    def _in_order_helper(self, node, result):
        if node is None:
            return
        self._in_order_helper(node.left, result)
        result.append(node.sequence)
        self._in_order_helper(node.right, result)