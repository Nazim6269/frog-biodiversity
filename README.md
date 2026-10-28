# Bangladesh Frog Records: Sampling Bias in GBIF Data

## Question
Does a map of frog records in Bangladesh show where frogs live,
or where observers go?

## Data
- Frog and toad (order Anura) records for Bangladesh from GBIF
- 1079 raw records, 634 after cleaning, 38 species
- 813 of the 1079 raw records come from iNaturalist
- Country border from Natural Earth

## Methods
1. Downloaded all records with coordinates via the GBIF API
2. Cleaned: removed missing species names, imprecise locations
   (>10 km), and non-sighting records (specimens, citations)
3. Grid cells of 0.5 degrees; rarefied to 10 records per cell
   (14 cells usable)
4. Sensitivity check: cell sizes 0.25, 0.5, 1.0 degrees and
   sample sizes 5, 10, 15

## Results
- Sampling is strongly biased in time: 2026 alone has 241 of 634
  records (38%)
- Sampling is biased in space: 27 of 53 cells have fewer than
  5 records
- The cell with most records (101) has only 5 species, so more
  records did not mean more species
- Rarefaction reduced the correlation between richness and
  records from 0.36 to 0.06 (0.5 degree, n = 10). Across 9 settings
  it was lower in all, but not stable in two
- The western and northeastern cells have the highest rarefied
  richness, but we cannot rank them

## Limitations
- Only 14 usable cells, so results are descriptive, not statistical
- Sightings only: 11 species known from specimens are missing
- 240 records with no location uncertainty were kept
- Three quarters of the data come from one platform (iNaturalist)
- Top cell changes with grid size

## Reproduce
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    python scripts/01_download_frogs.py
    (then scripts 03 to 07 in order)
