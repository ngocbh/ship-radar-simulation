import pickle
import pandas as pd
import numpy as np
import time
import datetime

encoders_path = './data/encoders.pickle'
model_path = './data/risk_assessment_model.pickle'
data_path = './data/clean_pirate_attacks_dataset.csv'

encoders = pickle.load(open(encoders_path, 'rb'))
model = pickle.load(open(model_path, 'rb'))
df = pd.read_csv(data_path)
vessel = df.iloc[-20].to_dict()
vessel['velocity'] = 20
print(vessel)

def get_timestamp(x):
    element = datetime.datetime.strptime(x,"%Y-%m-%d %H:%M")
    a = time.mktime(element.timetuple())
    element = datetime.datetime.strptime("1990-01-01","%Y-%m-%d") 
    b = time.mktime(element.timetuple())
    return (a - b)/ 1e9

def extract_sample_features(encoders, sample):
    sample['Timestamp'] = get_timestamp(sample['Date'] + ' ' + sample['Time'])
    df = pd.DataFrame([sample])
    df['ShortTime'] = df['Time'].apply(lambda x: int(x.split(':')[0])//2)
    cat_cols = ['Flag', 'Type of ship', 'Area', 'Place', 'ShortTime']
    Xs = []
    X = encoders.transform(df[cat_cols]).toarray()
    Xs.append(X)

    X_gross = sample['Gross tonnage'] / 10000
    X_gross = np.array(X_gross).reshape(1, 1)
    Xs.append(X_gross)

    Xs.append(df['Timestamp'].to_numpy().reshape(df['Timestamp'].shape[0], 1))

    return np.hstack(Xs)

def assess_risk(sample):
    pp = model.predict_proba(extract_sample_features(encoders, sample))
    return pp[0][1]

if __name__ == '__main__':
    print(assess_risk(vessel))
