__author__ = 'admin-pc'

from http.server import HTTPServer

from .classify_request_handler import ClassifyRequestHandler


class ClassificationServer:
    def __init__(self, model, cleaner, vectorizer):
        self.model = model
        self.cleaner = cleaner
        self.vectorizer = vectorizer

    def run(self, server_address=('', 8000)):
        httpd = HTTPServer(server_address, ClassifyRequestHandler.create_request_handler(
            self.cleaner, self.vectorizer, self.model
        ))
        httpd.serve_forever()
