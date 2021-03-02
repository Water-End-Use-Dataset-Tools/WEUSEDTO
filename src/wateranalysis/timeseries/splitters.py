"""
splitters
=======================================
This is a  module which implement different algorithms to split a timeseries
"""

import pandas as pd
import numpy as np
import scipy.integrate as integrate


class Splitter:

    ts = None
    out_data_dir = None

    def __init__(self, time_series, out_dir):
        """

        :param time_series: a csv files with two columns, epoch and water flow as float
        :param out_dir: a directory where the splitted files will be saved
        """
        self.ts = time_series
        self.out_data_dir = out_dir

    def split(self, sep=' ', head=None, threshold=0):
        """

        :param sep:
        :param head:
        :param threshold:
        :return:
        """
        df = pd.read_csv(self.ts, sep=sep, header=head, names=['time', 'flow'])
        cont = 0

        start_event = 0

        end_event = 0

        ts = df.to_numpy()

        timegap = np.zeros([len(ts), 1])

        Q = ts[:, 1]

        for k in range(0, len(ts) - 1):
            timegap[k + 1] = ts[k + 1, 0] - ts[k, 0]

        timelim = 4

        Qlim = 6

        idx = []

        vlim = 0.125  # volume in [l]

        for i in range(2, len(ts) - 1):

            ratioq = (np.mean(Q[i - 2:i + 3]) / Q[i])

            if timegap[i] <= timelim and Q[i] > Qlim:

                idx.append(i - 1)

            elif timegap[i] > timelim and timegap[i] < 90 and Q[i] > Qlim and ratioq > 0.9 and ratioq < 1.1:

                idx.append(i - 1)

            elif timegap[i] > timelim and len(
                    idx) > 3:  # per ogni time series è richiesto un numero di elementi maggiore di 3

                if Q[idx[0]] > 0:
                    start_event = idx[0]

                elif Q[idx[0]] == 0:

                    start_event = idx[1]

                end_event = idx[len(idx) - 1] + 2

                y = ts[start_event:end_event, 1] / 1000

                x = ts[start_event:end_event, 0]

                volume = integrate.trapz(y, x)  # volume [l]

                if volume > vlim:
                    cont += 1

                    np.savetxt(self.out_data_dir + '/' + str(cont) + '.csv', ts[start_event:end_event],
                               delimiter=sep, fmt="%d")

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] <= timelim and Q[i] <= Qlim and len(
                    idx) > 3:  # per ogni time series è richiesto un numero di elementi maggiore di 3

                if Q[idx[0]] > 0:

                    start_event = idx[0]

                elif Q[idx[0]] == 0:

                    start_event = idx[1]

                end_event = idx[len(idx) - 1] + 2

                y = ts[start_event:end_event, 1] / 1000

                x = ts[start_event:end_event, 0]

                volume = integrate.trapz(y, x)

                if volume > vlim:
                    cont += 1

                    np.savetxt(self.out_data_dir + '/' + str(cont) + '.csv', ts[start_event:end_event], delimiter=sep,
                               fmt="%d")

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] > timelim and len(idx) <= 3:

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] <= timelim and Q[i] <= Qlim and len(idx) <= 3:

                end_event = 0

                start_event = 0

                idx = []


class SimpleSplitter:
    """
    SimpleSplitter class provides methods to split a time-series in multiple usages using threshold as unique criteria
    """
    ts = None
    out_data_dir = None

    def __init__(self, time_series, out_dir):
        """

        :param time_series: a csv files with two columns, epoch and water flow as float
        :param out_dir: a directory where the splitted files will be saved
        """
        self.ts = time_series
        self.out_data_dir = out_dir

    def split(self, sep=' ', head=None, threshold=0):
        """
        This method split a time-series using a threshold as only one criteria.
        Splitted timeseries must be at least five samples long.

        :param sep: the delimiter for the csv file, default is the space
        :param head: not None if the first line of the csv contains column titles
        :param threshold: a float value that is compared with the samples to identify
         first and last sample for splitting

        """
        df = pd.read_csv(self.ts, sep=sep, header=head,
                         names=['time', 'flow'])

        this_usage = []
        cont = 0

        for i in range(0, len(df)):
            elemento = df.iloc[i]
            if abs(elemento[1]) > abs(threshold):
                riga = [elemento[0], elemento[1]]
                this_usage.append(riga)
            elif abs(elemento[1]) <= abs(threshold) and len(this_usage) >= 5:
                cont += 1

                df2 = pd.DataFrame(this_usage)
                df2.to_csv(self.out_data_dir + '/' + str(cont) + '.csv', header=None, sep=sep, index=False,
                           date_format='%d %d %f %d %d %d')
                this_usage = []
            elif elemento[1] == 0 and len(this_usage) < 5:
                this_usage = []
