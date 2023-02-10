import pandas as pd
import tsm
import os
import shutil

def json_to_communities(prefix = "main", num_comm = 10):
    streng = prefix + "_bins"
    df = pd.read_json("merged_english_clean.json")
    reference = {0: (0, 244), 1: (244, 358), 2: (358, 607), 3: (607, 919), 4: (919, 2338), 5: (2338, 2410), 6: (2410, 3000)}
    if streng in os.listdir():
        shutil.rmtree(streng)
    os.mkdir(streng)
    for i in range(0, 7):
        folder = streng + "/bin" + str(i)
        if folder in os.listdir(streng):
            shutil.rmtree(folder)
        os.mkdir(folder)
        print(f"BINNING NUMBER {i} NOW.")
        start, end = reference[i]
        mask = [start <= day < end for day in df['days']]
        community_subset = df.loc[mask]
        print(f"BIN LOCATED. LENGTH OF {len(community_subset)}. MAKING EDGELIST NOW.")
        filename = streng + "/bin" + str(i)
        community_subset.to_json((filename + "/tweets.json"))
        tsm.t2e((filename + "/tweets.json"), save_prefix = filename + "/")
        tsm.get_top_communities((filename + "/_edgelist.csv"), top_comm = (num_comm - 1), save_prefix = filename + "/")

def edgelist_to_communities(folder = "bins", num_comm = 10, save_prefix = ''):
    if folder not in os.listdir():
        raise Exception("Folder not found!")
    for i in range(0, 7):
        print(f"Community clustering for bin {i}:")
        edgepath = folder + "/bin" + str(i) + "/_edgelist.csv"
        tsm.get_top_communities(edgepath, top_comm = (num_comm - 1), save_prefix = (folder + "/bin" + str(i) + "/" + save_prefix))
edgelist_to_communities(folder = "bins", num_comm = 6, save_prefix = '6')
edgelist_to_communities(folder = "bins", num_comm = 10, save_prefix = '10')
edgelist_to_communities(folder = "bins", num_comm = 20, save_prefix = '20')
edgelist_to_communities(folder = "bins", num_comm = 50, save_prefix = '50')
