import pandas as pd
import geopandas as gpd
import shapely as shp
%matplotlib inline

rims_district = gpd.read_file('C:\\Users\\sivkumar\\Documents\\Project MOM\\VNPT\\Data\\VNPT_POI_DATA\\RIMS_District.json')

rims_district.plot()
rims_district[rims_district.TINHTP_ID == 1022]
rims_district[rims_district.TINHTP_ID == 1022].plot()
rims_district[(rims_district.TINHTP_ID == 1022) & (rims_district.QUANHUYEN_ID == 1176)].plot()
rims_district.to_crs({'proj' : 'merc'}).plot()
rims_district.crs = {'init' : 'epsg:4147'}
rims_district.crs = {'init' : 'epsg:4326'}

district_ax = rims_district.plot(figsize=(20,20))
district_ax.axis('off')


mbb_cluster = gpd.read_file('C:\\Users\\sivkumar\\Documents\\Project Refference\\VNPT\\Data\\MBB_CLUSTER\\shape_file\\MBB_CLUSTER_63.shp')
mbb_cluster.crs = {'init' : 'epsg:4326'}
mbb_cluster[mbb_cluster.province_c == 'HNI'].plot(figsize=(20,20))

mbb_cluster.set_index('cluster_na', inplace=True)

mbb_cluster['cust_count'] = cluster_with_ookla['cluster_na'].value_counts()

mbb_cluster.reset_index(inplace=True)

ookla_sample = pd.read_csv('C:\\Users\\sivkumar\\Documents\\Project MOM\\VNPT\\Data\\VNPT_POI_DATA\\OOKLA data\\android_cell_2018-10-30.csv')
ookla_sample.head()
for names in range(len(ookla_sample.columns)):
    print(names, ookla_sample.columns[names])

ookla_filter = ookla_sample.filter([ookla_sample.columns[0],
ookla_sample.columns[1],
ookla_sample.columns[15],
ookla_sample.columns[17],
ookla_sample.columns[18],
ookla_sample.columns[19],
ookla_sample.columns[20]])

ookla_filter.head()

shp.geometry.Point(ookla_filter.iloc[0]['client_latitude'], ookla_filter.iloc[0]['client_longitude'])

ookla_centroid = ookla_filter.apply(lambda row: shp.geometry.Point(row.client_longitude,row.client_latitude), axis = 1)
ookla_centroid_gdf = gpd.GeoDataFrame(ookla_filter, geometry = ookla_centroid)
ookla_centroid_gdf.crs = {'init' : 'epsg:4326'}
ookla_centroid_gdf.head()
ookla_centroid_gdf.plot()
ookla_centroid_gdf[ookla_centroid_gdf.client_city == 'Ho Chi Minh City'].plot()

ookla_ax = ookla_centroid_gdf.plot(figsize = (20,20), color = 'black', markersize = 3)
ookla_ax.axis('off')


#spatial joins of the two geo pandas data frames
cluster_with_ookla = gpd.sjoin(ookla_centroid_gdf, mbb_cluster, how='inner', op='within')
cluster_with_ookla.head()

ookla_with_cluster = gpd.sjoin(mbb_cluster, ookla_centroid_gdf, how='inner', op='contains')
ookla_with_cluster.head()

