#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import numpy as np
from cluster import *
from sklearn import manifold
from sklearn import __version__ as sklearn_version
from plot_utils import *
import cPickle as pickle
import os


def versiontuple(v):
    '''
    Format the version string to tuple of int type
    
    Argss:
            v : __version__ string
    '''
    return tuple(map(int, (v.split("."))))


def plot_rho_delta(rho, delta):
    '''
    Plot scatter diagram for rho-delta points

    Args:
            rho   : rho list
            delta : delta list
    '''
    logger.info("PLOT: rho-delta plot")
    plot_scatter_diagram(
        0, rho[1:], delta[1:], x_label='rho', y_label='delta', title='rho-delta')


def plot_cluster(cluster,load_old_MDS = False,old_MDS_address = './mds.data'):
    '''
    Plot scatter diagram for final points that using multi-dimensional scaling for data

    Args:
            cluster : DensityPeakCluster object
    '''
    logger.info("PLOT: cluster result, start multi-dimensional scaling")
    dp = np.zeros((cluster.max_id, cluster.max_id), dtype=np.float32)
    cls = []
    for i in xrange(1, cluster.max_id):
        for j in xrange(i + 1, cluster.max_id + 1):
            dp[i - 1, j - 1] = cluster.distances[(i, j)]
            dp[j - 1, i - 1] = cluster.distances[(i, j)]
        cls.append(cluster.cluster[i])
    cls.append(cluster.cluster[cluster.max_id])
    cls = np.array(cls, dtype=np.float32)
    fo = open(r'./tmp.txt', 'w')
    fo.write('\n'.join(map(str, cls)))
    fo.close()
    version = versiontuple(sklearn_version)
    if load_old_MDS == False:
        if version[0] > 0 or version[1] > 14:
            mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1,
                               dissimilarity='precomputed')
        else:
            mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1)
    else:
        if os.path.exists(old_MDS_address)==False:
            if version[0] > 0 or version[1] > 14:
                mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1,
                                   dissimilarity='precomputed')
            else:
                mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1)

            with open(old_MDS_address,'w') as f:
                pickle.dump(mds, f)
        else:
            with open(old_MDS_address, 'r') as f:
                mds = pickle.load(f)

    dp_mds = mds.fit_transform(dp)
    logger.info("PLOT: end mds, start plot")
    plot_scatter_diagram(1, dp_mds[:, 0], dp_mds[
                         :, 1], title='cluster', style_list=cls)

def plot_hybrid_cluster(cluster,load_old_MDS = False,old_MDS_address = './mds.data'):
    '''
    Plot scatter diagram for final points that using multi-dimensional scaling for data

    Args:
            cluster : DensityPeakCluster object
    '''
    cls = []
    dp = np.zeros((cluster.max_id, cluster.max_id), dtype=np.float32)
    for i in xrange(1, cluster.max_id):
        for j in xrange(i + 1, cluster.max_id + 1):
            dp[i - 1, j - 1] = cluster.distances[(i, j)]
            dp[j - 1, i - 1] = cluster.distances[(i, j)]
        cls.append(cluster.cluster[i])
    cls.append(cluster.cluster[cluster.max_id])
    cls = np.array(cls, dtype=np.float32)
    fo = open(r'./tmp.txt', 'w')
    fo.write('\n'.join(map(str, cls)))
    fo.close()
    if load_old_MDS == True and os.path.exists(old_MDS_address) == False:
        logger.info("PLOT: cluster result, start multi-dimensional scaling")
        version = versiontuple(sklearn_version)

        if version[0] > 0 or version[1] > 14:
            mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1,
                                   dissimilarity='precomputed')
        else:
            mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1)
        dp_mds = mds.fit_transform(dp)
        with open(old_MDS_address, 'w') as f:
            pickle.dump(dp_mds, f)
    elif load_old_MDS == True and os.path.exists(old_MDS_address) == True:
        with open(old_MDS_address, 'r') as f:
            dp_mds = pickle.load(f)
    logger.info("PLOT: end mds, start plot")
    plot_scatter_diagram(1, dp_mds[:, 0], dp_mds[
                         :, 1], title='cluster', style_list=cls)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    # dpcluster.local_density(load_paperdata, './example_distances.dat')
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    rho, delta, nneigh = dpcluster.cluster(
        load_paperdata, './data/data_in_paper/example_distances.dat', 20, 0.1)
    logger.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        logger.info('%d %f %f' % (idx, rho[center], delta[center]))
    plot_cluster(dpcluster)
