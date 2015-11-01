# -*- coding: utf-8 -*-
__author__ = 'AlexF'

import re
from collections import namedtuple

CleanTopic = namedtuple('CleanTopic', ['labels', 'words'])

from nltk.tokenize import regexp_tokenize
from snowballstemmer import RussianStemmer, EnglishStemmer
from nltk.corpus import stopwords

from topic_parser import Topic


class TopicCleaner:
    def __init__(self):
        self._russian_stemmer = RussianStemmer()
        self._english_stemmer = EnglishStemmer()
        self._russian_stops = stopwords.words('russian')
        self._english_stops = stopwords.words('english')
        self._label_bl = {'блог компании', 'черная дыра', 'я пиарюсь'}

    def clean(self, topic: Topic) -> CleanTopic:
        text = self.clean_text(topic.text)
        labels = self.clean_labels(topic.tags + topic.hubs)

        return CleanTopic(labels=labels, words=text)

    def clean_text(self, text: str) -> list:
        text = text.lower()
        text = TopicCleaner.delete_non_word_chars(text)
        tokens = TopicCleaner.tokenize_text(text)
        tokens = TopicCleaner.filter_variable_names(tokens)
        tokens = self.filter_stopwords(tokens)
        tokens = self.stemm_text(tokens)
        tokens = TopicCleaner.filter_words_with_repeatable_letters(tokens)
        tokens = TopicCleaner.filter_words_with_unusual_for_language_length(tokens)

        return tokens

    def clean_labels(self, labels: list) -> list:
        return [self.clean_label(label) for label in self.filter_bl_labels(labels)]

    def clean_label(self, label: str) -> str:
        label = label.lower()
        label = label.replace('ё', 'е')
        label_words = TopicCleaner.tokenize_text(label)
        label_words = self.stemm_text(label_words)
        return ' '.join(label_words)

    def filter_bl_labels(self, labels: list) -> list:
        return set(labels) - self._label_bl

    @staticmethod
    def tokenize_text(text: str) -> list:
        return regexp_tokenize(text, '[\\w\']+')

    def stemm_text(self, text: list) -> list:
        stemmed = self._english_stemmer.stemWords(text)
        return self._russian_stemmer.stemWords(stemmed)

    def filter_stopwords(self, text: list) -> list:
        return [word for word in text
                if word not in self._russian_stops
                and word not in self._english_stops]

    @staticmethod
    def filter_words_with_repeatable_letters(text: list) -> list:
        return [word for word in text if not re.match('(.)\\1{2}', word)]

    @staticmethod
    def filter_words_with_unusual_for_language_length(text: list) -> list:
        return [word for word in text
                if TopicCleaner.is_language_usual_word(word)]

    @staticmethod
    def is_language_usual_word(word: str) -> bool:
        length = len(word)
        is_eng = re.match('[a-z]', word)
        return length > 2 and ((not is_eng and length < 25)
                               or (is_eng and length < 15))

    @staticmethod
    def filter_variable_names(text: list) -> list:
        return [word for word in text if '_' not in word]

    @staticmethod
    def delete_non_word_chars(text: str):
        temp = text.replace('ё', 'е')
        temp = re.sub(r'(&[a-z0-9]*;)', ' ', temp)  # & encoded symbols
        temp = re.sub(r'(\W|\d)+', ' ', temp)  # non word or digit
        temp = re.sub(r'\s+', ' ', temp)  # 2+ spaces
        return temp.strip()
