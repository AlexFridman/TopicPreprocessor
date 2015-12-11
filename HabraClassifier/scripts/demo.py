# -*- coding: utf-8 -*-
__author__ = 'AlexF'
from urllib import parse
import json
import os

from requests import request

from HabraClassifier.code import TopicDownloader, TopicParser, TopicCleaner, NotFoundError

parser = TopicParser()
cleaner = TopicCleaner()


def get_raw_point(topic_id: int) -> (list, list):
    topic_html = TopicDownloader.download_topic(topic_id)
    raw_topic = parser.parse(topic_html)
    labels = raw_topic.hubs + raw_topic.tags
    raw_text = raw_topic.text

    return raw_text, labels


def send_classify_request(uri: str, text: str, label_n: int):
    encode = str.encode(text)
    params = {'text': encode, 'label_n': label_n}
    data = parse.urlencode(params)
    return request('POST', uri, data=data)


while True:
    print('=' * 25)
    user_input = input('command: ')
    if user_input == 'exit':
        break

    try:
        topic_id = int(user_input)
    except ValueError:
        print('Incorrect id')
        continue

    try:
        raw_text, labels = get_raw_point(topic_id)
    except NotFoundError:
        print('Cannot download topic')
        continue

    try:
        resp = send_classify_request('http://localhost:8000', raw_text, 5)
        prediction = json.loads(resp.headers['prediction'])
    except Exception as e:
        print('Server is down')
        continue

    print('Actual labels: ', ', '.join(labels))
    print('Predicted labels: ', ', '.join(prediction))
