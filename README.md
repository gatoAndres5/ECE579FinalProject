# ECE579 Final Project

This project implements a small FOODIE robot delivery system for ECE 579.

It includes:

- **Part A:** robot route optimization with obstacle detection and replanning
- **Part B:** FOODIE_BAGGER rule-based food bagging simulation
- **Part C:** FOODIE_SPA beverage-selection rule base, described in the report
- **Part D:** STRIPS-style robot arm loading rules, described in the report

## Project Structure

```text
bagging/              # Item, Bag, and FOODIE_BAGGER logic
obstacle/             # Obstacle detection and obstacle objects
order/                # Orders and order manager
robot/                # Robot, fleet manager, movement, and grasper control
routing/              # Graph, nodes, edges, and path planner
testing/              # Pytest test files
simulation_outputs/   # Saved graph outputs from Simulation A

simulation_a.py       # Route optimization simulation
simulation_b.py       # Rule-based bagging simulation
requirements.txt
README.md
````

## Setup

Run these commands from the project root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If dependencies are missing, install them manually:

```bash
pip install matplotlib pytest
```

## Run Simulation A

Simulation A demonstrates multiple robots delivering orders, detecting an obstacle, replanning, and returning to the Food Warehouse (`FW`).

```bash
python simulation_a.py
```

Expected behavior:

* Robot 0 delivers Order 1 to `C`.
* Robot 1 delivers Order 2 to `D`.
* Robot 0 detects a blocked edge `B_C`.
* Robot 0 replans through `D` and `E`.
* Both robots return to `FW`.
* The simulation prints completed orders, distance traveled, and estimated battery used.
* Graph images may be saved in `simulation_outputs/`.

## Run Simulation B

Simulation B demonstrates the FOODIE_BAGGER rule-based bagging system.

```bash
python simulation_b.py
```

The sample order includes:

* pint of milk
* gallon of water
* frozen pizza
* bag of apples
* loaf of bread
* bag of ice

Expected behavior:

* The order items are printed with their size, frozen, fragile, and heavy attributes.
* FOODIE_BAGGER processes the order using bagging rules.
* Frozen items are placed into freezer bags.
* Non-frozen items are placed into regular bags.
* Heavy and fragile item rules are used to avoid unsafe packing.
* The simulation prints a trace of the bagging process.

## Run Tests

Run all tests:

```bash
pytest
```

Run one test file:

```bash
pytest testing/test_path_planner.py
```

or:

```bash
pytest testing/test_bagging.py
```

## Notes

Run commands from the project root directory. If imports fail, make sure you are not running files from inside a subfolder.

If you see this Matplotlib warning:

```text
FigureCanvasAgg is non-interactive, and thus cannot be shown
```

the simulation still ran correctly. It only means the graph window cannot be displayed in the current terminal environment. Check `simulation_outputs/` for saved graph images if the simulation is configured to save them.



