"""
learning.randomforest
=======================================
This module use machine learning technique to learn to which cluster will belong the time-series
if it runs in a defined day at a defined hour.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn import metrics
from datetime import datetime
import logging


class RandomForest:
    """
    This class provide methods for learning, evaluating and predicting the cluster id of a time-series
    according the date-time it is running
    """
    def __init__(self, folder, fixture, n_clusters):
        """
        The class constructor.

        :param folder:  The folder containing the time-series.
        :param fixture: The name of the fixture, that is a prefix of the file containing the vectors of features-
        :param n_clusters: The number of clusters.
        """
        self.folder = folder
        self.filename = folder + '/' + fixture
        self.fixture = fixture
        self.n_cluster = n_clusters

    def compute_features(self, clusters):
        """
        This methods read the vector of features (datetime, duration, liters, maxflow) from the relateed file.
        It uses the date-time on which the time-series started to compute the hour of the day, the day of the month,
        the day of the week

        :param clusters: the list of cluster ids identified for the time-series to be analyzed.
        :return:
        """
        individuals = np.genfromtxt(self.filename+".individuals", delimiter=" ")
        delay = 0
        j = 2
        while clusters[-j] != clusters[-1] and len(clusters) - j > 0:
            delay += 1
            j += 1

        sequence_f = open(self.filename + ".sequence", "w")
        i = 0
        for j in range(len(individuals)-1):
            ind = individuals[j]
            start_time = ind[1]
            dt = datetime.fromtimestamp(start_time)
            day_week = dt.strftime("%w")
            day_month = dt.strftime("%d")
            hour = dt.strftime("%H")

            sequence_f.write(str(start_time) + "," + str(hour) + "," + str(day_week) + "," + str(day_month) + "," +
                             # str(ind[2]) + ',' + str(ind[3]) + ',' + str(ind[4]) + ',' +
                             str(clusters[i]) + "\n")
            i += 1
        sequence_f.close()

    def evaluate(self):
        """
        This method use The RandomForest algorithm to evaluate how works the learning and prediction of cluster id.
        :return:
        """
        dataset = np.genfromtxt(self.filename + ".sequence", delimiter=",")
        splitn = int(len(dataset) * 0.66)

        Y = []
        for i in range(0, len(dataset)):
            Y.append(chr(ord('a') + int(dataset[i, 4])))

        Y = dataset[:, 4]

        clf = RandomForestClassifier(n_estimators=10)
        clf = clf.fit(dataset[:splitn, 1:-1], Y[:splitn])

        labels = list(set(Y))
        labels.sort()

        pred = clf.predict(dataset[splitn:, 1:-1])
        pred = list(pred)

        temp1 = []
        temp2 = []

        logging.info(pred)
        logging.debug(Y[splitn:])
        logging.debug(labels)
        '''
        for i in range(0,len(pred)):
            temp1.append(ord(pred[i])-ord('a'))
            temp2.append(ord(Y[splitn+i]) - ord('a'))

        print(metrics.classification_report(temp2, temp1))

        print metrics.accuracy_score(temp2, temp1)
        print metrics.precision_score(temp2, temp1)
        print metrics.recall_score(temp2, temp1)
        '''
        print(metrics.accuracy_score(Y[splitn:], pred))
        # print(metrics.precision_score(np.array(Y[splitn:]), np.array(pred)))
        # print metrics.recall_score(Y[splitn:], pred)

        print(metrics.classification_report(Y[splitn:], pred))

    def learn(self, data_dir):
        """
        This methods learns how the cluster id depends on the following parameters of the time-series:
        hour, day_week, day_month
        :param data_dir: the folder where the learned model must be serialized
        :return: None
        """
        dataset = np.genfromtxt(self.filename + ".sequence", delimiter=",")
        splitn = int(len(dataset) * 0.66)

        Y = []
        for i in range(0, len(dataset)):
            Y.append(chr(ord('a') + int(dataset[i, 4])))

        Y = dataset[:, 4]

        clf = RandomForestClassifier(n_estimators=10)
        temp_ds = dataset[:, 1:-1]
        clf = clf.fit(dataset[:, 1:-1], Y)
        joblib.dump(clf, data_dir+'/model.pkl')

    @staticmethod
    def predict(model_file, file_items):
        """
        This methods loads the model_file
        :param model_file: the filename where the previous learning phase saved the odel.
        :param file_items: the vectors of features of the time-series whose cluster must be predicted.
        :return:
        """
        clf = joblib.load(model_file)
        dataset = np.genfromtxt(file_items, delimiter=",")
        temp_ds = dataset[:, 1:]
        result = clf.predict(temp_ds)
        return result

