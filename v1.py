import tkinter as tk
from tkinter import messagebox
import heapq

# Node class to represent each cell in the grid
class Node:
    def __init__(self, row, col, width, height):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.color = "white"  # Default color for a node
        self.neighbors = []  # Neighbors for A* algorithm
        self.wall = False
        self.start = False
        self.end = False

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.wall

    def make_wall(self):
        self.wall = True
        self.color = "black"

    def make_start(self):
        self.start = True
        self.color = "green"

    def make_end(self):
        self.end = True
        self.color = "red"

    def reset(self):
        self.wall = False
        self.start = False
        self.end = False
        self.color = "white"

    def draw(self, surface):
        tk.draw_rectangle(surface, self.color, self.col * self.width, self.row * self.height, self.width, self.height)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].is_wall():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < len(grid) - 1 and not grid[self.row][self.col + 1].is_wall():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

# A* algorithm implementation
def a_star_algorithm(draw, grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            reconstruct_path(came_from, current, draw)
            return

        for neighbor in current.neighbors:
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        draw()  # Draw the grid

    return False  # No path found

# Heuristic function (Manhattan distance)
def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstruct the path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = "blue"  # Color the path blue
        draw()

# Drawing the grid and nodes
def draw_grid(surface, grid):
    for row in grid:
        for node in row:
            node.draw(surface)

# Starting the algorithm
def start_algorithm():
    if not start or not end:
        messagebox.showwarning("Input Error", "Please select both a start and an end node!")
        return

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    a_star_algorithm(lambda: draw_fn(), grid, start, end)

# GUI setup
def draw_fn():
    surface.delete("all")
    draw_grid(surface, grid)

# Main Tkinter application
root = tk.Tk()
root.title("A* Pathfinding Visualizer")

# Grid setup
width = 800
height = 600
rows = 20
cols = 20
grid = [[Node(i, j, width // cols, height // rows) for j in range(cols)] for i in range(rows)]

surface = tk.Canvas(root, width=width, height=height)
surface.pack()

start = None
end = None

# Mouse click event for selecting nodes
def mouse_click(event):
    global start, end
    x, y = event.x, event.y
    col = x // (width // cols)
    row = y // (height // rows)
    node = grid[row][col]

    if not start and node != end:  # Set start
        start = node
        node.make_start()
    elif not end and node != start:  # Set end
        end = node
        node.make_end()
    elif node == start:  # Reset start
        start = None
        node.reset()
    elif node == end:  # Reset end
        end = None
        node.reset()

    draw_fn()

# Bind mouse click
surface.bind("<Button-1>", mouse_click)

# Start button
start_button = tk.Button(root, text="Start Pathfinding", command=start_algorithm)
start_button.pack()

# Reset button
def reset_grid():
    global start, end
    start = None
    end = None
    for row in grid:
        for node in row:
            node.reset()
    draw_fn()

reset_button = tk.Button(root, text="Reset", command=reset_grid)
reset_button.pack()

# Run the GUI
root.mainloop()
