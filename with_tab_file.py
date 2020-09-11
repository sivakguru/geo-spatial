import os
import pandas as pd
import geopandas as gpd
import shapely as shp
%matplotlib inline

path = 'C:/Users/sivkumar/Documents/Project Refference/VNPT/Data/network data/Polygon district/Polygon District/Cty 9/Ca Mau'

files = []
for path, dirname, file in os.walk(path):
    for i in range(len(file)):
        if file[i].rsplit('.',1)[1] == 'TAB':
            file_name = os.path.join(path,file[i])
            files.append(file_name.replace("\\","/"))

tab_files = []
for i in range(len(files)):
    t = gpd.read_file(filename=files[i])
    tab_files.append(t)

rims_district = pd.concat(tab_files, axis=0,ignore_index=True )

#avoid this line to make the file work with tableau
rims_district.crs = {'init' : 'epsg:4326'}

district_ax = rims_district.plot(figsize=(20,20))
district_ax.axis('off')

save_path = 'C:/Users/sivkumar/Documents/Study Materials/GeoSpatial/workshop'
rims_district.to_file('C:/Users/sivkumar/Documents/Project Refference/VNPT/Data/network data/Polygon district/Polygon District/district.geojson', driver='GeoJSON', encoding='utf-8')

rims_district.to_file('C:/Users/sivkumar/Documents/Project Refference/VNPT/Data/network data/Polygon district/Polygon District/consolidated_district_shape/vn_district.shp')

district_ax = rims_district.plot(figsize=(20,20), markersize = 0.5, edgecolor = 'white')
district_ax.axis('off')


file_path = "C:\\Users\\sivkumar\\Documents\\Project Refference\\VNPT\\Data\\Population Density Data\\population_vnm_2018-10-01.csv"

vn_csv = pd.read_csv(file_path, header=0)

vn_csv['geometry'] = vn_csv.apply(lambda row: shp.geometry.Point(row.longitude, row.latitude), axis=1)

vn_geopandas = gpd.GeoDataFrame(vn_csv)

#vn_geopandas.crs = {'init' : 'epsg:4326'}

vn_geopandas['s_no'] =  vn_geopandas.index

vn_geopandas[['s_no', 'geometry']].plot(figsize=(30,30), marker='*',markersize=vn_geopandas['population_2020'], color='black').axis('off')

# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# vietnam = world[world['name']=='Vietnam']
# vietnam.crs = {'init' : 'epsg:4326'}


fig , ax = plt.subplots(figsize=(30,30))

vn_axis = vn_geopandas.geometry.total_bounds
rims_axis = rims_district.geometry.total_bounds

xlim = ([vn_axis[0], vn_axis[2]])
ylim = ([vn_axis[1], vn_axis[3]])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

rims_district.plot(ax=ax, color='blue', edgecolor='black')
vn_geopandas.plot(ax=ax, marker='*', color='red', markersize=0.1)
ax.set_axis_off()
plt.axis('equal')
ax.set_aspect('equal')
plt.show()

base = rims_district.plot(color='white', edgecolor='black', figsize=(30,30))
vn_geopandas.plot(ax=base, marker='*', color='red', markersize=0.1)

rims_district.plot(figsize=(30,30), color='white', edgecolor='black').axis('off')

base = rims_district.plot(color='lightgrey', linewidth=0.5, edgecolor='white', figsize=(15,5))
vn_geopandas.plot(markersize=1, color='black', alpha=0.5, ax=base)

over_lap = gpd.sjoin(vn_geopandas, rims_district, how='inner', op='contains')

over_lap = gpd.sjoin(rims_district, vn_geopandas, how='inner', op='within')



###################################


file_path = "C:\\Users\\sivkumar\\Documents\\Project Refference\\VNPT\\Data\\Population Density Data\\population_vnm_2018-10-01.csv"

vn_csv = pd.read_csv(file_path, header=0)

vn_geo = gpd.GeoDataFrame(vn_csv, geometry=gpd.points_from_xy(vn_csv.longitude, vn_csv.latitude), crs={'init' : 'epsg:4326'})

#most important step in matching the CRS for matching the axis
rims_dist = rims_dist.to_crs(epsg=4326)
rims_dist.to_crs(epsg=4326).plot()

vn_geo = vn_geo.to_crs(epsg=4326)

base = rims_dist.plot(color='white', edgecolor='black', figsize=(30,30))
vn_geo.plot(ax=base, marker='*', color='red', markersize=vn_geo['population_2020'])

over_lap = gpd.sjoin(vn_geo, rims_dist, how='inner', op='within')

##########################
#explode to make the multipolygon to polygon
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

def explode(indata):
    count_mp = 0
    indf = indata
    outdf = gpd.GeoDataFrame(columns=indf.columns)
    for idx, row in indf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row,ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            count_mp = count_mp + 1
            multdf = gpd.GeoDataFrame(columns=indf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs,ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom,'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf,ignore_index=True)
    print("There were ", count_mp, "Multipolygons found and exploded")
    return outdf

####################################
#loading the Tamil nadu admin level data
file_path = 'C:/Users/sivkumar/Documents/Study Materials/GeoSpatial/gadm36_IND_shp/gadm36_IND_3.shp'

save_path = 'C:/Users/sivkumar/Documents/Study Materials/GeoSpatial/workshop'

india_3 = gpd.read_file(file_path)

tamil_nadu = india_3[india_3['NAME_1']=='Tamil Nadu']

# Making the Multipolygon to Polygon (Taking the first polygon and assign to Geometry)
# tamil_nadu.loc[1827,'geometry'] = multi_one[multi_one.index == 1827].iloc[0]['geometry'][0]

for idx, row in tamil_nadu[tamil_nadu.geom_type == 'MultiPolygon'].iterrows():
    tamil_nadu.loc[idx,'geometry'] = tamil_nadu[tamil_nadu.index == idx].iloc[0]['geometry'][0]

# to load the data in to postgreSQL data base 
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

from geoalchemy2 import Geometry, WKTElement
#convert the geometry column dtype from object to Geometry
tamil_nadu['geom'] = tamil_nadu['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
#remove the duplicate data column
tamil_nadu.drop('geometry', 1, inplace=True)

tamil_nadu.to_sql(name='tamil_nadu', con=engine, schema='prestage', if_exists='replace', index=False, dtype={'geom': Geometry('POLYGON', srid=4326)})