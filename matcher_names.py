from pathlib import Path

# ===== EDIT THESE PATHS =====
BASE_DIR = Path("/Users/nichitabulbuc/Desktop/Info_Cytoscape/files/matcher_output")
REF_FILE = BASE_DIR / "matches_150.tsv"
OUT_DIR = BASE_DIR / "fixed_names"
# ===========================

OUT_DIR.mkdir(parents=True, exist_ok=True)

def last_nonempty_field(fields):
    """Return the last non-empty (after strip) field, or ''."""
    for x in reversed(fields):
        x = x.strip()
        if x != "":
            return x
    return ""

def build_mapping(ref_path: Path) -> dict:
    """
    Build mapping accession -> name from matches_150.tsv.
    Accession is field #3 (index 2).
    Name is the last non-empty field in the line.
    """
    mapping = {}
    with ref_path.open("r", encoding="utf-8", errors="replace") as f:
        header = f.readline()  # skip header
        for line in f:
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 3:
                continue
            acc = fields[2].strip()
            name = last_nonempty_field(fields)
            if name == acc:
                continue
            if acc and name:
                mapping[acc] = name
    return mapping

def add_names_to_file(in_path: Path, out_path: Path, mapping: dict):
    """
    Reads a matches_XXX.tsv file and appends a name column using accession field #3.
    Preserves the entire original line (even if it contains extra tabs),
    then adds '\t<name>'.
    """
    with in_path.open("r", encoding="utf-8", errors="replace") as fin, \
         out_path.open("w", encoding="utf-8") as fout:

        header = fin.readline().rstrip("\n")
        if "name" not in header.split("\t"):
            fout.write(header + "\tname\n")
        else:
            fout.write(header + "\n")

        for line in fin:
            line_clean = line.rstrip("\n")
            fields = line_clean.split("\t")
            if len(fields) < 3:
                fout.write(line_clean + "\t\n")
                continue

            acc = fields[2].strip()
            name = mapping.get(acc, "")
            fout.write(line_clean + "\t" + name + "\n")

def main():
    if not REF_FILE.exists():
        raise FileNotFoundError(f"Reference file not found: {REF_FILE}")

    mapping = build_mapping(REF_FILE)
    print(f"Built mapping for {len(mapping)} accessions from {REF_FILE.name}")

    for t in range(160, 351, 10):
        in_file = BASE_DIR / f"matches_{t}.tsv"
        if not in_file.exists():
            print(f"Missing: {in_file.name}")
            continue

        out_file = OUT_DIR / f"matches_{t}_named.tsv"
        add_names_to_file(in_file, out_file, mapping)
        print(f"Wrote: {out_file.name}")

    print("Done.")

if __name__ == "__main__":
    main()
