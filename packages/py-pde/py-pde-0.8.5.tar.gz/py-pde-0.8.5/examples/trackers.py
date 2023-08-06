"""
Using simulation trackers
=========================

This example illustrates how trackers can be used to analyze simulations.
"""

from pde import (DiffusionPDE, UnitGrid, ScalarField, MemoryStorage,
                 PlotTracker, PrintTracker, RealtimeIntervals)

grid = UnitGrid([32, 32])  # generate grid
state = ScalarField.random_uniform(grid)  # generate initial condition

storage = MemoryStorage()

trackers = [
    'progress',                    # show progress bar during simulation
    'steady_state',                # abort when steady state is reached
    storage.tracker(interval=1),   # store data every simulation time unit
    PlotTracker(show=True),        # show images during simulation
    # print some output every 5 real seconds:
    PrintTracker(interval=RealtimeIntervals(duration=5))
]

eq = DiffusionPDE(0.1)  # define the PDE
eq.solve(state, 3, dt=0.1, tracker=trackers)


for field in storage:
    print(field.integral)
