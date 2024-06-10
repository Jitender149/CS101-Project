import networkx as nx
import pandas as pd
import random
import numpy as np
from collections import deque

def func1(file_path): # Creates graph from the excel sheet
    df = pd.read_excel(file_path)
    G = nx.DiGraph()
    for index, row in df.iterrows():
        node = str(row.iloc[0]).upper()
        if pd.isna(node):
            continue
        G.add_node(node)
        for col in range(1, len(row)):
            node2 = str(row.iloc[col]).upper() 
            if pd.isna(node2) or node2.lower() == "nan":
                continue
            G.add_edge(node, node2)

    return G

def func2(G, source, target, k): # function to check if there exist a path with atmost k nodes same as in shortest path and with path length <= 2*shortest path
    shortest_path = nx.shortest_path(G, source=source, target=target)
    if shortest_path:
        print('Path do exist.')
    else:
        print('No path exist.')
        return None
    shortest_len = nx.shortest_path_length(G, source=source, target=target)
    print(shortest_path)
    queue = deque([(source, [source])])
    # kind of modified bfs
    while queue:
        curr_node, curr_path = queue.popleft()
        if curr_node == target and len(curr_path) <= shortest_len * 2:
            shared_nodes = set(shortest_path) & set(curr_path)
            if len(shared_nodes) <= k+1:
                return curr_path
        for nbr in G[curr_node]:
            if nbr not in curr_path:
                queue.append((nbr, curr_path + [nbr]))
                
    return None

def main():
        file_path = "Impression_Edited_Version.xlsx"
        graph = func1(file_path)
        print("Nodes of the graph:", graph.nodes())
        print("Edges of the graph:", graph.edges())

        # This info (source, target , k) can be changed and seen
        source = '2022MCB1318'
        target = '2022MCB1337'
        k = 2

        path = func2(graph, source, target, k)
        if path:
            print("Path with at most {} shared nodes and not more than double the shortest path:".format(k), path)
        else:
            print("No such path exists.")
        
        

if __name__ == "__main__":
    main()
