import time
from fold_name import name_to_peptide, fold, mean_confidence

names = ["Chen", "Christopher", "Goldman Sachs", "Priya"]
settings = [("EAAAK", 3), ("EAAAK", 4), ("EAAAK", 5), ("EAAAKEAAAK", 3)]

print(f"{'Name':<16}{'Linker':<12}{'Rep':>4}{'Len':>5}{'Conf':>8}")
for n in names:
    for linker, reps in settings:
        seq = name_to_peptide(n, linker=linker, repeats=reps)
        pdb = fold(seq)
        with open(f"{n.lower().replace(' ', '_')}_{linker}_{reps}.pdb", "w") as f:
            f.write(pdb)
        print(f"{n:<16}{linker:<12}{reps:>4}{len(seq):>5}{mean_confidence(pdb):>8.3f}")
        time.sleep(1)