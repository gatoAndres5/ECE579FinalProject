import matplotlib.pyplot as plt

from routing.environment_graph import EnvironmentGraph
from routing.node import Node
from routing.edge import Edge
from routing.path_planner import PathPlanner

from order.order import Order
from order.order_manager import OrderManager

from robot.fleet_manager import Fleet_Manager
from robot.robot import Robot

from obstacle.obstacle import Obstacle


def build_environment():
    graph = EnvironmentGraph()

    # Nodes
    fw = Node(1, "FW", 0, 0)
    a = Node(2, "A", 1, 0)
    b = Node(3, "B", 2, 0)
    c = Node(4, "C", 3, 0)
    d = Node(5, "D", 2, -1)
    e = Node(6, "E", 3, -1)

    nodes = [fw, a, b, c, d, e]

    for node in nodes:
        graph.addNode(node)

    # Main shortest route: FW -> A -> B -> C
    edge1 = Edge(1, 1, fw, a, True, "FW_A")
    edge2 = Edge(2, 1, a, b, True, "A_B")
    edge3 = Edge(3, 1, b, c, True, "B_C")  # hidden obstacle will block this

    # Detour route after obstacle: B -> D -> E -> C
    edge4 = Edge(4, 1, b, d, True, "B_D")
    edge5 = Edge(5, 1, d, e, True, "D_E")
    edge6 = Edge(6, 1, e, c, True, "E_C")

    # Return route: C -> E -> D -> B -> A -> FW
    edge7 = Edge(7, 1, c, e, True, "C_E")
    edge8 = Edge(8, 1, e, d, True, "E_D")
    edge9 = Edge(9, 1, d, b, True, "D_B")
    edge10 = Edge(10, 1, b, a, True, "B_A")
    edge11 = Edge(11, 1, a, fw, True, "A_FW")

    edges = [
        edge1, edge2, edge3,
        edge4, edge5, edge6,
        edge7, edge8, edge9, edge10, edge11
    ]

    for edge in edges:
        graph.addEdge(edge)

    return graph, nodes, edges, fw, a, b, c, d, e, edge3


def draw_graph(nodes, edges, robots, step, title="Simulation A"):
    fig, ax = plt.subplots(figsize=(8, 8))

    x_vals = [node.position[0] for node in nodes]
    y_vals = [node.position[1] for node in nodes]

    buffer = 0.6
    ax.set_xlim(min(x_vals) - buffer, max(x_vals) + buffer)
    ax.set_ylim(min(y_vals) - buffer, max(y_vals) + buffer)

    # Draw edges
    for edge in edges:
        x1, y1 = edge.originNode.position
        x2, y2 = edge.destNode.position

        if edge.isPassable:
            edge_color = "grey"
            line_style = "-"
        else:
            edge_color = "red"
            line_style = "--"

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                color=edge_color,
                linestyle=line_style,
                linewidth=2.5,
                shrinkA=30,
                shrinkB=30
            ),
            zorder=1
        )

        # Edge cost label
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        ax.text(
            mid_x,
            mid_y,
            str(edge.cost),
            color="darkred",
            fontsize=9,
            ha="center",
            va="center",
            bbox=dict(facecolor="white", edgecolor="none", pad=2),
            zorder=4
        )

    # Draw nodes
    for node in nodes:
        x, y = node.position

        ax.scatter(x, y, s=3000, color="skyblue", zorder=2)
        ax.text(
            x,
            y,
            node.name,
            ha="center",
            va="center",
            fontweight="bold",
            fontsize=10,
            zorder=3
        )

    # Draw robots
    robot_offsets = {
        0: (-0.12, -0.18),
        1: (0.12, -0.18),
        2: (-0.12, 0.18),
        3: (0.12, 0.18)
    }

    for robot in robots:
        x, y = robot.getPosition().position
        offset_x, offset_y = robot_offsets.get(robot.getID(), (0, -0.18))

        if robot.getCurrentOrder() is None:
            label = f"R{robot.getID()}\n{robot.getStatus()}"
        else:
            label = f"R{robot.getID()}\nO{robot.getCurrentOrder().orderId}"

        ax.scatter(
            x + offset_x,
            y + offset_y,
            s=600,
            color="orange",
            edgecolor="black",
            zorder=5
        )

        ax.text(
            x + offset_x,
            y + offset_y,
            label,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            zorder=6
        )

    ax.set_aspect("equal")
    plt.axis("off")
    plt.title(f"{title} - Step {step}")
    plt.savefig(f"simulation_outputs/simulation_a_step_{step}.png", bbox_inches="tight")
    plt.show()
    plt.close()


