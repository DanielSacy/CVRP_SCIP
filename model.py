from pyscipopt import Model, quicksum

def sacystation(No, N, M, Arcs, demand, load_capacity, distance):
    """transp -- model for solving the transportation problem
    Parameters:
        No - set of customers
        N - customers + depot
        A - set of arcs (i,j)
        M - set of vehicles
        demand[i] - demand of customer i
        load_capacity[m] - capacity of vehicle m
        time_cost - Travel time per arc(i,j)

    ==================================
    Problems: Sending m to a charging station
    """
    
    model = Model("sacystation")

    #Binary decision variable
    x = {}
    for (i,j,m) in [(i,j,m) for (i,j) in Arcs for m in M]:
        x[i,j,m] = model.addVar(vtype="B", name=f"x{(i,j,m)}")
        
    #Load Variable
    l = {}
    for (i,j,m) in [(i,j,m) for (i,j) in Arcs for m in M]:
        l[i,j,m] = model.addVar(vtype="C", lb=0, ub=load_capacity[m], name=f"l{(i,j,m)}")
    
    """
    ROUTING CONSTRAINTS
    """
    
    '''
    1.Vehicles m must start their journey on the depot {0} and return to it
    2.Vehicles m must leave the depot to serve a customer 
    3.If vehicle m arrives at a customer it must leave it
    4.Each customer can be visited only once 
    '''
    
    '''
    Each customer is visited only once
    '''
    for i in No:
        model.addCons(quicksum(x[i,j,m] for j in N if (i,j) in Arcs for m in M) == 1, name=f'customer_visiting[{i},{j},{m}]')

    '''
    Tour connectivity
    Flow constraint
    '''  
    for m in M:
        for j in No:
            model.addCons(
                quicksum(x[i,j,m] for i in N if i!=j)
            -   quicksum(x[j,k,m] for k in N if k!=j)
            == (1 if i == 0 else 0)
            ,name=f'tour_connectivity[{i},{j},{m}]'
            )              
    
    '''
    Vehicles tours
    '''
    # if (len(No) - len(M)) < 0:
    if len(No) < len(M):
        for j in No:
            model.addCons(quicksum(x[0, j, m] for m in M) == 1, "num_vehicles_leaving_depot")
    else:
        for m in M:
            model.addCons(quicksum(x[0, j, m] for j in No) == 1, "num_vehicles_leaving_depot")

    '''
    Enforces that the vehicle starts from the depot and returns
    after the tour
    '''  
    for m in M:
        model.addCons(quicksum(x[0,j,m] for j in No) ==
                      quicksum(x[i,0,m] for i in No), name=f'depot_to_depot[{m}]')
                     
    """
    LOAD CONSTRAINTS
    """      
    '''
    Demand Satisfaction
    '''
    for i in No:
        model.addCons((
            quicksum(l[j,i,m]*x[j,i,m] for j in N if (j,i) in Arcs for m in M) -
            quicksum(l[i,k,m]*x[i,k,m] for k in N if (i,k) in Arcs for m in M))
            == demand[i], name=f'demand_satisfaction[{i}]'
            )    

    '''
    Initialize Load at Departure
    This restriction is necessary to ensure that the load at the departure of the vehicle is equal to all visiting nodes
    '''
    for m in M:
        for k in No:
            model.addCons(l[0, k, m] == quicksum(demand[j] * x[i, j, m] for i,j in Arcs),     name=f'init_load_departure[{0},{j},{m}]')
        
    '''
    Vehicle Load Capacity
    ''' 
    for m in M:
        for (i,j) in Arcs:
            model.addCons(demand[j] * x[i,j,m] <= l[i,j,m],     name=f'load_capacity[{i},{j},{m}')     
            model.addCons(l[i,j,m] * x[i,j,m] <= (load_capacity[m] - demand[i])*x[i,j,m]  , name=f'load_capacity[{i},{j},{m}')
  
    """
    Objective Function
    """
    distance_cost = quicksum(distance[i,j]*x[i,j,m] for (i,j) in Arcs for m in M)
    # travel_time_cost = quicksum(input_variables["Ctt"]*time_cost[i,j]*x[i,j,m] for (i,j) in Arcs for m in M)
    
    model.setObjective(distance_cost, "minimize")
    model.optimize()
    model.data = x
    
    return model, l
