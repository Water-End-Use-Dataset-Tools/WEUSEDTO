from matplotlib import pyplot as plt
import numpy as np
import glob
import os



if __name__ == '__main__':
	data_folder="data/spline"	
	conv = {0: lambda valstr: float(valstr.decode("utf-8").replace(',','.')), 1: lambda valstr: float(valstr.decode("utf-8").replace(',','.'))}
	for i in range(3):
		csv_files = glob.glob(data_folder+"/C"+str(i)+"*.csv")
		plt.figure()
		for csv_file in csv_files:


			ts = np.genfromtxt(csv_file, delimiter=";", converters = conv)
			plt.plot(ts[:, 0], ts[:, 1], '.', label=os.path.basename(csv_file))


		ts = np.genfromtxt(data_folder+"/B-splineC" + str(i) + ".csv", delimiter=";", converters=conv)
		plt.plot(ts[:, 0], ts[:, 1], '-', label="spline")
		plt.ylabel("liters (ml")
		plt.xlabel("time (sec)")
		plt.legend(loc="upper right")
		plt.savefig(data_folder+"/B-splineC" + str(i) + ".png")

