from models.graph_logic import cargar_grafo, info_nodos, calcular_camino_mas_corto

csv_path = "data/rutas_norte_sur.csv"

if __name__ == "__main__":
    G = cargar_grafo(csv_path)
    info_nodos(G)
    
    # Ejemplo de uso: pide origen y destino al usuario
    origen = input("Origen: ").strip().title()
    destino = input("Destino: ").strip().title()
    
    path, distancia, tiempo = calcular_camino_mas_corto(G, origen, destino)
    if path is not None:
        print(f"\nCamino más corto de {origen} a {destino}:")
        print(" → ".join(path))
        print(f"Distancia total: {distancia:.1f} km")
        print(f"Tiempo estimado total: {tiempo:.1f} min")
    else:
        print(f"No existe un camino entre {origen} y {destino}.")
