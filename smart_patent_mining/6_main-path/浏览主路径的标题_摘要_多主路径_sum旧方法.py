#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
import pymssql
import networkx as nx
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
TopN = 5
topology_weight = 0;
text_weight = 1;
roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
#1995105768  1997350223 1998600272 1999193225  1999193226 1999298559 2000372173 2004238335 2005495929  2009K61501 2009K62394
with open(texts_serialAddress,'r') as f:
    texts = pickle.load(f)
roadMap.loadNetworkFromPajeknet(spc_network_file)
roadMap.addLSIWeight2TopologyWeight4ArcInGraph(texts,topology_weight=topology_weight,text_weight=text_weight)
result = roadMap.multi_sources_globalMainPath()

topN_path_list = get_TOPN_mainPath(TopN,result)
subgraphs = [graph[1][1][0] for graph in topN_path_list]
g_result_topology = pu.combine_subGraphArray(subgraphs,roadMap.g)
components_group = nx.weakly_connected_components(g_result_topology)
counter_component = 0
for component in components_group:
    print '--component '+str(counter_component)+' with nodes of '+str(len(component))+'--'
    counter_component+=1;
    g_result_topology_gas ="(";
    for node in component:
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


