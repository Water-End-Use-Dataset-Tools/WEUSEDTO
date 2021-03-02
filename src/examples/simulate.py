from wateranalysis.learning import randomforest
from wateranalysis.simulation.generator import ProfileGenerator
import numpy as np
import os
import logging
import argparse
import glob
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import time


def sum_irr(ts1, ts2):
    if ts1[0, 0] < ts2[0,0]:
        tsmin = ts1
        tsmax = ts2
    else:
        tsmin = ts2
        tsmax = ts1

    j = 0
    ts_sum = [tsmin[0]]
    i = 1
    while i < len(tsmin):
        if tsmin[i, 0] == tsmax[j, 0]:
            ts_sum = np.vstack((ts_sum, [tsmin[i, 0], tsmin[i, 1] + tsmax[j, 1]]))
        elif tsmin[i, 0] > tsmax[j, 0]:
            if (j+1) < len(tsmax):
                j += 1

                if tsmin[i, 1] > 0 and tsmin[i-1, 1] > 0:
                    ts_sum = np.vstack((ts_sum, [tsmax[j-1, 0], tsmax[j-1, 1] + 0.5 *(tsmin[i, 1] + tsmin[i-1, 1])]))
                else:
                    ts_sum = np.vstack((ts_sum, tsmax[j - 1]))
                i -= 1
        else:
            if j-1 > 0 and tsmax[j, 1] > 0 and tsmax[j-1, 1] > 0 :
                ts_sum = np.vstack((ts_sum, [tsmin[i, 0], tsmin[i, 1] + 0.5 * (tsmax[j, 1] + tsmax[j - 1, 1])]))
            else:
                ts_sum = np.vstack((ts_sum, tsmin[i]))
        i += 1
    while j < len(tsmax):
        ts_sum = np.vstack((ts_sum, tsmax[j]))
        j +=1;


    return ts_sum


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    parser.add_argument('--smodel', dest='smodel', choices=['global', 'monthly', 'weekly'], default='monthly',
                        help='choose the statistic model to generate usages')
    parser.add_argument('--month', dest='month', type=int, choices=range(1, 13), default=8, help='month do be simulated')
    parser.add_argument('--weekday', dest='weekday', type=int, default=0, choices=range(0, 7), help='weekday to be simulated')
    parser.add_argument('--users', dest='users', type=int, default=1, help='number of users to simulate')



    args = parser.parse_args()
    fixture = args.fixture

    data_dir = 'data/csv_'+fixture

    '''
    Simulation of userscd /hspl 
    '''
    if not os.path.isdir(data_dir + "/simulation"):
        os.mkdir(data_dir + "/simulation")

    mg = ProfileGenerator(data_dir, data_dir + "/simulation")
    if args.smodel == "global":
        # GLOBAL
        mg.global_model(fixture, args.users)
    elif args.model == "monthly":
        mg.monthly_model(fixture, args.month, args.users)
    else:
        mg.weekly_model(fixture,args.weekday, args.users)

    simulation_file = data_dir + '/simulation/simulatedusages_' + fixture + '.csv'
    runs = np.genfromtxt(simulation_file, delimiter=" ")

    predict = open(data_dir + '/' + fixture+".predict", "w")

    for i in range(1, len(runs)):
        predict.write("Nan," + str(int(runs[i][3])) + ",0,10\n")
    predict.close()

    clusters = randomforest.RandomForest.predict(data_dir + "/model.pkl", data_dir + '/' + fixture + ".predict")
    # print(clusters)

    userid = None

    for i in range(1, len(runs)):
        cluster_ts = np.genfromtxt(data_dir + "/" + str(int(clusters[i-1])) + "_spline.csv", delimiter=",")
        cluster_ts = np.vstack((cluster_ts, [cluster_ts[-1, 0] + 1, 0]))
        cluster_ts = np.vstack(([cluster_ts[0, 0] - 1, 0], cluster_ts))
        start_time = runs[i][-2] * 3600 + runs[i][-1] * 60
        cluster_ts[:, 0] += start_time
        if userid is None:
            userid = runs[i][0]
            ts = cluster_ts
        elif userid != runs[i][0]:
            np.savetxt(data_dir +"/simulation/user_" + str(int(userid)) +"_predicted.csv", ts, fmt="%i,%f")
            userid = runs[i][0]
            ts = cluster_ts
        else:
            if ts[0, 0] < cluster_ts[0, 0]:
                shift_time = ts[-1, 0] - cluster_ts[0, 0]
                if shift_time > 0:
                    cluster_ts[:, 0] += shift_time + 1
                ts = np.vstack((ts, cluster_ts))
            else:
                shift_time = cluster_ts[-1, 0] - ts[0, 0]
                if shift_time > 0:
                    ts[:, 0] += shift_time + 1
                ts = np.vstack((cluster_ts, ts))
    np.savetxt(data_dir + "/simulation/user_" + str(int(userid)) + "_predicted.csv", ts, fmt="%i,%f")


    users_files = glob.glob(data_dir + "/simulation/user_*predicted.csv")

    # generate image
    i = 1
    ts_tot = None
    for user_file in users_files:

        ts = np.genfromtxt(user_file, delimiter=",")
        plt.plot(ts[:, 0], ts[:, 1], '-', label="user_" + str(i))
        i += 1

    plt.ylabel("water flow (ml/s)")
    plt.xlabel("hour")
    # plt.xlim(5.5*3600, 7.5*3600)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mtick.FixedLocator(ts[:,0]))
    loc = mtick.MaxNLocator(12)  # this locator puts ticks at regular intervals
    plt.gca().xaxis.set_major_locator(loc)
    plt.gca().xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda pos, _: time.strftime("%H:%M", time.localtime(pos)))
        )

    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.savefig(data_dir + "/simulation/allusers.png")









