#!/usr/bin/env python3

from setuptools import find_packages, setup

import tinie as my_pkg

setup(name='tinie',
      author=my_pkg.__author__,
      author_email=my_pkg.__author_email__,
      classifiers=[
          'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Physics',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'Operating System :: POSIX'
      ],
      description='A non-interacting equilibrium 2D quantum transport simulation framework',
      entry_points={
          'console_scripts': [
              'make_system_files = tinie.scripts.make_system_files:user_interface',
              'tinie = tinie.scripts.tinie:main',
              'tinie_dos = tinie.scripts.tinie_dos:main',
              'tinie_draw = tinie.scripts.tinie_draw:main',
              'tinie_prepare = tinie.scripts.tinie_prepare:main'
          ]
      },
      long_description=open("README.rst",'r').read(),
      long_description_content_type='text/x-rst',
      install_requires=['numpy', 'scipy', 'mpi4py', 'progressbar2', 'findiff',
                        'matplotlib', 'h5py', 'vegas'],
      keywords='numerics quantum transport physics',
      license=my_pkg.__license__,
      packages=find_packages(),
      package_data={'': ['test_files/*.h5', 'test_files/*.npy']},
      python_requires='>=3.6',
      test_suite='nose2.collector.collector',
      tests_require=['nose2'],
      url='https://gitlab.com/compphys-public/tinie',
      version=my_pkg.__version__,
      zip_safe=False
      )
