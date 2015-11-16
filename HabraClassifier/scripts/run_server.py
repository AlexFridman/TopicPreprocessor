__author__ = 'AlexF'

import numpy as np

from HabraClassifier import MLNBModel, TopicCleaner, TopicVectorizer, ClassificationServer

# with open('', 'r') as fp:
#     labels = json.load(fp)
# pi = np.load('')
# theta = np.load('')
# with open('', 'r') as fp:
#     feature_idx = json.load(fp)
# with open('', 'r') as fp:
#     label_idx = json.load(fp)

model = MLNBModel(labels=np.array([]), pi=np.array([]), theta=np.array([]))
vectorizer = TopicVectorizer(feature_idx={}, label_idx={})
cleaner = TopicCleaner()
server = ClassificationServer(model=model, cleaner=cleaner, vectorizer=vectorizer)

server.run()
