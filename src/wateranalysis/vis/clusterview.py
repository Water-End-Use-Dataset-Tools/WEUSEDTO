# from wateranalysis.models.spline import BSpline
import json
import matplotlib.pyplot as plt
import glob
import numpy as np
import os


class ClustersDraw:

    def __init__(self, folder):
        self.data_dir = folder

    @classmethod
    def p2e(cls,ts):
        temp = 0
        for i in range(1,len(ts)):
            temp=temp+(ts[i-1,1])*(ts[i,0]-ts[i-1,0])/3600
            ts[i-1,1] = temp
        ts[i]= [ts[i,0], ts[i-1,1]]
        return ts

    def draw_ts(self):

        cluster_dirs = glob.glob(self.data_dir + '/cluster_*')
        for cluster_dir in cluster_dirs:
            plt.figure()
            plt.title(os.path.basename(cluster_dir))
            ts_files = glob.glob(cluster_dir + '/*.csv')
            for ts_file in ts_files:
                ts = np.genfromtxt(ts_file, delimiter=" ")
                ts[:,0]=ts[:,0]-ts[0,0]
                plt.plot(ts[:,0],ts[:,1], label=os.path.basename(ts_file)[:-4])
            plt.legend()
            plt.show()
    '''
    def draw_spline(self, ):

        bsp= BSpline()
        spfile = open(self.data_dir+"/washbasin.spline", "r")
        i = 0
        cluster_dirs = glob.glob(self.data_dir + '/cluster_*')

        for jsonstr in spfile:
            #jsonstr=spfile.readline()
            elems = jsonstr.split(";")
            jsonspline = json.loads(elems[3])
            spline = bsp.json2bspline(jsonspline)
            yy = bsp.splev(spline,eval(elems[1]),eval(elems[2]),30,eval(elems[1]))

            yy[:,0]=yy[:,0]-yy[0,0]
            plt.plot(yy[:,0],yy[:,1])

            ts_files = glob.glob(cluster_dirs[i] + '/*.csv')
            i +=1
            temp_ts = None
            for ts_file in ts_files:
                ts = np.genfromtxt(ts_file, delimiter=" ")

                ts = self.p2e(ts)
                ts[:,0]=ts[:,0]-ts[0,0]
                plt.plot(ts[:, 0], ts[:, 1], c='gray')
            plt.show()
    '''
