import pandas as pd
import csv

class Gradscope_Similarity_HTML_Parser:
    def __init__(self,html_file_path:str,cutoff_simularity:int,assessment:str,files_to_comp:list) -> None:
        self.path = html_file_path
        self.cutoff = cutoff_simularity
        self.file_comp = files_to_comp
        self.assessment = assessment
        self.df = self.__create_df()


    def __create_df(self) -> pd.DataFrame:
        # reads html tables into df
        df = pd.read_html(self.path)[0]
        print(df.columns)
        # "xx%" -> int(xx)
        fix_percent = lambda x : list(map(lambda y: int(y[:-1]),x))
        
        # "COMPUTER_SCI_SECTION_X" -> 'X'
        fix_sec = lambda x : list(map(lambda y: y[-1] if type(y)==str else y,x))
        
        df["% Similarity"] = fix_percent(df["% Similarity"])
        df["Sections"] = fix_sec(df["Sections"])
        
        # filter by `submission.py` and similarity % that is greater than or equal to the cuttoff specified 
        data = df.loc[(df["File"].isin(self.file_comp)) & (df["% Similarity"] >= self.cutoff)].sort_values("% Similarity",ascending=False)
        
        # clean cols
        data = data.drop(columns=['Last, First Name Swap','Unnamed: 7'])
        data = data.rename(columns={'First & Last Name Swap':'Name','Sections':'Section','% Similarity':'Similarity'})
        return data

    # gives filterd dicts of df
    def __parse_students(self):
        students = {name[0]:{} for name in self.df.loc[:,["Name"]].values}
        for i,n in enumerate(self.df["Name"].values):
            students[n]["Top Source"]=self.df["Top Source"].values[i]
            students[n]["Similarity"]=self.df["Similarity"].values[i]
            students[n]["Section"]=self.df["Section"].values[i]
            students[n]["Match Length"]=self.df["Match Length"].values[i]
        blame= {}
        for i,v in students.items():
            if v:
                blame[i]=v
        return blame,students

    # csv same to seen filtered Gradescope Report for ref
    def generate_all_csv(self) -> None:
        name = f"assessment_{self.assessment}_raw.csv"
        self.df.to_csv(name,index=False)

    # filter unique pairs from df to a csv
    def generate_pairs_csv(self) -> None:
        pairs = {}
        blame,_ = self.__parse_students()
        pair = []
        for i,v in blame.items():
            pair.append(i)
            pair.append(v["Top Source"])
            pair = tuple(sorted(pair))
            pairs[pair] = [v["Similarity"],v["Match Length"]]
            pair = []
        print(pairs)

        to_csv = [["Pair","Similarity", "Match Length"]]

        for i,v in pairs.items():
            t = ["|".join(list(i))]
            for j in v:
                t.append(j)
            to_csv.append(t)
        name = f"assessment_{self.assessment}_pairs.csv"
        with open(name, "w+") as f:
            writer = csv.writer(f)
            writer.writerows(to_csv)

    # filter unique groups (num_students>=3) from df to a csv
    def generate_group_csv(self) -> None:
        groups = set()
        blame, all_students = self.__parse_students()
        
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
        
        # No groups found i.e. length >= 3
        if groups == []:
            print(f"No Groups where all studdents have Similarity >= {self.cutoff}%")
            return
        
        group_avg = {k:[] for k in groups}
        for k in groups:
            avg = 0
            l = len(k)
            for i in k:
                if i not in blame.keys():
                    # print(i," Not in blame")
                    l-=1
                    continue
                avg+=blame[i]['Similarity']
            group_avg[k].append(round(float(avg)/float(l),2))
        for k in groups:
            sections = []
            for i in k:
                if i in all_students.keys():
                    sections.append(str(all_students[i]["Section"]))
            sections = "".join(sections)
            group_avg[k].append(sections)

        # for i,v in group_avg.items():
        #     print(i,":",v)
        
        to_csv = [["Group","Average Similarity", "Sections"]]

        for i,v in group_avg.items():
            t = ["|".join(list(i))]
            for j in v:
                t.append(j)
            to_csv.append(t)
        name = f"assessment_{self.assessment}_groups.csv"
        with open(name, "w+") as f:
            writer = csv.writer(f)
            writer.writerows(to_csv)
        
