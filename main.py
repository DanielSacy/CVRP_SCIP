from pyscipopt import Model, quicksum
import numpy as np
import time

from instance_generator import instanSacy
from model import sacystation
from print_sol import print_sol
from write_LP import writeLP
from plot_graph import plot_graph

def run_instance(instance_params):
    No, N, M, Arcs, demand, load_capacity, distance = instance_params

    start = time.time()
    model, l = sacystation(No, N, M, Arcs, demand, load_capacity, distance)
    model.optimize()
    end = time.time()

    runtime = end - start

    print_sol(model, demand, distance, Arcs, M, l, runtime, No, N)
    
    # writeLP(model)
    
    # plot_graph(model, l, No)
    
    model.freeProb()

def main():
    """
    MAIN FUNCTION
    """
    instance_parameters_list = [
    #   (n_customers, n_vehicles, max_demand, max_distance)
        (5, 1, 200, 100),  
        (5, 2, 200, 100),  
        (10, 2, 200, 100),
        (10, 3, 200, 100),
        (15, 3, 200, 100),
        (20, 4, 200, 100)
    ]

    for params in instance_parameters_list:
        instance_params = instanSacy(*params)
        run_instance(instance_params)

if __name__ == "__main__":
    main()