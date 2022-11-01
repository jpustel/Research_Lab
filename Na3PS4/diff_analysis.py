from pymatgen.analysis.diffusion.aimd.pathway import ProbabilityDensityAnalysis
from pymatgen.core import Structure
import numpy as np

#First prepare the structrue and ionic trajectories files
trajectories = np.load("../pymatgen/analysis/diffusion/aimd/tests/cNa3PS4_trajectories.npy")
structure = Structure.from_file("../pymatgen/analysis/diffusion/aimd/tests/cNa3PS4.cif", False)

#ProbabilityDensityAnalysis object
pda = ProbabilityDensityAnalysis(structure, trajectories, interval=0.5)
#Save probability distribution to a CHGCAR-like file
pda.to_chgcar(filename="CHGCAR_new.vasp")

print("Maximum: %s, Minimum: %s" % (pda.Pr.max(), pda.Pr.min()))
# \int P(r)d^3r = 1
print("Total probability: %s" % np.sum(pda.Pr * pda.structure.lattice.volume / pda.lens[0]/pda.lens[1]/pda.lens[2]))


from pymatgen.analysis.diffusion.analyzer import DiffusionAnalyzer
import json

#ProbabilityDensityAnalysis object
filename="../pymatgen/analysis/diffusion/aimd/tests/cNa3PS4_pda.json"

data = json.load(open("../pymatgen/analysis/diffusion/aimd/tests/cNa3PS4_pda.json", "r"))
diff_analyzer = DiffusionAnalyzer.from_dict(data)

pda = ProbabilityDensityAnalysis.from_diffusion_analyzer(diff_analyzer, interval=0.5, 
                                                         species=("Na", "Li"))
#Save probability distribution to a CHGCAR-like file
pda.to_chgcar(filename="CHGCAR_new2.vasp")

print("Maximum: %s, Minimum: %s" % (pda.Pr.max(), pda.Pr.min()))
# \int P(r)d^3r = 1
print("Total probability: %s" % np.sum(pda.Pr * pda.structure.lattice.volume / pda.lens[0]/pda.lens[1]/pda.lens[2]))