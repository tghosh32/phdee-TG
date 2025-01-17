# Homework 2

# Importing libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import ttest_ind


# Setting directories and seed
input_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/input'
output_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/output'

np.random.seed(6578103)

# Reading data
eer_prog = pd.read_csv(os.path.join(input_dir, 'kwh.csv'))

# Split into treatment and control groups
control = eer_prog[eer_prog['retrofit'] == 0]
treatment = eer_prog[eer_prog['retrofit'] == 1]

# Variables to compare
variables = ['electricity', 'sqft', 'temp']
rows = []

# Generate the statistics for each variable
for var in variables:
    mean_control = control[var].mean()
    std_control = control[var].std()
    mean_treatment = treatment[var].mean()
    std_treatment = treatment[var].std()
    p_value = ttest_ind(control[var], treatment[var], equal_var=False).pvalue
    
    # Append data for each variable
    rows.append([
        var,
        f"{mean_control:.2f}", f"{mean_treatment:.2f}", f"{p_value:.4f}"
    ])
    rows.append(["", f"({std_control:.2f})", f"({std_treatment:.2f})", ""])

# Add observations row
rows.append([
    "Observations",
    len(control),
    len(treatment),
    ""
])

# Convert to DataFrame
balance_df = pd.DataFrame(
    rows, 
    columns=["Variable", "Control", "Treatment", "P-value"]
)

# Export as LaTeX table
balance_tab = balance_df.to_latex(index=False, escape=False, multicolumn=False)
output_path = os.path.join(output_dir, "balance_table.tex")

with open(output_path, "w") as f:
    f.write(balance_tab)




