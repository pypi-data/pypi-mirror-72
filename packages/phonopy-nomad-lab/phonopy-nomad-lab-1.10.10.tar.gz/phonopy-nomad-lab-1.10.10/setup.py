from distutils.core import setup, Extension
import numpy
import os

include_dirs_numpy = [numpy.get_include()]
cc = None
if 'CC' in os.environ:
    if 'clang' in os.environ['CC']:
        cc = 'clang'
    if 'gcc' in os.environ['CC']:
        cc = 'gcc'

######################
# _phonopy extension #
######################
include_dirs_phonopy = ['c/harmonic_h', 'c/kspclib_h'] + include_dirs_numpy
sources_phonopy = ['c/_phonopy.c',
                   'c/harmonic/dynmat.c',
                   'c/harmonic/derivative_dynmat.c',
                   'c/kspclib/kgrid.c',
                   'c/kspclib/tetrahedron_method.c']

if __name__ == '__main__':
    extra_compile_args_phonopy = []
    extra_link_args_phonopy = []
else:
    extra_compile_args_phonopy = ['-fopenmp',]
    if cc == 'gcc':
        extra_link_args_phonopy = ['-lgomp',]
    elif cc == 'clang':
        extra_link_args_phonopy = []
    else:
        extra_link_args_phonopy = ['-lgomp',]

extension_phonopy = Extension(
    'phonopy._phonopy',
    extra_compile_args=extra_compile_args_phonopy,
    extra_link_args=extra_link_args_phonopy,
    include_dirs=include_dirs_phonopy,
    sources=sources_phonopy)


#####################
# _spglib extension #
#####################
if __name__ == '__main__':
    extra_compile_args_spglib=[]
    extra_link_args_spglib=[]
else:
    extra_compile_args_spglib=['-fopenmp',]
    if cc == 'gcc':
        extra_link_args_spglib=['-lgomp',]
    elif cc == 'clang':
        extra_link_args_spglib=[]
    else:
        extra_link_args_spglib=['-lgomp',]

extension_spglib = Extension(
    'phonopy._spglib',
    include_dirs=['c/spglib_h'] + include_dirs_numpy,
    extra_compile_args=extra_compile_args_spglib,
    extra_link_args=extra_link_args_spglib,
    sources=['c/_spglib.c',
             'c/spglib/cell.c',
             'c/spglib/delaunay.c',
             'c/spglib/hall_symbol.c',
             'c/spglib/kgrid.c',
             'c/spglib/kpoint.c',
             'c/spglib/mathfunc.c',
             'c/spglib/niggli.c',
             'c/spglib/pointgroup.c',
             'c/spglib/primitive.c',
             'c/spglib/refinement.c',
             'c/spglib/sitesym_database.c',
             'c/spglib/site_symmetry.c',
             'c/spglib/spacegroup.c',
             'c/spglib/spg_database.c',
             'c/spglib/spglib.c',
             'c/spglib/spin.c',
             'c/spglib/symmetry.c'])

ext_modules_phonopy = [extension_phonopy, extension_spglib]
packages_phonopy = ['phonopy',
                    'phonopy.cui',
                    'phonopy.gruneisen',
                    'phonopy.harmonic',
                    'phonopy.interface',
                    'phonopy.phonon',
                    'phonopy.qha',
                    'phonopy.structure',
                    'phonopy.unfolding']
scripts_phonopy = ['scripts/phonopy',
                   'scripts/phonopy-qha',
                   'scripts/phonopy-FHI-aims',
                   'scripts/bandplot',
                   'scripts/outcar-born',
                   'scripts/propplot',
                   'scripts/tdplot',
                   'scripts/dispmanager',
                   'scripts/gruneisen',
                   'scripts/pdosplot']

if __name__ == '__main__':
    version = ''
    with open("phonopy/version.py") as w:
        for line in w:
            if "__version__" in line:
                version = line.split()[2].strip('\"')

    # To deploy to pypi/conda by travis-CI
    nanoversion = ''
    if os.path.isfile("__nanoversion__.txt"):
        with open('__nanoversion__.txt') as nv:
            try :
                for line in nv:
                    nanoversion = int(line.strip())
                    break
            except ValueError :
                pass
            if nanoversion :
                nanoversion = '.'+str(nanoversion)
            else :
                nanoversion = ''

    if all([x.isdigit() for x in version.split('.')]):
        setup(name='phonopy-nomad-lab',
              version=(version + nanoversion),
              description='This is the NOMAD clone of the phonopy module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://atztogo.github.io/phonopy/',
              packages=packages_phonopy,
              scripts=scripts_phonopy,
              ext_modules=ext_modules_phonopy)
    else:
        print("Phonopy version number could not be retrieved.")
