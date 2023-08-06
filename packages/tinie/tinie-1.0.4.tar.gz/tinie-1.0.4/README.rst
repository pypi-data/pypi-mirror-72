|pypi license| |pypi version| |pypi status| |Python implementation|
|Python versions| |Python wheel| |pipeline status| |coverage report|

Transport In a Non-Interacting Equilibrium simulation framework (TINIE)
=======================================================================

Overview
--------

We present to you a code that calculates conductance and electric
current running through 2D cavities, quantum dots or potential wells
with arbitrarily placed reservoirs in a perpendicular and constant
magnetic field. The code can be used in a wide range of calculations
involving 2D electron transport. The main difference between this code
and its competitors is the fact that TINIE does not need to be provided
with free parameters. The code is parallelized with ``mpi4py``, allowing
for computational tasks distribution across multiple processors.

Installation
------------

The code is a Python package (written using Python 3.6). In non-parallel
simulations, ``tinie`` can function without MPI-support in the
``HDF5``-library, but parallel simulations require the ``HDF5`` library
and its Python-wrapper ``h5py`` to be built with MPI support (see
`Parallel HDF5 – h5py
documentation <http://docs.h5py.org/en/stable/mpi.html>`__ for
installation instructions).

``tinie`` can be installed with ``pip``:

.. code:: bash

   $ pip install tinie

``tinie`` installs a command line interface toolset, and you can test
the functionality with the following commands:

.. code:: bash

   $ tinie_prepare
   $ tinie

Thorough test suite for the package has been implemented and can be
launched via ``python3 setup.py test`` from the root of the git
repository.

Package Functionality
---------------------

This package contains tools that could be used to calculate coupling of
a specific system that contains a central region (2DEG) and some leads.
After the coupling is calculated one could proceed to calculate
transmission coefficients and partial currents in the leads. All the
calculations are performed in Hartee atomic units. After installing the
package, a simple test run can be launched as follows:

.. code:: bash

   $ tinie_prepare
   $ tinie

Package Structure
-----------------

The code is written using object-oriented programming, and its
functionality can be shortly described in the following way: first,
``Lead``, and ``Center`` objects are created and passed as inputs for
the ``Coupling`` object and then all of them are passed into a
``SystemDump`` object, which calculates all the couplings and
Hamiltonians and dumps the data into an hdf5 file. ``SystemFetch`` is
then used to read the data from that hdf5 file. That data is passed into
the ``Calculator`` interface, where ``SelfEnergy`` interface calculates
the self-energies |selfenergy| and rate operators
|rateoperator| using the ``Coupling`` and the
eigenenergies of the ``Lead``.

.. |selfenergy| image:: https://latex.codecogs.com/svg.latex?\\Sigma_{L}(\\omega)
.. |rateoperator| image:: https://latex.codecogs.com/svg.latex?\\Gamma_{L}(\\omega)

After that, ``SelfEnergy`` for all the leads and the eigenenergies of
the ``Center`` are passed into the ``GreenFunction`` interface that
evaluates the advanced (|green_adv|) and retarded
(|green_ret|) Green’s functions, finalizing the
initialization of the ``Calculator``. From there the code is able to
compute the transmission matrix |transmat|
and the partial currents

|partial_current|

.. |green_adv| image:: https://latex.codecogs.com/svg.latex?G^{A}(\\omega)
.. |green_ret| image:: https://latex.codecogs.com/svg.latex?G^{R}(\\omega)
.. |transmat| image::  https://latex.codecogs.com/svg.latex?\\mathcal{T}_{\\alpha\\beta}(\\omega)=\\mathrm{Tr}[G^{R}(\\omega)\\Gamma_{\\beta}(\\omega)G^{A}(\\omega)\\Gamma_{\\alpha}(\\omega)]

.. |partial_current| image:: https://latex.codecogs.com/svg.latex?i_{\\alpha\\beta}=2\\int\\mathrm{d}\\omega\\frac{1}{2\\pi}[f(\\omega-V_{\\alpha}-\\mu)-f(\\omega-V_{\\beta}-\\mu)]\\mathcal{T}_{\\alpha\\beta}(\\omega)

in the lead, where |fd| is the Fermi-Dirac energy
distribution. Furthermore, it is then possible to compute other
transport properties, such as conductance at a specific temperature.
Additionally, we include the possibility of computing density of states
and local density of states.

.. |fd| image:: https://latex.codecogs.com/svg.latex?f(E)

