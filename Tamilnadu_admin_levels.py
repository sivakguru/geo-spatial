import os
import pandas as pd
import geopandas as gpd
import shapely as shp
import matplotlib as mlp
#for jupyter notebook to view the maps
#%matplotlib inline
# Convert Shapely geometries to WKTElements into column 'geom' (default in PostGIS)
from geoalchemy2 import Geometry, WKTElement

import sqlalchemy as db

file_path = 'C:/Users/sivkumar/Documents/Study Materials/GeoSpatial/gadm36_IND_shp/gadm36_IND_3.shp'

save_path = 'C:/Users/sivkumar/Documents/Study Materials/GeoSpatial/workshop'

india_3 = gpd.read_file(file_path)

tamil_nadu = india_3[india_3['NAME_1']=='Tamil Nadu']

# Making the Multipolygon to Polygon (Taking the first polygon and assign to Geometry)
# tamil_nadu.loc[1827,'geometry'] = multi_one[multi_one.index == 1827].iloc[0]['geometry'][0]

for idx, row in tamil_nadu[tamil_nadu.geom_type == 'MultiPolygon'].iterrows():
    tamil_nadu.loc[idx,'geometry'] = tamil_nadu[tamil_nadu.index == idx].iloc[0]['geometry'][0]

# fig, ax = mlp.pyplot.subplots(figsize=(20,20))
# tamil_nadu.plot(column='NAME_2',
# categorical=True,
# legend=False,
# ax=ax)
# ax.axis('off')


info = {
    "host" : "localhost",
    "db_port" : "5432",
    "db_user" : "postgres",
    "db_password" : "Sivkumar_123",
    "database" : "postgres",
    "db_schema" : "prestage"
}

db_conn = "postgres://{0}:{1}@{2}:{3}/{4}".format(
    info['db_user'],
    info['db_password'],
    info['host'],
    info['db_port'],
    info['database'])

engine = db.create_engine(db_conn)

# Convert Shapely geometries to WKTElements into column 'geom' (default in PostGIS)
tamil_nadu['geom'] = tamil_nadu['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
# remove the shapely geometric column
tamil_nadu.drop('geometry', 1, inplace=True)
# Load the table to potgres data base
tamil_nadu.to_sql(name='tamil_nadu', con=engine, schema='prestage', if_exists='replace', index=False, dtype={'geom': Geometry('POLYGON', srid=4326)})

sql = 'select * from prestage.india_population_density \
where latitude > 8 and latitude < 14 and longitude > 76 and longitude < 81'

# pop_dense = pd.read_sql(sql=sql, con=engine, chunksize=1000)
# pop_dense_geo = gpd.GeoDataFrame(pop_dense, geometry=gpd.points_from_xy(pop_dense.longitude, pop_dense.latitude), crs={'init' : 'epsg:4326'})
# over_lap = gpd.sjoin(pop_dense_geo, tamil_nadu, how='inner', op='within')

final = []
for chunk in pd.read_sql(sql=sql, con=engine, chunksize=1000):
    pop_dense_geo = gpd.GeoDataFrame(chunk, geometry=gpd.points_from_xy(chunk.longitude, chunk.latitude), crs={'init' : 'epsg:4326'})
    over_lap = gpd.sjoin(pop_dense_geo, tamil_nadu, how='inner', op='within')
    final.append(over_lap)

matching = pd.concat(final, axis=0, ignore_index=True)

matching['geom'] = matching['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))

matching.drop('geometry', 1, inplace=True)

matching.to_sql(name='tamil_nadu_pop_dense', con=engine, schema='prestage', if_exists='replace', index=False, dtype={'geom': Geometry('Point', srid=4326)})

###########################################################

for chunk in pd.read_sql(sql=sql, con=engine, chunksize=10000):
    pop_dense_geo = gpd.GeoDataFrame(chunk, geometry=gpd.points_from_xy(chunk.longitude, chunk.latitude), crs={'init' : 'epsg:4326'})
    over_lap = gpd.sjoin(pop_dense_geo, tamil_nadu, how='inner', op='within')
    over_lap['geom'] = over_lap['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    over_lap.drop('geometry', 1, inplace=True)
    over_lap.to_sql(name='tamil_nadu_pop_dense', con=engine, schema='prestage',if_exists='append', index=False, dtype={'geom' : Geometry('Point', srid=4326)})