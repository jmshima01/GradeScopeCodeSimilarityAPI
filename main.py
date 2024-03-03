
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
    fix_sec = lambda x : list(map(lambda y: y[-1] if type(y)==str else y,x))
    d["% Similarity"] = fix_percent(d["% Similarity"])
    d["Sections"] = fix_sec(d["Sections"])
    data = d.loc[(d["File"] == "submission.py") & (d["% Similarity"] >= cutoff)].sort_values("% Similarity",ascending=False)
    data = data.drop(columns=['Last, First Name Swap','Unnamed: 7'])
    data = data.rename(columns={'First & Last Name Swap':'Name','Sections':'Section','% Similarity':'Similarity'})

    for i,n in enumerate(data['Name'].values):
        students[n]["Top Source"]=data["Top Source"].values[i]
        students[n]["Similarity"]=data["Similarity"].values[i]
        students[n]["Section"]=data["Section"].values[i]
        
    
    blame= {}
    for i,v in students.items():
        if v:
            blame[i]=v
    for i,v in blame.items():

        print(i,":",v)
    
    data.to_csv("basic.csv",index=False)

    groups = set()
    
    for k in blame:
        group = set()
        
        group.add(k)
        for i,v in blame.items():
            if i == k:
                group.add(v["Top Source"])
            if v["Top Source"] == k:
                group.add(i)
        group = tuple(sorted(list(group)))
        if len(group) > 2:
            groups.add(group)

    groups = list(groups)
    print()
    print(groups)

    group_avg = {}
    for k in groups:
        avg = 0
        l = len(k)
        for i in k:
            if i not in blame.keys():
                print(i," Not in blame")
                l-=1
                continue
            avg+=blame[i]['Similarity']
        group_avg[k] = round(float(avg)/float(l),2)
    
    for i,v in group_avg.items():
        print(i,":",v)

        

    

        
