# -*- coding: utf-8 -*-
__author__ = 'AlexF'

import json
from collections import Counter

from topic_parser import Topic
from topic_cleaner import TopicCleaner
from HabraClassifier.code import TopicDownloader
from topic_parser import TopicParser


class Pipeline:
    def __init__(self, in_stream):
        self._processors = []
        self._in_stream = in_stream

    def add_processor(self, processor):
        if callable(processor):
            self._processors.append(processor)

    def add_processors(self, processors):
        for processor in processors:
            self.add_processor(processor)

    def process(self):
        pipeline = self._in_stream
        for processor in self._processors:
            pipeline = processor(pipeline)
        return pipeline


def json_parser(lines):
    for line in lines:
        yield json.loads(line)


def dict_to_topic(docs):
    for doc in docs:
        yield Topic(text=doc['Text'], hubs=doc['Labels'], tags=[])


def cleaner(topics):
    topic_cleaner = TopicCleaner()
    for topic in topics:
        yield topic_cleaner.clean(topic)


word_count = Counter()
label_count = Counter()


def set_ext(topics):
    for topic in topics:
        word_count.update(topic.words)
        label_count.update(topic.labels)
        yield topic


def clean_topic_to_dict(topics):
    for topic in topics:
        yield {'Labels': topic.labels, 'Text': topic.words}


def json_dumper(objs):
    for obj in objs:
        yield json.dumps(obj) + '\n'


def progress_indicator(objs):
    i = 0
    for obj in objs:
        i += 1
        if i % 100 == 0:
            print(i)
        yield obj


if __name__ == '__main__':
    html = TopicDownloader.download_topic(269995)
    parsed = TopicParser().parse(html)
    pass
    # with open('data/raw_data.json', 'r') as in_file, open('data/clean_data.json', 'w+') as out_file:
    #     pipe_1 = Pipeline(in_file)
    #     pipe_1.add_processors(
    #         [json_parser,
    #          dict_to_topic,
    #          cleaner,
    #          set_ext,
    #          clean_topic_to_dict,
    #          json_dumper,
    #          progress_indicator])
    #     out_file.writelines(pipe_1.process())
    #
    # with open('data/word_count.json', 'w+') as fp:
    #     json.dump(word_count, fp)
    #
    # with open('data/label_count.json', 'w+') as fp:
    #     json.dump(label_count, fp)
