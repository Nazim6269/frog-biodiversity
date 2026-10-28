import pandas as pd

df = pd.read_csv("data/raw_frogs.csv")

# Same cleaning as before, except we keep all record types
df = df.dropna(subset=["species"])
df = df[
    df["decimalLatitude"].between(20.5, 26.7)
    & df["decimalLongitude"].between(88.0, 92.8)
]
df = df[
    df["coordinateUncertaintyInMeters"].isna()
    | (df["coordinateUncertaintyInMeters"] <= 10000)
]

sightings = df[df["basisOfRecord"] == "HUMAN_OBSERVATION"]
others = df[df["basisOfRecord"] != "HUMAN_OBSERVATION"]

print("Sightings:", len(sightings), "records,", sightings["species"].nunique(), "species")
print("Specimens and other:", len(others), "records,", others["species"].nunique(), "species")
print("All together:", len(df), "records,", df["species"].nunique(), "species")
print()
print("Species found ONLY in specimens:")
print(sorted(set(others["species"]) - set(sightings["species"])))
print()
print("Year range of specimens:", others["year"].min(), "to", others["year"].max())
