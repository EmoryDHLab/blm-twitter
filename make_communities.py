import pandas as pd
import tsm
import os
import shutil

df = pd.read_json("merged_english_clean.json")
reference = {2: (359, 607), 3: (607, 919), 4: (919, 2338), 5: (2338, 2410), 6: (2410, 3000)}
if "bins" in os.listdir():
    shutil.rmtree("bins")
os.mkdir("bins")
for i in range(2, 7):
    folder = "bins/bin" + str(i)
    if folder in os.listdir("bins"):
        shutil.rmtree(folder)
    os.mkdir(folder)
    print(f"BINNING NUMBER {i} NOW.")
    start, end = reference[i]
    mask = [start <= day < end for day in df['days']]
    community_subset = df.loc[mask]
    print(f"BIN LOCATED. LENGTH OF {len(community_subset)}. MAKING EDGELIST NOW.")
    filename = "bins/bin" + str(i)
    community_subset.to_json((filename + "/tweets.json"))
    tsm.t2e((filename + "/tweets.json"), save_prefix = filename + "/")
    tsm.get_top_communities((filename + "/_edgelist.csv"), save_prefix = filename + "/")