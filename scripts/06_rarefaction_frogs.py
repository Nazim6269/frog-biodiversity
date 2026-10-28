import pandas as pd
import math
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

CELL=0.5
N_RARE = 10

df = pd.read_csv("data/clean_frogs.csv")
world = gpd.read_file('data/ne_countries/ne_10m_admin_0_countries.shp')
name_col = "NAME" if "NAME" in world.columns else "name"
bd = world[world[name_col] == "Bangladesh"]

df['cell_x']= np.floor(df['decimalLongitude'] / CELL) * CELL
df['cell_y']= np.floor(df['decimalLatitude'] / CELL) * CELL

def rarefy(counts, n):
    total = sum(counts)
    denom = math.comb(total, n)

    expected_species = 0

    for c in counts:
        probability = 1 - math.comb(total - c, n) / denom
        expected_species += probability

    return expected_species

#-------Rarefied richness
rows = []
for (x,y) , g in df.groupby(['cell_x', 'cell_y']):
   counts=g['species'].value_counts().tolist()
    if len(g) >= N_RARE:
        rows.append(
            {
                'cell_x':x,
                'cell_y':y,
                'cx': x +CELL /2,
                'cy': y + CELL /2,
                'records':len(g),
                'observed':len(counts),
                'rarefied': rarefy(counts,N_RARE)
            }
        )

res =pd.DataFrame(rows)
print("Cells with at least", N_RARE, "records",len(res))
print()
print(res.sort_values('rarefied',ascending=False)[['cell_x','cell_y',"records",'observed','rarefied']].round(1))

ranks = res[['records','observed','rarefied']].rank()
print()
print("Rank correlation with number of records: ")
print("  Observed richness:", round(ranks["records"].corr(ranks["observed"]), 2))
print(" Rarefied richness", round(ranks['records'].corr(ranks['rarefied']),2))

res.to_csv('data/rarefied_frogs.csv',index=False)

#----------Map
fig, ax= plt.subplots(figsize=(7,8))
bd.boundary.plot(ax=ax,color='black',linewidth=0.8)
sc=ax.scatter(
    res['cx'],
    res['cy'],
    c=res['rarefied'],
    cmap='viridis'
    s=400,
    marker='s'
)
plt.colorbar(sc,ax=ax,shrink=0.7,label="Expected species in 10 records")
ax.set_title("Rarefied frog species richness")
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.tight_layout()
plt.savefig("figures/frog_rarefied_map.png",dpi=150)
plt.close()

#------ accumulation curve
codes = pd.factorize(df['speices'])[0]
rng= np.random.default_rng(42)
plt.figure(figsize=(8,5))
for _ in range(5):
    perm = rng.permutation(codes)
    new_species = ~pd.Series(perm).duplicated().to_numpy()
    plt.plot(np.cumsum(new_species), color="olivedrab",alpha=0.6)
plt.xlabel('Number of records')    
plt.ylabel("Cumulative number of species")
plt.title('Frog species accumulation curve')
plt.tight_layout()
plt.savefig("figures/frog_accumulation_curve.png",dpi=150)
plt.close()
print()
print("Saved frog_rarefied_map.png and frog_accumulation_curve.png")
