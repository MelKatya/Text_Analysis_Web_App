import re
import math
from typing import Dict, List


def get_count_words(reading_file: str) -> Dict[str, int]:
    """
    Рассчитывает сколько раз слово встречается в тексте.

    Args:
        reading_file [str]: анализируемый файл.
    Returns:
        Dict[str, int]: cловарь, где ключ - слово, а значение - количество его вхождений в тексте.
    """
    count_words = {}
    template = re.compile(r'\b[a-zA-Zа-яА-я]+[-\']?[a-zA-Zа-яА-я]*\b')

    with open(reading_file, 'r', encoding='utf-8') as file:
        for line in file:
            words_in_line = template.findall(line.lower())
            for word in words_in_line:
                count_words[word] = count_words.get(word, 0) + 1

    return count_words


def calculate_tf(count_words: Dict[str, int]) -> Dict[str, float]:
    """
    Рассчитывает tf слова.

    Args:
        count_words [Dict[str, int]]: словарь соответствия слова и количества вхождений.
    Returns:
        Dict[str, float]: cловарь, где ключ - слово, а значение - tf.
    """

    all_words = sum(count_words.values())
    tf_dict = {word: count / all_words for word, count in count_words.items()}

    return tf_dict


def calculate_idf(words_count: Dict[str, int], reading_file: str) -> Dict[str, float]:
    """
    Рассчитывает обратную частоту документа. В качестве документов взято количество предложений.

    Args:
        words_count (Dict[str, int]): словарь соответствия слова и количества вхождений.
        reading_file [str]: анализируемый файл.
    Returns:
        Dict[str, float]: cловарь, где ключ - слово, а значение - его обратная частота документа (IDF).
    """
    idf_dict = {}
    template = re.compile(r'[.!?]\s+')
    with open(reading_file, 'r', encoding='utf-8') as file:
        sentences = template.split(file.read().lower())

    count_sentences = len(sentences)

    for word in words_count:
        count_in_sent = sum(1 if re.search(rf'\b{word}\b', sent) else 0 for sent in sentences)

        idf_dict[word] = math.log(count_sentences / count_in_sent)

    return idf_dict


def combine_count_tf_idf(file_path: str) -> Dict[str, List[float]]:
    """
    Объединяет count, tf и idf в один список.

    Args:
        file_path [str]: анализируемый файл.
    Returns:
        Dict[str, List[float]]: словарь, где ключ — слово, а значение — список: [count, TF, IDF].
    """
    count_words = get_count_words(file_path)
    tf_dict = calculate_tf(count_words)
    idf_dict = calculate_idf(count_words, file_path)

    words_status = {word: [count_words[word], tf_dict[word], idf_dict[word]] for word in tf_dict}

    return words_status


def sort_words_by_idf(file_path: str) -> Dict[str, List[float]]:
    """
    Сортирует по убыванию IDF и возвращает топ-50 слов.

    Args:
        file_path [str]: анализируемый файл.
    Returns:
        Dict[str, List[float]]: отсортированный словарь.
    """
    words_data = combine_count_tf_idf(file_path)

    # word[1][2] - IDF
    sorted_dict = sorted(words_data.items(), key=lambda word: word[1][2], reverse=True)

    return dict(sorted_dict[:50])


