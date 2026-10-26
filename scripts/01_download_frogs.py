import time
import warnings
import requests
import pandas as pd
from pygbif import occurrences as occ

warnings.filterwarnings("ignore", category=DeprecationWarning)

# 1. Get the taxon key for Anura
response = requests.get(
    "https://api.gbif.org/v1/species/match",
    params={"name": "Anura", "rank": "order"},
    timeout=30,
)
response.raise_for_status()
key = response.json()["usageKey"]
print("Taxon key:", key)

# 2. Download page by page
KEEP = ["gbifID", "species", "genus", "family",
        "decimalLatitude", "decimalLongitude",
        "coordinateUncertaintyInMeters", "year", "month",
        "stateProvince", "basisOfRecord", "datasetName"]

MAX_RECORDS = 20000   # safety cap
rows = []
offset = 0

while offset < MAX_RECORDS:
    res = occ.search(
        country="BD",
        taxonKey=key,
        hasCoordinate=True,
        hasGeospatialIssue=False,
        limit=300,
        offset=offset,
    )
    rows.extend(res["results"])
    print("Downloaded", len(rows), "records")
    if res["endOfRecords"]:
        break
    offset += 300
    time.sleep(0.5)

# 3. Make a table and look at it
df = pd.DataFrame(rows).reindex(columns=KEEP)

print()
print("Total records:", len(df))
print("Unique species:", df["species"].nunique())
print("Records without species name:", df["species"].isna().sum())
print()
print("Record types:")
print(df["basisOfRecord"].value_counts())
print()
print("Records per year:")
print(df["year"].value_counts().sort_index())

df.to_csv("data/raw_frogs.csv", index=False)
print()
print("Saved to data/raw_frogs.csv")
