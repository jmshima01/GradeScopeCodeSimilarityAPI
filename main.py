
import pandas as pd
from sys import argv
import subprocess

if __name__ == "__main__":
    
    if len(argv) < 2:
        print("Usage: python3 main.py percent_cutoff")
        exit(1)
    
    cutoff = int(argv[1])

    d = pd.read_html("curl.html")[0]
    name = "First & Last Name Swap"
    print(d.columns)
    
        
    students = {name[0]:{} for name in d.loc[:,[name]].values}
 
    fix_percent = lambda x : list(map(lambda y: int(y[:-1]),x))
    
    d["% Similarity"] = fix_percent(d["% Similarity"])
    
    data = d.loc[(d["File"] == "submission.py") & (d["% Similarity"] >= cutoff)].sort_values("% Similarity",ascending=False)
    for i,n in enumerate(data[name].values):
        students[n]["Top Source"]=data["Top Source"].values[i]
        students[n]["% Similarity"]=data["% Similarity"].values[i]
    
    for i,v in students.items():
        if v:
            print(f"{i}:{v}")


    

    