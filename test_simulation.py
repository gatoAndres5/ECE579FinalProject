import matplotlib.pyplot as plt

from routing.environment_graph import EnvironmentGraph
from routing.node import Node
from routing.edge import Edge

# Simulation test

graph = EnvironmentGraph()

fw = Node(1, "FW", 0, 0)
a = Node(2, "Destination A", 1, 0)
b = Node(3, "Destination B", 2, 0)
c = Node(4, "Destination C", 1, 1)

nodes = [fw, a, b, c]

for node in nodes:
    graph.addNode(node)

# Edges (directed)
e1 = Edge(1, 1, fw, a, True)
e2 = Edge(2, 1, a, b, True)
e3 = Edge(3, 2, fw, c, True)
e4 = Edge(4, 1, c, b, True)
e4.setPassibility(False)

edges = [e1, e2, e3, e4]

for edge in edges:
    graph.addEdge(edge)

print(f"Created graph")

# Display graphical representation
# Prompted an LLM for this portion, given a vision for the graphical representation, how to use 
# Matplotlib to achieve it, e.g how to display an arrow edge

fig, ax = plt.subplots(figsize=(8,8))

X = 0
Y = 1

# TODO make direction emphasized

x_vals = [node.position[X] for node in nodes]
y_vals = [node.position[Y] for node in nodes]

buffer = 0.5 # to prevent edges clipping
ax.set_xlim(min(x_vals) - buffer, max(x_vals) + buffer)
ax.set_ylim(min(y_vals) - buffer, max(y_vals) + buffer)

for edge in edges:
    x_coords = [edge.originNode.position[X], edge.destNode.position[X]]
    y_coords = [edge.originNode.position[Y], edge.destNode.position[Y]]

    if edge.isPassable:
        ax.plot(x_coords, y_coords, color='grey', linewidth=2.5, zorder=1)
    else:
        ax.plot(x_coords, y_coords, color='red', linestyle='--', linewidth=2.5, zorder=1)

    # show the cost
    mid_x = sum(x_coords) / 2
    mid_y = sum(y_coords) / 2
    ax.text(mid_x, mid_y, str(edge.cost), color='darkred', fontsize=10, ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', pad=2))
    
for node in nodes:
    x, y = node.position

    ax.scatter(x, y, s=3000, color='skyblue', zorder=2)
    ax.text(x, y, node.name, ha='center', va='center', fontweight='bold', fontsize=10, zorder=3)

#ax.margins(0.20) # add a margin to avoid cutting off node drawings
ax.set_aspect('equal')
plt.axis('off')
plt.title('Simulation')
plt.show()