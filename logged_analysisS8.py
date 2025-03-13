import pandas as pd
import numpy as np

#introducing dataframe
control8df = pd.read_csv("combined_runs_ControlS8.tsv", sep="\t")

# removing the barcode column
newcontrol8df = control8df.drop(columns= ["barcode"])

control8df_transposed = newcontrol8df.T

logcontrol8df = np.log2(control8df_transposed + 1)

print(logcontrol8df.head())

logcontrol8df.to_csv('LoggedControlS8.tsv', sep="\t")

