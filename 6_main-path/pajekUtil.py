#-*- coding:utf-8 -*-
#pajek util ,create pajek file
import networkx as nx
import copy
import queue_set
from xlwt import Workbook
import Queue
from xgmml import *
#import pymssql
class PajekUtil(object):
    def __init__(self):
        self.g = None
        self.sim_matrix = None
    # create Graph from (sourcenode,endnode) in a txt file
    def createNetFromFile(self,fileAddre):
        G=nx.DiGraph()
        arcs = []
        nodes =[]
        with open(fileAddre, 'r') as fp:
            line = fp.readline()
            while line:
                if line.startswith('\xef\xbb\xbf'):
            		line = line[3:]
                a = line.strip().split(',')
                b = [i.strip() for i in a if i is not '']
                print b
                arcs.append([b[0],b[1]])
                line = fp.readline()
        all_nodes = sum(arcs,[])
        nodes = [i for i in set(all_nodes)]
        for i in range(len(nodes)):
            G.add_node(i+1,ga = nodes[i])
        for i in arcs:
            G.add_edge(nodes.index(i[0])+1,nodes.index(i[1])+1,{'weight':1.0})
        return G
    def createNetFromList(self,pairList):
        G=nx.DiGraph()
        nodes =[]
        all_nodes = sum(pairList,[])
        nodes = [i for i in set(all_nodes)]
        for i in range(len(nodes)):
            G.add_node(i+1,ga = nodes[i])
        for i in pairList:
            G.add_edge(nodes.index(i[0])+1,nodes.index(i[1])+1,{'weight':1.0})
        return G
        
    # arc(node1,node2,weight)
    def createNetViaMatrixWithWeight(self,npArray):
				G=nx.DiGraph()
				#npArray = coocc
				arcs = []
				nodes =[]
				for i in range(npArray.shape[0]):
				    for j in range(i):
				        arcs.append([i+1,j+1,npArray[i,j]])
				        #all_nodes = sum([arc[:2] for arc in arcs],[])
				nodes = [i+1 for i in range(npArray.shape[0])]
				for i in range(len(nodes)):
				    G.add_node(i+1,ga = nodes[i])
				for i in arcs:
				    G.add_edge(nodes.index(i[0])+1,nodes.index(i[1])+1,{'weight':i[2]})
				return G

    def createNetViaPairWithWeight(self,fileAddre):
        G=nx.DiGraph()
        arcs = []
        nodes =[]
        with open(fileAddre, 'r') as fp:
            line = fp.readline()
            while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  arcs.append([b[0],b[1],b[2]])
                  line = fp.readline()
        all_nodes = sum([arc[:2] for arc in arcs],[])
        nodes = [i for i in set(all_nodes)]
        for i in range(len(nodes)):
            G.add_node(i+1,ga = nodes[i])
        for i in arcs:
            G.add_edge(nodes.index(i[0])+1,nodes.index(i[1])+1,weight=i[2])
        return G

    # list format [sourcenode,endnode,reltype]
    # notice:reltype is Integer
    def createNetWithRelTypeFromList(self,tripleList):
        G=nx.DiGraph()
        arcs = []
        nodes =[]
        all_nodes = sum([arc[:2] for arc in tripleList],[])
        nodes = [i for i in set(all_nodes)]
        for i in range(len(nodes)):
            G.add_node(i+1,ga = nodes[i])
        for i in tripleList:
            G.add_edge(nodes.index(i[0])+1,nodes.index(i[1])+1,type=i[2])
        return G


    # create partition for indicating entity type,and finally output file
    #entityType_list format [entity,type]
    # notice:entitytype is Integer
    # notice:entitytype_list may larger than e.nodes() as a result of isolation nodes existing in network
    def createPartition4EntityTypeFromList(self,g,entityType_list,fileAddre):
        partition = [0 for i in range(len(g.nodes()))]

        for i in g.node.keys():
            #partition.append(0)
            for j in range(len(entityType_list)):
                if entityType_list[j][0] == g.node[i]['ga']:
                    partition[i-1] = entityType_list[j][1]
                    break;
        with open(fileAddre, 'w') as fp:
            fp.write("*Vertices "+str(len(g))+"\n")
            for i in range(len(partition)):

                fp.write(str(partition[i])+"\n")
    # 20191007:update this function
    # 1.add paramter edgeType to indicate whether the output network is directed or not
    # 2.decide whether the network is weighted or not,edge is classified or not
    # networkType = {'Arcs','Edges'}
    def writeGraph2pajekNetFile(self,g,fileAddre,networkType='Arcs'):

        nodes = g.nodes()
        edges = g.edges()
        edges_list = []
        type_dict = {}
        #what this type_dict store is key = type,value = [[head node，tail node，weight][...]]

        for i in g.edges():
            if g[i[0]][i[1]].get('weight', -1.0) != -1.0:
                edge_tmp = str(nodes.index(i[0]) + 1) + " " + str(nodes.index(i[1]) + 1) + " "\
                            + str(g[i[0]][i[1]]['weight'])
            else:
                edge_tmp = str(nodes.index(i[0]) + 1) + " " + str(nodes.index(i[1]) + 1) + " " + str(
                    1.0)

            if g[i[0]][i[1]].get('type',-1.0)!=-1.0:
                type_tmp = g[i[0]][i[1]]['type']
                if type_dict.get(type_tmp,[])==[]:
                    type_dict[type_tmp]=[]
                type_dict[type_tmp].append(edge_tmp)
            else:
                edges_list.append(edge_tmp)

        with open(fileAddre, 'w') as fp:
            fp.write("*Vertices "+str(len(g))+"\n")
            for i in range(len(nodes)):
                fp.write(str(i+1)+" \""+str(g.node[nodes[i]]['ga'])+"\" 0.0 0.0 0.0\n")

            # check edge of network

            if edges_list!=[]:
                if networkType == 'Arcs':
                    fp.write("*Arcs \n")
                elif networkType == 'Edges':
                    fp.write("*Edges \n")
                else:
                    raise Exception, networkType + " is an Invalid type of Network!"
            	for str_tmp in edges_list:
                    fp.write(str_tmp+"\n")
            else:
                assert type_dict!={}
                for type_tmp in type_dict.keys():
                    if networkType == 'Arcs':
                        fp.write("*Arcs :"+ str(type_tmp) +"\n")
                    elif networkType == 'Edges':
                        fp.write("*Edges :"+ str(type_tmp) +"\n")
                    else:
                        raise Exception, networkType + " is an Invalid type of Network!"
                    for str_tmp in type_dict[type_tmp]:
                        fp.write(str_tmp + "\n")

    def writeGraph2CytoscapeXGMML(self,g,output_file_addr):

        with open(output_file_addr, 'w') as fid:
            addHead(fid, 'network')
            for nodeID in g.vs:
                addNode(fid, nodeID['name'], nodeID.index, fill='#007FFF', shape='RECTANGLE')
            for edge in g.get_edgelist():
                addEdge(fid, edge[0], edge[1], str(edge[0]) + ' to ' + str(edge[1]), SourceArrowShape='NONE',
                        TargetArrowShape='ARROW', )
            fid.write('</graph>\n')
    def writeNodeAttOfCytoscape2file(self,g,output_file_addr):

        with open(output_file_addr, 'w') as f:
            f.write('node_type' + '\n')
            for nodeID in g.nodes():
                f.write(g.node[nodeID]['ga'] + '=' + str(g.node[nodeID]['type']) + '\n')

    def writeEdgeAttOfCytoscape2file(self, g, output_file_addr):
        with open(output_file_addr, 'w') as f:
            f.write('edge_type' + '\n')
            for edge in g.edges():
                f.write(
                    g.node[edge[0]]['ga'] + '(pp)' + g.node[edge[1]]['ga'] + '=' + str(g[edge[0]][edge[1]]['type']) + '\n')
    def writeGraph2CytoscapeCSV(self,g,output_file_addr):
        with open(output_file_addr, 'w') as f:
            for edge in g.edges():
                f.write(g.node[edge[0]]['ga'] + '\t' + g.node[edge[1]]['ga'] + '\t' + str(
                    g[edge[0]][edge[1]]['type'])  + '\n')
                '''
                f.write(g.vs[edge[0]]['name'] + '\t' + g.vs[edge[1]]['name'] + '\t' + str(
                    g.es.find(_source=edge[0], _target=edge[1])['weight']) + '\t' + str(
                    g.vs[edge[0]]['weight']) + '\t' + str(g.vs[edge[1]]['weight']) + '\n')
                '''

    #debugged
    
    def getMaxWeightPathBySingleNode(self,nodeID):
        q = Queue.Queue()
        q.put(nodeID)
        dic = dict()
        dic[nodeID]=[0.0,[nodeID]]
        while not q.empty():
            tmp = q.get()
            successors = self.g.successors(tmp)
            for i in successors:
                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp3 = copy.copy(dic.get(tmp)[1])
                    tmp3.append(i)
                    dic[i]=[dic.get(tmp)[0]+self.g[tmp][i]['weight'],tmp3]
                else:
                    tmp2 = dic.get(i)
                    #print "way2"
                    if tmp2[0] < dic.get(tmp)[0]+self.g[tmp][i]['weight']:
                        tmp3 = copy.copy(dic.get(tmp)[1])
                        tmp3.append(i)
                        dic[i]=[dic.get(tmp)[0]+self.g[tmp][i]['weight'],tmp3]
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a
    # given file including pns,then create Partition 
    def createPartitionByLabelsListFile(self,g,fileAddre,fileAddre_1):
        partition = []
        nodes =[]
        with open(fileAddre, 'r') as fp:
            line = fp.readline()
            while line:
                  a = line.strip().find(',')
                  b = line[:a]
                  nodes.append(b.strip())
                  line = fp.readline()   
        for i in range(len(g.nodes())):
            partition.append(0)
            for j in range(len(nodes)):
                if nodes[j] == g.node[i]['ga']:
                    partition[i] = 1
                    break;
        with open(fileAddre_1, 'w') as fp:
            fp.write("*Vertices "+str(len(g))+"\n")
            for i in range(len(partition)):
                print(partition[i]+"\n")
                fp.write(partition[i]+"\n")


    # given parent net and child net,create Partition  signaling child nodes in parent net
    def createPartitionByNetFile(self,ParentNetFile,ChildNetFile,partitionFile):
        g1 = self.getGraphFromPajeknet(ParentNetFile)
        g2 = self.getGraphFromPajeknet(ChildNetFile)
        
        partition = []
        for i in range(len(g1.nodes())):
            partition.append(0)
            for j in range(len(g2.nodes())):
                if g2.node[j+1]['ga'] == g1.node[i+1]['ga']:
                    partition[i] = 1
                    break;
        with open(partitionFile, 'w') as fp:
            fp.write("*Vertices "+str(len(g1))+"\n")
            for i in range(len(partition)):
                fp.write(str(partition[i])+"\n")
    #return [weight,graph]
    def getMaxWeightPathBySingleNode_Graph(self,nodeID,g):
        q = Queue.Queue()
        graph = nx.DiGraph()
        q.put(nodeID)
        dic = dict()
        graph.add_node(nodeID,ga = g.node[nodeID]['ga'])
        dic[nodeID]=[0.0,graph]
        while not q.empty():
            tmp = q.get()
            successors = g.successors(tmp)
            for i in successors:
                if dic.get(i) is None:
                    q.put(i)
                    tmp3 = copy.deepcopy(dic.get(tmp)[1])
                    tmp3.add_node(i,ga = g.node[i]['ga'])
                    tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                    dic[i]=[dic.get(tmp)[0]+g[tmp][i]['weight'],tmp3]
                else:
                    tmp2 = dic.get(i)
                    if tmp2[0] < dic.get(tmp)[0]+g[tmp][i]['weight']:
                        tmp3 = copy.deepcopy(dic.get(tmp)[1])
                        tmp3.add_node(i,ga = g.node[i]['ga'])
                        tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                        dic[i]=[dic.get(tmp)[0]+g[tmp][i]['weight'],tmp3]
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        a = result[0]
        return a
    #if there exists multiple maxWeight path,draw them all
    #(3561, [4.200226000000001, [graph1,graph2,......]])
    def getmulti_MaxWeightPathBySingleNode_Graph(self,nodeID,g):
        q = Queue.Queue()
        graph = nx.DiGraph()
        q.put(nodeID)
        dic = dict()
        graph.add_node(nodeID,ga = g.node[nodeID]['ga'])
        dic[nodeID]=[0.0,[graph]]
        while not q.empty():
            tmp = q.get()
            successors = g.successors(tmp)
            for i in successors:

                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp4 = copy.deepcopy(dic.get(tmp)[1])
                    
                    for tmp3 in tmp4: 
                        tmp3.add_node(i,ga = g.node[i]['ga'])
                        tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                    dic[i]=[dic.get(tmp)[0]+g[tmp][i]['weight'],tmp4]
                else:
                    tmp2 = dic.get(i)
                    #print "way2"
                    if tmp2[0] < dic.get(tmp)[0]+g[tmp][i]['weight']:
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                        dic[i]=[dic.get(tmp)[0]+g[tmp][i]['weight'],tmp4]
                    elif tmp2[0] == dic.get(tmp)[0]+g[tmp][i]['weight']:
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                        tmp2[1].extend(tmp4)
                        dic[i]=tmp2
                '''
                for k in dic:
                    print "dict[%s]=" % k,dic[k][0]
                    for s in dic[k][1]:
                        print s.edges()
                '''
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        return result[0]
        

    #if there exists multiple maxWeight path,draw them all
    #(3561, [4.200226000000001, [graph1,graph2,......]])
    def getmulti_MaxWeightPathBySingleNode_Graph_newSumMethod(self,nodeID,g,gas,sim_matrix):
        q = Queue.Queue()
        graph = nx.DiGraph()
        q.put(nodeID)
        dic = dict()
        graph.add_node(nodeID,ga = g.node[nodeID]['ga'])
        dic[nodeID]=[0.0,[graph]]
        while not q.empty():
            tmp = q.get()
            successors = g.successors(tmp)
            for i in successors:

                if dic.get(i) is None:
                    #print "way1"
                    q.put(i)
                    tmp4 = copy.deepcopy(dic.get(tmp)[1])
                    
                    tmp_value = self.internode_sum_distance(g,gas,tmp4[0].nodes(),i,sim_matrix)
                    for tmp3 in tmp4: 
                        tmp3.add_node(i,ga = g.node[i]['ga'])
                        tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                    dic[i]=[dic.get(tmp)[0]+tmp_value,tmp4]
                    
                    #need change
                else:
                    tmp2 = dic.get(i)
                    #print "way2"
                    tmp_value = self.internode_sum_distance(g,gas,dic.get(tmp)[1][0].nodes(),i,sim_matrix)
                    if tmp2[0] < dic.get(tmp)[0]+tmp_value:
                    #need change
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                        dic[i]=[dic.get(tmp)[0]+tmp_value,tmp4]
                        #need change
                    elif tmp2[0] == dic.get(tmp)[0]+tmp_value:
                        #need change
                        tmp4 = copy.deepcopy(dic.get(tmp)[1])
                        for tmp3 in tmp4:
                            tmp3.add_node(i,ga = g.node[i]['ga'])
                            tmp3.add_edge(tmp,i,weight = g[tmp][i]['weight'])
                        tmp2[1].extend(tmp4)
                        dic[i]=tmp2
                '''
                for k in dic:
                    print "dict[%s]=" % k,dic[k][0]
                    for s in dic[k][1]:
                        print s.edges()
                '''
        result = sorted(dic.items(),lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        return result[0]
    # this function compute sum of distance in a dataset "sources" to a given node "target" in graph g  
    # and return sum value
    def internode_sum_distance(self,g,gas,sources,target,sim_matrix):
        sum_value =0.0
        tmp_id1 = gas.index(g.node[target]['ga'])
        for source in sources:
            tmp_id2 = gas.index(g.node[source]['ga'])
            sim = sim_matrix[tmp_id1][tmp_id2]
            sum_value=sum_value+sim
        return sum_value
    # I NEED A MATRIX FULL OF DISTANCE FROM ONE NODE TO THE OTHER,THe function below do this job

    # return a path,but it need some mends,cos forks are excluded in this function
    #debugged
    def globalMainPath(self):
        l = []
        sourceNodes = self.getSourceNodes(self.g)
        for i in sourceNodes:
            tmp = self.getMaxWeightPathBySingleNode(i)
            l.append(tmp)
        result = sorted(l,lambda x,y:cmp(x[1][0],y[1][0]),reverse=True)
        return result
    
    
    #debugged
    def multi_sources_globalMainPath(self,g):
        resultGraph = nx.DiGraph()
        sub_graphs = []
        sourceNodes = self.getSourceNodes(g)
        for i in sourceNodes:
            tmp = self.getmulti_MaxWeightPathBySingleNode_Graph(i,g)
            sub_graphs.extend(tmp[1][1])
        nodes = []
        edges=[]
        for i in sub_graphs:
            nodes.extend(i.nodes())
            edges.extend(i.edges())
        nodes = [i for i in set(nodes)]
        edges = [i for i in set(edges)]
        resultGraph.add_nodes_from(nodes)
        resultGraph.add_edges_from(edges)
        for i in resultGraph.nodes():
            resultGraph.node[i]['ga'] = g.node[i]['ga']
        for i in resultGraph.edges():
            resultGraph.edge[i[0]][i[1]]['weight'] = g.edge[i[0]][i[1]]['weight']
        return resultGraph

    #debugged
    def loadNetworkFromPajeknet(self,netAddress):
        G=nx.DiGraph()
        with open(netAddress, 'r') as fp:
          if fp.readline().lower().find("*vertices")!=-1:
              line = fp.readline()
              #print line
              while line.lower().find("*edges")==-1:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  #print b,len(b)
                  
                  b[1] = b[1].replace('\"','')
                  G.add_node(int(b[0]),ga = b[1])
                  line = fp.readline()
              line = fp.readline()
              while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  G.add_edge(int(b[0]),int(b[1]),weight=float(b[2]))
                  line = fp.readline()
        self.g = G

    def loadNetworkFromPajeknetWithMultipleRelType(self, netAddress):
        G = nx.DiGraph()
        with open(netAddress, 'r') as fp:
            if fp.readline().lower().find("*vertices") != -1:
                line = fp.readline()
                #print line
                while line.lower().find("*arcs") == -1:
                    a = line.strip().split(' ')
                    b = [i for i in a if i is not '']
                    #print b, len(b)

                    b[1] = b[1].replace('\"', '')
                    G.add_node(int(b[0]), ga=b[1])
                    line = fp.readline()
                line = line.replace('"','')
                current_type = int(line[line.find(':')+1:].strip())
                line = fp.readline()
                while line:
                    if line.lower().find("*arcs") == -1:
                        a = line.strip().split(' ')
                        b = [i for i in a if i is not '']
                        G.add_edge(int(b[0]), int(b[1]), weight=float(b[2]),type = current_type)
                        line = fp.readline()
                    else:
                        line = line.replace('"', '')
                        current_type = int(line[line.find(':') + 1:].strip())
                        line = fp.readline()
        return G
        
    #debugged
    def getGraphFromPajeknet(self,netAddress):
        G=nx.DiGraph()
        with open(netAddress, 'r') as fp:
          if fp.readline().lower().find("*vertices")!=-1:
              line = fp.readline()
              print line
              while line.lower().find("*arcs")==-1:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  #print b
                  b[1] = b[1].replace('\"','')
                  G.add_node(int(b[0]),ga = b[1])
                  line = fp.readline()
              line = fp.readline()
              while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  G.add_edge(int(b[0]),int(b[1]),weight=float(b[2]))
                  line = fp.readline()
        return G

    def addPartition2Graph(self,g,partition,partition_name):
        for i in g.nodes():
            g.node[i][partition_name]=partition[i-1]
        return g

    def convertPajek2Cytoscape(self,pajek_net,pajek_par,cyto_csv,cyto_node,cyto_edge):
        g = self.loadNetworkFromPajeknetWithMultipleRelType(pajek_net)
        par = self.loadPartitionFromClu(pajek_par)
        g = self.addPartition2Graph(g,par,'type')

        self.writeGraph2CytoscapeCSV(g, cyto_csv)
        self.writeNodeAttOfCytoscape2file(g, cyto_node)
        self.writeEdgeAttOfCytoscape2file(g, cyto_edge)


    def loadNetworkFromPajeknet_edges(self,netAddress):
        G=nx.DiGraph()
        with open(netAddress, 'r') as fp:
          if fp.readline().lower().find("*vertices")!=-1:
              line = fp.readline()
              print line
              while line.lower().find("*edges")==-1:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  #print b
                  b[1] = b[1].replace('\"','')
                  G.add_node(int(b[0]),ga = b[1])
                  line = fp.readline()
              line = fp.readline()
              while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  G.add_edge(int(b[0]),int(b[1]),weight=float(b[2]))
                  line = fp.readline()
        self.g = G
    #return list
    def loadPartitionFromClu(self,netAddress):
        l=[]
        with open(netAddress, 'r') as fp:
          if fp.readline().lower().find("*vertices")!=-1:
              line = fp.readline()
              while line:
                  a = line.strip().split(' ')
                  b = [i for i in a if i is not '']
                  l.append(b[0])
                  line = fp.readline()
        return l
    #create node_label-partition map,and write to excel
    def writeLabel_par_map_2_txt(self,g,clu,fileAddre):
        label_par_map = []
        for i in g.nodes():
            label_par_map.append([g.node[i]['ga'],clu[i-1]])
        label_par_map.sort(cmp=lambda x,y: cmp(x[1], y[1]), reverse=False)
        #judge whether dict exist
        with open(fileAddre,'w') as writeFile:
            for i in range(len(label_par_map)):
                writeFile.write(label_par_map[i][1]+','+label_par_map[i][0]+'\n')
    def createPartitionByList(self,g,list,fileAddr):
        with open(fileAddr, 'w') as fp:
            fp.write("*Vertices "+str(len(g))+"\n")
            for i in range(len(g)):
                if i+1 in list:
                    fp.write(str(1)+"\n")
                else:
                    fp.write("0\n")
                    
    def getSourceNodes(self,graph):
        result = []
        d_in = graph.in_degree(graph)
        for n in graph.nodes():
            if d_in[n]==0:
                result.append(n)
        return result
    # return a graph
    def multipleMaInPath(self):
        pass
    #debugged
    def localMainPath(self,graph):
        queue = queue_set.Queue_Set()
        sources = self.getSourceNodes(graph)
        result_g =nx.DiGraph()
        maxSuccessorLists = []
        for i in sources:    
            tmp_max_endNodes = self.getMaxWeightArcFromSrc(graph,i)
            if len(maxSuccessorLists)==0:
                maxSuccessorLists.append([i,tmp_max_endNodes])
                value_tmp = tmp_max_endNodes[0]
            elif value_tmp<tmp_max_endNodes[0]:
                maxSuccessorLists=[]
                maxSuccessorLists.append([i,tmp_max_endNodes])
                value_tmp = tmp_max_endNodes[0]
            elif value_tmp==tmp_max_endNodes[0]:
                maxSuccessorLists.append([i,tmp_max_endNodes])
        
# maxSuccessorLists STRUCTURE:[[5, [0.083333333, [1, 2]]], [8, [0.083333333, [1]]], [9, [0.083333333, [1, 2, 4]]]]
        for i in maxSuccessorLists:
            result_g.add_node(i[0],ga=graph.node[i[0]]['ga'])
            for j in i[1][1]:
                result_g.add_node(j,ga=graph.node[j]['ga'])
                queue.put(j)
                result_g.add_edge(i[0],j,{'weight': graph[i[0]][j]['weight']})
        
        while queue.isEmpty()==False:
            src = queue.get()
            tmp_max_endNodes = self.getMaxWeightArcFromSrc(graph,src)
            for i in tmp_max_endNodes[1]:
                result_g.add_node(i,ga=graph.node[i]['ga'])
                result_g.add_edge(src,i,{'weight': graph[src][i]['weight']})
                queue.put(i)
        
        return result_g 
    #return graph
    #debugged
    def getMaxWeightArcFromSrc(self,graph,src):
        successors = graph.successors(src)
        result_tmp = []
        value_tmp = 0.0
        for i in successors:
            if graph[src][i]['weight']>value_tmp:
                if len(result_tmp)>0:
                    result_tmp = []
                value_tmp = graph[src][i]['weight']
                result_tmp.append(i)
            elif graph[src][i]['weight']==value_tmp:
                result_tmp.append(i)
        return [value_tmp,result_tmp]
        
        
#debugged
    def localMainPathFromOneSource(self,graph,i):
        queue = queue_set.Queue_Set()
        result_g =nx.DiGraph()
        maxSuccessorLists = [] 
        tmp_max_endNodes = self.getMaxWeightArcFromSrc(graph,i)
        maxSuccessorLists.append([i,tmp_max_endNodes])
        
# maxSuccessorLists STRUCTURE:[[5, [0.083333333, [1, 2]]], [8, [0.083333333, [1]]], [9, [0.083333333, [1, 2, 4]]]]
        for i in maxSuccessorLists:
            result_g.add_node(i[0],ga=graph.node[i[0]]['ga'])
            for j in i[1][1]:
                result_g.add_node(j,ga=graph.node[j]['ga'])
                print result_g.node[j]['ga']
                queue.put(j)
                result_g.add_edge(i[0],j,{'weight': graph[i[0]][j]['weight']})
        
        while queue.isEmpty()==False:
            src = queue.get()
            tmp_max_endNodes = self.getMaxWeightArcFromSrc(graph,src)
            for i in tmp_max_endNodes[1]:
                result_g.add_node(i,ga=graph.node[i]['ga'])
                print result_g.node[i]['ga']
                result_g.add_edge(src,i,{'weight': graph[src][i]['weight']})
                queue.put(i)
        
        return result_g 
    def getSubGraphByOneSource(self,graph,sourceNode):
        q = Queue.Queue()
        q.put(sourceNode)
        sub_g = nx.DiGraph()
        sub_g.add_node(sourceNode)
        while not q.empty():
            src = q.get()
            #judge if subgraph has this node
            successors= graph.successors(src)
            for i in successors:
                if sub_g.has_node(i)==False:
                    sub_g.add_node(i)    
                    q.put(i)
                if sub_g.has_edge(src,i)==False:
                    sub_g.add_edge(src,i,weight = graph[src][i]['weight'])
        return sub_g
        
    def multiSourcePath(self,g):
        sources = self.getSourceNodes(g)
        sub_graphs = []
        resultGraph =nx.DiGraph()
        for i in sources:
            g_tmp =self.localMainPathFromOneSource(g,i)
            sub_graphs.append(copy.deepcopy(g_tmp))
        
        nodes = []
        edges=[]
        for i in sub_graphs:
            nodes.extend(i.nodes())
            edges.extend(i.edges())
        nodes = [i for i in set(nodes)]
        edges = [i for i in set(edges)]
        resultGraph.add_nodes_from(nodes)
        resultGraph.add_edges_from(edges)
        for i in resultGraph.nodes():
            resultGraph.node[i]['ga'] = g.node[i]['ga']
        for i in resultGraph.edges():
            resultGraph.edge[i[0]][i[1]]['weight'] = g.edge[i[0]][i[1]]['weight']
        return resultGraph
    #input parameter:[sub_graph1,sub_graph2,sub_graph3,.......]
    #output:[[weight_sum_sub1,sub_graph_1],[weight_sum_sub2,sub_graph_2],...]
    def sort_subGraph(self,sub_graphs):
        result = []
        for sub_graph in sub_graphs:
            sum = 0.0
            for arc in sub_graph.edges():
                sum+= sub_graph[arc[0]][arc[1]]['weight']
            result.append([sum,sub_graph])
        result.sort(cmp=lambda x,y: cmp(x[0], y[0]), reverse=True)
        return result
    def combine_subGraph(self,sub_graphs,g):
        resultGraph =nx.DiGraph()
        nodes = []
        edges=[]
        for i in sub_graphs:
            nodes.extend(i[1].nodes())
            edges.extend(i[1].edges())
        nodes = [i for i in set(nodes)]
        edges = [i for i in set(edges)]
        resultGraph.add_nodes_from(nodes)
        resultGraph.add_edges_from(edges)
        for i in resultGraph.nodes():
            resultGraph.node[i]['ga'] = g.node[i]['ga']
        for i in resultGraph.edges():
            resultGraph.edge[i[0]][i[1]]['weight'] = g.edge[i[0]][i[1]]['weight']
        return resultGraph
    #[sub_graph1,sub_graph2,......]
    def combine_subGraphArray(self,sub_graphs,g):
        resultGraph =nx.DiGraph()
        nodes = []
        edges=[]
        for i in sub_graphs:
            nodes.extend(i.nodes())
            edges.extend(i.edges())
        nodes = [i for i in set(nodes)]
        edges = [i for i in set(edges)]
        resultGraph.add_nodes_from(nodes)
        resultGraph.add_edges_from(edges)
        for i in resultGraph.nodes():
            resultGraph.node[i]['ga'] = g.node[i]['ga']
        for i in resultGraph.edges():
            resultGraph.edge[i[0]][i[1]]['weight'] = g.edge[i[0]][i[1]]['weight']
        return resultGraph
    # combine [[0.56,[subgraph1,subgraph2],[0.55,[subgraph3,subgraph4]]]
    def combine_multisubGraph(self,sub_graphs,g):
        resultGraph =nx.DiGraph()
        nodes = []
        edges=[]
        for i in sub_graphs:
            for j in i[1]:
                nodes.extend(j.nodes())
                edges.extend(j.edges())
        nodes = [i for i in set(nodes)]
        edges = [i for i in set(edges)]
        resultGraph.add_nodes_from(nodes)
        resultGraph.add_edges_from(edges)
        for i in resultGraph.nodes():
            resultGraph.node[i]['ga'] = g.node[i]['ga']
        for i in resultGraph.edges():
            resultGraph.edge[i[0]][i[1]]['weight'] = g.edge[i[0]][i[1]]['weight']
        return resultGraph
