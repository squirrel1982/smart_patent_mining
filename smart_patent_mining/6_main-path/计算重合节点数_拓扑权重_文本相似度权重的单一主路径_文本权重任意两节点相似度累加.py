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
g_result_topology = pu.combine_subGraphArray(subgraphs,roadMap.g)
g_result_topology_gas = []
for node in g_result_topology.nodes():
    g_result_topology_gas.append(g_result_topology.node[node]['ga'])
node_num_topology_weith_path = g_result_topology.number_of_nodes()
# get node number of  text weight path
topology_weight = 0;
text_weight = 1;
result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in result[:TopN]]
g_result_semantics = pu.combine_subGraphArray(subgraphs,roadMap.g)
g_result_semantics_gas = []
for node in g_result_semantics.nodes():
    g_result_semantics_gas.append(g_result_semantics.node[node]['ga'])
node_num_semantics_weith_path = g_result_semantics.number_of_nodes()

topology_weight = 0;
text_weight = 1;
g_result_list = []

for i in range(0,250,2):
    topology_weight = i;
    result = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file, corpus_serialAddress, topology_weight, text_weight)
    topN_path_list = get_TOPN_mainPath(TopN,result)
    subgraphs = [graph[1][1][0] for graph in topN_path_list]
    g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
    gas_tmp = []
    for node in g_result.nodes():
        gas_tmp.append(g_result.node[node]['ga'])
    g_result_list.append([set(gas_tmp).intersection(set(g_result_semantics_gas)),\
                          set(gas_tmp).intersection(set(g_result_topology_gas))])

with open('g_result_list.txt','w') as f:
    for i in g_result_list:
        f.write(str(len(i[0]))+' '+str(len(i[1]))+'\n')