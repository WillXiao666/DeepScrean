import pandas as pd
import os
import yaml
from pathlib import Path

def create_yaml_files():
    """
    Create YAML files for all SMILES in the mols.csv file
    """
    # TODO: Replace with actual input CSV file path
    input_csv = 'PLACEHOLDER_INPUT_CSV_PATH'  # Default: 'mols.csv'
    
    # TODO: Replace with actual template YAML file path
    template_yaml = 'PLACEHOLDER_TEMPLATE_YAML_PATH'  # Default: 'hsp_1.yaml'
    
    # TODO: Replace with actual output directory path
    output_dir = Path('PLACEHOLDER_OUTPUT_DIR_PATH')  # Default: 'hsp_config'
    
    # Create hsp_config folder
    output_dir.mkdir(exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Read mols.csv file
    try:
        df = pd.read_csv(input_csv)
        print(f"Successfully read {input_csv} file, total {len(df)} records")
    except Exception as e:
        print(f"Failed to read {input_csv} file: {e}")
        return
    
    # Read hsp_1.yaml template file
    try:
        with open(template_yaml, 'r', encoding='utf-8') as f:
            template_data = yaml.safe_load(f)
        print(f"Successfully read {template_yaml} template file")
    except Exception as e:
        print(f"Failed to read {template_yaml} template file: {e}")
        return
    
    # Create YAML file for each SMILES
    success_count = 0
    for index, row in df.iterrows():
        try:
            mol_id = row['ID']
            smiles = row['SMILES']
            
            # Copy template data
            yaml_data = template_data.copy()
            
            # Update ligand section with SMILES
            if 'sequences' in yaml_data and len(yaml_data['sequences']) > 1:
                if 'ligand' in yaml_data['sequences'][1]:
                    yaml_data['sequences'][1]['ligand']['smiles'] = smiles
            
            # Generate filename
            filename = f"hsp_{mol_id}.yaml"
            filepath = output_dir / filename
            
            # Write YAML file
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            success_count += 1
            print(f"Successfully created: {filename}")
            
        except Exception as e:
            print(f"Error processing ID {mol_id}: {e}")
    
    print(f"\nTask completed! Successfully created {success_count} YAML files")
    print(f"Files saved in: {output_dir.absolute()}")

if __name__ == "__main__":
    create_yaml_files()