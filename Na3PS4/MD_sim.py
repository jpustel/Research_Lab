import warnings
from pymatgen.analysis.diffusion.analyzer import (
    DiffusionAnalyzer,
    get_extrapolated_conductivity,
)
from ase.io.trajectory import Trajectory
from ase.md.analysis import DiffusionCoefficient
from m3gnet.models import MolecularDynamics
from mp_api.client import MPRester

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

t = 300

with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-985584")

data.make_supercell((3,3,3))

parameters = MolecularDynamics(
    atoms=data,
    temperature=300,  # 1000 K
    ensemble='nvt',  # NVT ensemble
    timestep=1, # 1fs,
    trajectory="Research_Lab/Na3PS4/trajectories/mo.traj" + str(t),  # save trajectory to mo.traj
    logfile="Research_Lab/Na3PS4/mo_log/mo.log",  # log file for MD
    loginterval=100,  # interval for record the log temperature = 350)
)

parameters.run(steps = 1000)