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
    def __init__(self, data_pairs_path):
        self.data_pairs_df = pd.read_csv(data_pairs_path)

    def __len__(self):
        return len(self.data_pairs_df)

    def __getitem__(self, idx):
        x = self.data_pairs_df.iloc[idx]['np_file_path']
        y = self.data_pairs_df.iloc[idx]['label']

        return x, y
        

if __name__ == "__main__":
    data_pairs_path = Path('../../data/processed/meta/data_pairs.csv')
    patient_dataset = PatientDataset(data_pairs_path)
    print(patient_dataset[0])

