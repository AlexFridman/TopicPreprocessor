__author__ = 'AlexF'
import json

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


while True:
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
        resp = request('GET', 'localhost:8000', headers={'text': raw_text})
        prediction = json.loads(resp.headers['prediction'])
    except:
        print('Server is down')
        continue

    print('Actual labels: ', ' ,'.join(labels))
    print('Predicted labels: ', ' ,'.join(prediction))
