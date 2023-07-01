import tkinter as tk
from tkinter import CENTER, messagebox

class GraphApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Árvore Geradora Mínima")

        # Definir o tamanho da janela
        width = 400
        height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.canvas = tk.Canvas(self.root, width=400, height=300)
        self.canvas.pack()
        self.num_vertices_label = tk.Label(self.root, text="Número de Vértices:")
        self.num_vertices_label.pack()
        self.num_vertices_entry = tk.Entry(self.root)
        self.num_vertices_entry.pack()
        self.num_arestas_label = tk.Label(self.root, text="Número de Arestas:")
        self.num_arestas_label.pack()
        self.num_arestas_entry = tk.Entry(self.root)
        self.num_arestas_entry.pack()
        self.create_graph_button = tk.Button(self.root, text="Criar Grafo", command=self.create_graph)
        self.create_graph_button.pack()
        self.restart_button = tk.Button(self.root, text="Reiniciar", state=tk.DISABLED, command=self.restart)
        self.restart_button.pack()
        self.vertices = 0
        self.arestas = 0
        self.grafo = None
        self.index_aresta = 1
        self.aresta_entries = []

    def create_graph(self):
        self.vertices = int(self.num_vertices_entry.get())
        self.arestas = int(self.num_arestas_entry.get())
        self.canvas.delete("all")
        self.grafo = Grafo(self.vertices)
        self.add_aresta_entry()

    def add_aresta_entry(self):
        if self.index_aresta <= self.arestas:
            aresta_label = tk.Label(self.root, text="Aresta {}: ".format(self.index_aresta))
            aresta_label.pack()
            aresta_entry = tk.Entry(self.root)
            aresta_entry.pack()
            aresta_entry.bind("<Return>", self.add_aresta)
            aresta_entry.focus_set()
            self.aresta_entries.append(aresta_entry)

    def add_aresta(self, event):
        aresta = event.widget.get()
        u, v, peso = map(int, aresta.split())
        self.grafo.adicionar_aresta(u-1, v-1, peso)
        self.index_aresta += 1
        event.widget.destroy()
        if self.index_aresta > self.arestas:
            arvore_geradora = self.grafo.kruskal()
            self.mostrar_arvore_geradora(arvore_geradora)
            self.restart_button.config(state=tk.NORMAL)
        else:
            self.add_aresta_entry()

    def mostrar_arvore_geradora(self, arvore_geradora):
        self.canvas.delete("all")
        self.canvas.create_text(200, 50, text="Árvore Geradora Mínima:", font=("Arial", 16), fill="black", justify=CENTER)
        y = 100
        for u, v, peso in arvore_geradora:
            texto = "{} - {} : {}".format(u+1, v+1, peso)
            self.canvas.create_text(200, y, text=texto, font=("Arial", 12), fill="black", justify=CENTER)
            y += 20

    def restart(self):
        self.num_vertices_entry.delete(0, tk.END)
        self.num_arestas_entry.delete(0, tk.END)
        self.create_graph_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.canvas.delete("all")
        self.index_aresta = 1
        for entry in self.aresta_entries:
            entry.destroy()
        self.aresta_entries = []

    def run(self):
        self.root.mainloop()


class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.grafo = []

    def adicionar_aresta(self, u, v, peso):
        self.grafo.append((u, v, peso))

    def encontrar(self, pai, i):
        if pai[i] == i:
            return i
        return self.encontrar(pai, pai[i])

    def unir(self, pai, rank, x, y):
        raiz_x = self.encontrar(pai, x)
        raiz_y = self.encontrar(pai, y)
        if rank[raiz_x] < rank[raiz_y]:
            pai[raiz_x] = raiz_y
        elif rank[raiz_x] > rank[raiz_y]:
            pai[raiz_y] = raiz_x
        else:
            pai[raiz_y] = raiz_x
            rank[raiz_x] += 1

    def kruskal(self):
        arvore_geradora = []
        self.grafo = sorted(self.grafo, key=lambda item: item[2])
        pai = []
        rank = []
        for v in range(self.V):
            pai.append(v)
            rank.append(0)
        i = 0
        arestas_selecionadas = 0
        while arestas_selecionadas < self.V - 1:
            u, v, peso = self.grafo[i]
            i += 1
            raiz_u = self.encontrar(pai, u)
            raiz_v = self.encontrar(pai, v)
            if raiz_u != raiz_v:
                arvore_geradora.append((u, v, peso))
                self.unir(pai, rank, raiz_u, raiz_v)
                arestas_selecionadas += 1
        return arvore_geradora


app = GraphApp()
app.run()
