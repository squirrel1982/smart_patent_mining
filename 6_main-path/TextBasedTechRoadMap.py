import os
import numpy as np
import logging
import cPickle as pickle
from scipy.spatial import distance
import string
import pymssql
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.cluster import util
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities
import networkx as nx
import logging
import Queue
import copy
from PajekUtil import *
from scipy.sparse import csr_matrix
class TextBasedTechRoadMap:
    def __init__(self,lsi_serializationAddress,dictionary_serialAddress,gas_serialAddress,index_serialAddress):
        self.g=[]
        self.pu = PajekUtil()
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
        f = file(lsi_serializationAddress)
        self.lsi = pickle.load(f)
        f.close;
        f = file(dictionary_serialAddress)
        self.dictionary = pickle.load(f)
        f.close;
        f = file(gas_serialAddress)
        self.gas = pickle.load(f)
        f.close;
        f = file(index_serialAddress)
        self.index = pickle.load(f)
        f.close;
        #remove gap in dicitonary
        # i dont know why this code--> index = similarities.MatrixSimilarity(lsi[corpus])
        self.english_punctuations = [',','.',':','?','(',')','[',']','&','!','*','@','#','$','%']

    def getAbstractByGA(self, ga):
        conn = pymssql.connect(host=".", user="su", password="123", database="car_database")
        cursor = conn.cursor();
        sql = "select ab from Original_Info where ga =\'" + ga + "\'"
        cursor.execute(sql)
        m = cursor.fetchall()
        ab = m[0][0]
        conn.close()
        return ab

    def getSourceNodes(self):
        result = []
        d_in = self.g.in_degree(self.g)
        for n in self.g.nodes():
            if d_in[n]==0:
                result.append(n)
        return result
    def getSimByNodeID(self,nodeID,sims):
        tmp = self.g.node[nodeID]['ga']
        tmp_id = self.gas.index(tmp)
        sim = sims[tmp_id]
        return sim
    def getNodeIDByNodeGA(self, NodeGA):
        result = None
        for n in self.g.nodes():
            if self.g.node[n]['ga'] == NodeGA:
                result = n
                break
        return result

    def getMaxWeightPathInGraph(self, sims):
        l = []
        sourceNodes = self.getSourceNodes()
        for i in sourceNodes:
            tmp = self.getMaxWeightPathBySingleNode(i,sims)
            l.append(tmp)
        l.sort(cmp = lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        #result.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        return l

    def getMaxWeightPathInGraph_returnGraphType_nodeWeight(self, sims):
        '''this function use node weight, which usually is the similarity between
        query text and docs in corpus, to generate query based global main path
        '''
        l = []
        sourceNodes = self.getSourceNodes()
        for i in sourceNodes:
            tmp = self.getMaxWeightPathBySingleNode_graph_nodeWeight(i,sims)
            l.append(tmp)
        l.sort(cmp = lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        #result.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        return l

    def getMaxWeightPathInGraph_returnGraphType_nodeWeight_arcWeight(self, sims,node_weight=1.0,arc_weight=1.0):
        '''this function use node weight, which usually is the similarity between
        query text and docs in corpus, to generate query based global main path

        '''
        l = []
        sourceNodes = self.getSourceNodes()
        for i in sourceNodes:
            tmp = self.getMaxWeightPathBySingleNode_graph_nodeWeight_arcWeight(i, sims,node_weight,arc_weight)
            l.append(tmp)
        l.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        # result.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        return l
    
    def getMaxWeightPathBySingleNode_nodeWeight(self, nodeID, sims):
        '''this function used for generating query based main path,
        Attention! Here only use node weight to search max weight main path
        it searches the path with the max Weight given a source nodeID
        Args:
            nodeID: a given source nodeID.,"circulation cooling air temperature control"
            sims: a list containing the similarites between the query text and every doc in corpus.
        Returns:
            A structure like [path_weight,[12,3,5,namely, node list on the result path]]
        '''
        q = Queue.Queue()
        q.put(nodeID)
        dic = dict()
        dic[nodeID]=[sims[nodeID],[nodeID]]
        while not q.empty():
            tmp = q.get()
            successors = self.g.successors(tmp)
            for i in successors:
                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp3 = copy.copy(dic.get(tmp)[1])
                    tmp3.append(i)
                    dic[i]=[dic.get(tmp)[0]+self.getSimByNodeID(i,sims),tmp3]
                else:
                    tmp2 = dic.get(i)
                    #print "way2"
                    if tmp2[0] < dic.get(tmp)[0]+self.getSimByNodeID(i,sims):
                        tmp3 = copy.copy(dic.get(tmp)[1])
                        tmp3.append(i)
                        dic[i]=[dic.get(tmp)[0]+self.getSimByNodeID(i,sims),tmp3]
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a

    def getMaxWeightPathBySingleNode_graph_nodeWeight(self, nodeID, sims):
        '''this function used for generating query based main path,
        Attention! Here only use node weight to search max weight main path
        it searches the path with the max Weight given a source nodeID
        Args:
            nodeID: a given source nodeID.,"circulation cooling air temperature control"
            sims: a list containing the similarites between the query text and every doc in corpus.
        Returns:
            A structure like [path_weight,[path_1_graph_type,path_2_graph_type]]
            commonly speaking, there is only one path output as result, but if there are two paths
            with identical weight, output them both
        '''
        q = Queue.Queue()
        graph = nx.DiGraph()
        q.put(nodeID)
        dic = dict()
        graph.add_node(nodeID, ga=self.g.node[nodeID]['ga'])
        dic[nodeID]=[self.getSimByNodeID(nodeID,sims),[graph]]
        #dic[nodeID] = [0.0, [graph]]
        while not q.empty():
            tmp = q.get()
            successors = self.g.successors(tmp)
            for i in successors:

                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp4 = copy.deepcopy(dic.get(tmp)[1])
                    for tmp3 in tmp4:
                        tmp3.add_node(i, ga=self.g.node[i]['ga'])
                        tmp3.add_edge(tmp, i)
                    dic[i] = [dic.get(tmp)[0] + self.getSimByNodeID(i,sims), tmp4]
                else:
                    tmp2 = dic.get(i)
                    if tmp2[0] < dic.get(tmp)[0]+self.getSimByNodeID(i,sims):
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = self.g.node[i]['ga'])
                            tmp3.add_edge(tmp,i)
                        dic[i]=[dic.get(tmp)[0]+self.getSimByNodeID(i,sims),tmp4]
                    elif tmp2[0] == dic.get(tmp)[0]+self.getSimByNodeID(i,sims):
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = self.g.node[i]['ga'])
                            tmp3.add_edge(tmp,i)
                        tmp2[1].extend(tmp4)
                        dic[i]=tmp2

        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a

    def getMaxWeightPathBySingleNode_graph_nodeWeight_arcWeight(self, nodeID, sims,node_weight,arc_Weight):
        '''this function used for generating query based main path,
        Attention! Here use both node weight and arc weight to search max weight main path
        it searches the path with the max Weight given a source nodeID
        Args:
            nodeID: a given source nodeID.,"circulation cooling air temperature control"
            sims: a list containing the similarites between the query text and every doc in corpus.
        Returns:
            A structure like [path_weight,[path_1_graph_type,path_2_graph_type]]
            commonly speaking, there is only one path output as result, but if there are two paths
            with identical weight, output them both
        '''
        q = Queue.Queue()
        graph = nx.DiGraph()
        q.put(nodeID)
        dic = dict()
        graph.add_node(nodeID, ga=self.g.node[nodeID]['ga'])
        dic[nodeID]=[self.getSimByNodeID(nodeID,sims)*node_weight,[graph]]
        #dic[nodeID] = [0.0, [graph]]
        while not q.empty():
            tmp = q.get()
            successors = self.g.successors(tmp)
            for i in successors:

                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp4 = copy.deepcopy(dic.get(tmp)[1])
                    for tmp3 in tmp4:
                        tmp3.add_node(i, ga=self.g.node[i]['ga'])
                        tmp3.add_edge(tmp, i,weight = self.g[tmp][i]['weight'])
                    dic[i] = [dic.get(tmp)[0] + arc_Weight*self.g[tmp][i]['weight']+ node_weight*self.getSimByNodeID(i,sims), tmp4]
                else:
                    tmp2 = dic.get(i)
                    if tmp2[0] < dic.get(tmp)[0]+node_weight*self.getSimByNodeID(i,sims)+arc_Weight*self.g[tmp][i]['weight']:
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = self.g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = self.g[tmp][i]['weight'])
                        dic[i]=[dic.get(tmp)[0]+node_weight*self.getSimByNodeID(i,sims)+arc_Weight*self.g[tmp][i]['weight'],tmp4]
                    elif tmp2[0] == dic.get(tmp)[0]+node_weight*self.getSimByNodeID(i,sims)+arc_Weight*self.g[tmp][i]['weight']:
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = self.g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = self.g[tmp][i]['weight'])
                        tmp2[1].extend(tmp4)
                        dic[i]=tmp2

        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a
    #maybe there is some problem in this funtion, since sims is ordered by documents retrieved from database,
    #but nodeID is assigned by pajek network
    def getSimByNodeID_nodeWeight(self,nodeID,sims):
    		return sims[nodeID-1]

    def getMaxWeightPathBySingleNode_nodeWeight_raw(self,nodeID,sims):
        '''this function is used for LLDA
        :param nodeID: given nodeID
        :param sims: #sims is llda.n_m_z[:,mc_id]
        :return: [sum_weight,[1,2,5,namely,nodeIDs of the result path]]
        '''
        q = Queue.Queue()
        q.put(nodeID)
        dic = dict()
        
        dic[nodeID]=[sims[nodeID-1],[nodeID]]
        while not q.empty():
            tmp = q.get()
            successors = self.g.successors(tmp)
            for i in successors:
                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp3 = copy.copy(dic.get(tmp)[1])
                    tmp3.append(i)
                    dic[i]=[dic.get(tmp)[0]+self.getSimByNodeID_nodeWeight(i,sims),tmp3]
                else:
                    tmp2 = dic.get(i)
                    #print "way2"
                    if tmp2[0] < dic.get(tmp)[0]+self.getSimByNodeID_nodeWeight(i,sims):
                        tmp3 = copy.copy(dic.get(tmp)[1])
                        tmp3.append(i)
                        dic[i]=[dic.get(tmp)[0]+self.getSimByNodeID_nodeWeight(i,sims),tmp3]
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a
    def getSimByNodePair(self,g,gas,node1,node2):
        tmp1 = g.node[node1]['ga']
        tmp2 = g.node[node2]['ga']
        tmp_id1 = gas.index(tmp1)
        tmp_id2 = gas.index(tmp2)
        sims = self.computeSimilarityByTermsAndSort()
        sim = sims[tmp_id1]
        result = sim[tmp_id2]
        return result       
    def computeSimilarityByTermsAndSort(self,terms):
        terms = self.preprocess(terms)
        terms_stemmed_bow = self.dictionary.doc2bow(terms)
        terms_stemmed_lsi = self.lsi[terms_stemmed_bow]
        #need to put terms_stemmed_lsi into node's attribution of citation_network
        sims = self.index[terms_stemmed_lsi]
        #sort_sims = sorted(enumerate(sims),key=lambda item:-item[1])
        return sims
    def preprocess(self,terms):
        terms_lower = [word for word in terms.lower().split()]
