import os
import json
import tempfile
import re
import shutil
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import reinvent
from reinvent.notebooks import load_tb_data, plot_scalars, get_image, create_mol_grid
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path


## Path Configuration
# IMPORTANT: Replace all placeholder paths below with your actual system paths

# 1. DockStream paths
# TODO: Set the path to your DockStream installation directory
dockstream_dir = "PLACEHOLDER_DOCKSTREAM_DIR"  # e.g., "/home/user/program/DockStream"
# TODO: Set the path to your DockStream conda environment
dockstream_env = "PLACEHOLDER_DOCKSTREAM_ENV"  # e.g., "/home/user/anaconda3/envs/DockStream"
docker_path = os.path.join(dockstream_dir, "docker.py")
target_preparator_path = os.path.join(dockstream_dir, "target_preparator.py") 

# TODO: Set the output directory for docking results
output_dir = "PLACEHOLDER_OUTPUT_DIR"  # e.g., "/home/user/task/docking-test/test3/docking_output/Grp94"

# 3.2 Receptor and ligand storage paths
# TODO: Set the path to the receptor PDB file
apo_1UYD_path = "PLACEHOLDER_RECEPTOR_PDB_PATH"  # e.g., "/home/user/task/docking-test/test3/docking_input/Grp94/Grp94.pdb"
# TODO: Set the path to the reference ligand PDB file
reference_ligand_path = "PLACEHOLDER_REFERENCE_LIGAND_PATH"  # e.g., "/home/user/task/docking-test/test3/docking_input/Grp94/ligand.pdb"
# TODO: Set the path to the SMILES file
smiles_path = "PLACEHOLDER_SMILES_PATH"  # e.g., "/home/user/task/docking-test/test3/smiles.txt"

# 3.3 Receptor preparation paths
target_prep_path = output_dir + "/ADV_target_prep.json"   # Configuration file path for receptor preparation
fixed_pdb_path = output_dir + "/ADV_fixed_target.pdb"   # Processed receptor PDB file path
adv_receptor_path = output_dir + "/ADV_receptor.pdbqt"   # Processed receptor PDBQT file path (PDB converted to PDBQT for docking)
log_file_target_prep = output_dir + "/ADV_target_prep.log"   # Log file for receptor preparation

# 3.4 Docking paths
docking_path = output_dir + "/ADV_docking.json"   # Docking configuration path
ligands_conformers_path = output_dir + "/ADV_embedded_ligands.sdf"   # Processed ligand SDF file path
ligands_docked_path = output_dir + "/ADV_ligands_docked.sdf"   # Final position and conformation SDF file path after docking
ligands_scores_path = output_dir + "/ADV_scores.csv"   # Ligand scoring file path
log_file_docking = output_dir + "/ADV_docking.log"   # Docking log file path

# 4. AutoDock Vina paths
# TODO: Set the path to your AutoDock Vina binary location
vina_binary_location = "PLACEHOLDER_VINA_BINARY_PATH"  # e.g., "/home/user/program/AutoDock-Vina/autodock_vina_1_1_2_linux_x86/bin"
# TODO: Set the path for docked ligand poses output
ligands_docked_poses_path = "PLACEHOLDER_DOCKED_POSES_PATH"  # e.g., "/home/user/task/docking-test/test3/docking_output/Grp94"
# TODO: Set the path for docking scores output
ligands_docking_scores_path = "PLACEHOLDER_DOCKING_SCORES_PATH"  # e.g., "/home/user/task/docking-test/test3/docking_output/Grp94"

# 5. REINVENT output path
# TODO: Set the working directory for REINVENT output
wd = "PLACEHOLDER_REINVENT_WD"  # e.g., "/home/user/task/docking-test/test3/docking_output/Grp94"

shutil.rmtree(output_dir, ignore_errors=True)
os.mkdir(output_dir)



