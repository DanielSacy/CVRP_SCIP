import numpy as np
import json

#Importing constant variables
with open('./input_variables.json', 'r') as file:
    input_variables = json.load(file)

def instanSacy(n_customers, n_vehicles, max_demand, max_distance):
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