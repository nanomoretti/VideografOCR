# -*- coding: utf-8 -*-
"""
Compute distance between words
"""

from collections import defaultdict

def levenshtein(str1, str2):
    """
    Compute distance between str1 and str2 using Levenshtein algorithm
    https://es.wikipedia.org/wiki/Distancia_de_Levenshtein
    """

    distances = defaultdict(lambda: defaultdict(int))
    len1 = len(str1)
    len2 = len(str2)

    # initiate matrix
    for i in range(len1 + 1):
        distances[i][0] = i
    for i in range(len2 + 1):
        distances[0][i] = i

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = not str1[i - 1] == str2[j - 1]
            distances[i][j] = min(
                distances[i][j - 1] + 1,        # deletion
                distances[i - 1][j] + 1,        # insertion
                distances[i - 1][j - 1] + cost  # substitution
            )
    return distances[len1][len2]

