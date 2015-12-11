# -*- coding: utf-8 -*-
__author__ = 'AlexF'

from collections import namedtuple

from bs4 import BeautifulSoup

Topic = namedtuple('Topic', ['text', 'hubs', 'tags', 'name'])


class TopicParser:
    @staticmethod
    def parse(html: str) -> Topic:
        soup = BeautifulSoup(html)
        tags = TopicParser.extract_tags(soup)
        hubs = TopicParser.extract_hubs(soup)
        text = TopicParser.extract_text(soup)
        name = TopicParser.extract_name(soup)

        return Topic(text=text, hubs=hubs, tags=tags, name=name)

    @staticmethod
    def extract_tags(soup: BeautifulSoup) -> list:
        tag_tags = soup.findAll(name='a', attrs={'rel': 'tag'})
        return [tag_tag.get_text().lower() for tag_tag in tag_tags]

    @staticmethod
    def extract_name(soup: BeautifulSoup) -> list:
        tag_tags = soup.find(name='span', attrs={'class': 'post_title'})
        return tag_tags.get_text()

    @staticmethod
    def extract_hubs(soup: BeautifulSoup) -> list:
        hub_tags = soup.findAll(name='a', attrs={'class': 'hub'})
        return [hub_tag.get_text().lower() for hub_tag in hub_tags]

    @staticmethod
    def extract_text(soup: BeautifulSoup) -> str:
        text_tag = soup.find(name='div', attrs={'class': 'content html_format'})
        return text_tag.get_text()
