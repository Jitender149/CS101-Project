import pandas as pd
import networkx as nx
import random
import numpy as np
from statistics import mode

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

def func2(G):
    arr = list(G.nodes())  # We make list of the nodes which is stored as arr
    cnt_visits = {node: 0 for node in arr}  # We then initialise the visit cnt for all the nodes
    seen = set()  # This set is to keep track of already visited nodes
    while len(seen) < G.number_of_nodes():
        jk = random.choice(arr)
        seen.add(jk)
        temp = 0
        while temp != 1000000:
            out = list(G.successors(jk))  # Get list of successors of this jk node chosen uniformly at random
            if len(out) == 0:
                jk = random.choice(arr)  # If this is the end so choose by teleportation
            else:
                jk = random.choice(out)
                cnt_visits[jk] += 1  # Update the visit count for the visited node
            seen.add(jk)
            temp += 1

    # Now we get the nodes with the highest visits
    maxi = max(cnt_visits.values())
    most_visited = [node for node, visits in cnt_visits.items() if visits == maxi]
    # here we return
    return cnt_visits, most_visited 

def func(i,j,adj_list):
    # Extract row and column matrix with a_{ij} element deleted from both
    extracted_row = np.delete(adj_list[i,:], j)
    extracted_col = np.delete(adj_list[:, j], i)
                
    # Create a copy of the adjacency matrix with ith row and jth col deleted
    copy = np.delete(np.delete(adj_list, i, axis=0), j, axis=1)

    try:
        X = np.linalg.lstsq(copy, extracted_col, rcond=None)[0] # This is a function from NumPy and solves Ax = b (least sqaure solution)
        # The least square method seeks to find the vector x that minimises the Eucldean norm of residual vector
        missing_val = np.dot(X, extracted_row) # taking dot with the extracted row matrix as stated in the explanation
    except np.linalg.LinAlgError:
            missing_val = 0  # This is to handle where least square method fails

    return missing_val

def func3(G, n):# here we are predicing the links
    adj_list = nx.to_numpy_array(G) # we first convert our graph to adjancency list using numpy
    print("Adjacency list is as follows: ")
    print(adj_list)
    cnt = 0
    for i in range(n):
        for j in range(n): 
            if adj_list[i, j] == 0 and adj_list[j, i] == 0: # the required condition in order to star prediction
                # we are one by one predicting for both (i,j) and (j,i) pair without updating in the original adj_list
                missing_val1 = func(i,j,adj_list)  # calling the func to do the estimation
                missing_val2 = func(j,i,adj_list)
                    
                if missing_val1 > 0:
                    # Updating original adjacency list
                    adj_list[i, j] = 1
                    cnt = cnt+1
                if missing_val2 > 0:
                    # Updating original adjacency list
                    adj_list[j,i] = 1
                    cnt = cnt+1
                # treating both the updation as separate so cnt updated in both case accordingly    
    print(cnt)


def main():
    try:
        file_path = "Impression_Edited_Version.xlsx"
        graph = func1(file_path)# creating the graph from the excel file
        print("Nodes of the graph:", graph.nodes())
        print("Edges of the graph:", graph.edges())

        # Calling for a random walk on the graph
        # returns most visited node and no of visits on that node
        visits, most_visited = func2(graph)
        # Print the most visited nodes
        print("\nMost visited node:")
        for node in most_visited:
            print(f"Node: {node}, Visits: {visits[node]}")

        # Now calling the func3 for predicting the missing links
        no_of_nodes = len(graph.nodes())
        func3(graph,no_of_nodes)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
