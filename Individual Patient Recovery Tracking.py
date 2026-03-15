# ====================================================
# MODEL 2 : INDIVIDUAL RECOVERY TRACKING
# ====================================================

import pandas as pd
import numpy as np
import os

# Directory for results
output_dir = "model2_results"
os.makedirs(output_dir, exist_ok=True)

# Genes analyzed
GENES = [
"MT-ATP6","MT-ND1","MT-ND4","MT-CO3","MT-CYB",
"MT-ND3","SYT1","DPP10","RBFOX1","HBB"
]

# ----------------------------------------------------
# LOAD MODEL 1 STATISTICS
# ----------------------------------------------------

summary_df = pd.read_csv("model1_results/gene_phase_statistics.csv")

# ----------------------------------------------------
# LOAD NEW PATIENT DATA
# ----------------------------------------------------

# Patient dataset should contain:
# baseline + post-injury samples

patient_df = pd.read_csv("new_patient_data.csv")

# Log transform expression
for gene in GENES:
    patient_df[gene] = np.log2(patient_df[gene] + 1)

# Identify baseline row
baseline = patient_df[patient_df["phase"]=="Baseline"].iloc[0]

results = []

# ----------------------------------------------------
# COMPARE PATIENT TO MODEL
# ----------------------------------------------------

for _,row in patient_df.iterrows():

    if row["phase"] == "Baseline":
        continue

    phase = row["phase"]

    for gene in GENES:

        patient_delta = row[gene] - baseline[gene]

        ref = summary_df[
            (summary_df["gene"]==gene) &
            (summary_df["phase"]==phase)
        ]

        if len(ref) == 1:

            mean_delta = ref.iloc[0]["mean_delta"]
            se = ref.iloc[0]["standard_error"]

            deviation = patient_delta - mean_delta

            results.append({
                "sample_id": row["sample_id"],
                "phase": phase,
                "gene": gene,
                "patient_delta": patient_delta,
                "expected_mean": mean_delta,
                "deviation": deviation
            })

results_df = pd.DataFrame(results)

# Save comparison table
results_df.to_csv(
    os.path.join(output_dir,"patient_gene_comparison.csv"),
    index=False
)

# ----------------------------------------------------
# CALCULATE RECOVERY SCORE
# ----------------------------------------------------

scores = (
    results_df.groupby(["sample_id","phase"])["deviation"]
    .apply(lambda x: np.mean(np.abs(x)))
    .reset_index()
)

scores.rename(columns={"deviation":"mean_absolute_deviation"}, inplace=True)

scores.to_csv(
    os.path.join(output_dir,"patient_recovery_scores.csv"),
    index=False
)

print("MODEL 2 COMPLETE")
print("Results saved in:", output_dir)