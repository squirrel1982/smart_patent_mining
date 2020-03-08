#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
import pymssql
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
roadMap.loadNetworkFromPajeknet(spc_network_file)
#step2
TopN = 1
# get node number of  topology weight path
topology_weight = 1;
text_weight = 0;
path_list = roadMap.queryBasedMainPath_nodeWeight_arcWeight("circulation cooling air temperature control",\
                                                                arc_Weight=topology_weight)
topN_path_list = get_TOPN_mainPath(TopN,path_list)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result_topology = pu.combine_subGraphArray(subgraphs,roadMap.g)
g_result_topology_gas ="(";
for node in g_result_topology.nodes():
    g_result_topology_gas = g_result_topology_gas+"'"+(g_result_topology.node[node]['ga'])+"',"
g_result_topology_gas= g_result_topology_gas[:-1]+")"

conn=pymssql.connect(host=".",user="sa",password="123",database="car_database")
cursor = conn.cursor();
sql = "select distinct GA,TI,AB from Original_Info where ga in "+g_result_topology_gas
cursor.execute(sql)
m=cursor.fetchall()
#put Pn number into a LIST, DOCUMENT INTO ANother list
for rawdata in m:
    print rawdata[0]
    print rawdata[1]
    print rawdata[2]
conn.close()


