import warnings
import time

from m3gnet.models import MolecularDynamics
from mp_api.client import MPRester

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

t = 311

start = time.time()
with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-1180167")
a = 3
b = 1
c = 1

data.make_supercell((a,b,c))

parameters = MolecularDynamics(
    atoms=data,
    temperature=300,  # 1000 K
    ensemble='nvt',  # NVT ensemble
    timestep=1, # 1fs,
    trajectory="Research_Lab/NaBH4/time/trajectories/mo.traj" + str(t),  # save trajectory to mo.traj
    logfile="Research_Lab/NaBH4/time/mo_log/mo.log" + str(t),  # log file for MD
    loginterval=100,  # interval for record the log temperature = 350)
)

parameters.run(steps = 10000)

print(f"Number of atoms: {a*b*c*10}")
end = time.time()
print(f"Secs: {int(end - start)}")

hr, rem = divmod(end-start, 3600)
mins, sec = divmod(rem, 60) 

print("Time of Simulation:{:0>2}:{:0>2}:{:05.2f}".format(int(hr),int(mins),sec))