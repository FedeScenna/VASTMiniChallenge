import pandas as pd
import os

df = pd.read_csv("data/email headers.csv", sep=",", encoding="cp1252")

long_df=pd.DataFrame(data = {"from": [],
                            "to":[],
                            "date":[],
                            "subject":[]})

for f in range(0,len(df["From"])):
    # ver a cuantos les mando
    to_array = df["To"][f].split(", ")
    # y replicar el resto de los datos
    for t in to_array:
        single_df = pd.DataFrame(data = {"from": df["From"][f],
            "to": t,
            "date": df["Date"][f],
            "subject":df["Subject"][f]
        },index = [0])
        long_df=long_df.append(single_df, ignore_index = True)

long_df.to_csv("data/employee_headers_long.csv", index = False)