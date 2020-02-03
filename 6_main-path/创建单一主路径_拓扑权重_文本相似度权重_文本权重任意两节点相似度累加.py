#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
# step 1:load SPN network

def get_TOPN_mainPath(topN,result_graph_list):
    weight_list = []
    topN_graph_list = []
    for i in result_graph_list:
        if i[1][0] in weight_list:
            pass
        else:
            weight_list.append(i[1][0])
    for i in result_graph_list:
        if i[1][0] in weight_list[:topN]:
            topN_graph_list.append(i)
    return topN_graph_list
pu = PajekUtil()
#step1
prefix_address = './data/'
lsi_serializationAddress = prefix_address+"text_lsi.data"
dictionary_serialAddress = prefix_address+"dictionary.data"
gas_serialAddress = prefix_address+"gas.data"
texts_serialAddress = prefix_address+"texts.data"
documents_serialAddress = prefix_address+"documents.data"
index_serialAddress = prefix_address+"index.data"
corpus_serialAddress = prefix_address+"corpus.data"

spc_network_file = prefix_address+'deleteLoops_spc_3603.net'
roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
#step2
TopN = 1
# get node number of  topology weight path
node_num_topology_weith_path = 0;
node_num_semantics_weith_path = 0;
topology_weight = 1.0;
text_weight = 0;
result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
pu.writeGraph2pajekNetFile(g_result,'top1_newSumMethod_hybrid_T1_S0.net')
# get node number of  text weight path
topology_weight = 0;
text_weight = 1;
result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
pu.writeGraph2pajekNetFile(g_result,'top1_newSumMethod_hybrid_T0_S1.net')



topology_weight = 200;
text_weight = 1;
result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
pu.writeGraph2pajekNetFile(g_result,'top1_newSumMethod_hybrid_T200_S1.net')


topology_weight = 300;
text_weight = 1;
result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
pu.writeGraph2pajekNetFile(g_result,'top1_newSumMethod_hybrid_T300_S1.net')
