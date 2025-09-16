virtual screaning vina
==========

Description
-----------

This procedure performs molecular screening of generated compounds against target proteins using AutoDock Vina.

Usage
-----------

Molecular Screening with AutoDock Vina

Follow the steps below to perform molecular screening using AutoDock Vina:

Save all generated SMILES from the molecular generation step into a file named smiles.txt (one SMILES per line).

Update the file paths and docking box coordinates in the script.

Run the following scripts to perform the screening:

```
python vina_docking_Grp94.py
python vina_docking_Hsp90.py
```