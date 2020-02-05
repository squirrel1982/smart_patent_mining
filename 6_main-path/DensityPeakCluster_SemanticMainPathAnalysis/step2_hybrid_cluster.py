#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from plot import *
from cluster import *


def plot(data, density_threshold, distance_threshold, auto_select_dc=False):
    #logging.basicConfig(
        #format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    rho, delta, nneigh = dpcluster.cluster(
        load_paperdata, data, density_threshold, distance_threshold, auto_select_dc=auto_select_dc)
    #logger.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        pass#logger.info('%d %f %f' % (idx, rho[center], delta[center]))
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    plot_cluster(dpcluster)

def hybrid_plot(data,path_len, density_threshold, distance_threshold,index = 0,local_den_weight=1.0, path_len_weight=1.0, auto_select_dc=False):
    #logging.basicConfig(
        #format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    rho, delta, nneigh = dpcluster.hybrid_cluster_onlyCenterInCluster(
        load_paperdata, data,path_len, density_threshold, distance_threshold,\
        local_den_weight, path_len_weight,auto_select_dc=auto_select_dc)
    #logger.info(str(len(dpcluster.ccenter)) + ' center as below')

    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    plot_hybrid_cluster(dpcluster,index,load_old_MDS=True)

if __name__ == '__main__':
    # plot('./data/data_in_paper/example_distances.dat', 20, 0.1)
    # normalize node number of path first

    with open('./data/data_main_path/node_num_of_path_list.data','r') as f:
        node_num_of_path_list = pickle.load(f)

    max_node_num = max(node_num_of_path_list)
    min_node_num = min(node_num_of_path_list)
    normalized_node_num_of_path_list = [1.0 * (i - min_node_num) / (max_node_num - min_node_num) for i in
                                        node_num_of_path_list]
    with open('./data/data_main_path/normalized_node_num_of_path_array.npy','w') as f:
        np.save(f,normalized_node_num_of_path_list)
    for index in range(100):

        hybrid_plot('./data/data_main_path/main_path_topic_T0_S1_cosine.forcluster',
             './data/data_main_path/normalized_node_num_of_path_array.npy',
             25, 0.4, index,local_den_weight=1.0, path_len_weight=index*1.0,auto_select_dc=False)
