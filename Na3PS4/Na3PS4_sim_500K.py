import warnings

from m3gnet.models import MolecularDynamics
from pymatgen.core.structure import Structure


from mp_api.client import MPRester
with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-985584")

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

data.make_supercell((3,3,3))

parameters = MolecularDynamics(
    atoms=data,
    temperature=500,  # 1000 K
    ensemble='nvt',  # NVT ensemble
    timestep=1, # 1fs,
    trajectory="Research_Lab/Na3PS4/mo.traj",  # save trajectory to mo.traj
    logfile="Research_Lab/Na3PS4/mo.log",  # log file for MD
    loginterval=1000,  # interval for record the log temperature = 350)
)

parameters.run(steps = 1000)

from pymatgen.analysis.diffusion.analyzer import (
    DiffusionAnalyzer,
    get_extrapolated_conductivity,
)
from ase.io.trajectory import Trajectory
traj = Trajectory("Research_Lab/Na3PS4/mo.traj")

analyzers = DiffusionAnalyzer.from_structures([data], "Na", 500, 1, 100)
#f = open("Research_Lab/Na3PS4/mo.traj", "r")
#with open("Research_Lab/Na3PS4/mo.traj", mode="rb") as f:
    #d = json.load(f)

rts = get_extrapolated_conductivity(
    [500],
    traj,
    new_temp=300,
    structure=analyzers[500].structure,
    species="Na",
)

print("The Na ionic conductivity for Na3PS4 at 500 K is %.4f mS/cm" % rts)