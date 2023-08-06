from sklearn.model_selection import train_test_split


def split_patients(df):
    patient_ids = df['PatientID'].unique()
    train_ids, test_ids = train_test_split(patient_ids, test_size=0.2, random_state=3)
    train_ids, val_ids = train_test_split(train_ids, test_size=0.2, random_state=3)

    return df[df['PatientID'].isin(train_ids)], df[df['PatientID'].isin(val_ids)], df[
        df['PatientID'].isin(test_ids)]
