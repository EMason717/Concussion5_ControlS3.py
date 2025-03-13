import pandas as pd
import numpy as np

#introducing dataframe
control2df = pd.read_csv("combined_runs_ControlS2.tsv", sep="\t")

# removing the barcode column
newcontrol2df = control2df.drop(columns= ["barcode"])

control2df_transposed = newcontrol2df.T

logcontrol2df = np.log2(control2df_transposed + 1)

print(logcontrol2df.head())

logcontrol2df.to_csv('LoggedControlS2.tsv', sep="\t")


#introducing dataframe
cte2df = pd.read_csv("combined_runs_CTES2.tsv", sep="\t")

# removing the barcode column
newcte2df = cte2df.drop(columns= ["barcode"])

cte2df_transposed = newcte2df.T

logcte2df = np.log2(cte2df_transposed + 1)

print(logcte2df.head())

logcte2df.to_csv('LoggedCTES2.tsv', sep="\t")