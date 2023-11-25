import pandas as pd


def reorganize_data():
    csv_path = '../../data/raw/meta/Emergency IKEM 2017-2023.csv'
    df = pd.read_csv(csv_path, delimiter=';')

    # Combine EntryDate and EntryTime to one datetime column
    df['entry_datetime'] = pd.to_datetime(df['EntryDate'] + ' ' + df['EntryTime'], format='%d.%m.%Y %H:%M:%S')
    end_datetime = pd.to_datetime(df['EndDate'] + ' ' + df['EndTime'], format='%d.%m.%Y %H:%M:%S')
    df['time_spent'] = (end_datetime - df['entry_datetime']).dt.total_seconds() / (24.0 * 60 * 60)

    # Drop the original date and time columns
    df = df.drop(['EntryDate', 'EntryTime', 'EndDate', 'EndTime'], axis=1)

    # Drop columns with majority of na values. 15928 and 16537 respectively
    df = df.drop(['AdmissionRZP', 'DischargeTo_unit_agg'], axis=1)

    # Drop rows where DgCode is na (11 entries)
    df['DgCode'] = df['DgCode'].fillna('unknown')

    # Specify the order of columns for sorting
    sort_order = ['patient_ID', 'visit_ID', 'entry_datetime']

    # Sort the DataFrame based on the specified columns
    df = df.sort_values(by=sort_order)

    # Ignore repeated measurements taken during the same visit
    df = df.drop_duplicates(subset=['patient_ID', 'visit_ID'], keep='first')

    # Filter patients who passed away
    df = df[df['DischargeTo_Agg'] != 'exitus']

    df.to_csv('../../data/processed/meta/IKEM_processed.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    reorganize_data()
    print("CSV cleaned and moved to '../data/processed/meta/IKEM_processed.csv'")
    