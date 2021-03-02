"""
statistiscs
=======================================
This module computes features of a timeseries
"""
import glob
import os
import numpy as np
import datetime as dt
import pandas as pd


class TSParameters:
    """ This class provide static methods to compute properties of a timeseries composed of water flow sample"""
    @staticmethod
    def liters(ts):
        """
        This methods compute the total amount of liters from a time series that provide flow samples
        :param ts: it is an array of samples (epoch, flow_value)
        :return: the total amount of liters as a float
        """
        total_lits = 0
        for i in range(1, len(ts)):
            total_lits += ts[i, 1] * (ts[i, 0] - ts[i - 1, 0])
        return total_lits

    @staticmethod
    def rename_usages(ts_dir):
        """
        This method rename csv files in a directory in a way that filenames are a sequence of numbers [1,n]
        :param ts_dir: the directory containing csv files (1.csv, 2.csv, 4.csv ...)

        """
        ts_files = glob.glob(ts_dir + "/*.csv")
        name_sequence = []
        for ts_file in ts_files:
            name_sequence.append(int(os.path.basename(ts_file)[:-4]))
        sorted_sequence = np.sort(name_sequence)
        for i in range(len(name_sequence)):
            if i != sorted_sequence[i]:
                os.rename(ts_dir + "/" + str(sorted_sequence[i])+".csv", ts_dir + "/" + str(i)+".csv")

    # Output file contains:
    @staticmethod
    def compute_parameters(outfile, ts_dir, csv_sep=" "):
        """
        This method compute a list of features of time-series contained in each csv file of ts_dir folder
        Result are saved in a [fixture]_usage.csv file containing the following properties:
        (start_datetime, duration, liters, month, hour, day, max_flow)
        :param outfile: output filename
        :param ts_dir: the folder containing csv file
        :param csv_sep: the delimiter used in the csv file, space is the default value

        """
        ts_files = glob.glob(ts_dir+"/*.csv")
        data = []
        for i in range(0, len(ts_files)):
            ts = np.genfromtxt(ts_dir+"/" + str(i)+".csv", delimiter=" ")
            duration = ts[-1, 0] - ts[0, 0]
            liters = TSParameters.liters(ts)
            start_dt = dt.datetime.fromtimestamp(ts[0, 0])
            month = start_dt.month
            hour = start_dt.hour
            day = start_dt.weekday()
            max_flow = np.max(ts[:, 1])
            this_usage = [ts[0, 0], int(duration), liters, month, hour, day, max_flow]
            data.append(this_usage)

        df2 = pd.DataFrame(data)
        df2.to_csv(outfile, header=None, sep=csv_sep, index=False,
                   date_format='%d %d %f %d %d %d %f')

    @staticmethod
    def usages_perday(outfile, filename, csv_sep=" "):
        """
        This method from the file of features (that in the first column contains start date_time
        of the time-series), computes  usages per day in [fixture]_num_usage.csv.
        Each row of the output file contains  four columns: [month, day, num_usages, weekday]
        :param fixture: prefix of produced output file
        :param filename: the input file, produced by the *compute_features* method.
        :param csv_sep:
        :return: the delimiter used in the csv file, space is the default value
        """
        usages = np.genfromtxt(filename, delimiter=" ")
        all_days = np.zeros(365)
        for usage in usages:
            date_time = dt.datetime.fromtimestamp(usage[0])
            year = date_time.year
            dd = date_time - dt.datetime(year, 1, 1)
            all_days[dd.days] += 1
        data = []
        year = dt.datetime.fromtimestamp(usages[0][0]).year
        for i in range(len(all_days)):
            date_time = dt.date(year, 1, 1) + dt.timedelta(i)
            day_usage = [date_time.month, date_time.day, int(all_days[i]), date_time.weekday()]
            data.append(day_usage)
        df2 = pd.DataFrame(data)
        df2.to_csv(outfile, header=None, sep=csv_sep, index=False,
                   date_format='%d %d %d %d')
