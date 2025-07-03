import tkinter as tk
from tkinter import ttk, messagebox
from models.graph_logic import cargar_grafo, calcular_todos_caminos_dijkstra
import matplotlib.pyplot as plt
import networkx as nx

CSV_PATH = "data/rutas_norte_sur.csv"

class GrafoDijkstraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dijkstra: caminos más cortos desde un origen")
        self.geometry("600x400")
        self.resizable(False, False)
        self.G = cargar_grafo(CSV_PATH)
        self.nodos = sorted(list(self.G.nodes()))
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self, text="Selecciona Origen:").pack(pady=(20,5))
        self.combo_origen = ttk.Combobox(self, values=self.nodos, state="readonly")
        self.combo_origen.pack()

        ttk.Button(self, text="Mostrar caminos más cortos (Dijkstra)", command=self.mostrar_caminos).pack(pady=20)
        self.resultado = tk.Text(self, height=10, width=70, state="disabled")
        self.resultado.pack()

    def mostrar_caminos(self):
        origen = self.combo_origen.get()
        if not origen:
            messagebox.showwarning("Advertencia", "Debes seleccionar un nodo de origen.")
            return

        distancias, caminos, tiempos, algoname = calcular_todos_caminos_dijkstra(self.G, origen)
        self.resultado.configure(state="normal")
        self.resultado.delete(1.0, tk.END)
        for destino in sorted(self.G.nodes()):
            if destino == origen: continue
            if destino in caminos:
                path = " → ".join(caminos[destino])
                dist = distancias[destino]
                tpo = tiempos[destino]
                self.resultado.insert(tk.END, f"{origen} → {destino}: {path}\n  Distancia: {dist:.1f} km, Tiempo: {tpo:.1f} min\n\n")
        self.resultado.configure(state="disabled")
        self.visualizar_grafo_dijkstra(origen, caminos)

    def visualizar_grafo_dijkstra(self, origen, caminos):
        # Colorear los caminos más cortos
        edges_en_camino = set()
        for path in caminos.values():
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                # aristas como conjunto no dirigido
                edges_en_camino.add(tuple(sorted((u, v))))

        pos = nx.kamada_kawai_layout(self.G, scale=3)
        plt.figure(figsize=(24, 14))

        # Nodos: resalta origen
        nx.draw_networkx_nodes(self.G, pos, node_color=[
            "orange" if n == origen else "skyblue" for n in self.G.nodes()
        ], node_size=650)
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_family="DejaVu Sans")

        # Aristas: resalta caminos
        edge_colors = [
            "red" if tuple(sorted((u, v))) in edges_en_camino else "grey"
            for u, v in self.G.edges()
        ]
        nx.draw_networkx_edges(self.G, pos, width=2, edge_color=edge_colors)

        # Etiquetas de distancia
        edge_labels = nx.get_edge_attributes(self.G, 'distancia')
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={k: f"{v:.1f} km" for k, v in edge_labels.items()},
            font_size=6,
            font_family="DejaVu Sans"
        )
        plt.title(f"Caminos más cortos desde {origen} (Dijkstra)", fontsize=18, fontfamily="DejaVu Sans")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = GrafoDijkstraApp()
    app.mainloop()
