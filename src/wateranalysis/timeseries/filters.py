"""
filters
=======================================
This module filters from a set of time-series overlays, whose features do not comply with some parameters
"""
import numpy as np
import glob
import os
import logging
import shutil


class TSFilter:
    """
    This class provide stati methods to filter overlays in a set of time-series
    """
    @staticmethod
    def liters(ts):
        """

        :param ts: the time series of water flow samples [ml/s]
        :return: the total amount of liters
        """
        total_lits = 0
        for i in range(1, len(ts)):
            total_lits += ts[i, 1] * (ts[i, 0]-ts[i-1, 0])
        return total_lits

    @staticmethod
    def outlayers(ts_dir, min_dur_const=0, min_lit_const=0, min_samp_const=1, sep=' '):
        """
        This method scan the csv files in a directory and identifies time series whose features to dont comply
        with provided constraints
        :param ts_dir:  the folder with csv fiels
        :param min_dur_const: the minimal duration of time-sereis
        :param min_lit_const: the minimum amount of liters of time-series
        :param min_samp_const: the minimum number of samples pf a times-series
        :param sep: the character used as separator in the csv file
        :return: the method returns a dictionary that for each constraint  lists the basename of csv file which
        violate the constraints
        """
        ts_files = glob.glob(ts_dir + '/splits/*.csv')
        parameters = {}
        durations = []
        all_liters = []
        parameters["i_min_duration"] = []
        parameters["i_min_liters"] = []
        parameters["i_min_samples"] = []
        for i in range(len(ts_files)):
            ts_file = ts_files[i]
            ts = np.genfromtxt(ts_file, delimiter=sep)
            duration = ts[-1, 0] - ts[0, 0]
            lits = TSFilter.liters(ts)
            durations.append(duration)
            all_liters.append(lits)
            fname = int(os.path.basename(ts_file)[:-4])
            if duration < min_dur_const:
                parameters["i_min_duration"].append(fname)
            if lits < min_lit_const:
                parameters["i_min_liters"].append(fname)
            if len(ts) <= min_samp_const:
                parameters["i_min_samples"].append(fname)

        parameters["min_duration"] = np.min(durations)
        parameters["min_liters"] = np.min(all_liters)

        return parameters

    @staticmethod
    def check_fixtures(filename):

        # filename includes start datetime, duration, liters, month, hour, day
        usages = np.genfromtxt(filename, delimiter=" ")
        parameters = {}
        parameters["min_duration"] = np.min(usages[:, 2])
        parameters["i_min_duration"] = np.where(usages[:, 2] == parameters["min_duration"])
        parameters["max_duration"] = np.max(usages[:, 2])
        parameters["i_max_duration"] = np.where(usages[:, 2] == parameters["max_duration"])
        parameters["min_liters"] = np.min(usages[:, 3])
        parameters["i_min_liters"] = np.where(usages[:, 3] == parameters["min_liters"])
        parameters["max_liters"] = np.max(usages[:, 3])
        parameters["i_max_liters"] = np.where(usages[:, 3] == parameters["max_liters"])

        return


    @staticmethod
    def rename_usages(ts_dir):
        """
        This  method rename the  n files in a directory in a way that their name corresponde to the first n numbers
        :param ts_dir:  the folder containing the files
        :return: None
        """
        ts_dir += '/splits'
        ts_files = glob.glob(ts_dir + "/*.csv")
        name_sequence = []
        for ts_file in ts_files:
            name_sequence.append(int(os.path.basename(ts_file)[:-4]))
        sorted_sequence = np.sort(name_sequence)
        for i in range(len(name_sequence)):
            if i != sorted_sequence[i]:
                os.rename(ts_dir + "/" + str(sorted_sequence[i])+".csv", ts_dir + "/" + str(i)+".csv")




    @staticmethod
    def remove_outlayers(ts_dir,  outlayers):
        """
        This method move the csv files listed in the outlayers dictionary to a subdire
        :param ts_dir: the folder containing the csv files
        :param outlayers: the dictionary listing the files to be moved
        :return: None
        """
        logging.debug("deleting " + str(len(outlayers["i_min_samples"])) + "files")
        if not os.path.isdir(ts_dir + '/outlayers'):
            os.mkdir(ts_dir + '/outlayers')
        for i in outlayers["i_min_samples"]:
            shutil.move(ts_dir + "/splits/" + str(i) + ".csv", ts_dir + "/outlayers/" + str(i) + ".csv")
        for i in outlayers["i_min_liters"]:
            if os.path.isfile(ts_dir + "/splits/" + str(i) + ".csv"):
                shutil.move(ts_dir + "/splits/" + str(i) + ".csv", ts_dir + "/outlayers/" + str(i) + ".csv")
        for i in outlayers["i_min_duration"]:
            if os.path.isfile(ts_dir + "/splits/" + str(i) + ".csv"):
                shutil.move(ts_dir + "/splits/" + str(i) + ".csv", ts_dir + "/outlayers/" + str(i) + ".csv")


