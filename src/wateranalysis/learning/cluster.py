"""
learning.cluster
=======================================
This module compute the k-means clustering of time-series reperesented as an array of features
"""

import matplotlib.pylab as plt
import os
from sklearn import mixture
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
from sklearn import cluster
import joblib
import shutil
import glob
import pandas as pd


class TSCluster:
    """
    This class implements the k-means clustering of a set of time-series represented as an array of featuers
    """
    def __init__(self, folder, filename, runs):
        """
        This is the class constructor.
        :param folder: the  folder containing the csv files of time-series
        :param filename: the fixture name, that is the prefix of filename
                         containing the vectors of features corresponding to each time-series
        :param runs: the number of time-series to use for clustering
        """
        self.data_dir = folder
        self.n_series = runs
        self.filename = filename

    def meanshift(self, testset):
        """
        Compute clustering with MeanShift
        :param testset:
        :return:
        """
        bandwidth = estimate_bandwidth(testset, quantile=0.8, n_samples=len(testset))

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(testset)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        print("number of estimated clusters : %d" % n_clusters_)

    def find_k1(self, testset):
        """
        This method compute the best number of clusters from the testest list of vectors
        :param testset: the vectors of features
        :return: the number of clusters
        """
        lowest_bic = np.infty
        bic = []
        n_components_range = range(1, 4)

        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            # gmm = mixture.GMM(n_components=n_components)
            gmm = mixture.GaussianMixture(n_components=n_components)
            gmm.fit(testset)
            bic.append(gmm.bic(testset))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
                best_n = n_components
        return best_n

    def compute_statistics(testset):
        pass

    def get_testset(self):
        """
        This returns the vectors of features normalizing each parameter
        :return: the normalized vectors of features.
        """
        individuals = np.genfromtxt(self.data_dir + '/' + self.filename + ".individuals", delimiter=' ')
        individuals = np.delete(individuals, 0, 0)
        testset = individuals[:, 2:]

        # Normalization
        maxduration = np.max(testset[:, 0])
        testset[:, 0] = testset[:, 0] / maxduration

        max_liters = np.max(testset[:, 1])
        testset[:, 1] = testset[:, 1] / max_liters
        maxpower = np.max(testset[:, 2])
        testset[:, 2] = testset[:, 2] / maxpower
        return testset

    def predict(self, file_model,testset):
        model = joblib.load(file_model)
        return model.predict(testset)['start', 'duration', 'liters', 'month', 'hour', 'day', 'max_flow']

    @staticmethod
    def plot_clusters(testset, clusters, axis=[0, 1]):
        """
        This method plots the clusters along two dimension
        :param testset: the vectors of features
        :param clusters: the cluster id of the corresponding vector
        :param axis: the features to be used a plot dimensions
        :return: plt
        """
        plt.scatter(testset[:, axis[0]], testset[:, axis[1]], c=clusters)
        return plt

    def extract_features(self, parameters=[]):
        """
        This methods projects the vectors of features contained in the [fixture]_usage.csv file of features,
        saving the result into the [fixture].individuals file
        :param parameters: the list of parameter names
        :return: None
        """
        features = pd.read_csv(self.data_dir + '/' + self.filename + '_usage.csv', sep=' ', header=None,
                               names=['start', 'duration', 'liters', 'month', 'hour', 'day', 'max_flow'])
        features = features[parameters]
        features.to_csv(self.data_dir + '/' + self.filename + '.individuals', header=None, sep=' ', index=True)

    def compute_clusters(self, testset):
        """
        This method compute the clustering of the time-series. It creates one sub-folder per cluster and
        copies the corresponding time-series there.
        :param testset: the vectors of featuers
        :return: the number of clusters, the array of cluster id.
        """

        cluster_dirs = glob.glob(self.data_dir + '/cluster_*')
        for cluster_dir in cluster_dirs:
            if os.path.isdir(cluster_dir):
                shutil.rmtree(cluster_dir)

        # optimal number of clusters
        k1 = self.find_k1(testset)

        # compute clusters with KMeans
        ml_obj = cluster.KMeans(n_clusters=k1)
        clusters = ml_obj.fit_predict(testset)
        return k1, clusters

    def mk_cluster_folders(self, k1, clusters, n_ts=-1):
        individuals = np.genfromtxt(self.data_dir + '/' + self.filename + ".individuals", delimiter=' ')
        if n_ts == -1:
            n_ts = self.n_series
        selections = []

        for i in range(0,k1):
            os.mkdir(self.data_dir+"/cluster_"+str(i))
            selections.append(n_ts)

        for i in range(0, len(clusters)):
            if selections[clusters[i]] > 0:
                selections[clusters[i]] -= 1
                shutil.copyfile(self.data_dir+"/splits/"+str(int(individuals[i][0]))+".csv",
                                self.data_dir+"/cluster_" + str(clusters[i])+"/"+str(i)+".csv")
            if np.sum(selections) == 0:
                break



