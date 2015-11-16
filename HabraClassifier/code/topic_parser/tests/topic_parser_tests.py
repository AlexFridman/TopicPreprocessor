# -*- coding: utf-8 -*-
__author__ = 'AlexF'
import unittest

from requests import request
from bs4 import BeautifulSoup

from HabraClassifier.code import TopicParser


class TopicParserTests(unittest.TestCase):
    def test_tags_extraction(self):
        html = request('GET', 'http://habrahabr.ru/post/269921/').text
        soup = BeautifulSoup(html)

        self.assertSequenceEqual(['кардинг',
                                  'информационная безопасность',
                                  'деанонимизация',
                                  'кредитные карты',
                                  'даркнет'],
                                 TopicParser.extract_tags(soup))

    def test_hubs_extraction(self):
        html = request('GET', 'http://habrahabr.ru/post/269921/').text
        soup = BeautifulSoup(html)

        self.assertSequenceEqual(['криптография',
                                  'информационная безопасность',
                                  'вирусы и антивирусы'],
                                 TopicParser.extract_hubs(soup))

    def test_text_extraction(self):
        html = request('GET', 'http://habrahabr.ru/post/269921/').text
        soup = BeautifulSoup(html)

        self.assertIn('В наше время развелось огромное множество «именитых»'
                      ' специалистов в области информационной безопасности, люди,'
                      ' считающие что знаний по настройке FireWall уже достаточно'
                      ' чтобы причислить себя к «хакерам» или спецам в области ИБ.',
                      TopicParser.extract_text(soup))


if __name__ == '__main__':
    unittest.main()
