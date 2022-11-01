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
    loginterval=1,  # interval for record the log temperature = 350)
)

parameters.run(steps = 1000)

from pymatgen.analysis.diffusion.aimd.pathway import ProbabilityDensityAnalysis
from pymatgen.analysis.diffusion.analyzer import DiffusionAnalyzer
import numpy as np

trajectories = np.load("Research_Lab/Na3PS4/mo.traj", allow_pickle=True)
pda = ProbabilityDensityAnalysis(data, trajectories, interval=0.5)
#diff_analyzer = DiffusionAnalyzer.from_structures(data, trajectories, interval=0.5)

#pda = ProbabilityDensityAnalysis.from_diffusion_analyzer(diff_analyzer, interval=0.5, species=("Na", "Li"))
#Save probability distribution to a CHGCAR-like file
pda.to_chgcar(filename="CHGCAR_new2.vasp")

print("Maximum: %s, Minimum: %s" % (pda.Pr.max(), pda.Pr.min()))
# \int P(r)d^3r = 1
print("Total probability: %s" % np.sum(pda.Pr * pda.structure.lattice.volume / pda.lens[0]/pda.lens[1]/pda.lens[2]))