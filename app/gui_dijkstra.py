import tkinter as tk
from tkinter import ttk, messagebox
from models.graph_logic import cargar_grafo, calcular_todos_caminos_dijkstra

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx

CSV_PATH = "data/rutas_norte_sur.csv"

class GrafoDijkstraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dijkstra: caminos más cortos desde un origen")
        self.geometry("1100x650")
        self.minsize(700, 400)
        self.G = cargar_grafo(CSV_PATH)
        self.nodos = sorted(list(self.G.nodes()))
        self._crear_layout()
        self._make_responsive()

    def _crear_layout(self):
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=1)

        # --- Lado izquierdo ---
        self.left = tk.Frame(self.container)
        self.left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self.left, text="Selecciona Origen:").pack(pady=(20,5), fill=tk.X)
        self.combo_origen = ttk.Combobox(self.left, values=self.nodos, state="readonly")
        self.combo_origen.pack(fill=tk.X)
        ttk.Button(self.left, text="Mostrar caminos más cortos (Dijkstra)", command=self.mostrar_caminos).pack(pady=20, fill=tk.X)
        self.resultado = tk.Text(self.left, height=28, width=43, state="disabled")
        self.resultado.pack(pady=10, fill=tk.BOTH, expand=True)

        # --- Lado derecho ---
        self.right = tk.Frame(self.container)
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_rowconfigure(1, weight=0)
        self.right.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(11, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        # --- Toolbar: Frame aparte solo para toolbar ---
        self.toolbar_frame = tk.Frame(self.right)
        self.toolbar_frame.grid(row=1, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        # Toolbar usa .pack() dentro de su propio frame, así nunca hay conflicto

    def _make_responsive(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def mostrar_caminos(self):
        origen = self.combo_origen.get()
        if not origen:
            messagebox.showwarning("Advertencia", "Debes seleccionar un nodo de origen.")
            return

        distancias, caminos, tiempos, algoname = calcular_todos_caminos_dijkstra(self.G, origen)
        # Actualiza el texto a la izquierda
        self.resultado.configure(state="normal")
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, f"{'Destino':<25} {'Distancia (km)':>18} {'Tiempo (min)':>15}\n")
        self.resultado.insert(tk.END, "-"*58 + "\n")
        for destino in sorted(self.G.nodes()):
            if destino == origen: continue
            if destino in caminos:
                dist = distancias[destino]
                tpo = tiempos[destino]
                self.resultado.insert(
                    tk.END,
                    f"{destino:<25} {dist:>13.1f} km {tpo:>14.1f} min\n"
                )
        self.resultado.configure(state="disabled")
        # Actualiza el grafo en el canvas de la derecha
        self.visualizar_grafo_dijkstra(origen, caminos)

    def visualizar_grafo_dijkstra(self, origen, caminos):
        self.ax.clear()
        edges_en_camino = set()
        for path in caminos.values():
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                edges_en_camino.add(tuple(sorted((u, v))))
        pos = nx.kamada_kawai_layout(self.G, scale=3)
        # Nodos
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color=[
            "orange" if n == origen else "skyblue" for n in self.G.nodes()
        ], node_size=650)
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10, font_family="DejaVu Sans")
        # Aristas
        edge_colors = [
            "red" if tuple(sorted((u, v))) in edges_en_camino else "grey"
            for u, v in self.G.edges()
        ]
        nx.draw_networkx_edges(self.G, pos, ax=self.ax, width=2, edge_color=edge_colors)
        # Etiquetas de distancia
        edge_labels = nx.get_edge_attributes(self.G, 'distancia')
        nx.draw_networkx_edge_labels(
            self.G, pos, ax=self.ax,
            edge_labels={k: f"{v:.1f} km" for k, v in edge_labels.items()},
            font_size=6,
            font_family="DejaVu Sans"
        )
        self.ax.set_title(f"Caminos más cortos desde {origen} (Dijkstra)", fontsize=18, fontfamily="DejaVu Sans")
        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = GrafoDijkstraApp()
    app.mainloop()
