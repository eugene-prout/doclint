from enum import Enum
import math
import re


def count_letters(text: str):
    return sum(c.isalpha() for c in text)


def count_words(text: str):
    return len(text.split())


def count_sentences(text: str):
    return len(re.split(r"[.!?]", text))


def split_into_paragraphs(text: str) -> list[str]:
    return text.split("\n\n")


def split_into_sentences(text: str) -> list[str]:
    return re.split(r"[.!?]", text)


class Difficulty(Enum):
    NORMAL = "Normal"
    HARD = "Hard"
    VERY_HARD = "Very Hard"


def map_level_to_difficulty(level: int) -> Difficulty:
    if level < 10:
        return Difficulty.NORMAL
    elif 10 <= level < 14:
        return Difficulty.HARD
    else:
        return Difficulty.VERY_HARD


def rate_text(text: str) -> Difficulty:
    paragraphs = split_into_paragraphs(text)
    levels = [
        calculate_ARI(count_letters(p), count_words(p), count_sentences(p))
        for p in paragraphs
    ]
    difficulties = [map_level_to_difficulty(level) for level in levels]

    # return max difficulty in the list
    if Difficulty.VERY_HARD in difficulties:
        return Difficulty.VERY_HARD
    elif Difficulty.HARD in difficulties:
        return Difficulty.HARD
    else:
        return Difficulty.NORMAL


def calculate_ARI(letter_count: int, word_count: int, sentence_count: int):
    if word_count == 0 or sentence_count == 0:
        return 0

    average_word_length = letter_count / word_count
    average_sentence_length = word_count / sentence_count
    raw_level = 4.71 * average_word_length + 0.5 * average_sentence_length - 21.43
    rounded_level = int(math.ceil(raw_level))
    return max(rounded_level, 0)
