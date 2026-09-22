import time
from fold_name import name_to_peptide, fold, mean_confidence

names = ["Jyotirmai", "Alex", "Maria", "Priya", "Chen", "Zoe",
         "Christopher", "Muhammad", "Elizabeth", "José", "Xavier",
         "Bo", "Anna Maria", "Google", "Amazon", "Goldman Sachs"]

print(f"{'Name':<16}{'Len':>5}{'Conf':>8}")
for n in names:
    try:
        seq = name_to_peptide(n)
        pdb = fold(seq)
        print(f"{n:<16}{len(seq):>5}{mean_confidence(pdb):>8.3f}")
    except Exception as e:
        print(f"{n:<16} ERROR: {e}")
    time.sleep(1)