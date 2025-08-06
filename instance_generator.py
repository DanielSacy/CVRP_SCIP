import numpy as np
import json

import pandas as pd

#Importing constant variables
with open('./input_variables.json', 'r') as file:
    input_variables = json.load(file)

def instanSacy(n_customers, n_vehicles, max_demand, max_distance):
    '''
    Original aleatory instance generator
    '''
    No = set(np.arange(1,n_customers+1)) #Set of customers
    N = No | {0} #Customers + depot
    
    Arcs = [(i,j) for i in N for j in N if i!=j] #Set of arcs between the nodes
    
    # demand = {i:0 if i == 0 else 100 for i in N} #Demand per customer
    demand = {i: 0 if i == 0 else int(np.random.randint(100, max_demand, 1)[0]) for i in N} #Demand per customer

    M = list(np.arange(1,n_vehicles+1)) #Set of vehicles

    # load_capacity = {m:9073 for m in M} #Load_capacity per vehicle
    load_capacity = {m:input_variables["Qm"] for m in M} #Load_capacity per vehicle
    
    '''Time cost as a function of distance and avg. speed'''
    distance =  {(i,j):int(np.random.randint(50, max_distance, 25)[0]) for i,j in Arcs}
        
    return No, N, M, Arcs, demand, load_capacity, distance  #,time_cost

def prepare_instance_from_csv_row(df: pd.DataFrame, instance_id: str):
    '''
    Instance generator from CSV file used in GAT
    '''
    instance_df = df[df['InstanceID'] == instance_id]
    
    if instance_df.empty:
        raise ValueError(f"No instance found for InstanceID {instance_id}")
    
    # Extracting the number of customers
    # n_customers = len(instance_df['FromNode'].unique()) - 1  # Exclude the depot (assumed to be node 0)
    n_customers = int(instance_id.split('_')[0])  # Assuming 'InstanceID' follows the pattern '{n_customers}_{instance_num}'

    
    # Extracting the number of vehicles
    n_vehicles = 5  # Default, can be manually set

    
    # Extracting demands
    demand = instance_df.groupby('FromNode')['Demand'].first().to_dict()
    demand = {k: (v) for k, v in demand.items()}
    # demand = {k: (v) for k, v in demand.items()}
    
    # Extracting distances
    edge_indices = instance_df[['FromNode', 'ToNode']].values
    # edge_distances = instance_df['Distance'].values
    edge_distances = instance_df['Distance_SCIP'].values
    distance = {(int(i), int(j)): int(dist) for (i, j), dist in zip(edge_indices, edge_distances)}# if i != j}
    # distance = {(i, j): (dist) for (i, j), dist in zip(edge_indices, edge_distances)}
    
    # Extracting arcs
    Arcs = [(int(i), int(j)) for i, j in edge_indices if i != j]
    
    # Extracting serialized fields (only from the first row)
    first_row = instance_df.iloc[0]

    # serialized_distance_matrix = first_row['DistanceMatrix']
    # distance_matrix = np.array(json.loads(serialized_distance_matrix))
    
    
    # Extracting load capacity
    load_capacity_value = instance_df['Capacity'].iloc[0]
    M = set(np.arange(1,n_vehicles+1)) #Set of vehicles
    load_capacity = {m: load_capacity_value for m in M} #Load_capacity per vehicle
    
    # Creating sets and other parameters
    No = set(np.arange(1, n_customers+1)) # Set of customers
    N = No | {0}  # Customers + depot
    
    return No, N, M, Arcs, demand, load_capacity, distance

if __name__ == "__main__":
    data_path = r"GNN\GAT_VRP1\gat_vrp1\src_batch\instances\Nodes3_Instances2.csv"
    # data_path = r"GNN\GAT_VRP1\gat_vrp1\src_batch\instances\validation\Nodes20_Instances100.csv"
    
    df = pd.read_csv(data_path)
    for instance_id in df['InstanceID'].unique():
        try:
            No, N, M, Arcs, demand, load_capacity, distance = prepare_instance_from_csv_row(df, instance_id)
            print(f'No: {No}\nN: {N}\nM: {M}\nArcs: {Arcs}\nDemand: {demand}\nLoad Capacity: {load_capacity}\nDistance: {distance}')
        except ValueError as e:
            print(e)
