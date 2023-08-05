Spinney
*******

Purpose
=======

**Spinney** is a software package developed in order to assist with first-principles investigations of point defects in solids 
within the supercell approach.
For this purpose, several tools able to aid in the various steps associated with this kind of studies are implemented. 

Some of the tasks that Spinney is able to perform are:

 - Compute, from external data (taken for example from online repositories), the ranges of validity 
   for the elements chemical potentials according to thermodynamic constraints;
 - Calculate the correction energy due to electrostatic finite-size-effects in charged supercells;
 - Calculate defect formation energies and transition levels;
 - Calculate defects and carriers concentrations.

**Spinney** is written in Python and offers a very general and flexible user interface which can be easily integrated with any first-principles code.

Installation
============

The easiest way to install **Spinney** is through `pip`:

::
    
    pip install spinney

We suggest to create a virtual environment in which the **Spinney** code can be installed.

The requirement for a successful installation are:

 - `Python` version 3.4 or newer;
 - `NumPy <https://www.numpy.org>`_ version  1.12 or newer;
 - `SciPy <https://www.scipy.org>`_ version 1.4 or newer;
 - `Pandas <https://pandas.pydata.org/>`_ version 0.25 or newer;
 - `Matplotlib <https://matplotlib.org/>`_ version 3.1.0 or newer;
 - `Atomic Simulation Environment <https://wiki.fysik.dtu.dk/ase>`_ version 3.18 or newer.

.. warning::

    **Spinney** **does not** support older versions of ASE.

Authors
-------
 - Marco Arrigoni - marco.arrigoni@tuwien.ac.at
 - Georg K. H. Madsen
