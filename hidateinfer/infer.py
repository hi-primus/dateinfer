"""
This file contains some modification aimed at fixing bugs and improving the dateinfer library.
The newlines/modification line are preceded with comments indicating the purpose.
"""

import collections
import itertools
import string

from hidateinfer.date_elements import (
    AMPM,
    DayOfMonth,
    Filler,
    Hour12,
    Hour24,
    Minute,
    MonthNum,
    MonthTextLong,
    MonthTextShort,
    Second,
    Timezone,
    UTCOffset,
    WeekdayLong,
    WeekdayShort,
    Year2,
    Year4,
)
from hidateinfer.ruleproc import (
    And,
    Contains,
    Duplicate,
    If,
    KeepOriginal,
    Sequence,
    Swap,
    SwapDuplicateWhereSequenceNot,
    SwapSequence,
)

# DATE_ELEMENTS is an ordered sequence of date elements, excluding the filler. It is ordered
# in descending "restrictivity".
# The order is a little loose since date element domains do not necessarily overlap (e.g., the
# range of Jan .. Dec is 12, but the domain is independent of hours 0 .. 23), but overall a lesser
# value should be preferred over a greater value.
# The RULES will be applied after the list is generated following these precedence rules.
DATE_ELEMENTS = (
    AMPM(),
    MonthNum(),
    Hour12(),
    Hour24(),
    DayOfMonth(),
    Minute(),
    Second(),
    Year2(),
    Year4(),
    UTCOffset(),
    MonthTextShort(),
    MonthTextLong(),
    WeekdayShort(),
    WeekdayLong(),
    Timezone(),
)

