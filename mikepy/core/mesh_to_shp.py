from mikeio import Mesh
import pandas as pd
import geopandas as gpd

filename = "xxx.dfsu"
item = 'Current speed'
step = -1


df = Dfsu(filename)
data = dfsu.read()
