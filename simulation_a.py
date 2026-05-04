from routing.environment_graph import EnvironmentGraph
from routing.node import Node
from routing.edge import Edge
from routing.path_planner import PathPlanner

from order.order import Order
from order.order_manager import OrderManager


def build_environment():
    graph = EnvironmentGraph()

    # Nodes
    a = Node(1, "A", 0, 0)
    b = Node(2, "B", 1, 0)
    c = Node(3, "C", 2, 0)
    d = Node(4, "D", 1, 1)
    e = Node(5, "E", 2, 1)

    # Add nodes to graph
    graph.addNode(a)
    graph.addNode(b)
    graph.addNode(c)
    graph.addNode(d)
    graph.addNode(e)

    # Directed edges
    graph.addEdge(Edge(1, 1, a, b, True, "A_B"))
    graph.addEdge(Edge(2, 1, b, c, True, "B_C"))
    graph.addEdge(Edge(3, 1, b, d, True, "B_D"))
    graph.addEdge(Edge(4, 1, d, e, True, "D_E"))
    graph.addEdge(Edge(5, 1, e, c, True, "E_C"))

    return graph, a, b, c, d, e


def get_edge_between(start_node, end_node):
    for edge in start_node.edges:
        if edge.originNode == start_node and edge.destNode == end_node:
            return edge
    return None


def run_simulation():
    graph, a, b, c, d, e = build_environment()
    planner = PathPlanner(graph)

    # Orders
    orders = [
        Order(1, c),
        Order(2, e),
    ]

    order_manager = OrderManager(orders, [], [])

    # Mock robots
    robot_positions = {
        1: a,
        2: d
    }

    robot_paths = {
        1: [],
        2: []
    }

    robot_orders = {
        1: None,
        2: None
    }

    robot_energy = {
        1: 0,
        2: 0
    }

    for step in range(10):
        print(f"\n--- Step {step} ---")

        # Assign pending orders to idle robots
        for rid in robot_positions:
            if robot_orders[rid] is None:
                order = order_manager.dispatchOrder()
                if order is not None:
                    robot_orders[rid] = order
                    path = planner.calculate_path(robot_positions[rid], order.destination)

                    # Remove current node from returned path so robot only moves forward
                    if path and path[0] == robot_positions[rid]:
                        path = path[1:]

                    robot_paths[rid] = path
                    print(f"Assigned Order {order.orderId} to Robot {rid}")

        # Introduce obstacle
        if step == 3:
            print("Obstacle introduced: blocking B_C")
            for edge in b.edges:
                if edge.name == "B_C" and edge.originNode == b:
                    edge.setPassibility(False)

        # Move robots
        for rid in robot_positions:
            if robot_orders[rid] is None:
                continue

            # If no path remains
            if not robot_paths[rid]:
                if robot_positions[rid] == robot_orders[rid].destination:
                    print(f"Robot {rid} delivered Order {robot_orders[rid].orderId}")
                    order_manager.markComplete(robot_orders[rid])
                    robot_orders[rid] = None
                else:
                    print(f"Robot {rid} has no available path.")
                continue

            next_node = robot_paths[rid][0]
            edge = get_edge_between(robot_positions[rid], next_node)

            # If next step is blocked, replan
            if edge is None or not edge.isPassable:
                print(f"Robot {rid} path blocked, replanning...")
                new_path = planner.calculate_path(robot_positions[rid], robot_orders[rid].destination)

                if new_path and new_path[0] == robot_positions[rid]:
                    new_path = new_path[1:]

                robot_paths[rid] = new_path

                if not robot_paths[rid]:
                    print(f"Robot {rid} could not find a new route.")
                continue

            # Move one step
            robot_paths[rid].pop(0)
            robot_positions[rid] = next_node
            robot_energy[rid] += edge.getCost()
            print(f"Robot {rid} moved to {next_node.name}")

            # Check if delivered
            if robot_positions[rid] == robot_orders[rid].destination:
                print(f"Robot {rid} delivered Order {robot_orders[rid].orderId}")
                order_manager.markComplete(robot_orders[rid])
                robot_orders[rid] = None
                robot_paths[rid] = []

    print("\nSimulation finished")
    print(f"Completed orders: {len(order_manager.completedOrders)}")
    print(f"Robot 1 energy used: {robot_energy[1]}")
    print(f"Robot 2 energy used: {robot_energy[2]}")


if __name__ == "__main__":
    run_simulation()