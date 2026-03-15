# ====================================================
# MODEL 1 : BUILD POPULATION RECOVERY CURVES
# ====================================================

# Import required libraries
import pandas as pd
import numpy as np
import os
import re

# ----------------------------------------------------
# SECTION 1: DEFINE DIRECTORIES
# ----------------------------------------------------

# These directories contain the data for each phase
baseline_dir = "1baseline_data"
acute_dir = "1acute_data"
subacute_dir = "1sub-acute_data"
chronic_dir = "1chronic_data"

# Directory where results will be saved
output_dir = "model1_results"

# Create results directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------------------------
# SECTION 2: DEFINE GENES OF INTEREST
# ----------------------------------------------------

# These are the ten genes used in the project
GENES = [
"MT-ATP6","MT-ND1","MT-ND4","MT-CO3","MT-CYB",
"MT-ND3","SYT1","DPP10","RBFOX1","HBB"
]

# ----------------------------------------------------
# SECTION 3: FUNCTION TO READ FILES FROM A DIRECTORY
# ----------------------------------------------------

def load_phase_data(directory, phase_name):

    """
    This function loads every CSV file inside a directory
    and assigns the correct phase label.
    """

    dataframes = []

    for file in os.listdir(directory):

        if file.endswith(".csv"):

            filepath = os.path.join(directory, file)

            df = pd.read_csv(filepath)

            # Extract subject number from filename
            # Example: acute_subject_3.csv -> subject_id = 3
            match = re.search(r"subject_(\d+)", file)

            if match:
                subject_id = int(match.group(1))
            else:
                subject_id = None

            # Add subject ID and phase label to dataframe
            df["patient_id"] = subject_id
            df["phase"] = phase_name

            dataframes.append(df)

    # Combine all samples in the directory
    if len(dataframes) > 0:
        return pd.concat(dataframes, ignore_index=True)

    else:
        return pd.DataFrame()

# ----------------------------------------------------
# SECTION 4: LOAD ALL PHASE DATA
# ----------------------------------------------------

# Load baseline samples
baseline_df = load_phase_data(baseline_dir, "Baseline")

# Load acute samples
acute_df = load_phase_data(acute_dir, "Acute")

# Load subacute samples
subacute_df = load_phase_data(subacute_dir, "Subacute")

# Load chronic samples
chronic_df = load_phase_data(chronic_dir, "Chronic")

# Combine all data together
df = pd.concat(
    [baseline_df, acute_df, subacute_df, chronic_df],
    ignore_index=True
)

# Save raw combined dataset
df.to_csv(os.path.join(output_dir,"combined_dataset_raw.csv"), index=False)

# ----------------------------------------------------
# SECTION 5: LOG TRANSFORM GENE EXPRESSION
# ----------------------------------------------------

# RNA sequencing data is typically log-transformed
# to stabilize variance

for gene in GENES:
    df[gene] = np.log2(df[gene] + 1)

# ----------------------------------------------------
# SECTION 6: IDENTIFY BASELINE VALUES PER PATIENT
# ----------------------------------------------------

# Extract baseline rows
baseline = df[df["phase"] == "Baseline"]

# Keep one baseline per patient
baseline = baseline[["patient_id"] + GENES].drop_duplicates(subset=["patient_id"])

# Use patient_id as index for fast lookup
baseline = baseline.set_index("patient_id")

# ----------------------------------------------------
# SECTION 7: CALCULATE DELTA FROM BASELINE
# ----------------------------------------------------

# Delta = change from baseline gene expression

for gene in GENES:

    df[f"{gene}_delta"] = df.apply(
        lambda row:
        row[gene] - baseline.loc[row["patient_id"], gene]
        if row["patient_id"] in baseline.index else np.nan,
        axis=1
    )

# Save dataset including deltas
df.to_csv(os.path.join(output_dir,"dataset_with_deltas.csv"), index=False)

# ----------------------------------------------------
# SECTION 8: REMOVE BASELINE FOR RECOVERY ANALYSIS
# ----------------------------------------------------

post_df = df[df["phase"] != "Baseline"]

# ----------------------------------------------------
# SECTION 9: CALCULATE MEAN RECOVERY PER PHASE
# ----------------------------------------------------

summary_rows = []

for gene in GENES:

    for phase in ["Acute","Subacute","Chronic"]:

        vals = post_df.loc[post_df["phase"] == phase, f"{gene}_delta"].dropna()

        if len(vals) > 0:

            mean_val = vals.mean()
            sd_val = vals.std(ddof=1)
            se_val = sd_val / np.sqrt(len(vals))

            summary_rows.append({
                "gene": gene,
                "phase": phase,
                "sample_count": len(vals),
                "mean_delta": mean_val,
                "sd": sd_val,
                "standard_error": se_val
            })

summary_df = pd.DataFrame(summary_rows)

# Save recovery curve statistics
summary_df.to_csv(
    os.path.join(output_dir,"gene_phase_statistics.csv"),
    index=False
)

# ----------------------------------------------------
# SECTION 10: CALCULATE RECOVERY SLOPE
# ----------------------------------------------------

# Estimate the rate at which gene expression returns
# toward baseline across phases

slope_rows = []

for gene in GENES:

    for patient_id, sub in post_df.groupby("patient_id"):

        # Map phase to numeric order
        phase_map = {"Acute":1,"Subacute":2,"Chronic":3}

        sub = sub.copy()
        sub["phase_order"] = sub["phase"].map(phase_map)

        sub = sub[["phase_order",f"{gene}_delta"]].dropna()

        if len(sub) >= 2:

            x = sub["phase_order"].values
            y = sub[f"{gene}_delta"].values

            slope = np.polyfit(x,y,1)[0]

            slope_rows.append({
                "patient_id": patient_id,
                "gene": gene,
                "slope_per_phase": slope
            })

slope_df = pd.DataFrame(slope_rows)

# Mean slope across patients
mean_slope = (
    slope_df.groupby("gene")["slope_per_phase"]
    .agg(["mean","std","count"])
    .reset_index()
)

mean_slope.to_csv(
    os.path.join(output_dir,"gene_recovery_slopes.csv"),
    index=False
)

print("MODEL 1 COMPLETE")
print("Results saved in:", output_dir)