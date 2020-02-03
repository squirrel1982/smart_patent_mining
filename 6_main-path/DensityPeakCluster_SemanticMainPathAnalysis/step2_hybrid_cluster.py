#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from plot import *
from cluster import *


def plot(data, density_threshold, distance_threshold, auto_select_dc=False):
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    rho, delta, nneigh = dpcluster.cluster(
        load_paperdata, data, density_threshold, distance_threshold, auto_select_dc=auto_select_dc)
    logger.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        logger.info('%d %f %f' % (idx, rho[center], delta[center]))
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    plot_cluster(dpcluster)

def hybrid_plot(data,path_len, density_threshold, distance_threshold,local_den_weight=1.0, path_len_weight=1.0, auto_select_dc=False):
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    rho, delta, nneigh = dpcluster.hybrid_cluster_onlyCenterInCluster(
        load_paperdata, data,load_mainPathLen,path_len, density_threshold, distance_threshold,\
        local_den_weight, path_len_weight,auto_select_dc=auto_select_dc)
    logger.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        logger.info('%d %f %f' % (idx, rho[center], delta[center]))
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    plot_hybrid_cluster(dpcluster,load_old_MDS=True)

if __name__ == '__main__':
    # plot('./data/data_in_paper/example_distances.dat', 20, 0.1)
    hybrid_plot('./data/data_main_path/main_path_topic_T0_S1_cosine.forcluster',
         './data/data_main_path/normalized_node_num_of_path_list.data',
         25, 0.4, local_den_weight=1.0, path_len_weight=0.01,auto_select_dc=False)
