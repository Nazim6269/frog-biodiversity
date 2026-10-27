import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import zipfile
import geopandas as gpd
import requests 

CELL = 0.5

df = pd.read_csv('data/clean_frogs.csv')

#--- Get Banglades Border
URL = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip"
SHP = "data/ne_countries/ne_10m_admin_0_countries.shp"

try:
    world = gpd.read_file(SHP)
except Exception:
    print("Downloading country borders...")
    r = requests.get(URL,timeout=120)
    r.raise_for_status()
    zipfile.ZipFile(io.BytesIO(r.content)).extractall("data/ne_countries")
    world=gpd.read_file(SHP)

name_col="NAME" if "NAME" in world.columns else "name"
bd=world[world[name_col] == "Bangladesh"]


#---- Put each record into grid cell
df["cell_x"]=np.floor(df['decimalLongitude'] /CELL) * CELL
df["cell_y"]= np.floor(df['decimalLatitude']/ CELL) * CELL

grid =df.groupby(["cell_x","cell_y"]).agg(records=("gbifID","count"),richness=("species","nunique")).reset_index()

grid['cx']=grid['cell_x'] + CELL /2
grid['cy']=grid['cell_y'] + CELL /2

print("Cells with Data", len(grid))
print("cells with fewer than 5 records:", (grid['records'] < 5).sum())
print()

print("Top 5 cells with records: ")
print(grid.sort_values("records",ascending=False).head(5)["cell_x","cell_y","records","richness"])
print()
print("Top 5 cells by observed richness")
print(grid.sort_values('richness',ascending=False).head(5)["cell_x","cell_y","records","richness"])

grid.to_csv("data/grid_frogs.csv",index=False)

#----- Two Maps side by side
fig,axes= plt.subplots(1,2,figsize=(13,7))
panels=[
   (axes[0],"records","Number of Records (sampling effor)", "YlOrRd"),
    (axes[1],"richness","observed species richness","viridis")
]
for ax,col,title,cmap  in panels:
    bd.boundary.plot(ax=ax,color="black",linewidth=0.8)
    sc=ax.scatter(
        grid['cx'],grid['cy'],c=grid['col'],cmap=cmap,s=300,marker="s",alpha=0.9
    )
    plt.colorbar(sc,ax=ax,shrink=0.7)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

plt.tight_layout()
plt.savefig("figure/frogs_richness_map.png",dpi=150)
plt.close()
print()
print("Saved figures/frogs_richness_map.png")
