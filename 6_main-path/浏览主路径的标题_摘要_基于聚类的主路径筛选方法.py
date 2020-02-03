#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
import pymssql
#step1
pu = PajekUtil()
subgraph_list_serialAddress = '.\DensityPeakCluster_SemanticMainPathAnalysis\data\data_main_path\subgraph_list.data'
#step2
with open(subgraph_list_serialAddress,'r') as f:
    subgraph_list = pickle.load(f)
# get node number of  topology weight path
cluster_center_index = [1,132,4,77,25]

for center_index in cluster_center_index:

    g_result_topology_gas ="(";
    g_result_topology = subgraph_list[center_index-1]
    print center_index,g_result_topology.number_of_nodes()

    for node in g_result_topology.nodes():
        g_result_topology_gas = g_result_topology_gas+"'"+(g_result_topology.node[node]['ga'])+"',"
    g_result_topology_gas= g_result_topology_gas[:-1]+")"
    pu.writeGraph2pajekNetFile(g_result_topology,'cluster_based_center_main_path_index_'+str(center_index)+'.net')
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


