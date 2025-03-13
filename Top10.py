import pandas as pd
import os


def aggregate_top25_samples(sample_ids, input_dir):
    """
    Reads the top 25 files for each sample from the input_dir and aggregates the Abs_Max_Difference metric.

    Parameters:
        sample_ids (list): List of sample identifiers (e.g., ["S1", "S2", ...]).
        input_dir (str): Directory where the top 25 files are stored.

    Returns:
        pd.DataFrame: DataFrame with aggregated Abs_Max_Difference per gene.
    """
    df_list = []

    for sample in sample_ids:
        file_name = f"{sample}_top25.tsv"
        file_path = os.path.join(input_dir, file_name)
        if os.path.exists(file_path):
            # Load file with gene names as index; we expect an "Abs_Max_Difference" column
            df_sample = pd.read_csv(file_path, sep='\t', index_col=0)
            if "Abs_Max_Difference" in df_sample.columns:
                df_list.append(df_sample[["Abs_Max_Difference"]])
            else:
                print(f"Warning: {file_path} does not contain the 'Abs_Max_Difference' column.")
        else:
            print(f"Warning: {file_path} not found.")

    if not df_list:
        print("No valid sample files were found.")
        return None

    # Concatenate all DataFrames (each row is a gene from one sample)
    aggregated_df = pd.concat(df_list, axis=0)
    # Group by gene (index) across samples and calculate the mean Abs_Max_Difference
    aggregated_df = aggregated_df.groupby(aggregated_df.index).mean()
    return aggregated_df


def main():
    # Set the base directory to the directory of the script
    base_dir = os.path.dirname(__file__)
    # Directory where all the top25 sample files are stored
    top25_dir = os.path.join(base_dir, "top25")
    # List of sample identifiers (assuming six samples: S1 to S6)
    sample_ids = ["S1", "S2", "S3", "S4", "S5", "S6"]

    aggregated_df = aggregate_top25_samples(sample_ids, top25_dir)
    if aggregated_df is None:
        return

    # Rank the genes by the aggregated Abs_Max_Difference and select the top 10 genes
    top_10_genes = aggregated_df["Abs_Max_Difference"].nlargest(10)

    # Create an output directory for the top 10 genes
    output_dir = os.path.join(base_dir, "top10")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "top10.tsv")

    # Save the top 10 genes to a TSV file
    top_10_genes.to_csv(output_file, sep='\t')
    print("Top 10 genes saved to:", output_file)


if __name__ == "__main__":
    main()