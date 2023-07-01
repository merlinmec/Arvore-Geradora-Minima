import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt


class GraphInputApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inserir Dados do Grafo")
        self.center_window(self.root, 400, 200)  # Centralizar a janela

        self.num_vertices_label = tk.Label(self.root, text="Número de Vértices:")
        self.num_vertices_label.pack()
        self.num_vertices_entry = tk.Entry(self.root, justify="center")  # Centralizar texto
        self.num_vertices_entry.pack()
        self.num_arestas_label = tk.Label(self.root, text="Número de Arestas:")
        self.num_arestas_label.pack()
        self.num_arestas_entry = tk.Entry(self.root, justify="center")  # Centralizar texto
        self.num_arestas_entry.pack()
        self.create_graph_button = tk.Button(self.root, text="Criar Grafo", command=self.create_graph)
        self.create_graph_button.pack()

        self.vertices = 0
        self.arestas = 0
        self.graph_data = []

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_graph(self):
        num_vertices = self.num_vertices_entry.get()
        num_arestas = self.num_arestas_entry.get()
        if not num_vertices.isdigit() or not num_arestas.isdigit():
            tk.messagebox.showerror("Erro", "Insira um número válido para o número de vértices e arestas.")
            return

        self.vertices = int(num_vertices)
        self.arestas = int(num_arestas)
        self.root.withdraw()  # Esconder a tela de entrada de dados
        self.graph_input = GraphDataInputApp(self.vertices, self.arestas, self.graph_data, self.create_new_graph)

    def create_new_graph(self):
        self.root.deiconify()  # Mostrar novamente a tela de entrada de dados
        self.graph_data = []  # Limpar os dados do grafo anterior
        self.num_vertices_entry.delete(0, tk.END)  # Limpar o campo de entrada de número de vértices
        self.num_arestas_entry.delete(0, tk.END)  # Limpar o campo de entrada de número de arestas


class GraphDataInputApp:
    def __init__(self, vertices, arestas, graph_data, create_new_graph_callback):
        self.root = tk.Toplevel()
        self.root.title("Inserir Dados das Arestas")
        self.center_window(self.root, 700, 400)  # Centralizar a janela

        self.vertices = vertices
        self.arestas = arestas
        self.graph_data = graph_data
        self.create_new_graph_callback = create_new_graph_callback

        self.aresta_label = tk.Label(self.root, text="Insira os dados das arestas:")
        self.aresta_label.pack()
        self.aresta_entries = []
        for i in range(self.arestas):
            frame = tk.Frame(self.root)
            frame.pack()
            u_label = tk.Label(frame, text="Vértice u:")
            u_label.pack(side=tk.LEFT)
            u_entry = tk.Entry(frame, justify="center")  # Centralizar texto
            u_entry.pack(side=tk.LEFT)
            v_label = tk.Label(frame, text="Vértice v:")
            v_label.pack(side=tk.LEFT)
            v_entry = tk.Entry(frame, justify="center")  # Centralizar texto
            v_entry.pack(side=tk.LEFT)
            peso_label = tk.Label(frame, text="Peso:")
            peso_label.pack(side=tk.LEFT)
            peso_entry = tk.Entry(frame, justify="center")  # Centralizar texto
            peso_entry.pack(side=tk.LEFT)
            self.aresta_entries.append((u_entry, v_entry, peso_entry))

        self.confirm_button = tk.Button(self.root, text="Confirmar", command=self.confirm_graph)
        self.confirm_button.pack()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def confirm_graph(self):
        for u_entry, v_entry, peso_entry in self.aresta_entries:
            u = int(u_entry.get())
            v = int(v_entry.get())
            peso = float(peso_entry.get())
            self.graph_data.append((u, v, peso))
        self.root.destroy()  # Fechar a tela de entrada de dados
        self.show_graph()

    def show_graph(self):
        grafo = Grafo(self.vertices)
        for u, v, peso in self.graph_data:
            grafo.adicionar_aresta(u, v, peso)

        arvore_geradora = grafo.kruskal()

        graph = nx.Graph()
        graph.add_edges_from([(u, v, {'weight': peso}) for u, v, peso in grafo.grafo.edges(data='weight')])

        pos = nx.spring_layout(graph)

        plt.figure(figsize=(8, 6))
        nx.draw_networkx(graph, pos=pos, with_labels=True, node_color='lightgreen', node_size=500)
        nx.draw_networkx_edges(graph, pos=pos, edgelist=arvore_geradora, edge_color='red', width=2)
        labels = {(u, v): f"{peso:.2f}" for (u, v, peso) in graph.edges(data='weight')}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='#000000', font_size=10)
        plt.axis('off')
        plt.show()

        self.create_new_graph_callback()


class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.grafo = nx.Graph()

    def adicionar_aresta(self, u, v, peso):
        self.grafo.add_edge(u, v, weight=peso)

    def encontrar(self, pai, i):
        if i >= len(pai):
            return -1  # Retorna -1 se o índice estiver fora do intervalo
        while pai[i] != i:
            i = pai[i]
        return i


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
        i = 0
        arestas = sorted(self.grafo.edges(data='weight'), key=lambda aresta: aresta[2])
        pai = []
        rank = []
        for vertice in range(self.V):
            pai.append(vertice)
            rank.append(0)
        while len(arvore_geradora) < self.V - 1 and i < len(arestas):
            u, v, peso = arestas[i]
            i += 1
            x = self.encontrar(pai, u)
            y = self.encontrar(pai, v)
            if x != y:
                arvore_geradora.append((u, v))
                self.unir(pai, rank, x, y)
        return arvore_geradora


if __name__ == "__main__":
    app = GraphInputApp()
    app.root.mainloop()
