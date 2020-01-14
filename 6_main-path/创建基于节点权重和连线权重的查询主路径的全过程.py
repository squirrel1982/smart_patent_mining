#coding = utf-8
from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *

pu = PajekUtil()
#step1
lsi_serializationAddress = "13401_text_lsi.data"
dictionary_serialAddress = "dictionary.data"
gas_serialAddress = "gas.data"
documents_serialAddress = "documents.data"
index_serialAddress = "index.data"
roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
#step2
roadMap.loadNetworkFromPajeknet("13371_deleteLoop_giantComponent_SPC.net")

g_result = roadMap.queryBasedMainPath_nodeWeight_arcWeight("circulation cooling air temperature control")

pu.writeGraph2pajekNetFile(g_result,'query.net')

gas_serialAddress = "gas.data"
documents_serialAddress = "documents.data"
pu = PajekUtil()
pu.loadNetworkFromPajeknet('query.net')
# display node abstracts
f = file(gas_serialAddress)
gas = pickle.load(f)
f.close();
f = file(documents_serialAddress)
documents = pickle.load(f)
f.close();
ga_abstract_list = []
for i in pu.g.nodes():
    ga_abstract_list.append([pu.g.node[i]['ga'],documents[gas.index(pu.g.node[i]['ga'])]])
for i in ga_abstract_list:
    print i[0]
    print i[1]





