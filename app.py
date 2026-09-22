from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os

from fold_name import name_to_peptide, fold, mean_confidence

app = FastAPI()

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

latest_fold = {"name": None, "sequence": None, "confidence": None}

@app.get("/api/fold")
def api_fold(name: str):
    name = name.strip()[:40]
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

    latest_fold["name"] = name
    latest_fold["sequence"] = seq
    latest_fold["confidence"] = conf

    return {"name": name, "sequence": seq, "confidence": conf, "pdb": pdb}

@app.get("/api/latest")
def api_latest():
    if latest_fold["name"] is None:
        return {"name": "Nobody yet", "sequence": "", "confidence": 0}
    return latest_fold

@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)