# %% 
# Homework 2

# Importing libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import ttest_ind
from scipy.optimize import minimize

# %% 
# Setting directories and seed
input_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/input'
output_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/output'

np.random.seed(6578103)

# %% 
# Reading data
eer_prog = pd.read_csv(os.path.join(input_dir, 'kwh.csv'))

# %% 
# Split into treatment and control groups
control = eer_prog[eer_prog['retrofit'] == 0]
treatment = eer_prog[eer_prog['retrofit'] == 1]

# %% 
# Variables to compare
variables = ['electricity', 'sqft', 'temp']
rows = []

# %% 
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

# %% 
# Export as LaTeX table
balance_tab = balance_df.to_latex(index=False, escape=False, multicolumn=False)
output_path = os.path.join(output_dir, "balance_table.tex")

with open(output_path, "w") as f:
    f.write(balance_tab)

# %% 
# Plot histograms
sns.kdeplot(control['electricity'], label='Control Group', shade=True, color='blue')
sns.kdeplot(treatment['electricity'], label='Treatment Group', shade=True, color='red')
plt.xlabel('Electricity Use')
plt.ylabel('Density')
plt.legend(title='Group')

output_path = os.path.join(output_dir, 'kdplot_electricity_use.pdf')
plt.savefig(output_path)
plt.show()

# %%
# Fit a linear regression model

Y = eer_prog['electricity'].values.reshape(-1, 1)
X = eer_prog[['sqft', 'retrofit', 'temp']].values
X = np.hstack([np.ones((X.shape[0], 1)), X]) # Add constant

# # --- Method 1: OLS by Hand ---
XtX = np.dot(X.T, X)  # X'X
XtY = np.dot(X.T, Y)  # X'Y
beta_ols_hand = np.dot(np.linalg.inv(XtX), XtY)  # (X'X)^(-1)X'Y

print(f"OLS by Hand: {beta_ols_hand}")

# # --- Method 2: OLS by Simulated Least Squares ---
def sum_squared_residuals(beta, X, Y):
    residuals = Y - np.dot(X, beta.reshape(-1, 1))
    return np.sum(residuals**2)

beta_initial = np.zeros(X.shape[1])

result = minimize(sum_squared_residuals, beta_initial, args=(X, Y), method='BFGS')
beta_simulated = result.x.reshape(-1, 1)

print(f"OLS by Simulated Least Squares: {beta_simulated}")

# # --- Method 3: OLS by statsmodels ---
model = sm.OLS(Y, X)
results = model.fit()
beta_statsmodels = results.params.reshape(-1, 1)

print(f"OLS by statsmodels: {beta_statsmodels}")

# Convert resuts to Dataframe
ols_coeffs = pd.DataFrame(
    {
        "Variable": ["Intercept", "Sqft", "Retrofit", "Temperature"],
        "OLS by Hand": beta_ols_hand.flatten(),
        "OLS by Simulation": beta_simulated.flatten(),
        "OLS by StatsModels": beta_statsmodels.flatten(),
    }
)

ols_coeffs.to_latex(f"{output_dir}/ols_coefficients.tex", index=False)
