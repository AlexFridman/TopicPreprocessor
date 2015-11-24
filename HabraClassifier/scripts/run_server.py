__author__ = 'AlexF'

import json

import numpy as np
import sys
sys.path.append('D:/Study/Repos/HabraClassifier')
from HabraClassifier.code import MLNBModel, TopicCleaner, TopicVectorizer, ClassificationServer

path = 'D:/Study/Repos/HabraClassifier/HabraClassifier/'
with open(path + 'data/l_idx.json', 'r') as fp:
    label_idx = json.load(fp)
labels_idxs = np.load(path + 'data/labels.npy')
label_idx_inv = dict((v, k) for k, v in label_idx.items())
labels = np.array([label_idx_inv[l_i] for l_i in labels_idxs])
pi = np.load(path + 'data/pi.npy')
theta = np.load(path + 'data/theta.npy')


model = MLNBModel(labels=labels, pi=pi, theta=theta)

with open(path + 'data/w_idx.json', 'r') as fp:
    feature_idx = json.load(fp)

vectorizer = TopicVectorizer(feature_idx=feature_idx, label_idx=label_idx)
cleaner = TopicCleaner()
server = ClassificationServer(model=model, cleaner=cleaner, vectorizer=vectorizer)

server.run()
