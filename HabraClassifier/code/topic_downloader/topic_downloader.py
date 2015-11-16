# -*- coding: utf-8 -*-
__author__ = 'AlexF'

from requests import request

from .not_found_error import NotFoundError


class TopicDownloader:
    @staticmethod
    def download_topic(topic_id: int) -> str:
        assert isinstance(topic_id, int)

        url = 'http://habrahabr.ru/post/{}/'.format(topic_id)
        html = TopicDownloader.download_html(url)

        if TopicDownloader.is_error_page(html):
            raise NotFoundError(url)

        return html

    @staticmethod
    def download_html(url: str) -> str:
        assert isinstance(url, str)

        response = request('GET', url)

        if response.status_code == 404:
            raise NotFoundError(url)

        data = response.text

        return data

    @staticmethod
    def is_error_page(html: str) -> bool:
        not_found_marker = 'Хабрахабр &#8212; страница не найдена (404)'
        blocked_marker = 'публикация скрыта в черновики (самим автором или НЛО)'

        return not_found_marker in html or blocked_marker in html


if __name__ == '__main__':
    pass
