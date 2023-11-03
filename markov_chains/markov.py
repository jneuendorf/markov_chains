import itertools as it
import os
import pickle
import random
from collections import defaultdict
from typing import Sequence, TypeVar, Generic, Literal, Self

from markov_chains.common import HashableSortable
from markov_chains.table_renderers import markdown

T = TypeVar("T", bound=HashableSortable)


class MarkovChain(Generic[T]):
    alphabet: tuple[T, ...]
    order: int
    transition_probs: dict[tuple[T, ...], dict[T, float]]
    cumulative_probs: dict[tuple[T, ...], tuple[tuple[T, float], ...]]

    def __init__(self, alphabet: Sequence[T], order: int, transition_probs: dict[tuple[T, ...], dict[T, float]]):
        assert order >= 0, f"Order must be positive"

        self.alphabet = tuple(sorted(set(alphabet)))
        self.order = order
        self.transition_probs = transition_probs

        # Calculate cumulative probabilities:
        #   [0.3, 0.3, 0.4] ~> [0.3, 0.6, 1.0]
        # This way, we can more easily pick the next word randomly
        # by using a random number in [0..1].
        self.cumulative_probs = {
            condition_group: tuple(zip(
                [word for word in probs_by_word],
                it.accumulate(probs_by_word.values()),
            ))
            for condition_group, probs_by_word in self.transition_probs.items()
        }

    @classmethod
    def from_data(cls, words: Sequence[T], order: int = 1) -> Self:
        alphabet = tuple(sorted(set(words)))
        group_counts: dict[tuple[T, ...], int] = defaultdict(int)
        condition_counts: dict[tuple[T, ...], int] = defaultdict(int)
        group_size = order + 1

        word_group: tuple[T, ...]
        for i in range(len(words)):
            word_group = tuple(words[i:i + group_size])
            # End reached
            if len(word_group) < group_size:
                break

            condition_group = word_group[:-1]
            group_counts[word_group] += 1
            condition_counts[condition_group] += 1

        # print(
        #     f"Stats:\n"
        #     f"  #words: {len(words)}\n"
        #     f"  #distinct words: {len(alphabet)}\n"
        #     f"  #distinct word groups: {len(group_counts)}\n"
        # )
        transition_probs = {
            condition_group: {
                word: group_counts[(*condition_group, word)] / condition_counts[condition_group]
                for word in alphabet
            }
            for condition_group in condition_counts
        }
        return cls(
            alphabet=alphabet,
            order=order,
            transition_probs=transition_probs,
        )

    @classmethod
    def from_file(cls, filename: str | os.PathLike) -> Self:
        with open(filename, mode="rb") as file:
            data = pickle.load(file)
        return cls(
            alphabet=data["alphabet"],
            order=data["order"],
            transition_probs=data["transition_probs"],
        )

    def save(self, filename: str | os.PathLike) -> None:
        with open(filename, mode="wb") as file:
            pickle.dump(
                dict(
                    alphabet=self.alphabet,
                    order=self.order,
                    transition_probs=self.transition_probs,
                ),
                file,
            )

    def generate(self, length: int, start: Sequence[T]) -> list[T]:
        assert len(start) >= self.order, "Provide a longer start sequence"
        state = tuple(start[-self.order:])
        result = []
        for i in range(length):
            if state not in self.cumulative_probs:
                raise NotImplementedError("TODO")

            rand = random.random()
            next_word: T | None = None
            for target, acc_prob in self.cumulative_probs[state]:
                if rand < acc_prob:
                    next_word = target
                    break
            if next_word is not None:
                # Shift sliding window
                state = (*state[1:], next_word)
                result.append(next_word)
            else:
                raise ValueError("Did not find next word")
        return result

    def render_transition_table(self, fmt: Literal["markdown", "latex", "typst"] = "markdown") -> str:
        if fmt == "markdown":
            return markdown(self.alphabet, self.transition_probs)
        else:
            raise NotImplementedError("Currently only markdown format is supported")
