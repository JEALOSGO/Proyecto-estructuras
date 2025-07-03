import networkx as nx

def shortest_path_dijkstra(G, origen, destino):
    try:
        # Calcula el camino más corto por distancia
        path = nx.dijkstra_path(G, origen, destino, weight='distancia')
        # Calcula la distancia total
        distancia = nx.dijkstra_path_length(G, origen, destino, weight='distancia')
        # Calcula el tiempo total sumando los eta de las aristas del camino
        tiempo = 0
        for i in range(len(path) - 1):
            tiempo += G[path[i]][path[i+1]]['eta']
        return path, distancia, tiempo
    except nx.NetworkXNoPath:
        return None, float('inf'), float('inf')
