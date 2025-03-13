import pandas as pd
import numpy as np

#introducing dataframe
control1df = pd.read_csv("combined_runs_ControlS1.tsv", sep="\t")

# removing the barcode column
newcontrol1df = control1df.drop(columns= ["barcode"])

control1df_transposed = newcontrol1df.T

logcontrol1df = np.log2(control1df_transposed + 1)

print(logcontrol1df.head())

logcontrol1df.to_csv('LoggedControlS1.1.tsv', sep="\t")


#introducing dataframe
cte1df = pd.read_csv("combined_runs_CTES1.tsv", sep="\t")

# removing the barcode column
newcte1df = cte1df.drop(columns= ["barcode"])

cte1df_transposed = newcte1df.T

logcte1df = np.log2(cte1df_transposed + 1)

print(logcte1df.head())

logcte1df.to_csv('LoggedCTES1.1.tsv', sep="\t")