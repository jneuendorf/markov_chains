import unittest
import random
from pathlib import Path

from markov import MarkovChain


class MyTestCase(unittest.TestCase):
    def test_shakespeare(self):
        random.seed(1337)
        mc = MarkovChain(
            Path("texts/shakespeare-hamlet.txt").read_text().lower(),
            # Path("texts/anonymous-luftpirat-1.txt").read_text().lower(),
            # order=1,
            order=9,
        )
        # start = "ein Luftball".lower()
        start = "For Hamlet".lower()
        sample = "".join(mc.generate(500, start))
        print(start + sample)


if __name__ == "__main__":
    unittest.main()