#remove stopword
        english_stopwords = stopwords.words('english')
        terms_filtered_stopwords = [word for word in terms_lower if not word in english_stopwords]
#some punctuations havent been removed completely, continues
        terms_filtered = [word for word in terms_filtered_stopwords if not word in self.english_punctuations]
#extract stem
        st = LancasterStemmer()
        terms_stemmed = [st.stem(word) for word in terms_filtered] 
        return terms_stemmed
#remove stopword
#check whether serialization file exists 
    def loadNetworkFromPajeknet(self,netAddress):
        G=nx.DiGraph()
        with open(netAddress, 'r') as fp:
          if fp.readline().find("*Vertices")!=-1:
              line = fp.readline()
              #print line
              while line.lower().find("*edges")==-1 and line.lower().find("*arcs")==-1:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  #print b
                  b[1] = b[1].replace('\"','')
                  b[1] = b[1].replace('#', '')
                  G.add_node(int(b[0]),ga = b[1])
                  line = fp.readline()
              line = fp.readline()
              while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']

                  G.add_edge(int(b[0]),int(b[1]),weight=float(b[2]))
                  line = fp.readline()
        self.g = G
    def computeArcWeight4GraphByTextSim(self,g,gas,sims):
        #tranverse all the arc
        arcs = g.edges()
        for arc in arcs:
            sim = self.getSimByNodePair(g,gas,arc[0],arc[1])
            g[arc[0]][arc[1]]['weight'] = sim
    def setArcWeight4GrahphByLSI(self,texts):
        arcs = self.g.edges()
        for arc in arcs:
            tmp_id1 = self.gas.index(self.g.node[arc[0]]['ga'])
            tmp_id2 = self.gas.index(self.g.node[arc[1]]['ga'])
            terms = texts[tmp_id1]
            terms_stemmed_bow = self.dictionary.doc2bow(terms)
            terms_stemmed_lsi = self.lsi[terms_stemmed_bow]
            sims = self.index[terms_stemmed_lsi]
            if sims[tmp_id2]==0.0:
                self.g[arc[0]][arc[1]]['weight'] = 0.001
            self.g[arc[0]][arc[1]]['weight'] = sims[tmp_id2]

    def addLSIWeight2TopologyWeight4ArcInGraph(self,texts,topology_weight=1.0,text_weight=1.0):
        arcs = self.g.edges()
        for arc in arcs:
            tmp_id1 = self.gas.index(self.g.node[arc[0]]['ga'])
            tmp_id2 = self.gas.index(self.g.node[arc[1]]['ga'])
            terms = texts[tmp_id1]
            terms_stemmed_bow = self.dictionary.doc2bow(terms)
            terms_stemmed_lsi = self.lsi[terms_stemmed_bow]
            sims = self.index[terms_stemmed_lsi]
            # as pajek doesn't show the line with weight value of 0, here we set line weight to 0.001 if the weight value is 0
            if topology_weight*self.g[arc[0]][arc[1]]['weight']+text_weight*sims[tmp_id2] ==0.0:
                self.g[arc[0]][arc[1]]['weight'] = 0.001
            else:
                self.g[arc[0]][arc[1]]['weight'] = topology_weight*self.g[arc[0]][arc[1]]['weight']+text_weight*sims[tmp_id2]

            
    def setArcWeight4GrahphByLSIViaSimMatrix(self,corpus):
        arcs = self.g.edges()
        matrix = self.create_sim_matrix(self.lsi,corpus)
        for arc in arcs:
            tmp_id1 = self.gas.index(self.g.node[arc[0]]['ga'])
            tmp_id2 = self.gas.index(self.g.node[arc[1]]['ga'])
            if type(matrix) is csr_matrix:
                sim = matrix[tmp_id1,tmp_id2]
            else:
                sim = matrix[tmp_id1][tmp_id2]
            self.g[arc[0]][arc[1]]['weight'] = sim

    def addyLSIWeight2TopologyWeight4ArcInGrahphViaSimMatrix(self,corpus,topology_weight,text_weight):
        arcs = self.g.edges()
        matrix = self.create_sim_matrix(self.lsi,corpus)
        for arc in arcs:
            tmp_id1 = self.gas.index(self.g.node[arc[0]]['ga'])
            tmp_id2 = self.gas.index(self.g.node[arc[1]]['ga'])
            sim = matrix[tmp_id1][tmp_id2]
            self.g[arc[0]][arc[1]]['weight'] = text_weight*sim+topology_weight*self.g[arc[0]][arc[1]]['weight']
    def create_sim_matrix(self,model,corpus):
        topics =[model[c] for c in corpus]
        dense = np.zeros((len(topics),100),float)
        for ti,t in enumerate(topics):
            for tj,v in t:
                dense[ti,tj] = v
        pairwise = np.nan_to_num(1.0-distance.squareform(distance.pdist(dense,'cosine')))
        return pairwise

    def create_sim_sparse_matrix(self):
        row = []
        col = []
        data = []
        arcs = self.g.edges()
        #add row col and data twice because matrix is symmetric;
        for arc in arcs:
            tmp_id1 = arc[0]-1
            tmp_id2 = arc[1]-1
            row.append(tmp_id1)
            col.append(tmp_id2)
            data.append(self.g[arc[0]][arc[1]]['weight'])
            row.append(tmp_id2)
            col.append(tmp_id1)
            data.append(self.g[arc[0]][arc[1]]['weight'])
            pairwise = csr_matrix((data,(row,col)),shape=(self.g.number_of_nodes(),self.g.number_of_nodes()),dtype = np.float32)
        return pairwise

    def queryBasedMainPath_nodeWeight(self,query_text,topN_graph=1):
        """Create query based main path
        Args:
            query_text: query text,e.g.,"circulation cooling air temperature control"
            topN_graph: combine top N query paths as the result path.
        Returns:
            A networkx.Digraph type value
            """
        retriveResult = self.computeSimilarityByTermsAndSort(query_text)
        maxWeightPath_list = self.getMaxWeightPathInGraph_returnGraphType_nodeWeight(retriveResult)
        subgraph_list = [graph_tmp[1][1] for graph_tmp in maxWeightPath_list[:topN_graph]]
        subgraph_list = sum(subgraph_list,[])
        g_result = self.pu.combine_subGraphArray(subgraph_list, self.g)
        return g_result


    def queryBasedMainPath_nodeWeight_arcWeight(self,query_text,node_Weight=1.0,arc_Weight=1.0):
        """Create query based main path
        Args:
            query_text: query text,e.g.,"circulation cooling air temperature control"
            topN_graph: combine top N query paths as the result path.
        Returns:
            A networkx.Digraph type value
            """
        retriveResult = self.computeSimilarityByTermsAndSort(query_text)
        maxWeightPath_list = self.getMaxWeightPathInGraph_returnGraphType_nodeWeight_arcWeight(retriveResult,node_Weight,arc_Weight)

        return maxWeightPath_list
    def multi_sources_globalMainPath(self):
        '''
        :param spc_network_file: 'deleteLoops_spc_3603.net'
        :param corpus_file: 'corpus.data',it must contains all texts of the nodes,and can be more than that,but not less
                          the order of texts should be consistant with that of gas
        :param topology_weight: 1.0
        :param text_weight: 1.0
        :return: list containing main paths from all source nodes
        '''
        result = []
        sources = self.pu.getSourceNodes(self.g)
        for i in sources:
            result.append(self.pu.getmulti_MaxWeightPathBySingleNode_Graph(i,self.g))
        result.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        return result
    def multi_sources_globalMainPath_textSim_topology_new_sum_method(self,spc_network_file,corpus_file,topology_weight,text_weight):
        '''
        :param spc_network_file: 'deleteLoops_spc_3603.net'
        :param corpus_file: 'corpus.data',it must contains all texts of the nodes,and can be more than that,but not less
                          the order of texts should be consistant with that of gas
        :param topology_weight: 1.0
        :param text_weight: 1.0
        :return: list containing main paths from all source nodes
        '''
        result = []
        self.loadNetworkFromPajeknet(spc_network_file);
        with open(corpus_file,'r') as f:
            corpus = pickle.load(f)
        matrix = self.create_sim_matrix(self.lsi, corpus)
        sources = self.pu.getSourceNodes(self.g)
        for i in sources:
            # result.append(pu.getmulti_MaxWeightPathBySingleNode_Graph(i,roadMap.g,roadMap.gas,sim_matrix))
            result.append(self.pu.getmulti_MaxWeightPathBySingleNode_Graph_newSumMethod_textSim_topology\
                              (i, self.g,self.gas,matrix,semantic_weight= text_weight,topology_weight = topology_weight))
        result.sort(cmp=lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
        return result