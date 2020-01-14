from PajekUtil import *
import cPickle as pickle
from gensim import corpora,models,similarities
import numpy as np
from TextBasedTechRoadMap import *
class PathTopic:
    def __init__(self,texts_serialAddress,gas_serialAddress,lsi_serializationAddress,dictionary_serialAddress,topic_num = 10):
        with open(texts_serialAddress, 'r') as f:
            self.texts = pickle.load(f)
        with open(gas_serialAddress, 'r') as f:
            self.gas = pickle.load(f)
        with open(lsi_serializationAddress, 'r') as f:
            self.index = pickle.load(f)
        with open(dictionary_serialAddress, 'r') as f:
            self.dictionary = pickle.load(f)
        corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        self.topic_number = topic_num;
        self.corpus_lsi_np = self.transformCorpusLsi2Numpy(self.index[corpus_tfidf])

    def transformCorpusLsi2Numpy(self,corpus_index):
        # = np.zeros([corpus_index.__len__(),self.topic_number])
        doc_list_tmp = list()
        for doc in corpus_index:
            if len(doc)==0:
                doc_list_tmp.append([0.0 for i in range(self.topic_number)])
            else:
                doc_list_tmp.append([i[1] for i in doc])

        corpus_index_np = np.array(doc_list_tmp)
        return corpus_index_np;

    def normalize(self,v):
        norm = np.linalg.norm(v)
        if norm ==0:
            return v
        return 1.0*v/norm
    def generatePathTopic(self,path):
        topic_list_tuple = list()
        for nodeID in path.nodes():
            topic_dis_tmp = self.corpus_lsi_np[nodeID-1]
            topic_list_tuple.append(topic_dis_tmp)
        topic_dis_array = np.vstack(tuple(topic_list_tuple))
        return self.normalize(topic_dis_array.sum(axis=0))