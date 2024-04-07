

import pandas as pd


def load_metadata(identifiers_path: str, patients_path: str) -> dict[str, dict]:
    # metadata about identifiers and patients
    identifiers_df = pd.read_csv(identifiers_path, sep="\t", header=0, dtype=str)
    patients_df = pd.read_csv(patients_path, sep="\t", header=0)
    patients_df = patients_df[patients_df['DONOR_ID'].notna()]

    # some maps to help 
    COMMON_PRIMARIES = ['renal', 'melanoma', 'breast', 'lung', 'colorectal']
    meta = {
        'primary': {},
        'common': {},
        'gender': {},
        'batch': {},
    }

    for index, row in patients_df.iterrows():
        meta['primary'][row['DONOR_ID']] = row['Primary Tumour']
        meta['common'][row['DONOR_ID']] = row['Primary Tumour'] in COMMON_PRIMARIES
        meta['gender'][row['DONOR_ID']] = row['Gender']
    meta['primary']['BM052'] = 'lung'

    for index, row in identifiers_df.iterrows():
        if row['DONOR_ID'] not in meta['batch']:
            meta['batch'][row['DONOR_ID']] = row['BATCH']
    
    return meta 