### Step 2: Process receptor
## Configuration file
tp_dict = {
  "target_preparation":
  {
    "header": {                                   # general settings
      "logging": {                                # logging settings (e.g. which file to write to)
        "logfile": log_file_target_prep
      }
    },
    "input_path": apo_1UYD_path,                  # this should be an absolute path
    "fixer": {                                    # based on "PDBFixer"; tries to fix common problems with PDB files
      "enabled": True,
      "standardize": True,                        # enables standardization of residues
      "remove_heterogens": True,                  # remove hetero-entries
      "fix_missing_heavy_atoms": True,            # if possible, fix missing heavy atoms
      "fix_missing_hydrogens": True,              # add hydrogens, which are usually not present in PDB files
      "fix_missing_loops": False,                 # add missing loops; CAUTION: the result is usually not sufficient
      "add_water_box": False,                     # if you want to put the receptor into a box of water molecules
      "fixed_pdb_path": fixed_pdb_path            # if specified and not "None", the fixed PDB file will be stored here
    },
    "runs": [                                     # "runs" holds a list of backend runs; at least one is required
      {
        "backend": "AutoDockVina",                # one of the backends supported ("AutoDockVina", "OpenEye", ...)
        "output": {
          "receptor_path": adv_receptor_path      # the generated receptor file will be saved to this location
        },
        "parameters": {
          "pH": 7.4,                              # sets the protonation states (NOT used in Vina)
          "extract_box": {                        # in order to extract the coordinates of the pocket (see text)
            "reference_ligand_path": reference_ligand_path,   # path to the reference ligand
            "reference_ligand_format": "PDB"                  # format of the reference ligand
          }
}}]}}

with open(target_prep_path, 'w') as f:
    json.dump(tp_dict, f, indent="    ")

## Run receptor processing program
subprocess.run([f"{dockstream_env}/bin/python", target_preparator_path, "-conf", target_prep_path])
with open(adv_receptor_path, 'r') as file:
    for i in range(25):
        print(file.readline(), end='')

## Output configuration file (docking box parameters can be found here)
result = subprocess.run(["cat", log_file_target_prep], capture_output=True, text=True)
if result.returncode == 0:
    print(result.stdout)
else:
    print("Error:", result.stderr)


### 第三步：对接配置
##dockstream配置
ed_dict = {
  "docking": {
    "ligand_preparation": {                      # the ligand preparation part, defines how to build the pool
      "embedding_pools": [
          {
          "pool_id": "RDkit_pool",
          "type": "RDkit",
          "parameters": {
            "addHs": True,
            "coordinate_generation": {
              "method": "UFF",
              "maximum_iterations": 300
            }
          },
          "input": {
            "standardize_smiles": False,
            "type": "smi",
            "input_path": smiles_path
          },
          "output": {                            # the conformers can be written to a file, but 
                                                 # "output" is not required
            "conformer_path": ligands_conformers_path,
            "format": "sdf"
          }
        }
      ]
    },
    "docking_runs": [
    {
      "backend": "AutoDockVina",
      "run_id": "AutoDockVina",
      "input_pools": ["RDkit_pool"],
      "parameters": {
        "binary_location": vina_binary_location,        # absolute path to the folder, where the "vina" binary
                                                        # can be found
        "parallelization": {
          "number_cores": 32
        },
        "seed": 42,                                     # use this "seed" to generate reproducible results; if
                                                        # varied, slightly different results will be produced
        "receptor_pdbqt_path": [adv_receptor_path],     # paths to the receptor files
        "number_poses": 10,                              # number of poses to be generated
        "search_space": {                               # search space (cavity definition); see text
          "--center_x": 17.8,
          "--center_y": -19.3,
          "--center_z": 53.3,
          "--size_x": 17.0,
          "--size_y": 17.3,
          "--size_z": 18.0
        }
      },
      "output": {
        "poses": { "poses_path": ligands_docked_path },
        "scores": { "scores_path": ligands_scores_path }
}}]}}

with open(docking_path, 'w') as f:
    json.dump(ed_dict, f, indent=2)

cmd = [
    f"{dockstream_env}/bin/python",
    docker_path,
    "-conf", docking_path,
    "-print_scores",
]
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print(result.stdout)
else:
    print("Error:", result.stderr)

print("Docking process completed successfully.")

print("=" * 100)  # Print 100 '=' characters
