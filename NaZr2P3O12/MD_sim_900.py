import warnings
import time

from m3gnet.models import MolecularDynamics
from mp_api.client import MPRester

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

t = 900

start = time.time()
with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-6475")

data.make_supercell((2,2,2))

parameters = MolecularDynamics(
    atoms=data,
    temperature=t,  # 1000 K
    ensemble='nvt',  # NVT ensemble
    timestep=2, # 1fs,
    trajectory="Research_Lab/NaZr2P3O12/trajectories/mo.traj" + str(t),  # save trajectory to mo.traj
    logfile="Research_Lab/NaZr2P3O12/mo_log/mo.log" + str(t),  # log file for MD
    loginterval=100,  # interval for record the log temperature = 350)
)

parameters.run(steps = 50000)

end = time.time()
print(f"Secs: {int(end - start)}")

hr, rem = divmod(end-start, 3600)
mins, sec = divmod(rem, 60) 

print("Time of Simulation:{:0>2}:{:0>2}:{:05.2f}".format(int(hr),int(mins),sec))