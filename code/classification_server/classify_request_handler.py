__author__ = 'AlexF'

import json
from http.server import SimpleHTTPRequestHandler


class ClassifyRequestHandler(SimpleHTTPRequestHandler):
    @classmethod
    def create_request_handler(cls, cleaner, vectorizer, model):
        cls.cleaner = cleaner
        cls.vectorizer = vectorizer
        cls.model = model

        return cls

    def do_GET(self):
        print('I have a request!')
        try:
            raw_text = self.headers['text']
        except KeyError:
            self.send_response(404)
            return
        labels_n = self.headers.get('labels_n', None)

        tokens = self.cleaner.clean_text(raw_text)
        feature_vec = self.vectorizer.vectorize_text(tokens)
        prediction = self.model.predict(feature_vec, labels_n)

        self.send_response(200)
        self.send_header("prediction", json.dumps(prediction))
        self.end_headers()
