import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    # 1. Set up paths and file names
    base_dir = os.path.dirname(__file__)
    analysis_dir = os.path.join(base_dir, "analysis1.0")

    # We'll look for files: analysisS1.tsv, analysisS2.tsv, ..., analysisS6.tsv
    analysis_files = [f"analysisS{i}.tsv" for i in range(1, 7)]

    df_list = []

    # 2. Loop through each file and compute Abs_Max_Difference
    for filename in analysis_files:
        file_path = os.path.join(analysis_dir, filename)
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} does not exist.")
            continue

        # Load the analysis output
        df_temp = pd.read_csv(file_path, sep='\t', index_col=0)

        # Ensure the required columns exist
        if not {'Max_Difference', 'Min_Difference'}.issubset(df_temp.columns):
            print(f"Warning: {filename} missing 'Max_Difference' or 'Min_Difference' columns.")
            continue

        # Compute Abs_Max_Difference
        df_temp['Abs_Max_Difference'] = df_temp[['Max_Difference', 'Min_Difference']].abs().max(axis=1)

        # Keep only that column and rename it to include sample info (e.g. "S1")
        sample_id = filename.replace("analysis", "").replace(".tsv", "")  # e.g. "S1"
        new_col = f"Abs_Max_Diff_{sample_id}"
        df_temp = df_temp[['Abs_Max_Difference']].rename(columns={'Abs_Max_Difference': new_col})

        df_list.append(df_temp)

    # Stop if no valid data was loaded
    if not df_list:
        print("No valid analysis files were found. Exiting.")
        return

    # 3. Combine all DataFrames on the gene index (outer join), fill missing with 0
    combined_df = pd.concat(df_list, axis=1).fillna(0)

    # 4. Calculate sum across all 6 samples, then divide by 6 to get the average
    combined_df['Sum_Across_All'] = combined_df.sum(axis=1)
    combined_df['Mean_Across_All'] = combined_df['Sum_Across_All'] / 6

    # 5. Select the top 20 genes based on the average (Mean_Across_All)
    top_20_genes = combined_df['Mean_Across_All'].nlargest(20)

    print("\nTop 20 Genes (by average Abs_Max_Difference across 6 files):")
    print(top_20_genes)

    # Create a directory to save results
    top20_dir = os.path.join(base_dir, "top20")
    os.makedirs(top20_dir, exist_ok=True)

    # Save the top 20 gene list to a TSV file
    output_file = os.path.join(top20_dir, "top20_across_all.tsv")
    top_20_genes.to_csv(output_file, sep='\t')
    print(f"\nTop 20 genes saved to: {output_file}")

    # 6. Create a heatmap for the top 20 genes
    #    We'll extract only the sample columns (Abs_Max_Diff_S1 ... S6) for these genes
    sample_cols = [col for col in combined_df.columns if col.startswith("Abs_Max_Diff_")]
    heatmap_data = combined_df.loc[top_20_genes.index, sample_cols]

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap_data, aspect='auto', cmap='viridis')
    cbar = plt.colorbar()
    cbar.set_label('Abs Max Difference')

    # Label the axes
    plt.xticks(
        ticks=np.arange(len(sample_cols)),
        labels=sample_cols,
        rotation=45,
        ha='right'
    )
    plt.yticks(
        ticks=np.arange(len(heatmap_data.index)),
        labels=heatmap_data.index
    )
    plt.title('Top 20 Genes: Abs Max Difference Across 6 Samples')
    plt.xlabel('Samples')
    plt.ylabel('Genes')
    plt.tight_layout()

    # If you want to save the figure instead of just showing it, uncomment:
plt.savefig(os.path.join(top20_dir, "top20_heatmap.png"), dpi=300)
plt.show()


if __name__ == "__main__":
    main()
