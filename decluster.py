from pathlib import Path

cluster_file = "combined_uni_ncbi_100_60.txt.clstr"
seeds_file   = "selected_members_APH2_3a.txt"
out_file     = "APH_APH2_3a_id_decluster.txt"


def parse_cdhit_id(line: str):
    """
    Extract comparable ID from a CD-HIT .clstr line.

    """
    if ">" not in line or line.startswith(">"):
        return None

    core = line.split(">", 1)[1].split("...", 1)[0].strip()

    if "|" in core:
        parts = core.split("|")
        if len(parts) >= 2 and parts[1]:
            return parts[1].strip()

    return core


# read seed IDs
seed_ids = {l.strip().lstrip(">") for l in open(seeds_file) if l.strip()}
expanded = set(seed_ids)

cur_members = []
cur_hit = False


def flush():
    global cur_members, cur_hit, expanded
    if cur_hit:
        expanded.update(cur_members)
    cur_members = []
    cur_hit = False


# parse CD-HIT clusters
with open(cluster_file, "r", errors="ignore") as f:
    for line in f:
        if line.startswith(">"): 
            flush()
            continue

        cid = parse_cdhit_id(line)
        if not cid:
            continue

        cur_members.append(cid)
        if cid in seed_ids:
            cur_hit = True

flush()


# output 
Path(out_file).parent.mkdir(parents=True, exist_ok=True)
with open(out_file, "w") as w:
    for x in sorted(expanded):
        w.write(x + "\n")

print("Seeds:", len(seed_ids))
print("Expanded:", len(expanded))
print("Added:", len(expanded) - len(seed_ids))
