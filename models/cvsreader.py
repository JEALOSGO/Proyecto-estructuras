import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('data/rutas_norte_sur.csv', sep=';', encoding='latin1')
df.columns = df.columns.str.strip()
G = nx.Graph()

for _, row in df.iterrows():
    origen = str(row['origen']).strip().title()
    destino = str(row['destino']).strip().title()
    distancia = float(row['distancia(km)'])
    eta = float(row['ETA(min)'])
    G.add_edge(origen, destino, distancia=distancia, eta=eta)

# Mostrar los nodos, cantidad y sus vecinos
print("NODOS EN EL GRAFO:")
for nodo in G.nodes():
    vecinos = list(G.neighbors(nodo))
    print(f"→ {nodo} | Grado: {G.degree[nodo]} | Vecinos: {vecinos}")

print(f"\nCantidad total de nodos: {G.number_of_nodes()}")

# Layout y visualización
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
