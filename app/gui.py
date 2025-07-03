import tkinter as tk
from tkinter import ttk, messagebox
from models.graph_logic import cargar_grafo, calcular_camino_mas_corto

CSV_PATH = "data/rutas_norte_sur.csv"

class GrafoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rutas entre Municipios de Bolívar - Camino más corto (Dijkstra)")
        self.geometry("600x300")
        self.resizable(False, False)
        self.G = cargar_grafo(CSV_PATH)
        self.nodos = sorted(list(self.G.nodes()))
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self, text="Selecciona Origen:").pack(pady=(20,5))
        self.combo_origen = ttk.Combobox(self, values=self.nodos, state="readonly")
        self.combo_origen.pack()

        ttk.Label(self, text="Selecciona Destino:").pack(pady=(15,5))
        self.combo_destino = ttk.Combobox(self, values=self.nodos, state="readonly")
        self.combo_destino.pack()

        ttk.Button(self, text="Calcular camino más corto (Dijkstra)", command=self.mostrar_camino).pack(pady=20)

        self.resultado = tk.Text(self, height=6, width=70, state="disabled")
        self.resultado.pack()

    def mostrar_camino(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Debes seleccionar ambos nodos.")
            return
        if origen == destino:
            messagebox.showinfo("Info", "El origen y destino son el mismo.")
            return

        path, distancia, tiempo = calcular_camino_mas_corto(self.G, origen, destino)
        self.resultado.configure(state="normal")
        self.resultado.delete(1.0, tk.END)
        if path:
            texto = (
                "Algoritmo seleccionado: Dijkstra\n"
                f"Camino más corto de {origen} a {destino}:\n"
                + " → ".join(path) +
                f"\nDistancia total: {distancia:.1f} km\n"
                f"Tiempo estimado total: {tiempo:.1f} min"
            )
        else:
            texto = f"No existe un camino entre {origen} y {destino}."
        self.resultado.insert(tk.END, texto)
        self.resultado.configure(state="disabled")

if __name__ == "__main__":
    app = GrafoApp()
    app.mainloop()