Modular structure of the code allows for the implementation of your own
custom type of conducting channel ("lead"), quantum dot ("central
region") and coupling via implementation of a class that inherits from
``Lead``, ``Center`` or ``Coupling``. The details of how exactly the
classes should be implemented will be explained in the sections to
follow.

Example: Usage of TINIE with ITP2D
----------------------------------

To better demonstrate how TINIE is used, we will show it by means of an
example problem. We will compute transport properties of a quantum-dot
system with two leads in a magnetic field. Specifically, we shall
procure the information about the central region from ITP2D, a
Schrödinger equation eigensolver that interfaces with TINIE. The
following workflow is typical for most transport problems solved with
TINIE:

**Step 0:** computation of the Hamiltonian and wavefunctions of the
central region. We may obtain this information from any eigensolver of
our choosing, provided that it is TINIE-compatible. Quantum dot may be
modeled by a radial harmonic potential of form |Vharmonic|. Solving the first
25 states of this model with magnetic field strength |Bis1| is
done in ITP2D as follows:

.. |Vharmonic| image:: https://latex.codecogs.com/svg.latex?V(r)=\\frac{1}{2}\\omega_0 r^2
.. |Bis1| image:: https://latex.codecogs.com/svg.latex?B=1

.. code:: bash

   $ itp2d -v -n 20 -l 12 -s 100 -p "harmonic(1)" -B 1.0 -o ITP2D_FILE_PATH

Here the central region occupies a |6to6| region in both x-and y-directions
and is centered at the origin. More information about
usage of ITP2D can be found on its `bitbucket
page <https://bitbucket.org/luukko/itp2d/>`__.

.. |6to6| image:: https://latex.codecogs.com/svg.latex?[-6,\\,6]


**Step 1:** the transport system preparation step. In this step, the
coupling matrices for the leads are computed. Suppose we wish to compute
overlap coupling between the central region and the leads and we want to
vary the probe energy within each lead in range |0to2| with
energy spacing of |dEis0.001|. In this case, the first 5
states of the central region are sufficient for the calculation. Our
leads are such that:

.. |0to2| image:: https://latex.codecogs.com/svg.latex?[0,\\,2]
.. |dEis0.001| image:: https://latex.codecogs.com/svg.latex?\\Delta%20E=0.001

* Lead 0 is confined to region |-10to-4| in x-direction, \
  |-5to5| in y-direction and connects to the lead from the left;
* Lead 1 is confined to region |4to10| in x-direction, |-5to5| in y-direction 
  and connects to the lead from the right.

.. |-10to-4| image:: https://latex.codecogs.com/svg.latex?[-10,\\,-4]
.. |-5to5| image:: https://latex.codecogs.com/svg.latex?[-5,\\,5]
.. |4to10| image:: https://latex.codecogs.com/svg.latex?[4,\\,10]


Both leads in this case have harmonic potential of strength
|omega0=1| in y-direction, and particle-in-a-box
potential in x-direction. This information is sufficient for
us to commence the system preparation. For that, ``tinie_prepare``
script is used as follows:

.. |omega0=1| image:: https://latex.codecogs.com/svg.latex?\\omega_0=1


.. code:: bash

   $ tinie_prepare -dE 1e-3 -B 1.0 -ctr "itp2d(ITP2D_FILE_PATH,(0,4))" -l 2 -ld "finharm(left,1.0,dir)" "finharm(right,1.0,dir)" -xlim "[-10.0,-4.0]" "[4.0,10.0]" -ylim "[-5.0,5.0]" "[-5.0,5.0]" -Elim "[0.0,2.0]" "[0.0,2.0]" -cpl "overlap()" "overlap()" -o TINIE_PREPARE_FILE_PATH

This produces the PREPTINIEFile that contains the information about the
coupling of the transport system which can be reused for different
transport calculations of the next step.

**Step 2:** the transport calculation step. This is where the real fun
begins, the steps before are in a sense just a preparation. To compute
various transport properties of the system, such as transmission,
conductance and current, we fix temperature of the system
|T=1|, chemical potential |mu=1| and fix bias
voltages in the leads to be |V0=0.5| in Lead 0 and
|V1=1.5|. Moreover, we adjust the energy spacing of probe
electrons to |w0=0.01| and set the Green’s function
boundary parameter to |eta=0.1|. With this information we can
use ``tinie`` script as follows:

.. |mu=1| image:: https://latex.codecogs.com/svg.latex?\\mu=1
.. |T=1| image:: https://latex.codecogs.com/svg.latex?T=1
.. |V0=0.5| image:: https://latex.codecogs.com/svg.latex?V_0=0.5
.. |V1=1.5| image:: https://latex.codecogs.com/svg.latex?V_1=1.5
.. |w0=0.01| image:: https://latex.codecogs.com/svg.latex?\\omega_0=0.01
.. |eta=0.1| image:: https://latex.codecogs.com/svg.latex?\\eta=0.1


.. code:: bash

   $ tinie -i TINIE_PREPARE_FILE_PATH -dw 1e-2 -eta 1e-1 -T 1.0 -mu 1.0 -V 0.5 1.5 -o TINIE_FILE_PATH

This produces the TINIEFile that contains all the above mentioned
transport quantities and more, with detailed description of its contents
outlined in the sections below.

In addition to the transport properties, we can compute local and
standard density of states (LDOS/DOS) of the system via the
``tinie_dos`` script. To that end, in addition to the parameters
specified above, user would want to specify the energies at which LDOS
should be evaluated, as well as the location of the file with the
central region wavefunctions. We then use the script as follows:

.. code:: bash

   $ tinie_dos -i TINIE_PREPARE_FILE_PATH -psi ITP2D_FILE_PATH --wf-range 0 4 -w 1.0 2.0 3.0 -dw 1e-2 -eta 1e-1 -T 1.0 -mu 1.0 -V 0.5 1.5 -o TINIE_DOS_FILE_PATH

Here, we evaluated LDOS at probe energies
|win123|. Results of this calculation are
stored in TINIEDOSFile, with details about its contents available in
sections below.

.. |win123| image:: https://latex.codecogs.com/svg.latex?\\omega\\in\{1,2,3\}


**Step 3:** visualizing the results. To that end, one can use the
``tinie_draw`` script. Suppose we want to plot transmission,
conductance, total current and DOS of the system in the energy range
|0to5|, as well as LDOS at probe energy
|w=1|. We then use the following command:

.. |0to5| image:: https://latex.codecogs.com/svg.latex?[0,5]
.. |w=1| image:: https://latex.codecogs.com/svg.latex?\\omega=1

.. code:: bash

   $ tinie_draw -i TINIE_FILE_PATH -idos TINIE_DOS_FILE_PATH -E 0.0 5.0 --ldos-E 1.0 --transmission --conductance --total-currents --dos --ldos -o FIGURE_PATH

This will produce beautiful LaTeX-rendered plots of the aforementioned
quantities. Below we show the example plots of conductance, DOS and LDOS
produced by the script:

=========== ======== =========
Conductance DOS      LDOS
=========== ======== =========
|image8|    |image9| |image10|
=========== ======== =========

Quantum transport calculations in two-dimensional systems have never been this easy!

Currently Implemented System Classes
------------------------------------

As of now, the following system classes are implemented:

* ``Center`` objects, located in ``transport_calculator/systems/central_region``
* ``Itp2dCenter``: itp2d-compatible interface.
* ``CustomCenter``: container for a custom predefined central region Hamiltonian |Hc|.
* ``Lead`` objects, located in ``transport_calculator/systems/leads``. Note that wavefunction normalization has \
  been omitted for the sake of compactness of the expression. Wavefunctions in the code are all normalized.
* ``FiniteHarmonicLead``: lead described by a wavefunction \
  |FiniteHarmonicLeadWF|, \
  where |HermiteL| is the the Hermite polynomial of order l, \
  |qexpr|, |omegac|, |omegac0| with |omega0| being the frequency of quantum harmonic oscillator \
  and |B| being magnetic field strength. The formula is provided \
  in Hartee atomic units. x and y coordinate \
  wavefunctions are interchangeable depending on the lead alignment.
* ``BoxLead``: particle in a box lead describe by wavefunction |BoxLeadWF| \
  where |Lx| and |Ly| are the length and width of the box correspondingly and \
  |klrange|.
* ``CustomLead``: container for a custom predefined lead region Hamiltonian |HL|
* ``Coupling`` objects, located in ``transport_calculator/systems/couplings``
* ``OverlapCoupling``: strong coupling of the type |Voverlap|, \
  where |psiLi| is the ith eigenfunction of the lead and |psiCj| s the  jth \
  eigenfunction of the central region and |Omega| is the overlap region of the lead and the quantum-dot.
* ``TightBindingCoupling``: weak coupling between non-overlapping lead and central regions of the type \
  |Vtightbinding| where |theta|, |OmegaL| is the lead region to be coupled and |Omegac| \
  is the central region to be coupled.
* ``OneLayerCoupling``: weak coupling between the boundaries of a non-overlapping lead and central regions of the type \
  |Vonelayer|.
* ``CustomCoupling``: container for custom predefined coupling matrix |V|. Compatible only with \
  ``CustomCenter`` and ``CustomLead`` objects.

The implementational details of these elements can be checked in the source code, which is rich with insightful and
helpful comments.


.. |Hc| image:: https://latex.codecogs.com/svg.latex?\\mathbf{H}^C
.. |FiniteHarmonicLeadWF| image:: https://latex.codecogs.com/svg.latex?\\psi^{L}_{k,l}(x,q)=\\cos\\left[k(x-x^{L}_{max})+\\frac{\\pi}{2}\\right]e^{-\\frac{1}{2}q^2}H_{l}(q)
.. |HermiteL| image:: https://latex.codecogs.com/svg.latex?H_l(q)
.. |qexpr| image:: https://latex.codecogs.com/svg.latex?q=\\sqrt{\\omega_{c0}y-\\frac{l}{B}\\frac{\\omega^{2}_{c}}{\\omega^{2}_{c0}}}
.. |omegac| image:: https://latex.codecogs.com/svg.latex?\\omega_{c}=B
.. |omegac0| image:: https://latex.codecogs.com/svg.latex?\\omega^2_{c0} = \\omega_c^2+\\omega_0^2
.. |omega0| image:: https://latex.codecogs.com/svg.latex?\\omega_0
.. |B| image:: https://latex.codecogs.com/svg.latex?B
.. |BoxLeadWF| image:: https://latex.codecogs.com/svg.latex?\\psi^{L}_{k,l}(x,y)=\\sin\\left[\\frac{k\\pi}{L_{x}}(x-x^L_{max})\\right]\\sin\\left[\\frac{l\\pi}{L_{y}}(y-y^L_{max})\\right]
.. |Lx| image:: https://latex.codecogs.com/svg.latex?L_x
.. |Ly| image:: https://latex.codecogs.com/svg.latex?L_y
.. |klrange| image:: https://latex.codecogs.com/svg.latex?k,l%20\\in\\mathbb{Z}_{+}\\setminus\\{0\\}
.. |HL| image:: https://latex.codecogs.com/svg.latex?\\mathbf{H}^L
.. |Voverlap| image:: https://latex.codecogs.com/svg.latex?\\mathbf{V}_{ij}=-\\frac{1}{2}\\int_{\\Omega}\\mathrm{d}\\mathbf{r}\\psi^{*}_{L,i}(\\mathbf{r})\\Delta\\psi_{C,j}(\\mathbf{r})
.. |Omega| image:: https://latex.codecogs.com/svg.latex?\\Omega
.. |psiLi| image:: https://latex.codecogs.com/svg.latex?\\psi_{L,i}
.. |psiCj| image:: https://latex.codecogs.com/svg.latex?\\psi_{C,j}
.. |Vtightbinding| image:: https://latex.codecogs.com/svg.latex?\\mathbf{V}_{ij}=-\\frac{1}{2}\\int_{\\Omega_{L}}\\mathrm{d}\\mathbf{r'}\\psi^{*}_{L,i}(\\mathbf{r'})\\int_{\\Omega_{C}}\\mathrm{d}\\mathbf{r}\\frac{\\psi_{C,j}(\\mathbf{r})}{\\Vert\\mathbf{r'}-\\mathbf{r}\\Vert^2}e^{-i\\theta}
.. |theta| image:: https://latex.codecogs.com/svg.latex?\\theta=-\\frac{B}{2}(x'-x)(y'-y)
.. |OmegaL| image:: https://latex.codecogs.com/svg.latex?\\Omega_L
.. |OmegaC| image:: https://latex.codecogs.com/svg.latex?\\Omega_C
.. |Vonelayer| image:: https://latex.codecogs.com/svg.latex?\\mathbf{V}_{ij}=-\\frac{1}{2}\\int_{\\partial\\Omega_{L}}\\mathrm{d}\\mathbf{r'}\\psi^{*}_{L,i}(\\mathbf{r'})\\int_{\\partial\\Omega_{C}}\\mathrm{d}\\mathbf{r}\\frac{\\psi_{C,j}(\\mathbf{r})}{\\Vert\\mathbf{r'}-\\mathbf{r}\\Vert^2}e^{-i\\theta}
.. |V| image:: https://latex.codecogs.com/svg.latex?V


Adding Your Own Custom System Classes
-------------------------------------

As it has been mentioned before, the code has been designed in such a
way as to allow as much freedom in expansion as possible. In particular,
you can introduce additional types of central regions, lead regions and
coupling methods. All you have to do is to create your own class file in
the corresponding folder in ``tinie/systems`` and make sure that the
class you are creating inherits from one of the basic abstract classes
(``Center``, ``Lead`` or ``Coupling``). Below you can find a list of
functions you would have to implement (correctly) in order for your
custom class to be fully integrated into the transport scheme:

-  ``Center`` region:

   -  ``__init__(*attrs)``: initializer
   -  ``get_type_specific_parameters()``: retrieves child-specific extra
      parameters
   -  ``get_energies()``: retrieves central region Hamiltonian
      |HC|
   -  ``get_potential()``: retrieves potential energy values in the
      central region
   -  ``get_state(n)``: retrieves nth wavefunction
   -  ``get_states()``: retrieves all wavefunctions on the grid
   -  ``get_number_of_states()``: retrieves the number of states in the
      central region
   -  ``get_sliced_state(n, width, side)``: retrieves nth
      wavefunction on a grid slice
   -  ``get_sliced_states(width, side)``: retrieves all wavefunctions on
      a grid slice
   -  ``get_boundary_state(n, side)``: retrieves nth wavefunction
      evaluated on some boundary
   -  ``get_coordinate_ranges()``: retrieves x and y coordinate ranges
   -  ``get_coordinates()``: retrieves the coordinate meshes
   -  ``get_slice_coordinates(width, side)``: retrieves the sliced
      coordinate meshes
   -  ``get_boundary_coordinates(side)``: retrieves the boundary
      coordinate range

-  ``Lead`` region:

   -  ``__init__(*attrs)``: initializer
   -  ``set_magnetic_field_strength(B)``: sets magnetic field strength
   -  ``set_energy_spacing(delta_E)``: sets lead energy spacing
   -  ``get_type_specific_parameters()``: retrieves child-specific extra
      parameters
   -  ``get_energies()``: retrieves lead region Hamiltonian |HL|
   -  ``get_state_point(x, y, n)``: evaluates the nth state
      wavefunction at a single point |xy|
   -  ``get_state(x_points, y_points, n, mode)``: retrieves the nth state wavefunction on a custom/discretized grid
   -  ``get_number_of_states()``: retrieves the number of states in the
      lead region
   -  ``get_boundary_state(n, num_boundary_points)``: retrieves
      nth wavefunction evaluated on the lead boundary
   -  ``get_boundary(num_boundary_points)``: retrieves the boundary grid
      with specified discretization

.. |xy| image:: https://latex.codecogs.com/svg.latex?(x,y)

-  ``Coupling`` region:

   -  ``__init__(Center_object, Lead_object, *attrs)``: initializer,
      sets the center and lead objects ready for the coupling matrix
      calculations
   -  ``get_coupling_matrix_element(i, j)``: retrieves coupling matrix
      element |Vij|, that is, the coupling between
      ith lead state and jth central state
   -  ``get_coupling_matrix()``: retrieves the coupling matrix
      |bfV|
      
.. |Vij| image:: https://latex.codecogs.com/svg.latex?V_{ij}
.. |bfV| image:: https://latex.codecogs.com/svg.latex?\\mathbf{V}


Details about the input/output parameter types can be found in the
source code. Upon implementing all of these functions correctly for the
corresponding custom object and extending the parser interface
accordingly, the code extension will be fully consistent with the
original code!

Scripts Included in the Package
-------------------------------

tinie includes a few scripts that should ease the usage of the software:

tinie_prepare
-------------

This script prepares the coupling system and saves it in a ``tinie_prepare``
hdf5 file, which contains the following attributes and datasets:

+---------------------------------+--------------------------------------+
| Attribute                       | Description                          |
+=================================+======================================+
| ``type``                        | File type, must be "PREPTINIEFile"   |
+---------------------------------+--------------------------------------+
| ``center/type``                 | Type of the central region           |
+---------------------------------+--------------------------------------+
| ``center/num_states``           | Number of states in the central      |
|                                 | region                               |
+---------------------------------+--------------------------------------+
| ``center/parameters``           | Type-dependent parameters of the     |
|                                 | central region                       |
+---------------------------------+--------------------------------------+
| ``leads/num_leads``             | Number of leads                      |
+---------------------------------+--------------------------------------+
| ``leads/lead_n/type``           | Type of the lead n                   |
+---------------------------------+--------------------------------------+
| ``leads/lead_n/num_states``     | Number of states in lead n           |
+---------------------------------+--------------------------------------+
| ``leads/lead_n/energy_spacing`` | Energy spacing in lead n             |
+---------------------------------+--------------------------------------+
| ``leads/lead_n/parameters``     | Type-dependent parameters of lead n  |
+---------------------------------+--------------------------------------+
| ``couplings/num_couplings``     | Number of couplings                  |
+---------------------------------+--------------------------------------+
| ``couplings/coupling_n/type``   | Type of coupling between lead        |
|                                 | n and the central region             |
+---------------------------------+--------------------------------------+

+------------------------------------------+---------------------------------------------------------------+
| Dataset                                  | Description                                                   |
+==========================================+===============================================================+
| ``center/hamiltonian``                   | Hamiltonian of the central region                             |
+------------------------------------------+---------------------------------------------------------------+
| ``center/potential``                     | Potential energy values in the central region                 |
+------------------------------------------+---------------------------------------------------------------+
| ``leads/lead_n/hamiltonian``             | Hamiltonian of the lead region n                              |
+------------------------------------------+---------------------------------------------------------------+
| ``leads/lead_n/x_axis_limits``           | x-axis limits of lead n                                       |
+------------------------------------------+---------------------------------------------------------------+
| ``leads/lead_n/y_axis_limits``           | y-axis limits of lead n                                       |
+------------------------------------------+---------------------------------------------------------------+
| ``leads/lead_n/energy_limits``           | Energy limits of lead n                                       |
+------------------------------------------+---------------------------------------------------------------+
| ``couplings/coupling_n/coupling_matrix`` | Coupling matrix between lead n and the central region         |
+------------------------------------------+---------------------------------------------------------------+

Some of these datasets are stored in chunked/compressed format for more
data-intensive simulations. All the simulation parameters are adjusted
via a parser user interface, which takes the following arguments (type
``tinie_prepare --help`` if you ever feel lost!):

+---------------------+--------------------------------------------------------+
| Argument            | Description                                            |
+=====================+========================================================+
| ``-dE``,            | Lead energy spacing                                    |
| ``--delta-E``       |                                                        |
+---------------------+--------------------------------------------------------+
| ``-B``              | Magnetic field strength                                |
+---------------------+--------------------------------------------------------+
| ``-xlim``,          | x-axis limits of each lead, typed in form              |
| ``--x-axis-limits`` | ``[x_min_0, x_max_0] [x_min_1, x_max_1] ...``          |
+---------------------+--------------------------------------------------------+
| ``-ylim```          | y-axis limits of each lead, typed in form              |
| ``--y-axis-limits`` | ``[y_min_0, y_max_0] [y_min_1, y_max_1] ...``          |
+---------------------+--------------------------------------------------------+
| ``-Elim``           | Energy limits of each lead, typed in form              |
| ``--energy-limits`` | ``[E_min_0, E_max_0] [E_min_1, E_max_1] ...``          |
+---------------------+--------------------------------------------------------+
| ``-ctr``            | Central region type, typed in as                       |
| ``--center-type``   | ``"ctr_type(*ctr_params)"``                            |
+---------------------+--------------------------------------------------------+
| ``-l``              | Number of leads                                        |
| ``--lead-number``   |                                                        |
+---------------------+--------------------------------------------------------+
| ``-ld``             | Lead region types, typed in form                       |
| ``--lead-types``    | ``"ld0_type(*ld0_params)"``                            |
|                     | ``"ld1_type(*ld1_params)" ...``                        |
+---------------------+--------------------------------------------------------+
| ``-cpl`             | Coupling region types, typed in form                   |
| ``--coupling-types``| ``"cpl0_type(*cpl0_params)"``                          |
|                     | ``"cpl1_type(*cpl1_params)" ...``                      |
+---------------------+--------------------------------------------------------+
| ``-o``,             | Path, where preptinie file is saved                    |
| ``--output-file``   |                                                        |
+---------------------+--------------------------------------------------------+

tinie
-----

This script reads the preptinie hdf5 file, performs the transport
calculation and saves the results in a tinie hdf5 with the following
attributes and datasets:

+----------------------------------+--------------------------------------------------------+
| Attribute                        | Description                                            |
+==================================+========================================================+
| ``type``                         | File type, must be "TINIEfile"                         |
+----------------------------------+--------------------------------------------------------+
| ``evaluated_chemical_potential`` | Chemical potential |mu| of the system                  |
+----------------------------------+--------------------------------------------------------+
| ``evaluated_bias_voltage``       | Bias voltage in the leads of the system                |
+----------------------------------+--------------------------------------------------------+
| ``evaluated_temperature``        | Temperature of the system                              |
+----------------------------------+--------------------------------------------------------+
| ``omega_spacing``                | Probe energy spacing                                   |
+----------------------------------+--------------------------------------------------------+
| ``lead_energy_spacing``          | Lead energy spacing                                    |
+----------------------------------+--------------------------------------------------------+
| ``eta``                          | Small number |eta| used in the Green's function        |
+----------------------------------+--------------------------------------------------------+
| ``number_of_couplings``          | Number of couplings in the system                      |
+----------------------------------+--------------------------------------------------------+

.. |eta| image:: https://latex.codecogs.com/svg.latex?\\eta

+-----------------------------------------+-------------------------------------------------------+
| Dataset                                 | Description                                           |
+=========================================+=======================================================+
| ``partial_currents``                    | Matrix of partial currents between each lead          |
+-----------------------------------------+-------------------------------------------------------+
| ``total_currents``                      | Total currents in each lead                           |
+-----------------------------------------+-------------------------------------------------------+
| ``omega_dependent_partial_currents``    | Energy profile of the partial current matrix          |
+-----------------------------------------+-------------------------------------------------------+
| ``omega_ldos_dependent_total_currents`` | Energy profile of the total currents                  |
+-----------------------------------------+-------------------------------------------------------+
| ``transmission``                        | Transmission matrix as a function of the probe energy |
+-----------------------------------------+-------------------------------------------------------+
| ``transmission_error``                  | Imaginary component of transmission                   |
+-----------------------------------------+-------------------------------------------------------+
| ``conductance``                         | System conductance matrix                             |
+-----------------------------------------+-------------------------------------------------------+

.. |mu| image:: https://latex.codecogs.com/svg.image?\\mu

Some of these datasets are stored in chunked/compressed format for more
data-intensive simulations. All the transport calculation parameters are
adjusted via a parser user interface, which takes the following
arguments (type ``tinie --help`` if you ever feel lost!):

+-------------------------------------+-------------------------------------------------------------------------------------------------+
| Argument                            | Description                                                                                     |
+=====================================+=================================================================================================+
| ``-dw`, ``--delta-omega``           | Probe energy spacing                                                                            |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-eta``                            | Small imaginary constant used in calculating Green's function                                   |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``--mu``, ``--chem-pot``            | Chemical potential at which the system is evaluated                                             |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-V``, ``--lead-bias``             | Lead biases, at which the system is evaluated, typed in form ``V_0 V_1 ...``                    |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-T``, ``--temperature``           | Temperature at which the system is evaluated                                                    |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-i``, ``--input-file``            | Path to the ``tinie_prepare``'s output file                                                     |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-o``, ``--output-file``           | Path for the output file                                                                        |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``--wide-band``, ``--no-wide-band`` | Boolean flags user can specify if they wish to use the wide band approximation methods (or not) |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-S``, ``--self-energy``           | Path from which an array of custom self energies is read                                        |
+-------------------------------------+-------------------------------------------------------------------------------------------------+
| ``-G``, ``--rate-operator``         | Path from which an array of custom rate operators is read                                       |
+-------------------------------------+-------------------------------------------------------------------------------------------------+

Note that if you wish to use the wide band approximation approach you
must specify either self energies or rate operators or both!

tinie_dos
---------

This scripts reads the preptinie hdf5 file and the file containing the
eigenfunctions of the central region, computes DOS/LDOS and saves the
results in dostinie hdf5 file with the following attributes and
datasets:

========= =================================
Attribute Description
========= =================================
``type``  File type, must be "TINIEDOSFile"
========= =================================

============== ==========================================
Dataset        Description
============== ==========================================
``dos``        Density of states values
``ldos``       Local density of states values
``x``          x-axis values of the system central region
``y``          y-axis values of the system central region
``omega_dos``  Energies at which DOS was evaluated
``omega_ldos`` Energies at which LDOS was evaluated
============== ==========================================

Some of these datasets are stored in chunked/compressed format for more
data-intensive simulations. All the DOS/LDOS calculation parameters are
adjusted via a parser user interface, which takes the following
arguments (type ``tinie_dos --help`` if you ever feel lost!):

+-----------------------------+---------------------------------------------------------------------------+
| Argument                    | Description                                                               |
+-----------------------------+---------------------------------------------------------------------------+
| ``-w``, ``--omega-ldos``    | Probe energies at which the LDOS should be avaluated                      |
+-----------------------------+---------------------------------------------------------------------------+
| ``-dw``, ``--delta-omega``  | Probe energy spacing                                                      |
+-----------------------------+---------------------------------------------------------------------------+
| ``-eta``                    | Small imaginary constant used in the calculation of the Green's function  |
+-----------------------------+---------------------------------------------------------------------------+
| ``--mu``, ``--chem-pot``    | Chemical potential at which the system is evaluated                       |
+-----------------------------+---------------------------------------------------------------------------+
| ``-V``, ``--lead-bias``     | Lead biases at which the system is evaluated, typed in as ``V_0 V_1 ...`` |
+-----------------------------+---------------------------------------------------------------------------+
| ``-T``, ``--temperature``   | Temperature at which the system is evaluated                              |
+-----------------------------+---------------------------------------------------------------------------+
| ``-i``, ``--input-file``    | Path to the ``tinie_prepare``'s output file                               |
+-----------------------------+---------------------------------------------------------------------------+
| ``--psi``, ``--wf-file``    | Path from which central region wavefunctions are read                     |
+-----------------------------+---------------------------------------------------------------------------+
| ``-o``, ``--output-file``   | Path where the ``tinie_dos``` file is saved                               |
+-----------------------------+---------------------------------------------------------------------------+
| ``--dos``, ``--no-dos``     | Boolean, decides if DOS is computed                                       |
+-----------------------------+---------------------------------------------------------------------------+
| ``--ldos``, ``--no-ldos``   | Boolean, decides if LDOS is computed                                      |
+-----------------------------+---------------------------------------------------------------------------+


tinie_draw
----------

This script reads data from the tinie hdf file, makes pretty
transmission/backsacttering/current/density of states plots and saves
them. This script has a parser user interface, where you can specify the
following plot arguments:

+---------------------------------------------------+---------------------------------------------------------------+
| Argument                                          | Description                                                   |
+===================================================+===============================================================+
| ``-i``, ``--input-file``                          | Path to the ``tinie``-file                                    |
+---------------------------------------------------+---------------------------------------------------------------+
| ``-idos``, ``--input-dos-file``                   | Path to the ``tinie_dos``-file                                |
+---------------------------------------------------+---------------------------------------------------------------+
| ``-o``, ``--output-file``                         | Basepath for plots                                            |
+---------------------------------------------------+---------------------------------------------------------------+
| ``-E``, ``--energy-rangs``                        | Range of energies over which to draw the figures              |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--transmission``, ``--no-transmission``         | Boolean, decides if transmission is plotted                   |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--backscattering``, ``--no-backscattering``     | Boolean, decides if backscattering is plotted                 |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--partial-currents``, ``--no-partial-currents`` | Boolean, decides if partial currents are plotted              |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--total-currents``, ``--no-total-currents``     | Boolean, decides if total currents are plotted                |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--dos``, ``--no-dos``                           | Boolean, decides if DOS is plotted                            |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--ldos``, ``--no-ldos``                         | Boolean, decides if LDOS is plotted                           |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--norm-ldos``, ``--no-norm-ldos``               | Boolean, decides if the LDOS will be normalized to 1          |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--ldos-E``                                      | Evaluate LDOS at an index corresponding to a probe energy     |
+---------------------------------------------------+---------------------------------------------------------------+
| ``--stability``, ``--no-stability``               | Boolean, decides if the numerical stability tests are plotted |
+---------------------------------------------------+---------------------------------------------------------------+


make_system_files
-----------------

This script generates custom Hamiltonians or coupling matrices and saves
them in a .npy file to be passed on as arguments for
``CustomCenter``/``CustomLead``/``CustomCoupling`` objects. They can
also be used to generate custom self-energy/rate operators for the
wide-band approximation. Run the script, follow the instructions and the
rest is history.

Naturally, these scripts provide only some of the basic functionality
extensions. Additional scripts/code modifications may be added based on
the user’s end goals.

.. |pypi license| image:: https://img.shields.io/pypi/l/tinie?color=blue
   :target: https://pypi.org/project/tinie/
.. |pypi version| image:: https://img.shields.io/pypi/v/tinie
   :target: https://pypi.org/project/tinie
.. |pypi status| image:: https://img.shields.io/pypi/status/tinie
   :target: https://pypi.org/project/tinie
.. |Python implementation| image:: https://img.shields.io/pypi/implementation/tinie.svg
   :target: https://pypi.org/project/tinie/
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/tinie.svg
   :target: https://pypi.org/project/tinie/
.. |Python wheel| image:: https://img.shields.io/pypi/wheel/tinie.svg
   :target: https://pypi.org/project/tinie/
.. |pipeline status| image:: https://gitlab.com/compphys-public/tinie/badges/master/pipeline.svg
   :target: https://gitlab.com/compphys-public/tinie/-/commits/master
.. |coverage report| image:: https://gitlab.com/compphys-public/tinie/badges/master/coverage.svg
   :target: https://gitlab.com/compphys-public/tinie/-/commits/master
.. |image8| image:: https://gitlab.com/compphys-public/tinie/-/raw/master/example_figures/conductance.png
.. |image9| image:: https://gitlab.com/compphys-public/tinie/-/raw/master/example_figures/dos.png
.. |image10| image:: https://gitlab.com/compphys-public/tinie/-/raw/master/example_figures/ldos.png
