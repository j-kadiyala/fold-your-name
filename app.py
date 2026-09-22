from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from fold_name import name_to_peptide, fold, mean_confidence

app = FastAPI()

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

@app.get("/api/fold")
def api_fold(name: str):
    name = name.strip()[:40]  # keep inputs short and sane
    if not name:
        return JSONResponse({"error": "Type a name first."}, status_code=400)

    safe = "".join(c for c in name.lower() if c.isalnum()) or "name"
    cache_path = os.path.join(CACHE_DIR, f"{safe}.pdb")

    if os.path.exists(cache_path):
        pdb = open(cache_path).read()
    else:
        try:
            seq = name_to_peptide(name)
            pdb = fold(seq)
        except Exception as e:
            return JSONResponse({"error": f"Folding failed: {e}"}, status_code=500)
        with open(cache_path, "w") as f:
            f.write(pdb)

    conf = mean_confidence(pdb)
    seq = name_to_peptide(name)
    return {"name": name, "sequence": seq, "confidence": conf, "pdb": pdb}

@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()