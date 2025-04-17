# This example demonstrates how to create a simple two-compartment model (two STR reactors) using the CADETProcess library.

from CADETProcess.processModel import ComponentSystem
from CADETProcess.modelBuilder import CompartmentBuilder
from CADETProcess.processModel import MassActionLaw
from CADETProcess.simulator import Cadet
import matplotlib.pyplot as plt

component_system = ComponentSystem(['A', 'B']) # in this case 2 components, A and B

volume = [1e-3, 1e-3] # units are still not clear
flow_rate_matrix = [ # units are still not clear
    0,      0.1e-3,
    0.1e-3, 0
]

builder_simple = CompartmentBuilder(
    component_system,
    volume, flow_rate_matrix,
)

builder_simple.init_c = 1 # Initial concentration of both compornents (A & B) in both compartments in mM

# Add reaction kinetics
reaction_model = MassActionLaw(component_system)
reaction_model.add_reaction([0, 1], [-1, 1], k_fwd=2, k_bwd=1)

builder_simple.bulk_reaction_model = reaction_model

process_simulator = Cadet()

process = builder_simple.process
process.cycle_time = 100

simulation_results = process_simulator.run(process)

_ = simulation_results.solution[f'compartment_0'].outlet.plot()
_ = simulation_results.solution[f'compartment_1'].outlet.plot()

plt.show()