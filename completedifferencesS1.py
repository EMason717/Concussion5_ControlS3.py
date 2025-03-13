import pandas as pd
import os

# File paths for input data
control_path = "LoggedControlS1.tsv"
cte_path = "LoggedCTES1.tsv"

# Define output directory and file name
output_dir = "differences"
output_file = "differencesS1.1.tsv"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Full output path
output_path = os.path.join(output_dir, output_file)

# Load the data
control_df = pd.read_csv(control_path, sep="\t", index_col=0)
cte_df = pd.read_csv(cte_path, sep="\t", index_col=0)

# Convert expression data into binary (1 = expressed, 0 = not expressed)
control_bin = (control_df > 0).astype(int)
cte_bin = (cte_df > 0).astype(int)

# Identify gained and lost genes
gained_genes = (cte_bin > control_bin).astype(int)  # Genes turned on
lost_genes = (control_bin > cte_bin).astype(int)  # Genes turned off

# Sum across barcodes to find total number of times each gene was gained or lost
gained_counts = gained_genes.sum(axis=1)
lost_counts = lost_genes.sum(axis=1)

# Keep only genes that were expressed in either condition
expressed_in_either = (control_bin.sum(axis=1) > 0) | (cte_bin.sum(axis=1) > 0)
filtered_gained_counts = gained_counts[expressed_in_either]
filtered_lost_counts = lost_counts[expressed_in_either]

# Create a DataFrame with results
changes_df = pd.DataFrame({
    "Genes": filtered_gained_counts.index,  # Gene names
    "Gained_Expression": filtered_gained_counts,  # How many barcodes gained expression
    "Lost_Expression": filtered_lost_counts   # How many barcodes lost expression
})

# Sort by most gained and most lost genes
changes_df = changes_df.sort_values(by=["Gained_Expression", "Lost_Expression"], ascending=[False, False])

# Save results to file
changes_df.to_csv(output_path, sep="\t", index=False)

# Print confirmation
print(f"Analysis complete. Results saved to {output_path}")
