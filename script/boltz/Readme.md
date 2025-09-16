virtual screaning boltz
==========

Description
-----------

This procedure performs molecular screening of generated compounds against target proteins using boltz2.

Usage
-----------

Molecular Screening with Boltz2

Follow the steps below to perform molecular screening with Boltz2:

Place the generated mol.csv file into the working directory for Boltz2 virtual screening.

Edit the grp_1.yaml and hsp_1.yaml files by replacing the protein field with the target protein for affinity prediction.

Run the following scripts to generate the Boltz2 configuration files (example with placeholder paths):

```
python generate_grp_yaml.py
python generate_hsp_yaml.py
```

Execute the prediction using the command below (replace with your actual paths):

```
CUDA_VISIBLE_DEVICES=6 boltz predict path/to/input \
  --use_msa_server \
  --devices 1 \
  --out_dir path/to/output \
  --cache path/to/weight \
  --no_trifast
```