#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *

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
node_Weight=1.0
arc_Weight=16
TopN = 1
roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
roadMap.loadNetworkFromPajeknet(spc_network_file)

path_list = roadMap.queryBasedMainPath_nodeWeight_arcWeight("circulation cooling air temperature control",\
                                                         node_Weight=node_Weight,arc_Weight=arc_Weight)
topN_path_list = get_TOPN_mainPath(TopN,path_list)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
pu.writeGraph2pajekNetFile(g_result,'query_cooling_Top1_T16_S1.net')
'''
total_statistics = []
num_statistics = []
for i in range(1,20,1):
    path_list = roadMap.queryBasedMainPath_nodeWeight_arcWeight("circulation cooling air temperature control",\
                                                                arc_Weight=i)
    topN_path_list = get_TOPN_mainPath(TopN,path_list)
    subgraphs = [graph[1][1][0] for graph in topN_path_list]
    g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)
    gas_list = [g_result.node[node_tmp]['ga'] for node_tmp in g_result.nodes()]

    #print i,g_result.number_of_nodes(),nx.number_weakly_connected_components(g_result)
    total_statistics.append([i,g_result.number_of_nodes(),nx.number_weakly_connected_components(g_result),\
                             gas_list])
    num_statistics.append(g_result.number_of_nodes())
    pu.writeGraph2pajekNetFile(g_result,'.\query_net\query_cooling_Top1_T1_S'+str(i)+'1.net')
with open('total_statistics.txt','w') as f:
    for i in total_statistics:
        f.write(str(i[0])+' '+str(i[1])+' '+str(i[2])+' '+' '.join(i[3])+'\n')
with open('num_statistics.txt','w') as f:
    for i in num_statistics:
        f.write(str(i)+'\n')
'''