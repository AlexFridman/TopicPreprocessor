__author__ = 'AlexF'

import json
import cgi
from base64 import decodebytes
from http.server import SimpleHTTPRequestHandler


class ClassifyRequestHandler(SimpleHTTPRequestHandler):
    @classmethod
    def create_request_handler(cls, cleaner, vectorizer, model):
        cls.cleaner = cleaner
        cls.vectorizer = vectorizer
        cls.model = model

        return cls

    def do_GET(self):
        try:
            # raw_text = json.loads(self.headers['text'])
            path = self.headers['path']
            with open(path, 'r') as fp:
                raw_text = fp.read()

        except KeyError:
            self.send_response(404)
            return

        labels_n = self.headers.get('labels_n', None)

        tokens = self.cleaner.clean_text(raw_text)
        feature_vec = self.vectorizer.vectorize_text(tokens)
        prediction = self.model.predict(feature_vec, labels_n)
        # predicted_labels = [l for l,w in prediction[:10]]
        self.send_response(200)
        self.send_header('prediction', json.dumps(prediction))
        # self.send_header('prediction', json.dumps(predicted_labels))
        self.end_headers()

    def do_POST(self):
        data = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        text = data['text'].value
        if 'label_n' in data:
            label_n = int(data['label_n'].value)
        else:
            label_n = None

        tokens = self.cleaner.clean_text(text)
        feature_vec = self.vectorizer.vectorize_text(tokens)
        prediction = self.model.predict(feature_vec, label_n)
        self.send_response(200)
        self.send_header('prediction', json.dumps(list(prediction)))
        self.end_headers()
