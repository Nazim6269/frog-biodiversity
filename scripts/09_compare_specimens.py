import math
import numpy as np
import pandas as pd

CELL = 0.5
N_RARE = 10


def rarefy(counts, n):
    total = sum(counts)
    denom = math.comb(total, n)
    return sum(1 - math.comb(total - c, n) / denom for c in counts)


def analyse(df, label):
    gx = np.floor(df["decimalLongitude"] / CELL) * CELL
    gy = np.floor(df["decimalLatitude"] / CELL) * CELL
    rows = []
    for (x, y), g in df.groupby([gx, gy]):
        if len(g) >= N_RARE:
            counts = g["species"].value_counts().tolist()
            rows.append({"x": x, "y": y, "records": len(g),
                         "observed": len(counts),
                         "rarefied": rarefy(counts, N_RARE)})
    res = pd.DataFrame(rows)
    ranks = res[["records", "observed", "rarefied"]].rank()
    print(label)
    print("  Usable cells:", len(res))
    print("  Correlation, observed:", round(ranks["records"].corr(ranks["observed"]), 2))
    print("  Correlation, rarefied:", round(ranks["records"].corr(ranks["rarefied"]), 2))
    print("  Top 3 cells by rarefied richness:")
    print(res.sort_values("rarefied", ascending=False).head(3).round(1))
    print()


# Sightings only (the cleaned data we already have)
sightings = pd.read_csv("data/clean_frogs.csv")

# All record types, with the same cleaning except the sightings filter
everything = pd.read_csv("data/raw_frogs.csv")
everything = everything.dropna(subset=["species"])
everything = everything[
    everything["decimalLatitude"].between(20.5, 26.7)
    & everything["decimalLongitude"].between(88.0, 92.8)
]
everything = everything[
    everything["coordinateUncertaintyInMeters"].isna()
    | (everything["coordinateUncertaintyInMeters"] <= 10000)
]

analyse(sightings, "Sightings only")
analyse(everything, "All record types")
