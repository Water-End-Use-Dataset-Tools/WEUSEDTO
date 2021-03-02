from wateranalysis.learning import cluster
from wateranalysis.timeseries.splitters import SimpleSplitter, Splitter
from wateranalysis.models.statistics import ModelBuilder
import numpy as np
import os
from wateranalysis.timeseries.filters import TSFilter
import logging
from wateranalysis.timeseries.statistics import TSParameters
import argparse
from wateranalysis.models.spline import TSSPline

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    parser.add_argument('--nosplit', dest='nosplit', action='store_true', default=False, help='skip the split stage')
    parser.add_argument('--nofilter', dest='nofilter', action='store_true', default=False, help='skip the filter stage')
    parser.add_argument('--nomodel', dest='nomodel', action='store_true', default=False,  help='skip the model stage')
    parser.add_argument('--nocluster', dest='nocluster', action='store_true', default=False, help='skip the cluster stage')
    parser.add_argument('--nospline', dest='nospline', action='store_true', default=False,
                        help='skip the spline stage')
    parser.add_argument('--splitalg', dest='splitalg', choices=['SimpleSplitter', 'Splitter'], default='Splitter',
                        help='skip the spline stage')


    args = parser.parse_args()
    fixture = args.fixture

    data_dir = 'data/csv_'+fixture
    if not args.nosplit:
        if not os.path.isdir(data_dir + '/splits'):
            os.makedirs(data_dir + '/splits')

        # This section detects usages and splits the original timeseries
        if args.splitalg is not None and args.splitalg == 'SimpleSplitter':
            splitter = SimpleSplitter('data/feed_'+fixture+'.MYD.csv', data_dir + '/splits')
        else:
            splitter = Splitter('data/feed_'+fixture+'.MYD.csv', data_dir + '/splits')
        splitter.split()

    outlayers = []
    if not args.nofilter:
        # this method checks all splitted timeseries with a duration < 10 secs, consumption < 250 ml,
        # less than 7 samples
        # result is a dictionary
        outlayers = TSFilter.outlayers(data_dir, 10, 250, 7)
        logging.info("identified " + str(len(outlayers)) + " outlayers")
        # here we delete those file which have been identified as outlayers
        if len(outlayers) > 0:
            TSFilter.remove_outlayers(data_dir, outlayers)
            TSFilter.rename_usages(data_dir)

    if not args.nomodel:
        # Compute usages
        ff = TSParameters()
        if len(outlayers) > 0:
            ff.rename_usages(data_dir + '/splits')
        # Output file contains: start datetime, duration, liters, month, hour, day
        ff.compute_parameters(data_dir + '/' + fixture + '_usage.csv', data_dir + '/splits')
        #  Output file (fixture_num_usage.csv) contains month, day of month, count,  dayweek (sunday=7)
        ff.usages_perday(data_dir + '/' + fixture + '_num_usage.csv', data_dir + '/' + fixture + "_usage.csv")

        mb = ModelBuilder(fixture, 'global', data_dir)
        mb.build_model()

        mb = ModelBuilder(fixture, 'monthly', data_dir)
        mb.build_model()

        mb = ModelBuilder(fixture, 'weekly', data_dir)
        mb.build_model()

    if not args.nocluster:
        # Compute clusters
        # only 200 timeseries are clustered
        cluster = cluster.TSCluster(data_dir, fixture, 200)

        # each timeseres i represented by the following features (duration, liters, maxflow)
        cluster.extract_features(['start', 'duration', 'liters', 'max_flow'])
        testset = cluster.get_testset()
        kn, clusters = cluster.compute_clusters(testset)
        np.savetxt(data_dir + '/' + fixture+".clusters", clusters)

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

