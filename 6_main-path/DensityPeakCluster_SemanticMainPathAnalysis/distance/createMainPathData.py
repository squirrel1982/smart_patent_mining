from PajekUtil import *
import cPickle as pickle
from TextBasedTechRoadMap import *
from PathTopic import *
#step 1
# get all main path

num_topics = 10

pu = PajekUtil()
prefix_address = '../../data/'
lsi_serializationAddress = prefix_address+"text_lsi.data"
dictionary_serialAddress = prefix_address+"dictionary.data"
gas_serialAddress = prefix_address+"gas.data"
texts_serialAddress = prefix_address+"texts.data"
corpus_serialAddress = prefix_address+"corpus.data"
documents_serialAddress = prefix_address+"documents.data"
index_serialAddress = prefix_address+"index.data"

# update lsi_index with different topic number
with open(texts_serialAddress,'r') as f:
    texts = pickle.load(f)
with open(dictionary_serialAddress,'r') as f:
    dictionary = pickle.load(f)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=num_topics)
index = similarities.MatrixSimilarity(lsi[corpus])

with open(lsi_serializationAddress,'w') as f:
    pickle.dump(lsi,f)
with open(index_serialAddress,'w') as f:
    pickle.dump(index,f)


roadMap = TextBasedTechRoadMap(lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress)
spc_network_file = prefix_address+'deleteLoops_spc_3603.net'
g_result_raw = roadMap.multi_sources_globalMainPath_textSim_topology_new_sum_method(spc_network_file,corpus_serialAddress,text_weight=1.0,topology_weight=0)

# sum all nodes' topic distribution in one main path and normalize it
pt = PathTopic(texts_serialAddress,gas_serialAddress,lsi_serializationAddress,dictionary_serialAddress)
node_num_of_path_list = []
path_topic_list = []
subgraph_list = []
for graph_tmp in g_result_raw:
    subgraphs = graph_tmp[1][1]
    g_result = pu.combine_subGraphArray(subgraphs, roadMap.g)
    subgraph_list.append(g_result)
    node_num_of_path_list.append(g_result.number_of_nodes())
    path_topic_tmp = pt.generatePathTopic(g_result)
    path_topic_list.append(path_topic_tmp)
#integrate path topic with path length
#normalize path length

max_node_num = max(node_num_of_path_list)
min_node_num = min(node_num_of_path_list)
normalized_node_num_of_path_list = [ 1.0*(i-min_node_num)/(max_node_num-min_node_num) for i in node_num_of_path_list]
normalized_node_num_of_path_array = np.array(normalized_node_num_of_path_list)

path_topic_np  = np.array(path_topic_list)
#integrated_path_topic_np = np.hstack((path_topic_np, normalized_node_num_of_path_np))


#output path topic to file
with open('../data/data_main_path/main_path_topic_T0_S1.data','w') as f:
    for path_topic in path_topic_np:
        f.write(' '.join(path_topic.astype('S6'))+'\n')

with open('../data/data_main_path/node_num_of_path_list.data','w') as f:
    pickle.dump(node_num_of_path_list,f)

with open('../data/data_main_path/normalized_node_num_of_path_array.npy','w') as f:
    np.save(f,normalized_node_num_of_path_array)

with open('../data/data_main_path/subgraph_list.data','w') as f:
    pickle.dump(subgraph_list,f)




# count the number of nodes in one main path


#step 2
# write out the normalized topic distribution in one file
# write out the number of nodes in one file
