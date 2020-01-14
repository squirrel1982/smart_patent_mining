#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
# step 1:load SPN network

pu = PajekUtil()
#step1
prefix_address = './data/'
lsi_serializationAddress = prefix_address+"text_lsi.data"
dictionary_serialAddress = prefix_address+"dictionary.data"
gas_serialAddress = prefix_address+"gas.data"
texts_serialAddress = prefix_address+"texts.data"
documents_serialAddress = prefix_address+"documents.data"
index_serialAddress = prefix_address+"index.data"
roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
#step2
roadMap.loadNetworkFromPajeknet(prefix_address+'deleteLoops_spc_3603.net')
# step 2:add textual similarity to network
f = file(texts_serialAddress)
texts = pickle.load(f)
f.close();
roadMap.addLSIWeight2TopologyWeight4ArcInGraph(texts,topology_weight=10.0,text_weight=1.0)
# step 3:get topic main path
sim_matrix = roadMap.create_sim_sparse_matrix()
sources = pu.getSourceNodes(roadMap.g)

result = []
for i in sources:
    #result.append(pu.getmulti_MaxWeightPathBySingleNode_Graph(i,roadMap.g,roadMap.gas,sim_matrix))
    result.append(pu.getmulti_MaxWeightPathBySingleNode_Graph(i, roadMap.g))
    #result.append(pu.getmulti_MaxWeightPathBySingleNode_Graph(i, roadMap.g))
result.sort(cmp=lambda x,y: cmp(x[1][0], y[1][0]), reverse=True)

subgraphs = [graph[1][1][0] for graph in result[:10]]
g_result = pu.combine_subGraphArray(subgraphs,roadMap.g)

pu.writeGraph2pajekNetFile(g_result,'top10_oldMethod_hybrid_T10_S1.net')