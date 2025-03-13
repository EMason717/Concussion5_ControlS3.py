import pandas as pd
import numpy as np

#introducing dataframe
control6df = pd.read_csv("combined_runs_ControlS6.tsv", sep="\t")

# removing the barcode column
newcontrol6df = control6df.drop(columns= ["barcode"])

control6df_transposed = newcontrol6df.T

logcontrol6df = np.log2(control6df_transposed + 1)

print(logcontrol6df.head())

logcontrol6df.to_csv('LoggedControlS6.tsv', sep="\t")


#introducing dataframe
cte6df = pd.read_csv("combined_runs_CTES6.tsv", sep="\t")

# removing the barcode column
newcte6df = cte6df.drop(columns= ["barcode"])

cte6df_transposed = newcte6df.T

logcte6df = np.log2(cte6df_transposed + 1)

print(logcte6df.head())

logcte6df.to_csv('LoggedCTES6.tsv', sep="\t")