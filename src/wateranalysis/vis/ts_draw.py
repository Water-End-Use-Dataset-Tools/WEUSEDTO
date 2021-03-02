import matplotlib.pyplot as plt
import glob
import numpy as np
import os

fixture = "Shower"

class TsDraw:

    images_dir = "data/images"

    def draw_all_ts(self, ts_dir, first=1, n=None):
        ts_files = glob.glob(ts_dir + '/*.csv')
        if n is None:
            n = len(ts_files)
        for i in range(first, n):
            self.draw_ts(ts_files[i])

    def draw_ts(self, ts_file):
        plt.figure()
        ts = np.genfromtxt(ts_file, delimiter=" ")
        ts[:, 0] = ts[:, 0]-ts[0, 0]
        plt.plot(ts[:, 0], ts[:, 1])
        filename = os.path.basename(ts_file)
        if not os.path.isdir(self.images_dir+"/"+fixture):
            os.mkdir(self.images_dir+"/"+fixture)
        plt.savefig(self.images_dir+"/"+fixture+"/"+filename[:-4]+".jpg")


if __name__ == "__main__":
    tsd = TsDraw()
    tsd.draw_all_ts("data/splits/csv_"+fixture, 1, 50)