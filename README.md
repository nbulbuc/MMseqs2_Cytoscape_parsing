# MMseqs2_Cytoscape_parsing
Repository with custom python code that allows to annotate MMseqs2 files for Cytoscape visuals 
## matcher_card.py

### Purpose

- Scans clustering membership files and extracts occurrences of a predefined set of target accession IDs.
 - Iterates over multiple all_vs_all_100-{t}clust_membership.txt files across a defined threshold range.
 - Searches every column of each line for accession IDs listed in targets.
 - Records every match with: Line number, Column number, Matched accession, Full original line
 - Writes results to per-threshold TSV files (matches_{t}.tsv).
### Output
One TSV file per threshold in OUTPUT_DIR.
Each file contains all detected target accessions and their positions in the original file.
