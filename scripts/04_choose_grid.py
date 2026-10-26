import numpy as np
import pandas as pd

df = pd.read_csv("data/clean_frogs.csv")
print("Records:", len(df))
print()

for cell in [0.25, 0.5, 1.0]:
    # Which cell does each record fall into?
    x = np.floor(df["decimalLongitude"] / cell) * cell
    y = np.floor(df["decimalLatitude"] / cell) * cell

    # Number of records in each cell
    counts = df.groupby([x, y]).size()

    print("Cell size:", cell, "degrees")
    print("  Cells with data:", len(counts))
    print("  Cells with >= 10 records:", (counts >= 10).sum())
    print("  Cells with >= 20 records:", (counts >= 20).sum())
    print("  Most records in one cell:", counts.max())
    print("  Share of records in the top 3 cells:",
          round(counts.sort_values(ascending=False).head(3).sum() / len(df), 2))
    print()

print("Records per year:")
print(df["year"].value_counts().sort_index())
