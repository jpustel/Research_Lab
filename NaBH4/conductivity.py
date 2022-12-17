import warnings
import matplotlib.pyplot as plt
from pymatgen.analysis.diffusion.analyzer import (
    DiffusionAnalyzer,
    get_extrapolated_conductivity,
    get_arrhenius_plot
)
from ase.io.trajectory import Trajectory
from ase.md.analysis import DiffusionCoefficient
from mp_api.client import MPRester


for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-1180167")

data.make_supercell((2,2,2))

temperatures = [300, 500, 700, 900]
Na_diffuse = dict.fromkeys(temperatures)
analyzers = dict.fromkeys(temperatures)

for t in temperatures:
    traj = Trajectory("Research_Lab/NaBH4/trajectories/mo.traj" + str(t), mode="r")
    temp = DiffusionCoefficient(traj, 1, atom_indices=None, molecule=False)
    atoms_diffuse, std = temp.get_diffusion_coefficients()
    Na_diffuse[t] = atoms_diffuse[0]*0.1

    #Need data for each structure at the temperatures
    analyzers[t] = DiffusionAnalyzer.from_structures([data], "Na", t, 1, 100)

diffusivities = []
for diff in Na_diffuse.values():
    diffusivities.append(diff)

plot = get_arrhenius_plot(temperatures, diffusivities)

rts = get_extrapolated_conductivity(
    temperatures,
    diffusivities,
    new_temp=300,
    structure=analyzers[300].structure,
    species="Na",
)

print("The Na ionic conductivity for NaBH4 at 300 K is %.4f mS/cm" % rts)