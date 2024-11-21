import time
from collections import deque
import heapq
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# 城市距离数据
city_distances = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Bucharest': {'Urziceni': 85, 'Pitesti': 101, 'Giurgiu': 90, 'Fagaras': 211},
    'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Eforie': {'Hirsova': 86},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Giurgiu': {'Bucharest': 90},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Neamt': {'Iasi': 87},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Pitesti': {'Rimnicu': 97, 'Bucharest': 101, 'Craiova': 138},
    'Rimnicu': {'Sibiu': 80, 'Pitesti': 97, 'Craiova': 146},
    'Sibiu': {'Rimnicu': 80, 'Fagaras': 99, 'Arad': 140, 'Oradea': 151},
    'Timisoara': {'Lugoj': 111, 'Arad': 118},
    'Urziceni': {'Vaslui': 142, 'Bucharest': 85, 'Hirsova': 98},
    'Vaslui': {'Iasi': 92, 'Urziceni': 142},
    'Zerind': {'Oradea': 71, 'Arad': 75}
}

city_positions = {
    'Arad': (91, 492),
    'Bucharest': (400, 327),
    'Craiova': (253, 288),
    'Drobeta': (165, 299),
    'Eforie': (562, 293),
    'Fagaras': (305, 449),
    'Giurgiu': (375, 270),
    'Hirsova': (534, 350),
    'Iasi': (473, 506),
    'Lugoj': (165, 379),
    'Mehadia': (168, 339),
    'Neamt': (406, 537),
    'Oradea': (131, 571),
    'Pitesti': (320, 368),
    'Rimnicu': (233, 410),
    'Sibiu': (207, 457),
    'Timisoara': (94, 410),
    'Urziceni': (456, 350),
    'Vaslui': (509, 444),
    'Zerind': (108, 531)
}


# 广度优先搜索（BFS）
def bfs(start, goal):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for neighbor in city_distances[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))


# 深度优先搜索（DFS）
def dfs(start, goal, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    if start == goal:
        return path
    visited.add(start)
    for neighbor in city_distances[start]:
        if neighbor not in visited:
            new_path = dfs(neighbor, goal, path + [neighbor], visited)
            if new_path:
                return new_path


# 启发函数
def heuristic(node, goal):
    x1, y1 = city_positions[node]
    x2, y2 = city_positions[goal]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# A* 搜索算法
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    g_costs = {start: 0}
    while open_set:
        _, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        for neighbor, cost in city_distances[current].items():
            tentative_g_score = g_costs[current] + cost
            if neighbor not in g_costs or tentative_g_score < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))


# 比较算法性能
def compare_algorithms(start, goal, selected_algorithm):
    results = []
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": a_star
    }
    if selected_algorithm != "All":
        algorithms = {selected_algorithm: algorithms[selected_algorithm]}

    for algorithm, func in algorithms.items():
        start_time = time.time()
        path = func(start, goal)
        execution_time = time.time() - start_time
        path_length = sum(city_distances[path[i]][path[i + 1]] for i in range(len(path) - 1))
        results.append((algorithm, path, execution_time, path_length))

    return results


# 可视化路径代价
def visualize_cost(results):
    algorithms = [res[0] for res in results]
    costs = [res[3] for res in results]

    plt.bar(algorithms, costs)
    plt.title("Path Cost Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Path Cost")
    plt.show()


# 创建GUI
def run_algorithm():
    start = start_var.get()
    goal = goal_var.get()
    selected_algorithm = algo_var.get()

    if start == goal:
        messagebox.showerror("错误", "起点和终点不能相同！")
        return

    results = compare_algorithms(start, goal, selected_algorithm)
    output = ""
    for algorithm, path, exec_time, path_length in results:
        output += f"{algorithm}:\n路径: {path}\n时间: {exec_time:.4f} 秒\n路径长度: {path_length}\n\n"

    output_var.set(output)

    # 可视化代价
    visualize_cost(results)


# 创建主窗口
root = tk.Tk()
root.title("城市搜索算法对比")

# 界面布局
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="选择起点:").grid(row=0, column=0)
start_var = tk.StringVar()
start_menu = ttk.Combobox(frame, textvariable=start_var, values=list(city_distances.keys()))
start_menu.grid(row=0, column=1)

tk.Label(frame, text="选择终点:").grid(row=1, column=0)
goal_var = tk.StringVar()
goal_menu = ttk.Combobox(frame, textvariable=goal_var, values=list(city_distances.keys()))
goal_menu.grid(row=1, column=1)

tk.Label(frame, text="选择算法:").grid(row=2, column=0)
algo_var = tk.StringVar(value="All")
algo_menu = ttk.Combobox(frame, textvariable=algo_var, values=["All", "BFS", "DFS", "A*"])
algo_menu.grid(row=2, column=1)

tk.Button(frame, text="运行", command=run_algorithm).grid(row=3, column=0, columnspan=2, pady=10)

output_var = tk.StringVar()
output_label = tk.Label(frame, textvariable=output_var, wraplength=400, justify="left")
output_label.grid(row=4, column=0, columnspan=2)

# 程序入口
if __name__ == "__main__":
    root.mainloop()
