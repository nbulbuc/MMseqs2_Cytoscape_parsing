from pathlib import Path
from collections import defaultdict

# =========================
# CONFIG
# =========================

AMINO_DIR = Path(
    "/Users/nichitabulbuc/Desktop/Annotations/Serine_Threonine_Kinases/Metabolic_and_Homeostatic_Kinases/Inositol_Phosphate_Kinases/"
)

MEMBERSHIP_DIR = Path("/Users/nichitabulbuc/Desktop/Info_Cytoscape/files/")

OUT_DIR = Path(
    "/Users/nichitabulbuc/Desktop/citic/"
)

COLUMN_NAME = "Inositol_Phosphate_Kinases"

START = 320
END = 350
STEP = 10

# If your files use a different prefix/suffix, change only this:
MEMBERSHIP_PATTERN = "all_vs_all_100-{t}clust_membership.txt"
OUT_PATTERN = "Inositol_Phosphate_Kinases{t}summary.txt"


# =========================
# HELPERS
# =========================

def parse_membership_two_column(path: Path) -> dict[str, str]:
    """
    Parse membership file with header, then rows:
      node <tab/space> member
    Returns: seq_id -> node_id
    """
    seq_to_node: dict[str, str] = {}

    with path.open("r", encoding="utf-8", errors="replace") as f:
        # skip header if present
        first = next(f, "").strip()
        # If the first line is not a header (rare), try parsing it as data
        if first and not first.lower().startswith("node"):
            parts = first.split()
            if len(parts) >= 2 and parts[0].isdigit():
                seq_to_node[parts[1]] = parts[0]

        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue

            node, seq_id = parts[0], parts[1]
            if not node.isdigit():
                continue
            seq_to_node[seq_id] = node

    return seq_to_node


def get_ids_from_txt_filenames(folder: Path) -> set[str]:
    """Extract sequence IDs from *.txt filenames (stem)."""
    return {p.stem for p in folder.glob("*.txt")}


def write_summary(out_file: Path, all_nodes: list[str], counts: dict[str, int]) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as out:
        out.write(f"node\t{COLUMN_NAME}\n")
        for node in all_nodes:
            out.write(f"{node}\t{counts.get(node, 0)}\n")


# =========================
# MAIN LOOP
# =========================

def main() -> None:
    if not AMINO_DIR.exists():
        raise FileNotFoundError(f"AMINO_DIR not found: {AMINO_DIR}")
    if not MEMBERSHIP_DIR.exists():
        raise FileNotFoundError(f"MEMBERSHIP_DIR not found: {MEMBERSHIP_DIR}")

    amino_ids = get_ids_from_txt_filenames(AMINO_DIR)
    if not amino_ids:
        print(f" No .txt files found in {AMINO_DIR} (counts will all be zero).")

    print(f"Annotation IDs loaded: {len(amino_ids)} from {AMINO_DIR}")

    for t in range(START, END + 1, STEP):
        membership_file = MEMBERSHIP_DIR / MEMBERSHIP_PATTERN.format(t=t)
        if not membership_file.exists():
            print(f"⏭️  Skipping {t}: membership file not found ({membership_file.name})")
            continue

        seq_to_node = parse_membership_two_column(membership_file)
        if not seq_to_node:
            print(f"  {t}: parsed 0 mappings (check file format): {membership_file.name}")
            continue

        all_nodes = sorted(set(seq_to_node.values()), key=lambda x: int(x))

        counts = defaultdict(int)
        missing = 0

        for seq_id in amino_ids:
            node = seq_to_node.get(seq_id)
            if node is None:
                missing += 1
            else:
                counts[node] += 1

        out_file = OUT_DIR / OUT_PATTERN.format(t=t)
        write_summary(out_file, all_nodes, counts)

        print(
            f" {t}: wrote {out_file.name} | nodes={len(all_nodes)} | "
            f"matched={len(amino_ids) - missing}/{len(amino_ids)} | missing={missing}"
        )


if __name__ == "__main__":
    main()
