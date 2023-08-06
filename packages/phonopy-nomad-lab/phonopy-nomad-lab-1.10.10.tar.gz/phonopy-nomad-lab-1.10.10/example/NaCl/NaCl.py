from phonopy import Phonopy
from phonopy.interface.vasp import read_vasp
from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
import numpy as np

def append_band(bands, q_start, q_end):
    band = []
    for i in range(51):
        band.append(np.array(q_start) +
                    (np.array(q_end) - np.array(q_start)) / 50 * i)
    bands.append(band)

bulk = read_vasp("POSCAR")
phonon = Phonopy(bulk,
                 [[2, 0, 0],
                  [0, 2, 0],
                  [0, 0, 2]],
                 primitive_matrix=[[0, 0.5, 0.5],
                                   [0.5, 0, 0.5],
                                   [0.5, 0.5, 0]],
                 is_auto_displacements=False)

symmetry = phonon.get_symmetry()
print "Space group:", symmetry.get_international_table()

force_sets = parse_FORCE_SETS()
phonon.set_displacement_dataset(force_sets)
phonon.produce_force_constants()

born = [[[1.08703, 0, 0],
         [0, 1.08703, 0],
         [0, 0, 1.08703]],
        [[-1.08672, 0, 0],
         [0, -1.08672, 0],
         [0, 0, -1.08672]]]
epsilon = [[2.43533967, 0, 0],
           [0, 2.43533967, 0],
           [0, 0, 2.43533967]]
factors = 14.400
phonon.set_nac_params({'born': born,
                       'factor': factors,
                       'dielectric': epsilon})

# BAND = 0.0 0.0 0.0  0.5 0.0 0.0  0.5 0.5 0.0  0.0 0.0 0.0  0.5 0.5 0.5
bands = []
append_band(bands, [0.0, 0.0, 0.0], [0.5, 0.0, 0.0])
append_band(bands, [0.5, 0.0, 0.0], [0.5, 0.5, 0.0])
append_band(bands, [0.5, 0.5, 0.0], [0.0, 0.0, 0.0])
append_band(bands, [0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
phonon.set_band_structure(bands)
q_points, distances, frequencies, eigvecs = phonon.get_band_structure()
for q, d, freq in zip(q_points, distances, frequencies):
    print q, d, freq
phonon.plot_band_structure().show()

# Mesh sampling 20x20x20
phonon.set_mesh([20, 20, 20])
phonon.set_thermal_properties(t_step=10,
                              t_max=1000,
                              t_min=0)

# DOS
phonon.set_total_DOS(sigma=0.1)
for omega, dos in np.array(phonon.get_total_DOS()).T:
    print "%15.7f%15.7f" % (omega, dos)
phonon.plot_total_DOS().show()

# Thermal properties
for t, free_energy, entropy, cv in np.array(phonon.get_thermal_properties()).T:
    print ("%12.3f " + "%15.7f" * 3) % ( t, free_energy, entropy, cv )
phonon.plot_thermal_properties().show()

# PDOS
phonon.set_mesh([20, 20, 20],
                is_mesh_symmetry=False,
                is_eigenvectors=True)
phonon.set_partial_DOS(tetrahedron_method=True)
omegas, pdos = phonon.get_partial_DOS()
pdos_indices = [[0], [1]]
phonon.plot_partial_DOS(pdos_indices=pdos_indices,
                        legend=pdos_indices).show()
