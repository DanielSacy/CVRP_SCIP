import pandas as pd
from pyscipopt import Model, quicksum
import numpy as np
import time

from instance_generator import instanSacy, prepare_instance_from_csv_row
from model import sacystation
from print_sol import print_sol, reconstruct_route
from write_LP import writeLP
from plot_graph import plot_graph

def update_csv_with_results(df, results, file_path):
    # # Ensure the columns exist
    # if 'SCIP_Value' not in df.columns:
    #     df['SCIP_Value'] = np.nan
    # if 'SCIP_Route' not in df.columns:
    #     df['SCIP_Route'] = ""
    # if 'SCIP_Runtime' not in df.columns:
    #     df['SCIP_Runtime'] = np.nan
    
    for instance_id, (scip_value, scip_routes, runtime) in results.items():
        first_occurrence_idx = df.index[df['InstanceID'] == instance_id].tolist()[0]
        df.at[first_occurrence_idx, f'SCIP_Value_{len(scip_routes)}'] = scip_value
        df.at[first_occurrence_idx, f'SCIP_Route_{len(scip_routes)}'] = str(scip_routes)
        df.at[first_occurrence_idx, f'SCIP_Runtime_{len(scip_routes)}'] = runtime
    
    df.to_csv(file_path, index=False)

def run_instance(instance_params):
    No, N, M, Arcs, demand, load_capacity, distance = instance_params

    start = time.time()
    model, l = sacystation(No, N, M, Arcs, demand, load_capacity, distance)
    model.optimize()
    end = time.time()

    runtime = (f'{end - start:.4f}')
    runtime = float(runtime)

    sol, _, _, _, objective_value = print_sol(model, demand, distance, Arcs, M, l, runtime, No, N)
    
    model.freeProb()

    # Extract SCIP solution value and route
    scip_value = (f'{objective_value/100:.4f}')
    scip_value = float(scip_value)
    scip_route = reconstruct_route(sol, M)
    
    return scip_value, scip_route, runtime

def main():
    """
    MAIN FUNCTION
    """
    # Define paths
    data_path = r"D:\DAY2DAY\MESTRADO\Codes\GNN\GAT_VRP1\gat_vrp1\src_batch\instances\Nodes3_Instances2.csv"
    # data_path = r"D:\DAY2DAY\MESTRADO\Codes\GNN\GAT_VRP1\gat_vrp1\src_batch\instances\validation\Nodes10_Instances100.csv"
    # data_path = "TSP_test_20_100.CSV"
    
    # Load CSV instances
    df = pd.read_csv(data_path)
    
    # Run SCIP model on each instance and collect results
    results = {}
    for instance_id in df['InstanceID'].unique():
        try:
            instance_params = prepare_instance_from_csv_row(df, instance_id)
            scip_value, scip_route, runtime = run_instance(instance_params)
            results[instance_id] = (scip_value, scip_route, runtime)
            print(f"\nInstance {instance_id} and results: {results[instance_id]}\n")
        except ValueError as e:
            print(e)
    
    # Update the CSV with SCIP results
    update_csv_with_results(df, results, data_path)

if __name__ == "__main__":
    main()