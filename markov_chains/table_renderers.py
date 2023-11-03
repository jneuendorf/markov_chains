import re
import string
from typing import Sequence, TypeVar, Iterable

from markov_chains.common import HashableSortable

T = TypeVar("T", bound=HashableSortable)


def markdown(
    alphabet: Sequence[T],
    transition_probs: dict[tuple[T, ...], dict[T, float]],
) -> str:
    longest_condition_length = max([
        len(str(condition))
        for condition in transition_probs
    ])
    header_row = f"{' ' * (longest_condition_length + 2)} | {' | '.join([
        # use repr() for non-printable and whitespace characters
        ''.join([
            char
            if (
                char in string.digits + string.ascii_letters + string.punctuation 
                and char != "|"
            )
            else repr(char)
            for char in str(word)
        ]).center(4)
        for word in alphabet
    ])} |"
    col_positions = [0] + [match.start() for match in re.finditer(r"[|]", header_row)]

    lines = [
        f"{header_row}",
        f"{''.join([
            '|' if i in col_positions else '-'
            for i in range(len(header_row))
        ])}",
    ]
    for condition, probs_by_word in transition_probs.items():
        lines += [
            f"| {str(condition)} | {' | '.join([
                '{:4.2f}'.format(prob) 
                for prob in probs_by_word.values()
            ])} |"
        ]
    return "\n".join(lines)
