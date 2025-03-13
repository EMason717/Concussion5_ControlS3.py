import pandas as pd
import os


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

    # 5. Select the top 10 genes based on the average (Mean_Across_All)
    top_10_genes = combined_df['Mean_Across_All'].nlargest(10)

    # Print them to the console
    print("\nTop 10 Genes (by average Abs_Max_Difference across 6 files):")
    print(top_10_genes)

    # Create a directory to save results
    top10_dir = os.path.join(base_dir, "top10")
    os.makedirs(top10_dir, exist_ok=True)

    # Save the top 10 gene list to a TSV file
    output_file = os.path.join(top10_dir, "top10_across_all.tsv")
    top_10_genes.to_csv(output_file, sep='\t')
    print(f"\nTop 10 genes saved to: {output_file}")


if __name__ == "__main__":
    main()
