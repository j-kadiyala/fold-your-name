import sys
import unicodedata
import requests

SUBS = {"B": "N", "J": "L", "O": "K", "U": "C", "X": "A", "Z": "Q"}
URL = "https://api.esmatlas.com/foldSequence/v1/pdb/"

def name_to_peptide(name, linker="EAAAKEAAAK", repeats=3):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    core = "".join(SUBS.get(c, c) for c in name.upper() if c.isalpha())
    if not core:
        raise ValueError("No usable letters in that name")
    return linker.join([core] * repeats)

def fold(seq):
    r = requests.post(URL, data=seq, timeout=120)
    r.raise_for_status()
    return r.text

def mean_confidence(pdb_text):
    vals = []
    for line in pdb_text.splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            vals.append(float(line[60:66]))
    return sum(vals) / len(vals) if vals else None

if __name__ == "__main__":
    name = " ".join(sys.argv[1:]) or input("Name: ")
    seq = name_to_peptide(name)
    print("Sequence:", seq, f"({len(seq)} residues)")
    pdb = fold(seq)
    filename = name.lower().replace(" ", "_") + ".pdb"
    with open(filename, "w") as f:
        f.write(pdb)
    print("Saved", filename)
    print("Mean confidence (B-factor column):", mean_confidence(pdb))