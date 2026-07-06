import unittest

from src.models.mutation import Mutation
from src.models.enums import MutationType, Base


class TestMutation(unittest.TestCase):

    def setUp(self):
        self.m = Mutation(
            MutationType.SUBSTITUTION,
            1,
            Base.A,
            Base.T
        )

    def test_create(self):

        self.assertEqual(self.m.position, 1)
        self.assertEqual(self.m.new_base, Base.T)


if __name__ == "__main__":
    unittest.main()
    