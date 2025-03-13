import pandas as pd
import numpy as np

#introducing dataframe
control3df = pd.read_csv("combined_runs_ControlS3.tsv", sep="\t")

# removing the barcode column
newcontrol3df = control3df.drop(columns= ["barcode"])

control3df_transposed = newcontrol3df.T

logcontrol3df = np.log2(control3df_transposed + 1)

print(logcontrol3df.head())

logcontrol3df.to_csv('LoggedControlS3.tsv', sep="\t")


#introducing dataframe
cte3df = pd.read_csv("combined_runs_CTES3.tsv", sep="\t")

# removing the barcode column
newcte3df = cte3df.drop(columns= ["barcode"])

cte3df_transposed = newcte3df.T

logcte3df = np.log2(cte3df_transposed + 1)

print(logcte3df.head())

logcte3df.to_csv('LoggedCTES3.tsv', sep="\t")