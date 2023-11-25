import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import sys
import pickle
import numpy as np
sys.path.append('../utils/')
from ecg_processing import ECGXMLReader

class PatientDataset(Dataset):
    def __init__(self, meta_path):
        self.data = pd.read_csv(meta_path)
        self.mapping_dict = {'outpatient': 0, 'cardiology clinic': 1, 'other': 2}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        meta = {
            'patient_ID': self.data.iloc[idx]['patient_ID'],
            'visit_ID': self.data.iloc[idx]['visit_ID'],
            'DischargeTo_Agg': self.data.iloc[idx]['DischargeTo_Agg'],
            'file': self.data.iloc[idx]['file'],
        }

        try:
            raw_data_dir = Path('../../data/raw/xml')
            xml_file_path = raw_data_dir / meta['file']
            ecg_reader = ECGXMLReader(xml_file_path)
            ecg_data = ecg_reader.getAllVoltages()
        except Exception as e:
            print(f"Error in the ECG XML Reader: {str(e)}")

        ecg_data_np = np.array(list(ecg_data.values()))
        x, y = ecg_data_np, self.mapping_dict[meta['DischargeTo_Agg']]

        return x, y

if __name__ == "__main__":
    processed_meta_path = Path('../../data/processed/meta/IKEM_processed.csv')
    patient_dataset = PatientDataset(processed_meta_path)
    # print(patient_dataset[3])

    batch_of_data = list()
    for i in range(10):
        batch_of_data.append(patient_dataset[i][0])

    # Specify the file path where you want to save the data
    batch_of_data_path = 'batch_of_data.pickle'

    # Open the file in binary write mode
    with open(batch_of_data_path, 'wb') as file:
        # Dump the data into the file using pickle
        pickle.dump(batch_of_data, file)

    print(f"Data saved to {batch_of_data_path}")
