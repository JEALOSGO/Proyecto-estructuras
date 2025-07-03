import networkx as nx

def shortest_path_dijkstra(G, origen, destino):
    """Camino más corto de origen a destino usando Dijkstra"""
    try:
        path = nx.dijkstra_path(G, origen, destino, weight='distancia')
        distancia = nx.dijkstra_path_length(G, origen, destino, weight='distancia')
        tiempo = sum(G[path[i]][path[i+1]]['eta'] for i in range(len(path)-1))
        return path, distancia, tiempo, "Dijkstra"
    except nx.NetworkXNoPath:
        return None, float('inf'), float('inf'), "Dijkstra"

def shortest_paths_from_source_dijkstra(G, origen):
    """Caminos más cortos desde origen a todos los nodos usando Dijkstra"""
    try:
        length, paths = nx.single_source_dijkstra(G, origen, weight='distancia')
        tiempos = {}
        for destino in paths:
            if destino == origen:
                tiempos[destino] = 0
            else:
                tiempo = sum(G[paths[destino][i]][paths[destino][i+1]]['eta'] for i in range(len(paths[destino])-1))
                tiempos[destino] = tiempo
        return length, paths, tiempos, "Dijkstra"
    except Exception as e:
        print(e)
        return {}, {}, {}, "Dijkstra"

    
