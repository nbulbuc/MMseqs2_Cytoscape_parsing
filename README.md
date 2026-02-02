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

## matcher_names.py

### Purpose

- Adds human-readable names to match files based on a reference mapping.
- Uses matches_150.tsv as a reference to build a mapping:
- Accession ID → name (last non-empty column).
- Iterates over other matches_{t}.tsv files.
- Appends a name column to each file using the reference mapping.
### Output
Named TSV files (matches_{t}_named.tsv) written to fixed_names/.

## aminoglyc_table.py
### Purpose
- Summarizes how many annotated sequences fall into each cluster node at different clustering thresholds.
- Reads annotation IDs from .txt filenames in a specified directory.
- Parses clustering membership files mapping sequence IDs to node IDs.
- Counts how many annotated sequences fall into each cluster node.
- Produces a node-by-node summary table for each threshold.
### Output
One summary file per threshold ({t}summary.txt).

## decluster.py (edited custom code from Tokuriki Lab)
### Purpose 
- Expands a list of seed protein IDs using a CD-HIT clustering file. 
- Identifies clusters that contain at least one seed ID.
- Collects all sequence IDs from those clusters.
- Outputs a de-clustered list of unique protein IDs.
### Output 
Text file containing all seed IDs and all cluster members associated with them.
