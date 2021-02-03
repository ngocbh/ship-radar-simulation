import pandas as pd
from dms2dec.dms_convert import dms2dec

sea_area = {
 'Malacca Strait':{'max_lat':8.454, 'min_long':95.4423, 'min_lat':0.8573, 'max_long':103.5107}, # OK
 'West Africa':{'max_lat':6.6227, 'min_long':-7.7263, 'min_lat':-1.7296, 'max_long':10.1827}, ## Gulf of Guinea
 'South China Sea':{'max_lat':25.5673, 'min_long':102.2385, 'min_lat':-3.2287, 'max_long':122.1513}, # OK
 'South America (A)':{'max_lat':0.0751, 'min_long':-69.6008, 'min_lat':-60, 'max_long':20.0091}, # South Atlantic Ocean
 'Arabian Sea':{'max_lat':25.5974, 'min_long':51.0223, 'min_lat':-0.7034, 'max_long':74.335}, # OK
 'North Atlantic Ocean':{'max_lat':68.6387, 'min_long':-98.0539, 'min_lat':-0.936, 'max_long':12.0059}, # OK
 'Indian Ocean':{'max_lat':31.1859, 'min_long':20.0026, 'min_lat':-60, 'max_long':146.8982}, # OK
 'South America (P)':{'max_lat':3.3911, 'min_long':130.1113, 'min_lat':-60, 'max_long':-67.2667}, # South Pacific Ocean
 'East Africa':{'max_lat':-2.52, 'min_long':38.67, 'min_lat':-16.63, 'max_long':43.24}, # OK
 'North Pacific Ocean':{'max_lat':66.5629, 'min_long':117.5162, 'min_lat':0, 'max_long':-76.9854}, # OK
 'South America (C)':{'max_lat':22.7065, 'min_long':-89.4129, 'min_lat':7.7098, 'max_long':-59.4216}, # Caribbean Sea
 'Persian Gulf':{'max_lat':31.1859, 'min_long':47.7024, 'min_lat':23.959, 'max_long':57.34}, # OK
 'Mediterranean Sea':{'max_lat':45.7833, 'min_long':-6.0327, 'min_lat':30.2639, 'max_long':36.2173}, # OK
 'Yellow Sea':{'max_lat':41.1592, 'min_long':117.5162, 'min_lat':33.276, 'max_long':127.4589},
 'Far East':{'max_lat':33.372, 'min_long':118.478, 'min_lat':24.0576, 'max_long':131.1322}, # East China Sea
 'North Sea':{'max_lat':61.017, 'min_long':-4.4454, 'min_lat':50.9954, 'max_long':12.0059}, # OK
 'China Sea':{'max_lat':33.3295, 'min_long':119.0975, 'min_lat':25.3484, 'max_long':126.2457} # OK
}

def check(long, lat):
    dec_long = dms2dec(long)
    dec_lat = dms2dec(lat)

    for k, v in sea_area.items():
        if dec_long < v['max_long'] and \
            dec_long > v['min_long'] and \
            dec_lat < v['max_lat'] and \
            dec_lat > v['min_lat']:
            return k
    return None

df = pd.read_csv('neg_incidents.csv')
df['New Area'] = None
print(df.head())
# print(df.loc[0, 'Latitude'])
# print(len(df))

for i in range(len(df)):
    # print('str = ', df.loc[i, 'Longitude'])
    # print('type = ', type(df.loc[i, 'Longitude']))
    try:
        df.loc[i, 'New Area'] = check(df.loc[i, 'Longitude'], df.loc[i, 'Latitude'])
    except:
        pass
print(df.head())
df.to_csv('new_neg_incidents.csv')



