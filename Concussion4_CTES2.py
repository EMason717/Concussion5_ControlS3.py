import os
import pandas as pd
# Set directory
base_dir = os.path.dirname(__file__)
# Construct paths to files
file_run1 = os.path.join(base_dir, "data", "CTE_2.1.counts.tsv")
file_run2 = os.path.join(base_dir, "data", "CTE_2.2.counts.tsv")
file_run3 = os.path.join(base_dir, "data", "CTE_3.1.counts.tsv")
file_run4 = os.path.join(base_dir, "data", "CTE_3.2.counts.tsv")
file_run5 = os.path.join(base_dir, "data", "CTE_4.1.counts.tsv")
file_run6 = os.path.join(base_dir, "data", "CTE_4.2.counts.tsv")
file_run7 = os.path.join(base_dir, "data", "CTE_4.3.counts.tsv")
# Read each file into Pandas dataframe
df_run1 = pd.read_csv(file_run1, sep='\t')
df_run2 = pd.read_csv(file_run2, sep='\t')
df_run3 = pd.read_csv(file_run3, sep='\t')
df_run4 = pd.read_csv(file_run4, sep='\t')
df_run5 = pd.read_csv(file_run5, sep='\t')
df_run6 = pd.read_csv(file_run6, sep='\t')
df_run7 = pd.read_csv(file_run7, sep='\t')
# Check the first few lines to make sure it loaded correctly
print(df_run1.head())
#print(df_run2.head())
#print(df_run3.head())
# Set 'barcode' as index so we can align by barcode when add
df_run1.set_index("barcode", inplace=True)
df_run2.set_index("barcode", inplace=True)
df_run3.set_index("barcode", inplace=True)
df_run4.set_index("barcode", inplace=True)
df_run5.set_index("barcode", inplace=True)
df_run6.set_index("barcode", inplace=True)
df_run7.set_index("barcode", inplace=True)
# Sum the gene counts across the runs
# fill_value = 0 so that if a barcode is missing from one file,
# it's treated as 0 instead of NaN.
df_combined = df_run1.add(df_run2, fill_value=0).add(df_run3, fill_value=0).add(df_run4, fill_value=0).add(df_run5, fill_value=0).add(df_run6, fill_value=0).add(df_run7, fill_value=0)
# Bring back 'barcode' back as normal column instead of the index:
df_combined.reset_index(inplace=True)
# Save the combined results to a new TSV file
control_5 = os.path.join(base_dir, "combined_runs", "combined_runs_CTES2.tsv")
df_combined.to_csv(control_5, sep='\t', index=False)
# Print confirmation
print("Combined file created at:", control_5)
print(df_combined.head())