def create_route_only_bags(order_id, count=1):
    """
    Simulation A focuses on route optimization, not bagging.
    These placeholder bags use real robots while still allowing
    orders to represent carried inventory at a simple level without the rule based system.
    """

    class RouteBag:
        def __init__(self, bag_id):
            self.bag_id = bag_id
            self.order = None

        def getID(self):
            return self.bag_id

        def getName(self):
            return self.bag_id

    bags = []

    for i in range(count):
        bag = RouteBag(f"route_bag_order_{order_id}_{i + 1}")
        bags.append(bag)

    return bags


def get_order_id(order):
    if hasattr(order, "orderId"):
        return order.orderId
    if hasattr(order, "id"):
        return order.id
    return "unknown"


def run_simulation():
    graph, nodes, edges, fw, a, b, c, d, e, blocked_edge = build_environment()
    planner = PathPlanner(graph)

    # Obstacle exists in the real environment, but the graph does not know yet.
    # The robot should discover it through Movement_Controller / ObstacleDetection.
    true_obstacles = [
        Obstacle(1, blocked_edge)
    ]

    fleet_manager = Fleet_Manager(fw, graph, true_obstacles, planner)

    # robots
    robot1 = Robot(fleet_manager, 0, fw, graph, true_obstacles)
    robot2 = Robot(fleet_manager, 1, fw, graph, true_obstacles)

    fleet_manager.addRobot(robot1)
    fleet_manager.addRobot(robot2)

    orders = [
        Order(1, c),
        Order(2, d),
    ]

    order_manager = OrderManager(orders, [], [])

    # generated code to make the graphs look nice for each step

    print("Created graph")
    print("Using shortest-path planning to minimize delivery time and energy usage.")
    print("Multiple robots can deliver orders concurrently.")
    print("A hidden obstacle exists on edge B_C and should trigger replanning when detected.")

    draw_graph(
        nodes,
        edges,
        fleet_manager.robots,
        step="Initial",
        title="Simulation A: Robot Route Optimization"
    )

    dispatched_orders = {}

    total_orders = len(orders)

    for step in range(12):
        print(f"\n--- Step {step} ---")

        # Dispatch available orders to available robots
        while fleet_manager.hasAvailableRobot():
            order = order_manager.dispatchOrder()

            if order is None:
                break

            bags = create_route_only_bags(get_order_id(order), count=1)
            robot = fleet_manager.dispatchOrder(order, bags)

            if robot is not None:
                dispatched_orders[robot.getID()] = order
                print(
                    f"Order {get_order_id(order)} dispatched to Robot {robot.getID()} "
                    f"with destination {order.getDestination().name}."
                )
            else:
                print(f"Order {get_order_id(order)} could not be dispatched.")
                break

        # Tick each robot once
        for robot in fleet_manager.robots:
            previous_position = robot.getPosition()
            previous_status = robot.getStatus()
            previous_order = robot.getCurrentOrder()

            robot.tick()

            current_position = robot.getPosition()
            current_status = robot.getStatus()

            if previous_position != current_position:
                print(
                    f"Robot {robot.getID()} moved from "
                    f"{previous_position.name} to {current_position.name}."
                )

            if previous_order is not None:
                destination = previous_order.getDestination()

                if current_position == destination:
                    if previous_order not in order_manager.completedOrders:
                        print(
                            f"Robot {robot.getID()} delivered Order "
                            f"{get_order_id(previous_order)} to {destination.name}."
                        )
                        order_manager.markComplete(previous_order)

            if previous_status != current_status:
                print(
                    f"Robot {robot.getID()} status changed from "
                    f"{previous_status} to {current_status}."
                )

        draw_graph(
            nodes,
            edges,
            fleet_manager.robots,
            step=step,
            title="Simulation A: Robot Route Optimization"
        )

        all_orders_completed = len(order_manager.completedOrders) == total_orders
        all_robots_ready = all(
            robot.getStatus() == "ready"
            for robot in fleet_manager.robots
        )

        if all_orders_completed and all_robots_ready:
            print("\nAll orders completed and all robots returned to FW.")
            break

    print("\nSimulation finished")
    print(f"Completed orders: {len(order_manager.completedOrders)}")

    for robot in fleet_manager.robots:
        distance = robot.movementController.getDistanceTravelled()
        battery_used = 100 - robot.getBattery()

        print(f"Robot {robot.getID()} final position: {robot.getPosition().name}")
        print(f"Robot {robot.getID()} distance traveled: {distance}")
        print(f"Robot {robot.getID()} estimated battery used: {battery_used}")


if __name__ == "__main__":
    run_simulation()