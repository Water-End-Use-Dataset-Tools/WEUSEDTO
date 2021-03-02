from wateranalysis.learning import randomforest, cluster
import numpy as np
import logging
import argparse
from wateranalysis.models.spline import TSSPline

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    parser.add_argument('--nocluster', dest='nocluster', action='store_true',
                        default=False, help='skip the cluster stage')
    parser.add_argument('--nospline', dest='nospline', action='store_true', default=False,
                        help='skip the spline stage')

    args = parser.parse_args()
    fixture = args.fixture

    data_dir = 'data/csv_'+fixture

    if not args.nocluster:
        # Compute clusters
        # only 200 timeseries are clustered
        cluster = cluster.TSCluster(data_dir, fixture, 200)

        # each timeseres i represented by the following features (duration, liters, maxflow)
        cluster.extract_features(['start', 'duration', 'liters', 'max_flow'])
        testset = cluster.get_testset()
        kn, clusters = cluster.compute_clusters(testset)
        np.savetxt(data_dir + '/' + fixture+".clusters",  clusters, fmt='%i')

        # ten timeseries per cluster are saved in different folders
        cluster.mk_cluster_folders(kn, clusters, 10)

        # plot all timeseries, in terms of features,  with a different color per cluster
        # (first two parameters: duration and liters)

        plt = cluster.plot_clusters(testset, clusters, [0, 1])
        plt.xlabel("duration ")
        plt.ylabel("ml_liters")
        plt.savefig(data_dir + "/clustering_0_1.png")
        plt.close()

        # timeseries of each cluster ar plotted
        plt = cluster.plot_clusters(testset, clusters, [1, 2])
        plt.xlabel("ml_liters ")
        plt.ylabel("max_flow")
        plt.savefig(data_dir + "/clustering_1_2.png")
        plt.close()

        # cdraw = clusterview.ClustersDraw("data/splits/csv_Washbasin")
        # cdraw.draw_ts()

    if not args.nospline:
        tsspl = TSSPline(data_dir)
        tsspl.compute()
        tsspl.draw_all()
        tsspl.to_csv(20)

    '''
    the random forest is used to learn the cluster from following usage parameters
     (which are  preliminary computed and stored in .sequence file)
    start_datetime, hour, day_week, day_month, time after same cluster, clusters
    '''
    clusters = np.genfromtxt(data_dir + '/' + fixture + ".clusters", delimiter=' ', dtype="i4")
    kn = np.max(clusters)
    rf = randomforest.RandomForest(data_dir, args.fixture, kn)

    rf.compute_features(clusters)
    rf.evaluate()
    rf.learn(data_dir)
