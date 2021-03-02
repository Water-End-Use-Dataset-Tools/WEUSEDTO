import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import os
import pandas as pd
import pickle
# https://github.com/kawache/Python-B-spline-examples


class TSSPline:
    splines = {}

    def __init__(self, data_dir):
        self.folder = data_dir

    def draw_spline(self):
        pass

    def compute(self):
        cluster_dirs = glob.glob(self.folder + '/cluster_*')
        for cluster_dir in cluster_dirs:
            if os.path.isdir(cluster_dir):
                ts_files = glob.glob(cluster_dir + '/*.csv')
                all_ts = None
                for ts_file in ts_files:
                    ts = np.genfromtxt(ts_file, delimiter=" ")
                    ts[:, 0] = ts[:, 0] - ts[0, 0]
                    if all_ts is None:
                        all_ts = ts
                    else:
                        all_ts = np.concatenate((all_ts, ts), 0)
                # plt.show()
                all_ts = all_ts[all_ts[:, 0].argsort()]
                x = all_ts[:, 0]
                y = all_ts[:, 1]
                l = len(x)
                t = np.linspace(0, 1, l - 2, endpoint=True)
                t = np.append([0, 0, 0], t)
                t = np.append(t, [1, 1, 1])
                tck = [t, [x, y], 3]
                spline_obj = {'spline': tck, 'end': x[-1]}
                self.splines[os.path.basename(cluster_dir)] = spline_obj

    def to_csv(self, num=None):
        for key in self.splines.keys():
            spline_obj = self.splines[key]
            if num is None:
                num = 2 * int(spline_obj['end'] / 10)
            xs = np.linspace(0, 1, num, endpoint=True)
            out = interpolate.splev(xs, spline_obj['spline'])
            d = {'x': out[0], 'y': out[1]}
            df = pd.DataFrame(d)

            df.to_csv(self.folder + '/' + key.split("_")[1] + '_spline.csv', header=False, index=False)


    def draw_all(self):
        cluster_dirs = glob.glob(self.folder + '/cluster_*')
        for cluster_dir in cluster_dirs:
            if os.path.isdir(cluster_dir):
                plt.figure()
                filename = os.path.basename(cluster_dir)
                plt.title(filename)
                ts_files = glob.glob(cluster_dir + '/*.csv')
                all_ts = None
                for ts_file in ts_files:
                    ts = np.genfromtxt(ts_file, delimiter=" ")
                    ts[:, 0] = ts[:, 0]-ts[0, 0]
                    # plt.scatter(ts[:, 0], ts[:, 1])
                    # ts = ClustersDraw.p2e(ts)
                    if all_ts is None:
                        all_ts = ts
                    else:
                        all_ts = np.concatenate((all_ts, ts), 0)
                # plt.show()
                all_ts = all_ts[all_ts[:, 0].argsort()]
                plt.scatter(all_ts[:, 0], all_ts[:, 1])
                x = all_ts[:, 0]
                y = all_ts[:, 1]
                l = len(x)
                t = np.linspace(0, 1, l - 2, endpoint=True)
                t = np.append([0, 0, 0], t)
                t = np.append(t, [1, 1, 1])
                tck = [t, [x, y], 3]

                # tck, u = interpolate.splprep([x, y], k=3, s=32)
                # tck, xs = interpolate.splev([x, y])
                xs = np.linspace(0, 1, 2*int(x[-1]/10), endpoint=True)
                out = interpolate.splev(xs, tck)
                plt.plot(x, y, 'ro', out[0], out[1], 'b')
                plt.savefig(self.folder + '/' + filename + '_spline.png')

    def serialize(self):
        with open(self.folder +'/splines.pickle', 'wb') as f:
            pickle.dump(self.splines,f)

    def load(self):
        with open(self.folder +'/splines.pickle', 'rb') as f:
            self.splines = pickle.load(f)