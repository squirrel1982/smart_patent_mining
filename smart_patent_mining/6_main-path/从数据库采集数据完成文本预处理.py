import cPickle as pickle
from gensim import corpora,models,similarities
import logging
import cPickle as pickle
#achive text
import pymssql
from PajekUtil import *
pu = PajekUtil()
prefix_address = './data/'
num_topics = 10
pu.loadNetworkFromPajeknet(prefix_address+'deleteLoops_spc_3603.net')
for i in pu.g.nodes():
    if pu.g.node[i]['ga'].find('#') !=-1:
        pu.g.node[i]['ga'] = pu.g.node[i]['ga'].replace('#','')
pu.writeGraph2pajekNetFile(pu.g, prefix_address+'deleteLoops_spc_3603.net')

pu.loadNetworkFromPajeknet(prefix_address+'deleteLoops_3603.net')
gas = []
for i in pu.g.nodes():
    if pu.g.node[i]['ga'].find('#') !=-1:
        pu.g.node[i]['ga'] = pu.g.node[i]['ga'].replace('#','')
    gas.append(pu.g.node[i]['ga'])
pu.writeGraph2pajekNetFile(pu.g,prefix_address+ 'deleteLoops_3603.net')

conn=pymssql.connect(host=".",user="sa",password="123",database="car_database")
cursor = conn.cursor();
sql = "select distinct A.GA,B.AB from cite_13401_network_node_list A,Original_Info B where A.ga = B.GA;"
cursor.execute(sql)
m=cursor.fetchall()
#put Pn number into a LIST, DOCUMENT INTO ANother list

gas_raw = [rawdata[0] for rawdata in m]
documents_raw =[rawdata[1] for rawdata in m]
documents = []
for ga in gas:
    idx = gas_raw.index(ga)
    documents.append(documents_raw[idx])

#lowercase of word
texts_lower = [[word for word in document.lower().split()] for
document in documents]
#remove punctuation--biao dian
from nltk.tokenize import word_tokenize
texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in documents]
#remove stopword
from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')
texts_filtered_stopwords = [[word for word in document if not word
in english_stopwords] for document in texts_tokenized]
#some punctuations havent been removed completely, continues
english_punctuations = [',','.',':','?','(',')','[',']','&','!','*','@','#','$','%']
texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
#extract stem
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]
#remove words only occurred once
all_stems = sum(texts_stemmed, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
dictionary = corpora.Dictionary(texts)
#remove gap in dicitonary
dictionary.compactify()
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=num_topics)
f = file(prefix_address+'text_lsi.data','w')
pickle.dump(lsi,f)
f.close;
f = file(prefix_address+'dictionary.data','w')
pickle.dump(dictionary,f)
f.close;

f = file(prefix_address+'corpus.data','w')
pickle.dump(corpus,f)
f.close;
f = file(prefix_address+'gas.data','w')
pickle.dump(gas,f)
f.close;
index = similarities.MatrixSimilarity(lsi[corpus])
f = file(prefix_address+'index.data','w')
pickle.dump(index,f)
f.close;
f = file(prefix_address+'documents.data','w')
pickle.dump(documents,f)
f.close;

f = file(prefix_address+'texts.data','w')
pickle.dump(texts,f)
f.close;