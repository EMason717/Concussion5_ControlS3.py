import pandas as pd
import numpy as np

#introducing dataframe
control7df = pd.read_csv("combined_runs_ControlS7.tsv", sep="\t")

# removing the barcode column
newcontrol7df = control7df.drop(columns= ["barcode"])

control7df_transposed = newcontrol7df.T

logcontrol7df = np.log2(control7df_transposed + 1)

print(logcontrol7df.head())

logcontrol7df.to_csv('LoggedControlS7.tsv', sep="\t")
