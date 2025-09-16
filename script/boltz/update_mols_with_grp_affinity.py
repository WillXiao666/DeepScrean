import pandas as pd
import json
import os

def update_mols_with_affinity():
    """
    Read affinity_grp file for each molecule, get affinity_pred_value,
    then add new column affinity_with_grp(boltz) to mols.csv
    """
    
    # TODO: Replace with actual input CSV file path
    csv_path = 'PLACEHOLDER_INPUT_CSV_PATH'  # Default: 'mols.csv'
    
    # TODO: Replace with actual predictions directory path
    predictions_dir = 'PLACEHOLDER_PREDICTIONS_DIR_PATH'  # Default: 'grp_predictions'
    
    # Read mols.csv file
    df = pd.read_csv(csv_path)
    
    print(f"Read {len(df)} molecule data")
    
    # Create new column to store affinity values
    affinity_values = []
    
    # Iterate through each ID, read corresponding affinity file
    for mol_id in df['ID']:
        affinity_file_path = f'{predictions_dir}/grp_{mol_id}/affinity_grp_{mol_id}.json'
        
        try:
            # Check if file exists
            if os.path.exists(affinity_file_path):
                with open(affinity_file_path, 'r') as f:
                    affinity_data = json.load(f)
                    affinity_pred_value = affinity_data['affinity_pred_value']
                    affinity_values.append(affinity_pred_value)
                    print(f"ID {mol_id}: affinity_pred_value = {affinity_pred_value}")
            else:
                print(f"Warning: File {affinity_file_path} does not exist")
                affinity_values.append(None)  # Add None if file doesn't exist
                
        except Exception as e:
            print(f"Error reading affinity file for ID {mol_id}: {e}")
            affinity_values.append(None)
    
    # Add new column to DataFrame
    df['affinity_with_grp(boltz)'] = affinity_values
    
    # Save updated CSV file (overwrite original file)
    df.to_csv(csv_path, index=False)
    
    print(f"\nSuccessfully updated {csv_path} file")
    print(f"Added new column 'affinity_with_grp(boltz)'")
    print(f"Processed {len([v for v in affinity_values if v is not None])} valid affinity values")
    
    # Display first few rows of results
    print("\nFirst 5 rows of updated data:")
    print(df.head())

if __name__ == "__main__":
    update_mols_with_affinity()