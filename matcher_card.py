from pathlib import Path

# ------------ EDIT THESE 2 SETTINGS ------------
INPUT_DIR = Path("/Users/nichitabulbuc/Desktop/Info_Cytoscape/files")
OUTPUT_DIR = Path("/Users/nichitabulbuc/Desktop/Info_Cytoscape/files/matcher_output")
FILE_TEMPLATE = "all_vs_all_100-{t}clust_membership.txt"
# ----------------------------------------------

targets = {
    "AAG11411.2","EPF73263.1","ENV34035.1","AAX38178.1","AAK63040.1","AAB49832.1",
    "AAC14693.1","AGV10818.1","AAW34150.1","WCI13726.1","BAA34540.1","BAA12910.1",
    "BAA03776.1","CAJ98570.1","EEL41021.1","ACU86041.1","AHE40505.1","ATL63232.1",
    "AJE92936.1","WP_050815728.1","BAL43359.1","ABI20451.1","AMR06225.1","AAS13767.1",
    "APB03226.1","BAA32494.1","BAA32493.1","CAA68516.1","CAA29136.1","CAA25854.1",
    "AAC23556.1","CAA27276.1","CAA24743.1","CAA52372.1"
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def scan_file(in_path: Path, out_path: Path):
    with in_path.open("r", encoding="utf-8", errors="replace") as infile, \
         out_path.open("w", encoding="utf-8") as outfile:

        outfile.write("line\tcolumn\taccession\tfull_line\n")

        for line_number, line in enumerate(infile, start=1):
            cols = line.rstrip("\n").split()
            for col_index, value in enumerate(cols, start=1):
                if value in targets:
                    outfile.write(
                        f"{line_number}\t{col_index}\t{value}\t{line.rstrip()}\n"
                    )

def main():
    missing = []

    for t in range(150, 351, 10):  # ← THIS IS THE KEY CHANGE
        in_file = INPUT_DIR / FILE_TEMPLATE.format(t=t)
        out_file = OUTPUT_DIR / f"matches_{t}.tsv"

        if not in_file.exists():
            missing.append(str(in_file))
            continue

        scan_file(in_file, out_file)

    print("Done.")
    if missing:
        print("Missing files:")
        for m in missing:
            print("  -", m)

if __name__ == "__main__":
    main()
