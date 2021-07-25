# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:15:00 2018

@author: Xing Su
"""
import networkx as nx
import NMI as NMI_fuc
import time
import modularity as modu
import matplotlib.pyplot as plt

def jaccard(gh, node1, node2):
    s1 = set(gh.neighbors(node1))
    s1.add(node1)
    s2 = set(gh.neighbors(node2))
    s2.add(node2)
    s12 = len(s1 & s2)
    return s12 / float(len(s1)+len(s2)-s12)

# phase1: calculate the similarity between two nodes.
def similarities(gh, node1, node2):
    result = jaccard(gh, node1, node2)
    return result

# phase2: calculate the similarity between two groups when merging.
def group_similarities(gh, group1, group2):
    total_similarity = 0.0

    for node1 in group1:
        for node2 in group2:
            if gh.has_edge(node1, node2):
                total_similarity += similarities(gh, node1, node2)

    total_similarity /= len(group2)
    return total_similarity

# phase 2： calculate ratio for each preliminary community
def ratio(gh, group):
    inout_ratio = 0.0
    inner_edge = 0
    out_edge = 0

    for node1 in group:
        N_node1 = gh.neighbors(node1)
        for node2 in N_node1:
            if node2 in group: inner_edge +=1
            else: out_edge +=1
        else: continue

    if out_edge == 0.0:
        inout_ratio = 1000
    else:
        inout_ratio = (inner_edge/(out_edge*2)) * (len(group)/len(gh))

    return inout_ratio


#The first step of NSA，FPC
def InitialMerge(gh):
    sorted_nodes = []
    nodes_degree = dict(graph.degree())
    sorted_degree = sorted(nodes_degree.items(),key=lambda deg:deg[1],reverse=True)

    for i in range(len(sorted_degree)):
        sorted_nodes.append(sorted_degree[i][0])

    merge = []
    for v in sorted_nodes:
        max_similarity = 0
        max_node = ''
        for u in graph.neighbors(v):
            if graph.has_edge(v,u):
                similarity = similarities(graph,v,u)
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_node = u

        if max_node == '':
            continue
        if merge==[] :
            merge.extend([v.split() + max_node.split()])
            sorted_nodes.remove(max_node)

        else:
            merge_index = -1
            for i in range(len(merge)):
                if max_node in merge[i]:
                    merge_index = i
                    break
            if merge_index== -1:
                merge.extend([v.split() + max_node.split()])
                sorted_nodes.remove(max_node)
            else:
                merge[merge_index] = merge[merge_index] + v.split()
    global groups
    groups = merge
    return groups


#The second step of NSA：PCM
def merge_closure_by_ratio(gh):
    closure_ratio = []
    for i in range(len(groups)):
        closure_ratio.append(ratio(gh, groups[i]))
    min_ratio=min(closure_ratio)

    while min_ratio < merge_ratio:
        max_similarity = 0
        max_index = -1
        min_groups_index=closure_ratio.index(min(closure_ratio))
        for j in range(len(groups)):
            if j != min_groups_index :
                total_similarity = group_similarities(gh, groups[min_groups_index], groups[j])
                if total_similarity > max_similarity:
                    max_similarity = total_similarity
                    max_index = j
        groups[max_index]=groups[min_groups_index]+groups[max_index]
        closure_ratio[max_index] = ratio(gh, groups[max_index])
        del closure_ratio[min_groups_index]
        del groups[min_groups_index]

        min_ratio = min(closure_ratio)
    return groups


merge_ratio = 0.1  # Parameter

if __name__ == '__main__':
#    start = time.clock()
    graph = nx.read_pajek("./dataset sample/karate.net")  #ratio range：[0.09, 0.22] the best performance
#    graph = nx.read_pajek("./SmallNetworks/football_12.net")  #ratio range：[0.035, 0.06] the best performance
#    graph = nx.read_pajek("./SmallNetworks/dolphins1.net")   #ratio range：[0.02, 0.031] the best performance
#    graph = nx.read_pajek("./SmallNetworks/riskmap.net")   #ratio range：[0.05, 0.1] the best performance
#    graph = nx.read_pajek("./SmallNetworks/santafe.net")   #ratio range：[0.08, 0.15] the best performance
#    graph = nx.read_pajek("./SmallNetworks/polbooks_id.net")  #ratio range：[0.2, 0.271] the best performance
#    graph = nx.read_pajek("./SmallNetworks/email.net")  #ratio range：[0.043, 0.067] the best performance
#    graph = nx.read_pajek("./SmallNetworks/lesmis.net")  #ratio range：[0.026, 0.097] the best performance
#    graph = nx.read_pajek("./SmallNetworks/YeastL_id.net")  #ratio range：[0.021, 0.022] the best performance
#    graph = nx.read_pajek("./SmallNetworks/com-dblp.ungraph.net")  #ratio range：[0.008] the best performance
#    graph = nx.read_pajek("./SmallNetworks/com-amazon.ungraph.net")   #ratio range：[0.04] the best performance
#    graph = nx.read_pajek("./SmallNetworks/netsience_id.net")#1589
#    graph = nx.read_pajek("./SmallNetworks/ColiNeta.net") # n=423

#    g = nx.read_pajek("./SmallNetworks/PGPgiantcompo.net")
#    graph = g.to_undirected()

#    graph = nx.read_pajek("./LFR-result-net/1000B/mu0.8/LFR-1000B-mu0.8-9.net")
#    graph = nx.read_pajek("./LFR-result-net/1000S/mu0.8/LFR-1000S-mu0.8-9.net")
#    graph = nx.read_pajek("./LFR-result-net/5000B/mu0.4/LFR-5000B-mu0.4-7.net")
#    graph = nx.read_pajek("./LFR-result-net/5000S/mu0.4/LFR-5000S-mu0.4-5.net")

    initial_groups = InitialMerge(graph)
#    print(initial_groups)
    final_groups = merge_closure_by_ratio(graph)
    print(final_groups)

    num = len(final_groups)
    a = [i for i in range(num)]
    communities = dict(zip(a,final_groups))
##    print (communities)
    print ('raio =',merge_ratio, 'Q =', modu.modularity(graph , communities))


###————————————calculate NMI——————————————###
# =============================================================================
#     nodes = graph.nodes()
#     vs = graph.node
#     gt={}
#     for v in nodes:
#         if vs[v]['label'] not in gt:
#             gt[vs[v]['label']] = [v]
#         else:
#             gt[vs[v]['label']] = gt[vs[v]['label']] + [v]
#     print ("NMI=={}".format(NMI_fuc.NMI(gt,communities)))
#
# =============================================================================
