import matplotlib.pyplot as plt
import networkx as nx

def visualizar_grafo(G):
    pos = nx.kamada_kawai_layout(G, scale=3)
    plt.figure(figsize=(28, 16))

    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=350)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="DejaVu Sans")
    nx.draw_networkx_edges(G, pos, width=1)

    # Distancias en cada arista
    edge_labels = nx.get_edge_attributes(G, 'distancia')
    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels={k: f"{v:.1f} km" for k, v in edge_labels.items()},
        font_size=6, 
        font_family="DejaVu Sans"
    )

    plt.title("Grafo de Rutas entre Municipios de Bolívar (mejorado)", fontsize=16, fontfamily="DejaVu Sans")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