F = Filler  # short-hand to clarify rules
RULES = [
    If(Sequence(Year4, Year2), SwapSequence([Year4, Year2], [Year4, MonthNum])),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), Year4),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), Year4],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year4],
        ),
    ),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), Hour24),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), Hour24],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("-"), r"\d", F("-"), Hour24),
        SwapSequence(
            [MonthNum, F("-"), r"\d", F("-"), Hour24],
            [MonthNum, F("-"), DayOfMonth, F("-"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("/"), r"\d", F("/"), MonthNum),
        SwapSequence(
            [MonthNum, F("/"), r"\d", F("/"), MonthNum],
            [MonthNum, F("/"), DayOfMonth, F("/"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F("-"), r"\d", F("-"), MonthNum),
        SwapSequence(
            [MonthNum, F("-"), r"\d", F("-"), MonthNum],
            [MonthNum, F("-"), DayOfMonth, F("-"), Year2],
        ),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d", F(":"), r"\d"),
        SwapSequence(
            [MonthNum, F(":"), r"\d", F(":"), r"\d"],
            [Hour12, F(":"), Minute, F(":"), Second],
        ),
    ),
    If(
        Sequence(Hour24, F(":"), r"\d", F(":"), r"\d"),
        SwapSequence(
            [Hour24, F(":"), r"\d", F(":"), r"\d"],
            [Hour24, F(":"), Minute, F(":"), Second],
        ),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d", r"\D"),
        SwapSequence([MonthNum, F(":"), "."], [Hour12, F(":"), Minute]),
    ),
    If(
        Sequence(Hour24, F(":"), r"\d", r"\D"),
        SwapSequence([Hour24, F(":"), r"\d"], [Hour24, F(":"), Minute]),
    ),
    If(
        Sequence(MonthNum, F(":"), r"\d"),
        SwapSequence([MonthNum, F(":"), "."], [Hour24, F(":"), Minute]),
    ),
    If(
        And(Sequence(Hour12, F(":"), Minute), Contains(Hour24)),
        Swap(Hour24, DayOfMonth),
    ),
    If(
        And(Sequence(Hour12, F(":"), Minute), Duplicate(Hour12)),
        SwapDuplicateWhereSequenceNot(Hour12, MonthNum, (Hour12, F(":"))),
    ),
    If(
        And(Sequence(Hour24, F(":"), Minute), Duplicate(Hour24)),
        SwapDuplicateWhereSequenceNot(Hour24, DayOfMonth, [Hour24, F(":")]),
    ),
    If(Contains(MonthNum, MonthTextLong), Swap(MonthNum, DayOfMonth)),
    If(Contains(MonthNum, MonthTextShort), Swap(MonthNum, DayOfMonth)),
    If(
        Sequence(MonthNum, ".", Hour12),
        SwapSequence([MonthNum, ".", Hour12], [MonthNum, KeepOriginal, DayOfMonth]),
    ),
    If(
        Sequence(MonthNum, ".", Hour24),
        SwapSequence([MonthNum, ".", Hour24], [MonthNum, KeepOriginal, DayOfMonth]),
    ),
    If(
        Sequence(Hour12, ".", MonthNum),
        SwapSequence([Hour12, ".", MonthNum], [DayOfMonth, KeepOriginal, MonthNum]),
    ),
    If(
        Sequence(Hour24, ".", MonthNum),
        SwapSequence([Hour24, ".", MonthNum], [DayOfMonth, KeepOriginal, MonthNum]),
    ),
    If(Duplicate(MonthNum), Swap(MonthNum, DayOfMonth)),
    If(Sequence(F("+"), Year4), SwapSequence([F("+"), Year4], [UTCOffset, None])),
    If(
        Sequence(Second, F("-"), Year4),
        SwapSequence([Second, F("-"), Year4], [Second, UTCOffset, None]),
    ),
    If(
        Sequence(Minute, F("-"), Year4),
        SwapSequence([Minute, F("-"), Year4], [Minute, UTCOffset, None]),
    ),
    If(
        Sequence(Hour24, ".", r"\D"),
        SwapSequence([Hour24, ".", r"\D"], [DayOfMonth, KeepOriginal, KeepOriginal]),
    ),
    If(
        Sequence(DayOfMonth, ".", MonthNum, ".", DayOfMonth),
        SwapSequence(
            [DayOfMonth, ".", MonthNum, ".", DayOfMonth],
            [DayOfMonth, KeepOriginal, MonthNum, KeepOriginal, Year2],
        ),
    ),
    If(
        And(Duplicate(Minute), Contains(Hour24)),
        SwapDuplicateWhereSequenceNot(Minute, Second, [Minute]),
    ),
    If(And(Duplicate(DayOfMonth), Contains(MonthNum)), Swap(MonthNum, Year2)),
    If(
        Duplicate(DayOfMonth),
        SwapDuplicateWhereSequenceNot(DayOfMonth, MonthNum, [DayOfMonth]),
    ),
]


_alt_directives = {'%z': '%Y',
                   '%Y': '%z'}


def infer(examples, alt_rules=None):
    """
    Returns a datetime.strptime-compliant format string for parsing the *most likely* date format
    used in examples. examples is a list containing example date strings.
    """
    date_classes = _tag_most_likely(examples)

    if alt_rules:
        date_classes = _apply_rewrites(date_classes, alt_rules)
    else:
        date_classes = _apply_rewrites(date_classes, RULES)

    date_string = ""
    directives = []
    for date_class in date_classes:
        directive = date_class.directive
        if '%' in directive:
            if directive in directives:
                directive = _alt_directives.get(directive, directive)
            if directive in directives:
                continue
        directives.append(directive)
        date_string += directive

    return date_string


def _apply_rewrites(date_classes, rules):
    """
    Return a list of date elements by applying rewrites to the initial date element list
    """
    for rule in rules:
        date_classes = rule.execute(date_classes)

    return date_classes


def _mode(elems):
    """
    Find the mode (most common element) in list elems. If there are ties, this function returns the
    least value.

    If elems is an empty list, returns None.
    """
    if not elems:
        return None

    c = collections.Counter()
    c.update(elems)

    most_common = c.most_common(1)
    most_common.sort()
    return most_common[0][
        0
    ]  # most_common[0] is a tuple of key and count; no need for the count


def _most_restrictive(date_elems):
    """
    Return the date_elem that has the most restrictive range from date_elems
    """
    most_index = len(DATE_ELEMENTS)
    for date_elem in date_elems:
        if date_elem in DATE_ELEMENTS and DATE_ELEMENTS.index(date_elem) < most_index:
            most_index = DATE_ELEMENTS.index(date_elem)
    if most_index < len(DATE_ELEMENTS):
        return DATE_ELEMENTS[most_index]

    raise KeyError("No least restrictive date element found")


def _percent_match(date_classes, tokens):
    """
    For each date class, return the percentage of tokens that the class matched (floating point
    [0.0 - 1.0]).

    The returned value is a tuple of length patterns. Tokens should be a list.
    """
    match_count = [0] * len(date_classes)

    for i, date_class in enumerate(date_classes):
        for token in tokens:
            if date_class.is_match(token):
                match_count[i] += 1

    percentages = tuple([float(m) / len(tokens) for m in match_count])
    return percentages


def _tag_most_likely(examples):
    """
    Return a list of date elements by choosing the most likely element for a token within examples
    (context-free).
    """
    tokenized_examples = [_tokenize_by_character_class(example) for example in examples]

    # We currently need the tokenized_examples to all have the same length, so drop instances that
    # have a length that does not equal the mode of lengths within tokenized_examples
    token_lengths = [len(e) for e in tokenized_examples]
    token_lengths_mode = _mode(token_lengths)
    tokenized_examples = [
        example for example in tokenized_examples if len(example) == token_lengths_mode
    ]

    # Now, we iterate through the tokens, assigning date elements based on their likelihood.
    # In cases where the assignments are unlikely for all date elements, assign filler.
    most_likely = []
    for token_index in range(0, token_lengths_mode):
        tokens = [token[token_index] for token in tokenized_examples]
        probabilities = _percent_match(DATE_ELEMENTS, tokens)
        max_prob = max(probabilities)
        if max_prob < 0.5:
            most_likely.append(Filler(_mode(tokens)))
        else:
            if probabilities.count(max_prob) == 1:
                most_likely.append(DATE_ELEMENTS[probabilities.index(max_prob)])
            else:
                choices = []
                for index, prob in enumerate(probabilities):
                    if prob == max_prob:
                        choices.append(DATE_ELEMENTS[index])
                most_likely.append(_most_restrictive(choices))

    return most_likely


def _tokenize_by_character_class(s):
    """
    Return a list of strings by splitting s (tokenizing) by character class.

    For example:
    _tokenize_by_character_class('Sat Jan 11 19:54:52 MST 2014') =>
        ['Sat', ' ', 'Jan', ' ', '11', ' ', '19', ':', '54', ':', '52', ' ', 'MST', ' ', '2014']

    _tokenize_by_character_class('2013-08-14') => ['2013', '-', '08', '-', '14']
    """
    # Callables per character class. Return True/False depending on whether the character is in the
    # respective class.
    character_classes = [
        lambda x: x.isdigit(),
        lambda x: x.isalpha(),
        lambda x: x in string.punctuation,
        lambda x: x.isspace(),
    ]

    result = []
    rest = list(s)
    while rest:
        progress = False
        for part_of_class in character_classes:
            if part_of_class(rest[0]):
                progress = True
                token = ""
                for take_away in itertools.takewhile(part_of_class, rest[:]):
                    token += take_away
                    rest.pop(0)
                result.append(token)
                break
        if (
            not progress
        ):  # none of the character classes matched; unprintable character?
            result.append(rest[0])
            rest = rest[1:]

    return result
