import pgeocode as pg
import pandas as pd

# nomination of India to query
nomi = pg.Nominatim('in')
# sample zip codes
zip_data = nomi.query_postal_code(['632515', '600017'])

df = pd.read_csv('C:\\Users\\sivkumar\\Documents\\Study Materials\\GeoSpatial\\placenamelatlon.csv', header="infer", sep=',')
# to print the data for all the pincodes
# print(nomi.query_postal_code(str(df.loc[idx,'pincode'])))

pin_code = []
for idx, row in df.iterrows():
    pin_code.append(str(df.loc[idx,'pincode']))
data = nomi.query_postal_code(pin_code)

combi_data = pd.concat([df,data], axis=1, join="inner", sort=False, ignore_index=False)

combi_data.to_csv('C:\\Users\\sivkumar\\Documents\\Study Materials\\GeoSpatial\\zip_with_data.csv', sep=',' ,header=True, index=True, index_label='id')