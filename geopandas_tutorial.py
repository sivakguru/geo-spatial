import geopandas as gpd
import sqlalchemy as db
import matplotlib.pyplot as plt
import pandas as pd

import contextily as ctx

#load all the shape files and CSV files
india = gpd.read_file(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\ind_basemaps\india_admin_layers\gadm36_IND_0.shp')

india_one = gpd.read_file(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\ind_basemaps\india_admin_layers\gadm36_IND_1.shp')

india_district = gpd.read_file(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\ind_basemaps\india_admin_layers\gadm36_IND_2.shp')

tn_nh = gpd.read_file(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\ind_basemaps\tamil_nadu_highway\tamil_nadu_highway.shp')

#load csv file with lat long data
india_city = pd.read_csv(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\in.csv', header='infer', sep=',')

#teesting with Geojson.io
tamilnadu_bomb = gpd.read_file(r'C:\Users\sivkumar\Documents\Github Repositories\Sample Data\ind_basemaps\layers\POLYGON.shp')

#convert latlong in to geometry data
india_city_geo = gpd.GeoDataFrame(india_city, geometry=gpd.points_from_xy(india_city.lng, india_city.lat), crs={'init' : 'epsg:4326'})

#filter geo dataframe
tamilnadu_city = india_city_geo[india_city_geo['admin_name']=='Tamil Nādu']

tamilnadu = india_one[india_one['NAME_1']=='Tamil Nadu']

tamilnadu_district = india_district[india_district['NAME_1']=='Tamil Nadu']

#CRS system
tamilnadu.to_crs(crs=3857, inplace=True)
tamilnadu_city.to_crs(crs=3857, inplace=True)

#equal area projections
tamilnadu.to_crs(crs=6933, inplace=True)


#draw buffer for all the points
tamilnadu_city['geometry'] = tamilnadu_city.buffer(distance=50000, resolution=20)

tamilnadu_chennai = tamilnadu_district[tamilnadu_district['NAME_2']=='Chennai']

#boundary
tamilnadu.boundary.plot(figsize=(10,10))
india_one.boundary.plot(figsize=(10,10))

#centroid
india_one.centroid.plot(figsize=(10,10))

#convex_hull
fig, ax = plt.subplots(figsize=(10,10))
india_one.convex_hull.plot(ax=ax)


#plotting
india_one.plot(ax=ax, column='NAME_1', cmap='jet', edgecolor='grey')

fig, ax = plt.subplots(figsize=(10,10))
india.plot(ax=ax,edgecolor='black')
tamilnadu.plot(ax=ax,color='none',edgecolor='black')

fig, ax = plt.subplots(figsize=(10,10))
tamilnadu.plot(ax=ax,color='blue',edgecolor='black')
tamilnadu_city.plot(ax=ax, color='orange', edgecolor='black')

fig, ax = plt.subplots(figsize=(10,10))
tamilnadu.plot(ax=ax,color='blue',edgecolor='black')
tamilnadu_city.plot(ax=ax,marker='*', markersize=5, color='red')

fig, ax = plt.subplots(figsize=(10,10))
india_one.plot(ax=ax, color='grey', edgecolor='black')
india_one.centroid.plot(ax=ax, marker='*', color='red')



#ovelay
tn_city_buffer = gpd.overlay(tamilnadu, tamilnadu_city, how='intersection')

tn_district_buffer = gpd.overlay(tamilnadu, tamilnadu_city, how='intersection')

#Load data in to Postgis using SQL Alchemy
info = {
    "host" : "localhost",
    "db_port" : "5432",
    "db_user" : "postgres",
    "db_password" : "postgres",
    "database" : "postgres",
    "db_schema" : "public"
}

db_conn = "postgres://{0}:{1}@{2}:{3}/{4}".format(
    info['db_user'],
    info['db_password'],
    info['host'],
    info['db_port'],
    info['database'])

sql_engine = db.create_engine(db_conn)

india_one.to_postgis(name='india_one', schema='public', con=sql_engine, index=False, if_exists='replace')