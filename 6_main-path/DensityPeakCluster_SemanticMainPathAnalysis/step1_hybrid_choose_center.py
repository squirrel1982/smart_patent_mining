#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
#from plot import *
from cluster import *
from PajekUtil import *
import networkx as nx
'''
def plot(data, path_len,auto_select_dc=False):
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    distances, max_dis, min_dis, max_id, rho = dpcluster.local_hybrid_density(
        load_paperdata, data,load_mainPathLen,path_len, local_den_weight=1.0, path_len_weight=10.0\
        ,auto_select_dc=auto_select_dc)
    delta, nneigh = min_distance(max_id, max_dis, distances, rho)
    plot_rho_delta(rho, delta)  # plot to choose the threthold

'''
def printChosenCenter(data, path_len,normalized_path_len,rho_threshold,delta_threshold,auto_select_dc=False):
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dpcluster = DensityPeakCluster()
    path_len_list = load_mainPathLen(path_len)
    path_len_list = [0] + path_len_list
    distances, max_dis, min_dis, max_id, rho = dpcluster.local_hybrid_density(
        load_paperdata, data,load_mainPathLen,normalized_path_len, local_den_weight=1.0, path_len_weight=20.0\
        ,auto_select_dc=auto_select_dc)
    delta, nneigh = min_distance(max_id, max_dis, distances, rho)
    for index,(r_tmp,d_tmp) in enumerate(zip(rho, delta)):
        if r_tmp>rho_threshold and d_tmp>delta_threshold:
            print index,path_len_list[index],r_tmp,d_tmp

def outputChosenCenter_indicated_mainPath(data, path_len,normalized_path_len,subgraph_list,rho_threshold,delta_threshold,\
                                          auto_select_dc=False):
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    pu = PajekUtil()
    dpcluster = DensityPeakCluster()
    path_len_list = load_mainPathLen(path_len)
    path_len_list = [0] + path_len_list
    subgraph_list = load_mainPathLen(subgraph_list)
    subgraph_list = [nx.DiGraph()] + subgraph_list

    distances, max_dis, min_dis, max_id, rho = dpcluster.local_hybrid_density(
        load_paperdata, data,load_mainPathLen,normalized_path_len, local_den_weight=1.0, path_len_weight=20.0\
        ,auto_select_dc=auto_select_dc)
    delta, nneigh = min_distance(max_id, max_dis, distances, rho)
    for index,(r_tmp,d_tmp) in enumerate(zip(rho, delta)):
        if r_tmp>rho_threshold and d_tmp>delta_threshold:
            print index,path_len_list[index],r_tmp,d_tmp
            pu.writeGraph2pajekNetFile(subgraph_list[index],'subgraph_'+str(index)+'.net')


if __name__ == '__main__':
    # plot('./data/data_in_paper/example_distances.dat')
    #plot('./data/data_iris_flower/iris.forcluster', auto_select_dc=True)
    '''
    plot('./data/data_main_path/main_path_topic_T0_S1_cosine.forcluster',\
         './data/data_main_path/normalized_node_num_of_path_list.data',\
        auto_select_dc=False)
    
    printChosenCenter('./data/data_main_path/main_path_topic_T0_S1_cosine.forcluster',\
         './data/data_main_path/node_num_of_path_list.data', \
                      './data/data_main_path/normalized_node_num_of_path_list.data',\
                      30,0.4,
        auto_select_dc=False);l
    '''
    outputChosenCenter_indicated_mainPath('./data/data_main_path/main_path_topic_T0_S1_cosine.forcluster',\
         './data/data_main_path/node_num_of_path_list.data', \
                      './data/data_main_path/normalized_node_num_of_path_list.data', \
                                          './data/data_main_path/subgraph_list.data', \
                                          30,0.4,
        auto_select_dc=False);