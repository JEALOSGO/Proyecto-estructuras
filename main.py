from models.graph_logic import cargar_grafo, info_nodos
from models.graph_view import visualizar_grafo

csv_path = "data/rutas_norte_sur.csv"

if __name__ == "__main__":
    G = cargar_grafo(csv_path)
    info_nodos(G)
    visualizar_grafo(G)
