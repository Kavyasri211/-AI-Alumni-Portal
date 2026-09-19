from pathlib import Path
import joblib
from Backend.database import get_db
MODEL=Path(__file__).resolve().parents[2]/"ML"/"alumni_knn_model.pkl"

def recommend(uid,n=4):
    c=get_db(); target=c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
    rows=c.execute("SELECT * FROM users WHERE role='alumni' AND id<>?",(uid,)).fetchall(); c.close()
    if not target: return []
    candidates=[dict(r) for r in rows]
    try:
        m=joblib.load(MODEL)
        q=m.features([dict(target)])
        distances,indices=m.knn.kneighbors(q,n_neighbors=min(n,len(candidates)))
        return [{**candidates[i],"similarity":round((1-float(distances[0][j]))*100,1)} for j,i in enumerate(indices[0])]
    except Exception:
        ts=set(s.strip().lower() for s in (target["skills"] or "").split(","))
        scored=[]
        for x in candidates:
            ss=set(s.strip().lower() for s in (x["skills"] or "").split(","))
            score=len(ts&ss)*3+(x["department"]==target["department"])*2+(x["location"]==target["location"])
            scored.append((score,x))
        scored.sort(key=lambda z:z[0],reverse=True)
        return [{**x,"similarity":min(98,50+score*8)} for score,x in scored[:n]]
