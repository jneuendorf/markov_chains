import itertools as it
import random
from collections import defaultdict
from pprint import pprint
from typing import Sequence, TypeVar, Hashable, Generic, Self

T = TypeVar("T", bound=Hashable)


# Word = T
Words = Sequence[T]
# State = Words
# FrozenWords = tuple[T, ...]


class MarkovChain(Generic[T]):
    seq: Words
    order: int
    transition_probs: dict[Words, dict[T, float]]
    cumulative_probs: dict[Words, list[tuple[T, float]]]

    def __init__(self, words: Words, order: int = 1):
        assert order >= 0, f"Order must be positive"

        self.order = order

        # print(f"words: {words}")

        distinct_words = tuple(set(words))
        # ngram_size = order + 1
        # Lower order n-gram size
        # lo_ngram_size = order
        group_counts: dict[Words, int] = defaultdict(int)
        condition_counts: dict[Words, int] = defaultdict(int)

        # print(f"counting {ngram_size}-grams and {lo_ngram_size}-grams")

        group_size = order + 1
        word_group: tuple[T, ...]
        for i in range(len(words)):
            word_group = tuple(words[i:i + group_size])
            # print(f"word group: {word_group}")
            # End reached
            if len(word_group) < group_size:
                break

            condition_group = word_group[:-1]
            # print(f"{ngram_size}-gram: {word_group}, {lo_ngram_size}-gram: {lo_ngram}")
            group_counts[word_group] += 1
            condition_counts[condition_group] += 1

        # pprint(dict(group_counts))
        # pprint(dict(condition_counts))
        # transition_probs = {
        #     (word_group[:-1], word_group[-1]): counts[word_group] / lo_counts[word_group[:-1]]
        #     for word_group in counts.keys()
        #     for word in distinct_words
        # }
        self.transition_probs = {
            condition_group: {
                word: group_counts[(*condition_group, word)] / condition_counts[condition_group]
                for word in distinct_words
            }
            for condition_group in condition_counts
        }
        # print("transition_probs")
        # pprint(self.transition_probs)

        # Generate cumulative probabilities: [0.3, 0.3, 0.4] ~> [0.3, 0.6, 1.0]
        # This way, we can
        self.cumulative_probs = {
            condition_group: list(zip(
                [word for word in probs_by_word],
                it.accumulate(probs_by_word.values()),
            ))
            for condition_group, probs_by_word in self.transition_probs.items()
        }
        # print("cumulative_probs:")
        # print(self.cumulative_probs)

    def generate(self, length: int, start: Sequence[T]) -> list[T]:
        assert len(start) >= self.order, "Provide a longer start sequence"
        state = tuple(start[-self.order:])
        # print(f"starting state: {state}")
        result = []
        for i in range(length):
            # if state not in self.cumulative_probs:
            #     continue
            rand = random.random()
            # print(f"rand = {rand}")
            next_word: T | None = None
            for target, acc_prob in self.cumulative_probs[state]:
                # print(f"checking {(target, acc_prob)}")
                if rand < acc_prob:
                    next_word = target
                    break
            if next_word is not None:
                # print(f"transition to {next_word}")
                # Shift sliding window
                state = (*state[1:], next_word)
                result.append(next_word)
            else:
                raise ValueError("Did not find next word")
        return result

    def __str__(self):
        return repr(self.transition_probs)


if __name__ == "__main__":
    mc: MarkovChain[str] = MarkovChain(
        "AABABAABAAABABABAAA",
        # order=1,
        order=2,
    )
    print()
    print(mc)
    print(mc.generate(10, "BA"))
