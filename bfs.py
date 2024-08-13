import tkinter as tk
from tkinter import messagebox
from collections import deque

def bfs_all_paths_without_cycles(graph, start, end, max_path_length=10):
    queue = deque([[start]])
    all_paths = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if len(path) > max_path_length:
            continue

        if node == end:
            all_paths.append(path)
        else:
            visited = set(path)  
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    
    return all_paths

def add_edge():
    node1 = node1_entry.get().strip()
    node2 = node2_entry.get().strip()
    
    if not node1 or not node2:
        messagebox.showerror("Input Error", "Please enter both nodes for the edge.")
        return
    
    if node1 not in graph:
        graph[node1] = []
    if node2 not in graph:
        graph[node2] = []
    
    if node2 not in graph[node1]:
        graph[node1].append(node2)
    if node1 not in graph[node2]:
        graph[node2].append(node1)
    
    edges_text.insert(tk.END, f"{node1} - {node2}\n")
    node1_entry.delete(0, tk.END)
    node2_entry.delete(0, tk.END)
    print(f"Edge added: {node1} - {node2}")

def run_bfs():
    start_node = start_entry.get().strip()
    end_node = end_entry.get().strip()
    
    if not start_node or not end_node:
        messagebox.showerror("Input Error", "Please enter both start and end nodes.")
        return
    
    if start_node not in graph or end_node not in graph:
        messagebox.showerror("Input Error", "Start or end node not in graph.")
        return
    
    print("Starting BFS...")
    all_paths = bfs_all_paths_without_cycles(graph, start_node, end_node, max_path_length=10)
    print(f"Number of paths found: {len(all_paths)}")

    if not all_paths:
        all_results = ["No path found"]
    else:
        all_results = [f"Path {i+1}: {' -> '.join(path)}" for i, path in enumerate(all_paths)]
    
    result_label.config(text="All Paths:\n" + "\n".join(all_results))

root = tk.Tk()
root.title("BFS")

graph = {}

tk.Label(root, text="Node 1:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
node1_entry = tk.Entry(root)
node1_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Node 2:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
node2_entry = tk.Entry(root)
node2_entry.grid(row=1, column=1, padx=10, pady=10)

add_edge_button = tk.Button(root, text="Add Edge", command=add_edge)
add_edge_button.grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(root, text="Edges:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
edges_text = tk.Text(root, width=40, height=10, state=tk.NORMAL)
edges_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Start Node:").grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
start_entry = tk.Entry(root)
start_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="End Node:").grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
end_entry = tk.Entry(root)
end_entry.grid(row=6, column=1, padx=10, pady=10)

find_paths_button = tk.Button(root, text="Find All Paths", command=run_bfs)
find_paths_button.grid(row=7, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="All Paths: ")
result_label.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
