import numpy as np
import cPickle as pickle
from plot_utils import *

with open('node_group_100_loop.data','r') as f:
    node_group = pickle.load(f)

with open('./mds.data', 'r') as f:
    dp_mds = pickle.load(f)
    #logger.info("PLOT: end mds, start plot")
    plot_scatter_diagram_20_loop_center_combined(dp_mds[:, 0], dp_mds[
                         :, 1],title='cluster', style_list=node_group)