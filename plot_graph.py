import networkx as NX
import matplotlib.pyplot as P

def plot_graph(model, l, No):
    x = model.data  # model.data contains the decision variables
    
    # Initialize the graph
    G = NX.DiGraph()

    # Define the number of vehicles, for example:
    M = range(1, 11)  # If you have 10 vehicles numbered from 1 to 10

    # Get a colormap from matplotlib
    colormap = P.cm.inferno  # You can use 'viridis', 'plasma', 'inferno', 'magma', etc.

    # Normalize the vehicle indices to [0, 1] for color mapping
    vehicle_colors = {m: colormap((m - 1) / (len(M) - 1)) for m in M}

    # Add nodes for customers, depots, and charging stations
    for node in No:  # Assuming No is the set of customer nodes
        G.add_node(node, node_color='lightblue')
    G.add_node(0, node_color='green')  # Depot

    # Add edges based on the model's solution and assign colors based on the vehicle
    edge_colors = []
    for (i, j, m) in x:
            if model.getVal(x[i, j, m]) > 0.5:  # Check if arc is used
                G.add_edge(i, j)
                edge_colors.append(vehicle_colors[m])  # Assign color based on vehicle

    # Plot
    P.clf()
    position = NX.spring_layout(G)  
    
    # Test
        # Collect all annotations for node 0
    annotations = []

    # Mark the load of each vehicle at each node
    for (i, j, m) in x:
        if model.getVal(x[i, j, m]) > 0.5:
            load_value = f'L[{i},{j},{m}]: {model.getVal(l[i, j, m]):.0f}'
            if i == 0:# or j == 0:
                annotations.append(load_value)
            else:
                P.annotate(f'{load_value}', xy=position[i], textcoords='offset points', xytext=(0, 15), ha='center')

    # Add collected annotations to node 0, each on its own line
    if annotations:
        annotation_text = "\n".join(annotations)
        P.annotate(annotation_text, xy=position[0], textcoords='offset points', xytext=(0, 15), ha='center')


    # # Marcar a carga de cada veículo em cada nó
    # for (i, j, m) in x:
    #     if model.getVal(x[i, j, m]) > 0.5:
    #         load_value = f'L[{i},{j},{m}]: {model.getVal(l[i, j, m]):.0f}'
    #         P.annotate(f'{load_value}', xy=position[i], textcoords='offset points', xytext=(0,15), ha='center')

    # Desenhar o grafo
    NX.draw(G, position, with_labels=True, node_size=800, node_color=[G.nodes[node]['node_color'] for node in G.nodes], edge_color=edge_colors)
    P.show()
