import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

class PatientDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = {
            'patient_ID': self.data.iloc[idx]['patient_ID'],
            'visit_ID': self.data.iloc[idx]['visit_ID'],
            'EntryDate': self.data.iloc[idx]['EntryDate'],
            'age': self.data.iloc[idx]['age'],
            'discharge_reason': self.data.iloc[idx]['discharge_reason'],
            'file': self.data.iloc[idx]['file'],
        }

        # You can add more processing or transformations here if needed

        return sample