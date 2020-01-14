#coding = utf-8
from TextBasedTechRoadMap import *
import PajekUtil
pu = PajekUtil.PajekUtil()
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
g_result = roadMap.queryBasedMainPath_nodeWeight_arcWeight("circulation cooling air temperature control",topN_graph=5,node_Weight=1.0,arc_Weight=10.0)
pu.writeGraph2pajekNetFile(g_result,'query_top5_node1_arc10.net')
'''
# display node abstracts
f = file(gas_serialAddress)
gas = pickle.load(f)
f.close();
f = file(documents_serialAddress)
documents = pickle.load(f)
f.close();
ga_abstract_list = []
for i in g_result.nodes():
    ga_abstract_list.append([g_result.node[i]['ga'],documents[gas.index(g_result.node[i]['ga'])]])
for i in ga_abstract_list:
    print i[0]
    print i[1]
'''


