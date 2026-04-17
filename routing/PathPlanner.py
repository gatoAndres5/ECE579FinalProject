import heapq


class PathPlanner:
    def __init__(self, environment_graph, destinations=None):
        self.environment_graph = environment_graph
        if destinations:
            self.destinations =  destinations
        else:
            self.destinations = []
        self.current_path = []

    def heuristic(self, node_a, node_b):
        x1, y1 = node_a.position
        x2, y2 = node_b.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def reconstruct_path(self, came_from, current):
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    def calculate_path(self, start_node, goal_node):
        open_set = []
        heapq.heappush(open_set, (0, start_node))

        came_from = {}
        g_score = {start_node: 0}
        f_score = {start_node: self.heuristic(start_node, goal_node)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal_node:
                self.current_path = self.reconstruct_path(came_from, current)
                return self.current_path

            for edge in current.edges:
                if not edge.isPassable:
                    continue

                if edge.originNode != current:
                    continue

                neighbor = edge.destNode
                tentative_g_score = g_score[current] + edge.cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal_node)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        self.current_path = []
        return []