import json
import csv

def reconstruct_route(sol, M):
    """
    Reconstruction of the route from the solution.
    """
    routes = {m: [0] for m in M}  # Initialize routes for each vehicle starting at the depot (node 0)
    # route = []

    for m in M:
        current_node = 0
        while True:
            next_node = None
            for key, value in sol.items():
                    print(key, value)
                    i, j, vehicle = map(int, key[2:-1].split(", "))
                    if vehicle == m and i == current_node and value > 0.5:  # Check the current vehicle and node
                        next_node = j  # Set the next node
                        routes[m].append(j)  # Append the next node to the route
                        break  # Exit the loop once we find the next node
            if next_node is None or next_node == 0:
                break
            current_node = next_node
        print(routes)

    return routes  # Start and end with depot
    # return [0] + routes  # Start and end with depot


def print_sol(model, demand, distance, Arcs, M, l, runtime, No, N):
    """
    Print the solution of the model
    """
    x = model.data  # model.data contains the decision variables

    print("_______________________________________________________________________")
    if model.getStatus() == "optimal":
        objective_value = model.getObjVal()
        print("\nOptimal value:", objective_value)
    else:
        print("Problem could not be solved to optimality")
        objective_value = None
    
    sol = {}
    for (i, j, m) in x:
        if model.getVal(x[i, j, m]) > 0.5:
            sol.update({f"x({i}, {j}, {m})":model.getVal(x[i, j, m])})
            
    distanceij = {}
    demandi = {}
    lijm = {}

    for i, j, m in [(i, j, m) for i, j in Arcs for m in M]: 
        if model.getVal(x[i, j, m]) > 0.5:
            distanceij.update({str((i,j)):distance[i,j]})
            demandi.update({str(i):demand[i]})
            lijm.update({str((i,j,m)):model.getVal(l[i,j,m])})

    debug = {
        "Sols":sol,
        "distance": distanceij,
        "demandi": demandi,
        "lijm":lijm,
        "runtime": runtime
    }

    file_path = "./debug.json"
    with open(file_path, "w") as json_file:
        json.dump(debug, json_file, indent=4)
        print(f"\nInput variables have been written to {file_path}\n") 
        print(json.dumps(debug, indent=4))
        
    # Log to CSV file
    csv_file_path = "./cvrp_log.csv"
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Consumidores', 'Veículos', 'Função Objetivo', 'Runtime']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if file is new
        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'Consumidores': len(No),
            'Veículos': len(M),
            'Função Objetivo': f'{objective_value}km',
            'Runtime': f'{runtime:.3f}s'
        })
    

    return sol, distanceij, demandi, lijm, objective_value