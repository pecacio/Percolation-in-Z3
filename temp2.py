import os
import pickle
import matplotlib.pyplot as plt

# Collect all data

folders = ["test", "test2", "test3", "test4", "test5"]
dest_folder_path = os.path.join(os.getcwd(), "all_record")
rec = {}

for folder in folders:
    folderpath = os.path.join(os.getcwd(), folder)
    files = os.listdir(folderpath)
    for filename in files:
        filepath = os.path.join(folderpath, filename)


        with open(filepath, "rb") as fp:
            data = dict(pickle.load(fp))

            p = data["p"]

            # find n_max
            n_max = 1
            while True: 
                if n_max+1 not in data.keys():
                    break
                n_max += 1
            if n_max not in rec.keys():
                rec[n_max] = {}
            
            if p not in rec[n_max].keys():
                rec[n_max][p] = {"trials_done":0}
                
                for j in range(1, n_max+1):
                    rec[n_max][p][j] = 0
            
            for k in range(1, n_max+1):
                rec[n_max][p][k] += data[k]
            rec[n_max][p]["trials_done"] += data["trials_done"]



# print completed trials info

for n_max in rec.keys():
    print(f"n_max = {n_max}")
    for p in rec[n_max].keys():
        print(f"p = {p}")
        print(f"trials done = {rec[n_max][p]['trials_done']}\n")
    print()
        

# creating relevent plots

for n_max in rec.keys():
    plt.figure(figsize = (10,6), dpi = 300)
    plt.title(f"n_max = {n_max}")
    p_vals = sorted(list(rec[n_max].keys()))
    for p in p_vals:
        trials_done = rec[n_max][p]["trials_done"]
        density = [rec[n_max][p][i]/trials_done for i in range(1, n_max+1)]
        plt.plot(range(1, n_max+1), density, label = f"p = {p}")
    
    plt.legend()
    plt.savefig(os.path.join(dest_folder_path, f"n_max = {n_max}.png"))
    plt.close()