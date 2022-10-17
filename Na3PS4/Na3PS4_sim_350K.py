import warnings

from m3gnet.models import Relaxer, MolecularDynamics
#from pymatgen.core import Lattice, Structure


from mp_api.client import MPRester
with MPRester(api_key="bl5ZA4p8qFoei37Lo61kGU9Yr0JD6TE5") as mpr:
    data = mpr.get_structure_by_material_id("mp-985584")

for category in (UserWarning, DeprecationWarning):
    warnings.filterwarnings("ignore", category=category, module="tensorflow")

data.make_supercell((3,3,3))

settings = MolecularDynamics(atoms = data, temperature = 350)

relaxer = Relaxer()  # This loads the default pre-trained model

relax_results = relaxer.relax(data, verbose=True)

final_structure = relax_results['final_structure']
final_energy_per_atom = float(relax_results['trajectory'].energies[-1] / len(data))

print(f"Relaxed lattice parameter is {final_structure.lattice.abc[0]:.3f} Å")
print(f"Final energy is {final_energy_per_atom:.3f} eV/atom")
