import warnings
from pymatgen.analysis.diffusion.analyzer import (
    DiffusionAnalyzer,
    get_extrapolated_conductivity,
)
from ase.io.trajectory import Trajectory
from ase.md.analysis import DiffusionCoefficient
from m3gnet.models import MolecularDynamics
from mp_api.client import MPRester

with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-985584")

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

temperatures = [300, 500, 700, 900, 1100]
Na_diffuse = dict.fromkeys(temperatures)
analyzers = dict.fromkeys(temperatures)

for t in temperatures:
    data.make_supercell((3,3,3))

    parameters = MolecularDynamics(
        atoms=data,
        temperature=t,  # 1000 K
        ensemble='nvt',  # NVT ensemble
        timestep=1, # 1fs,
        trajectory="Research_Lab/Na3PS4/trajectories/mo.traj" + str(t),  # save trajectory to mo.traj
        logfile="Research_Lab/Na3PS4/mo_log/mo.log" + str(t),  # log file for MD
        loginterval=100,  # interval for record the log temperature = 350)
    )
    parameters.run(steps = 1000)

    traj = Trajectory("Research_Lab/Na3PS4/trajectories/mo.traj" + str(t), mode="r")
    temp = DiffusionCoefficient(traj, 1.0, atom_indices=None, molecule=False)
    atoms_diffuse, std = temp.get_diffusion_coefficients()
    Na_diffuse[t] = atoms_diffuse[0]*0.1

    analyzers[t] = DiffusionAnalyzer.from_structures([data], "Na", t, 1, 100)

rts = get_extrapolated_conductivity(
    temperatures,
    [Na_diffuse],
    new_temp=300,
    structure=analyzers[700].structure,
    species="Na",
)

print("The Na ionic conductivity for Na3PS4 at 300 K is %.4f mS/cm" % rts)