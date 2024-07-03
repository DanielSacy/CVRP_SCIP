import json
import csv

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
    
    return sol, distanceij, demandi, lijm