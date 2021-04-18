# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import os
# from tqdm import tqdm
import shutil


def ensure_dir(path):
    if(not os.path.exists(path)):
        os.makedirs(path)


def label_save(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(str(i) + '\n')


def edge_save(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(str(i[0]) + ', ' + str(i[1]) + '\n')


def get_data():
    data_name = 'BIPARTITE'
    graph_types = os.listdir('./datas')
    if(os.path.exists('./data/' + data_name)):
        shutil.rmtree('./data/' + data_name)
    edge_label = []
    node_label = []
    graph_label = []
    graph_indicator = []
    edges = []
    last_node_idx, graph_idx = 1, 1
    total_edge_num = 0
    fake_edge_num = 0

    for graph in graph_types:
        print('generate datasets of {}...'.format(graph), end='')
        type_idx = graph_types.index(graph)
        files = os.listdir('./datas/{}'.format(graph))
        # for file in tqdm(files):
        for file in files:
            data = np.genfromtxt(
                './datas/{}/{}'.format(graph, file), dtype=int, delimiter='\t', comments='%')
            edge_num = len(data)
            total_edge_num += edge_num
            s_nodes_array = data[:, 0]
            t_nodes_array = data[:, 1]
            s_nodes_set = set(s_nodes_array)
            t_nodes_set = set(t_nodes_array)
            s_nodes_list = list(s_nodes_set)
            t_nodes_list = list(t_nodes_set)
            s_nodes = [s_nodes_list.index(
                i) + last_node_idx for i in s_nodes_array]
            t_nodes_start_idx = max(s_nodes) + 1
            t_nodes = [t_nodes_list.index(
                i) + t_nodes_start_idx for i in t_nodes_array]
            data = np.array([list(i) for i in zip(s_nodes, t_nodes)])
            nodes_set = set(s_nodes)
            nodes_set.update(t_nodes)

            last_node_idx = max(t_nodes) + 1

            for node in set(nodes_set):
                graph_indicator.append(graph_idx)
                node_label.append(0)

            for i in range(edge_num):
                edges.append([s_nodes[i], t_nodes[i]])
                edge_label.append(0)

            nodes_len = len(nodes_set)
            node_matr = np.zeros([nodes_len, nodes_len])
            node_min = min(s_nodes)

            graph_label.append(type_idx)
            graph_idx += 1
        print('finished')
    ensure_dir('./data/')
    ensure_dir('./data/{}/'.format(data_name))
    data_path = './data/{}/{}/raw/'.format(data_name, data_name)
    ensure_dir(data_path)

    data_path = data_path + data_name
    # print('total edge num:{}'.format(total_edge_num))
    # label_save(data_path + '_edge_labels.txt', edge_label)
    label_save(data_path + '_graph_labels.txt', graph_label)
    # label_save(data_path + '_node_labels.txt', node_label)
    label_save(data_path + '_graph_indicator.txt', graph_indicator)

    edge_save(data_path + '_A.txt', edges)
    print('All datasets saved!')

# if __name__ == '__main__':
#     get_data()
