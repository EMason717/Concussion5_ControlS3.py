import pandas as pd
import numpy as np

#introducing dataframe
control5df = pd.read_csv("combined_runs_ControlS5.tsv", sep="\t")

# removing the barcode column
newcontrol5df = control5df.drop(columns= ["barcode"])

control5df_transposed = newcontrol5df.T

logcontrol5df = np.log2(control5df_transposed + 1)

print(logcontrol5df.head())

logcontrol5df.to_csv('LoggedControlS5.tsv', sep="\t")


#introducing dataframe
cte5df = pd.read_csv("combined_runs_CTES5.tsv", sep="\t")

# removing the barcode column
newcte5df = cte5df.drop(columns= ["barcode"])

cte5df_transposed = newcte5df.T

logcte5df = np.log2(cte5df_transposed + 1)

print(logcte5df.head())

logcte5df.to_csv('LoggedCTES5.tsv', sep="\t")