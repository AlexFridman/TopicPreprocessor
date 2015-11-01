__author__ = 'AlexF'

from collections import Counter, namedtuple

import numpy as np

from topic_cleaner import CleanTopic

VectTopic = namedtuple('VectTopic', ['labels', 'feature_vect'])


class TopicVectorizer:
    def __init__(self, feature_idx: dict, label_idx: dict):
        self._feature_idx = feature_idx
        self._label_idx = label_idx
        self._feature_num = len(feature_idx)

    def vectorize(self, topic: CleanTopic) -> VectTopic:
        feature_vect = self.vectorize_text(topic.words)
        labels = self.vectorize_labels(topic.labels)

        return VectTopic(labels=labels, feature_vect=feature_vect)

    def vectorize_text(self, text: list) -> np.ndarray:
        words = self.filter_features(text)
        word_count = Counter(words)
        not_null_idxs = [self._feature_idx[w] for w, c in word_count.items()]
        feature_values = word_count.values()

        feature_vector = np.zeros(self._feature_num)
        feature_vector[not_null_idxs] = feature_values

        return feature_vector

    def filter_features(self, features: list) -> list:
        return [f for f in features if f in self._feature_idx]

    def vectorize_labels(self, labels: list) -> list:
        return [self._label_idx[l] for l in self.filter_labels(labels)]

    def filter_labels(self, labels: list) -> list:
        return [l for l in labels if l in self._label_idx]
