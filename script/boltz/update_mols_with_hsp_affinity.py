import pandas as pd
import json
import os

def update_mols_with_hsp_affinity():
    """
    Read affinity_hsp file for each molecule, get affinity_pred_value,
    then add new column affinity_with_hsp(boltz) to mols.csv
    """
    
    # TODO: Replace with actual input CSV file path
    csv_path = 'PLACEHOLDER_INPUT_CSV_PATH'  # Default: 'mols.csv'
    
    # TODO: Replace with actual predictions directory path
    predictions_dir = 'PLACEHOLDER_PREDICTIONS_DIR_PATH'  # Default: 'hsp_predictions'
    
    # Read mols.csv file
    df = pd.read_csv(csv_path)
    
    print(f"Read {len(df)} molecule data")
    print(f"Current column count: {len(df.columns)}")
    print(f"Current column names: {list(df.columns)}")
    
    # Create new column to store HSP affinity values
    hsp_affinity_values = []
    
    # Iterate through each ID, read corresponding HSP affinity file
    for mol_id in df['ID']:
        affinity_file_path = f'{predictions_dir}/hsp_{mol_id}/affinity_hsp_{mol_id}.json'
        
        try:
            # Check if file exists
            if os.path.exists(affinity_file_path):
                with open(affinity_file_path, 'r') as f:
                    affinity_data = json.load(f)
                    affinity_pred_value = affinity_data['affinity_pred_value']
                    hsp_affinity_values.append(affinity_pred_value)
                    print(f"ID {mol_id}: HSP affinity_pred_value = {affinity_pred_value}")
            else:
                print(f"Warning: File {affinity_file_path} does not exist")
                hsp_affinity_values.append(None)  # Add None if file doesn't exist
                
        except Exception as e:
            print(f"Error reading HSP affinity file for ID {mol_id}: {e}")
            hsp_affinity_values.append(None)
    
    # Add new column to DataFrame
    df['affinity_with_hsp(boltz)'] = hsp_affinity_values
    
    # Save updated CSV file (overwrite original file)
    df.to_csv(csv_path, index=False)
    
    print(f"\nSuccessfully updated {csv_path} file")
    print(f"Added new column 'affinity_with_hsp(boltz)'")
    print(f"Processed {len([v for v in hsp_affinity_values if v is not None])} valid HSP affinity values")
    print(f"Updated column count: {len(df.columns)}")
    
    # Display first few rows of results
    print("\nFirst 5 rows of updated data:")
    print(df.head())
    
    # Display column names
    print("\nAll column names:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")

if __name__ == "__main__":
    update_mols_with_hsp_affinity()