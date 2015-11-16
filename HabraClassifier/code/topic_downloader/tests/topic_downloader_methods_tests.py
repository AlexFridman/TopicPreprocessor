# -*- coding: utf-8 -*-
__author__ = 'AlexF'

import unittest

from requests import request

from HabraClassifier.code import TopicDownloader


class TopicDownloaderMethodsTests(unittest.TestCase):
    def test_download_html(self):
        url = 'http://habrahabr.ru/interesting/'

        html = TopicDownloader.download_html(url)

        self.assertEqual(request('GET', url).text, html)

    def test_is_error_page(self):
        html_1 = request('GET', 'http://geektimes.ru/post/10000/').text
        html_2 = request('GET', 'http://habrahabr.ru/post/951000/').text

        self.assertTrue(TopicDownloader.is_error_page(html_1))
        self.assertTrue(TopicDownloader.is_error_page(html_2))


if __name__ == '__main__':
    unittest.main()
