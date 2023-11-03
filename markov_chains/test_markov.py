import logging
import unittest

from markov_chains.markov import MarkovChain

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MarkovChainsTests(unittest.TestCase):
    def test_alphabet(self):
        self.assertEqual(
            MarkovChain.from_data("AABABAABAAAB").alphabet,
            ("A", "B"),
        )

    def test_table_render(self):
        mc = MarkovChain.from_data(
            "AABABAABAAABABABAAA",
            order=1,
        )
        self.assertEqual(
            mc.render_transition_table(fmt="markdown"),
            (
                "         |  A   |  B   |\n"
                "|--------|------|------|\n"
                "| ('A',) | 0.50 | 0.50 |\n"
                "| ('B',) | 1.00 | 0.00 |"
            ),
        )

    # def test_shakespeare(self):
    #     random.seed(1337)
    #     mc = MarkovChain.from_data(
    #         # Path("texts/shakespeare-hamlet.txt").read_text().lower(),
    #         Path("texts/anonymous-luftpirat-1.txt").read_text().lower(),
    #         # order=1,
    #         order=5,
    #     )
    #     start = "ein Luftball".lower()
    #     # start = "For Hamlet".lower()
    #     sample = "".join(mc.generate(500, start))
    #     print(start + sample)


if __name__ == "__main__":
    unittest.main()
