import warnings
import requests
from pygbif import occurrences as occ

warnings.filterwarnings("ignore", category=DeprecationWarning)

# 1. Ask GBIF for the key of the frog and toad order (Anura)
response = requests.get(
    "https://api.gbif.org/v1/species/match",
    params={"name": "Anura", "rank": "order"},
    timeout=30,
)
response.raise_for_status()
match = response.json()

print("GBIF match for Anura:")
print(match)
print()

key = match["usageKey"]
print("Using taxon key:", key)
print()

# 2. Total frog records for Bangladesh
total = occ.search(country="BD", taxonKey=key, limit=0)["count"]
print("Total frog records for Bangladesh:", total)

with_coords = occ.search(country="BD", taxonKey=key, hasCoordinate=True,
                         hasGeospatialIssue=False, limit=0)["count"]
print("Records with usable coordinates:", with_coords)
print()

# 3. Records per year
print("Records per year (with coordinates):")
for year in range(2010, 2026):
    n = occ.search(country="BD", taxonKey=key, year=year, hasCoordinate=True,
                   hasGeospatialIssue=False, limit=0)["count"]
    print(year, n)
