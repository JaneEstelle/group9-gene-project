import sys
import os

# Get project root directory (group9-gene-project-master)
# Current file: tests/models/test_MST.py, go up 3 levels to project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import unittest
from src.visualisation.MST_graph import PhylogeneticGraph


class TestMST(unittest.TestCase):
    """Test Minimum Spanning Tree functionality"""

    def test_single_species(self):
        """Single species, MST should have 0 edges"""
        graph = PhylogeneticGraph()
        graph.add_species("A")
        mst = graph.compute_mst()
        self.assertEqual(len(mst.edges), 0)

    def test_two_species(self):
        """Two species, MST should have 1 edge"""
        graph = PhylogeneticGraph()
        graph.add_relationship("A", "B", 5)
        mst = graph.compute_mst()
        self.assertEqual(len(mst.edges), 1)
        self.assertEqual(mst.edges[0][2], 5)

    def test_three_species(self):
        """Three species, MST total weight should be 5+8=13"""
        graph = PhylogeneticGraph()
        graph.add_relationship("A", "B", 10)
        graph.add_relationship("B", "C", 5)
        graph.add_relationship("A", "C", 8)
        mst = graph.compute_mst()
        total = sum(edge[2] for edge in mst.edges)
        self.assertEqual(total, 13)

    def test_four_species(self):
        """Four species, MST total weight should be 2+3+4=9"""
        graph = PhylogeneticGraph()
        graph.add_relationship("A", "B", 4)
        graph.add_relationship("A", "C", 2)
        graph.add_relationship("A", "D", 10)
        graph.add_relationship("B", "C", 3)
        graph.add_relationship("B", "D", 8)
        graph.add_relationship("C", "D", 4)
        mst = graph.compute_mst()
        self.assertEqual(len(mst.edges), 3)
        total = sum(edge[2] for edge in mst.edges)
        self.assertEqual(total, 9)


def demo_mst():
    """Demo: print MST edges and total weight"""
    print("\n" + "=" * 50)
    print("MST Computation Demo")
    print("=" * 50)

    # Create graph
    graph = PhylogeneticGraph()
    graph.add_relationship("A", "B", 4)
    graph.add_relationship("A", "C", 2)
    graph.add_relationship("B", "C", 1)
    graph.add_relationship("B", "D", 5)
    graph.add_relationship("C", "D", 3)

    # Compute MST
    mst = graph.compute_mst()

    print("MST Edges:")
    for u, v, w in mst.edges:
        print(f"  {u} -- {v} : {w}")
    print(f"MST Total Weight: {sum(edge[2] for edge in mst.edges)}")
    print("=" * 50)


if __name__ == "__main__":
    unittest.main(exit=False)
    sys.stdout.flush()  
    demo_mst()