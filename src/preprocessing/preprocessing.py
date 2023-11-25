import pandas as pd
from pathlib import Path
import sys
import numpy as np
sys.path.append('../utils/')
from ecg_processing import ECGXMLReader
from tqdm import tqdm

def process_data():
    data_dir = Path('../../data')
    raw_data_dir = data_dir / 'raw' / 'xml'
    processed_meta_dir = data_dir / 'processed' / 'meta'
    processed_data_dir = data_dir / 'processed' / 'npy'

    processed_meta_df = pd.read_csv(processed_meta_dir / 'IKEM_processed.csv')

    mapping_dict = {'outpatient': 0, 'cardiology clinic': 1, 'other': 2}
    np_file_paths, labels = list(), list()

    for idx in tqdm(range(len(processed_meta_df))):
        xml_file_path = raw_data_dir / processed_meta_df.iloc[idx]['file']
        np_file_path = processed_data_dir / (xml_file_path.stem + '.npy')
        
        try:
            ecg_reader = ECGXMLReader(xml_file_path)
            ecg_data = ecg_reader.getAllVoltages()
        except Exception as e:
            print(f"Error in the ECG XML Reader: {str(e)}")

        x = np.array(list(ecg_data.values()))
        y = mapping_dict[processed_meta_df.iloc[idx]['DischargeTo_Agg']]
        
        assert x.shape == (8, 5000), f"Expected shape (8, 5000), but got {x.shape} in {xml_file_path}"
        np.save(np_file_path, x)

        # Remove the leading '../../' in the saved paths
        np_file_paths.append(Path(*np_file_path.parts[2:]))
        labels.append(y)

    assert len(np_file_paths) == len(labels)
    data_pairs = pd.DataFrame({'np_file_path': np_file_paths, 'label': labels})

    # Save the DataFrame as a CSV file
    data_pairs.to_csv(processed_meta_dir / 'data_pairs.csv', index=False)

if __name__ == "__main__":
    process_data()
