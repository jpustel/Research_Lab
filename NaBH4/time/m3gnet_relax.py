import warnings

from m3gnet.models import Relaxer
from mp_api.client import MPRester

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

# Init a Mo structure with stretched lattice (DFT lattice constant ~ 3.168)
with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    mo = mpr.get_structure_by_material_id("mp-1180167")

mo.make_supercell((2,2,2))

relaxer = Relaxer()  # This loads the default pre-trained model

relax_results = relaxer.relax(mo, verbose=True)

final_structure = relax_results['final_structure']
final_energy_per_atom = float(relax_results['trajectory'].energies[-1] / len(mo))

print(f"Relaxed lattice parameter is {final_structure.lattice.abc[0]:.3f} Å")
print(f"Final energy is {final_energy_per_atom:.3f} eV/atom")