import tkinter as tk
from tkinter import ttk, messagebox
from models.graph_logic import cargar_grafo, calcular_caminos_a_todos

CSV_PATH = "data/rutas_norte_sur.csv"

class GrafoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rutas entre Municipios de Bolívar - Dijkstra (Todos los caminos)")
        self.geometry("950x430")
        self.resizable(False, False)
        self.G = cargar_grafo(CSV_PATH)
        self.nodos = sorted(list(self.G.nodes()))
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self, text="Selecciona Origen:").pack(pady=(20,5))
        self.combo_origen = ttk.Combobox(self, values=self.nodos, state="readonly")
        self.combo_origen.pack()

        ttk.Button(self, text="Calcular caminos más cortos a todos (Dijkstra)", command=self.mostrar_todos_caminos).pack(pady=20)

        # Treeview para resultados tabulados
        columns = ("Destino", "Camino", "Distancia (km)", "Tiempo (min)")
        self.tabla = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200 if col=="Camino" else 120, anchor="center")
        self.tabla.pack()

    def mostrar_todos_caminos(self):
        origen = self.combo_origen.get()
        if not origen:
            messagebox.showwarning("Advertencia", "Debes seleccionar un nodo de origen.")
            return

        distancias, caminos, tiempos, algoritmo = calcular_caminos_a_todos(self.G, origen)

        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for destino in sorted(self.G.nodes()):
            if destino == origen:
                continue
            if destino in caminos:
                camino_str = " → ".join(caminos[destino])
                distancia = distancias[destino]
                tiempo = tiempos[destino]
                self.tabla.insert("", "end", values=(destino, camino_str, f"{distancia:.1f}", f"{tiempo:.1f}"))
            else:
                self.tabla.insert("", "end", values=(destino, "No hay camino", "---", "---"))

if __name__ == "__main__":
    app = GrafoApp()
    app.mainloop()
