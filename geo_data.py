import geopandas
import pandas as pd
import shapefile as shp
path_to_data = 'subsections\C2021_SECCOES_1304.gpkg'
gdf = geopandas.read_file(path_to_data)


pd.set_option('display.max_columns', 20)
sf = shp.Reader("UNIR\linhas_unir.dbf")

print(sf.fields)
print(sf.records()[1])
print(sf.records()[4])
