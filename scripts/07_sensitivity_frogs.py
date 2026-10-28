import pandas as pd
import math
import numpy as np
from pandas.core.algorithms import rank

df = pd.read_csv('data/clean_frogs.csv')

def rarefy(counts,n):
    total = sum(counts)
    denom = math.comb(total,n)

    expected_species = 0;
    for c in counts:
        probabilty = 1 - math.comb(total-c, n)/denom
        expected_species +=probabilty

    return expected_species

for cell in [0.25,0.5,1.0]:
    gx = np.floor(df['decimalLongitude']/ cell) * cell
    gy = np.floor(df['decimalLatitude']/ cell) * cell

    for n in [5,10,15]:
        rows = []
        for (x,y), g in df.groupby([gx,gy]):
            if len(g) > n:
                counts = g['species'].value_counts().tolist()
                rows.append(
                    {
                        'x':x,
                        'y':y,
                        'records': len(g),
                        'observed':len(counts),
                        'rarefied': rarefy(counts,n)
                    }
                )
        print("cell", cell, "| sample size",n," |usable cells: " ,len(rows) ) 
        if len(rows) < 5:
            print("Too few cells, skipped")
            print()
            continue
        res = pd.DataFrame(rows)
        ranks = res[['records','observed','rarefied']].rank()
        
        print("Corrlation Obsrved: " ,round(ranks['records'].corr(ranks['observed']),2))
        print("Corrlation Rarefied: ",round(ranks['records'].corr(ranks['rarefied']),2))
        top = res.sort_values('rarefied',ascending=False).iloc[0] 
        print("  Top cell:", top["x"], top["y"], "rarefied =", round(top["rarefied"], 1))
        print()
