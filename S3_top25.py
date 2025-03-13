import pandas as pd
import os

# Set base directory (directory of the script)
base_dir = os.path.dirname(__file__)

# Construct the correct file path assuming the file is in the "analysis1.0" folder
file_path = os.path.join(base_dir, "analysis1.0", "analysisS4.tsv")

# Load the analysis output from the correct location
df = pd.read_csv(file_path, sep='\t', index_col=0)

# Display the first few rows to check the structure
print(df.head())

# Compute a new column for maximum absolute difference using 'Max_Difference' and 'Min_Difference'
df['Abs_Max_Difference'] = df[['Max_Difference', 'Min_Difference']].abs().max(axis=1)

# Rank genes by the maximum absolute difference (instead of mean difference)
top_25_genes = df['Abs_Max_Difference'].nlargest(25)

# Print the top 25 changed genes
print(top_25_genes)

# Construct the output directory path for top25 genes
top25_dir = os.path.join(base_dir, "top25")
os.makedirs(top25_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Construct the full output file path
output_file = os.path.join(top25_dir, "S3_top25.tsv")

# Save the top 25 genes to the file
top_25_genes.to_csv(output_file, sep='\t')

# Print confirmation
print("Combined file created at:", output_file)
