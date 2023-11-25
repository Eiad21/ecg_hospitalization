from fhir.resources.patient import Patient
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.bundle import Bundle
from fhirclient import client

import pandas as pd

def convert_csv_to_patients(csv_file):
    processed_meta_path = '../../data/processed/meta/IKEM_processed.csv'

    df = pd.read_csv(processed_meta_path, delimiter=';')
    # Read CSV and convert to FHIR Patient resources
    patients = []
    # Your CSV reading and conversion logic here...
    for row in df:
        patient = Patient()
        patient.identifier = [Identifier(value=row['patient_ID'])]
        patient.birthDate = row['age']
        # Map other columns to corresponding fields in Patient resource
        patients.append(patient)
    return patients