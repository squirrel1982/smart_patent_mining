#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# data reference : R. A. Fisher (1936). "The use of multiple measurements
# in taxonomic problems"

from distance_builder import *
from distance import *


if __name__ == '__main__':
    builder = DistanceBuilder()
    builder.load_points(r'../data/data_main_path/main_path_topic_T0_S1.data')
    builder.build_distance_file_for_cluster(
        ConsineDistance(), r'../data/data_main_path/main_path_topic_T0_S1_cosine.forcluster')
    '''
    builder.build_distance_file_for_cluster(
        ConsineDistance(), r'../data/data_main_path/integrated_main_path_sim_length_cosine.forcluster')
    '''
