from pathlib import Path
import pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import hstack

BASE=Path(__file__).resolve().parent
df=pd.read_csv(BASE/"dataset"/"alumni_dataset.csv")
def text(d):
    return (d["department"].fillna("")+" "+d["skills"].fillna("")+" "+d["job_role"].fillna("")+
            " "+d["interests"].fillna("")+" "+d["location"].fillna("")+" "+d["previous_role"].fillna(""))
v=TfidfVectorizer(token_pattern=r"(?u)\b[\w+#.-]+\b",ngram_range=(1,2))
X1=v.fit_transform(text(df)); s=StandardScaler(); X2=s.fit_transform(df[["experience"]]); X=hstack([X1,X2])
knn=NearestNeighbors(n_neighbors=min(5,len(df)),metric="cosine").fit(X)
class Model:
    def __init__(self,v,s,knn): self.v,self.s,self.knn=v,s,knn
    def features(self, rows):
        d=pd.DataFrame(rows); return hstack([self.v.transform(text(d)),self.s.transform(d[["experience"]])])
joblib.dump(Model(v,s,knn),BASE/"alumni_knn_model.pkl")
print("Saved",BASE/"alumni_knn_model.pkl")
