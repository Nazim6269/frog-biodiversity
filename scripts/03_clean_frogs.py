import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw_frogs.csv")
print("Start:", len(df), "records")

# 1. Remove records without a species name
df = df.dropna(subset=["species"])
print("After removing missing species:", len(df))

# 2. Remove duplicates
df = df.drop_duplicates(subset=["gbifID"])
print("After removing duplicates:", len(df))

# 3. Keep points inside Bangladesh's rough bounding box
df = df[
    df["decimalLatitude"].between(20.5, 26.7)
    & df["decimalLongitude"].between(88.0, 92.8)
]
print("After bounding box:", len(df))

# 4. Remove imprecise locations (more than 10 km uncertainty)
print("Records with no uncertainty value:", df["coordinateUncertaintyInMeters"].isna().sum())
df = df[
    df["coordinateUncertaintyInMeters"].isna()
    | (df["coordinateUncertaintyInMeters"] <= 10000)
]
print("After removing imprecise locations:", len(df))

# 5. Keep sightings only
df = df[df["basisOfRecord"] == "HUMAN_OBSERVATION"]
print("After keeping sightings only:", len(df))

# Summary
print()
print("Final records:", len(df))
print("Final unique species:", df["species"].nunique())
print("Year range:", df["year"].min(), "to", df["year"].max())
print("Records with missing year:", df["year"].isna().sum())

df.to_csv("data/clean_frogs.csv", index=False)

# Chart: top species
top = df["species"].value_counts().head(15).sort_values()
plt.figure(figsize=(8, 6))
plt.barh(top.index, top.values, color="olivedrab")
plt.xlabel("Number of records")
plt.title("Most recorded frog species (cleaned data)")
plt.tight_layout()
plt.savefig("figures/top_frog_species.png", dpi=150)
plt.close()

print()
print("Saved data/clean_frogs.csv and figures/top_frog_species.png")
