import pandas as pd
import numpy as np

#introducing dataframe
control4df = pd.read_csv("combined_runs_ControlS4.tsv", sep="\t")

# removing the barcode column
newcontrol4df = control4df.drop(columns= ["barcode"])

control4df_transposed = newcontrol4df.T

logcontrol4df = np.log2(control4df_transposed + 1)

print(logcontrol4df.head())

logcontrol4df.to_csv('LoggedControlS4.tsv', sep="\t")


#introducing dataframe
cte4df = pd.read_csv("combined_runs_CTES4.tsv", sep="\t")

# removing the barcode column
newcte4df = cte4df.drop(columns= ["barcode"])

cte4df_transposed = newcte4df.T

logcte4df = np.log2(cte4df_transposed + 1)

print(logcte4df.head())

logcte4df.to_csv('LoggedCTES4.tsv', sep="\t")