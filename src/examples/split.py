from wateranalysis.timeseries.splitters import SimpleSplitter, Splitter
from wateranalysis.timeseries.filters import TSFilter
import os
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    parser.add_argument('--nosplit', dest='nosplit', action='store_true', default=False, help='skip the split stage')
    parser.add_argument('--nofilter', dest='nofilter', action='store_true', default=False, help='skip the filter stage')
    parser.add_argument('--alg', dest='splitalg', default="SompleSplitter")

    args = parser.parse_args()
    fixture = args.fixture
    data_dir = 'data/csv_' + fixture

    if not args.nosplit:
        if not os.path.isdir(data_dir + '/splits'):
            os.makedirs(data_dir + '/splits')

        # This section detects usages and splits the original timeseries
        if args.splitalg is not None and args.splitalg == 'SimpleSplitter':
            splitter = SimpleSplitter('data/feed_' + fixture + '.MYD.csv', data_dir + '/splits')
        else:
            splitter = Splitter('data/feed_' + fixture + '.MYD.csv', data_dir + '/splits')
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

