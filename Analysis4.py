import pandas as pd
import os

def load_tsv(file_path):
    """Loads a TSV file into a pandas DataFrame."""
    return pd.read_csv(file_path, sep='\t', index_col=0)

def compare_expression(control_file, cte_file):
    """Compares gene expression levels between control and CTE conditions."""
    control_df = load_tsv(control_file)
    cte_df = load_tsv(cte_file)

    # Ensure both dataframes have the same genes (columns)
    common_genes = control_df.columns.intersection(cte_df.columns)
    control_df = control_df[common_genes]
    cte_df = cte_df[common_genes]

    # Compute the difference in expression levels
    diff_df = cte_df - control_df

    # Summarize statistics instead of averaging across genes
    diff_df['Mean_Difference'] = diff_df.mean(axis=1)
    diff_df['Max_Difference'] = diff_df.max(axis=1)
    diff_df['Min_Difference'] = diff_df.min(axis=1)

    return diff_df

def main():
    """Main function to run the analysis."""
    base_dir = os.path.join(os.getcwd(), 'Logged_runs')
    control_path = os.path.join(base_dir, 'LoggedControlS4.tsv')
    cte_path = os.path.join(base_dir, 'LoggedCTES4.tsv')

    if not os.path.exists(control_path) or not os.path.exists(cte_path):
        print("One or both input files are missing.")
        return

    result_df = compare_expression(control_path, cte_path)

    # Save results to the analysis directory
    output_dir = os.path.join(os.getcwd(), 'analysis1.0')
    os.makedirs(output_dir, exist_ok=True)
    result_path = os.path.join(output_dir, 'analysisS4.tsv')
    result_df.to_csv(result_path, sep='\t', chunksize=1000)
    print(f"Analysis complete. Results saved to {result_path}")

if __name__ == "__main__":
    main()