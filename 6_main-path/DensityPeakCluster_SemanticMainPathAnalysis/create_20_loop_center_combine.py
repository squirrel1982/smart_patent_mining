import numpy as np
import cPickle as pickle
loop_num = 100
node_group = [[]for i in range(5)]
node_len_group = [[]for i in range(5)]
raw_coordinate = []
raw_path_index = []
coor_tmp =[]
index_tmp = []
with open('./data/data_main_path/node_num_of_path_list.data', 'r') as f:
    node_num_of_path_list = pickle.load(f)

with open('coordinate_'+str(loop_num)+'_center.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        tmp = line.split(' ')
        if len(tmp)>1:
            coor_tmp.append([float(tmp[1]), float(tmp[2])])
            index_tmp.append(float(tmp[0]))
        else:
            if coor_tmp==[]:
                pass
            else:
                raw_path_index.append(index_tmp)
                raw_coordinate.append(coor_tmp)
                coor_tmp = []
                index_tmp = []
raw_coordinate.append(coor_tmp)
raw_path_index.append(index_tmp)
#raw_coordinate_array = np.array(raw_coordinate)
'''
array_tmp = []
for i in range(20):
    for k in range(5):
        array_tmp = np.zeros(5)
        for j in range(5):
            if i==0:
                tmp = np.linalg.norm(raw_coordinate_array[0,k]-raw_coordinate_array[i,j])
            else:
                tmp = np.linalg.norm(raw_coordinate_array[0, k] - raw_coordinate_array[i, j])
            array_tmp[j] = tmp
        index_tmp = array_tmp.argmin()
        node_group[k].append(raw_coordinate[i][index_tmp])
'''

array_tmp = []
for i in range(loop_num):
    for k in range(5):
        array_tmp = np.zeros(len(raw_coordinate[i]))
        for j in range(len(raw_coordinate[i])):
            tmp = np.linalg.norm(np.array(raw_coordinate[0][k]) - np.array(raw_coordinate[i][j]))
            array_tmp[j] = tmp
        index_tmp = array_tmp.argmin()
        node_len_group[k].append(node_num_of_path_list[int(raw_path_index[i][index_tmp])-1])
        node_group[k].append(raw_coordinate[i][index_tmp])
with open('node_group_'+str(loop_num)+'_loop.data','w') as f:
    pickle.dump(node_group,f)
with open('node_len_group_'+str(loop_num)+'_loop.data','w') as f:
    pickle.dump(node_len_group,f)


