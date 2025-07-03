import pandas as pd
import networkx as nx

def cargar_grafo(csv_path):
    df = pd.read_csv(csv_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    G = nx.Graph()

    for _, row in df.iterrows():
        origen = str(row['origen']).strip().title()
        destino = str(row['destino']).strip().title()
        distancia = float(row['distancia(km)'])
        eta = float(row['ETA(min)'])
        G.add_edge(origen, destino, distancia=distancia, eta=eta)
    return G

def info_nodos(G):
    print("NODOS EN EL GRAFO:")
    for nodo in G.nodes():
        vecinos = list(G.neighbors(nodo))
        print(f"→ {nodo} | Grado: {G.degree[nodo]} | Vecinos: {vecinos}")
    print(f"\nCantidad total de nodos: {G.number_of_nodes()}")
