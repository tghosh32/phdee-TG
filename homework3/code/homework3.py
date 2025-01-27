# %% 
# Homework 3

# Importing libraries
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.utils import resample
import matplotlib.pyplot as plt

# %% 
# Setting directories and seed
input_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework3/input'
output_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework3/output'

np.random.seed(6578103)

# %% 
# Reading data
eer_prog = pd.read_csv(os.path.join(input_dir, 'kwh.csv'))
# %%
# Log transformation

eer_prog['ln_electricity'] = np.log(eer_prog['electricity'])
eer_prog['ln_sqft'] = np.log(eer_prog['sqft'])
eer_prog['ln_temp'] = np.log(eer_prog['temp'])

# %%
# Define the model
X = sm.add_constant(eer_prog[['retrofit','ln_sqft', 'ln_temp']])
y = eer_prog['ln_electricity']
model = sm.OLS(y, X)
result = model.fit()

alpha, ln_delta, gamma_sqft, gamma_temp = result.params
# %%
# Marginal effects

eer_prog['dy_dsqft'] = gamma_sqft * eer_prog['electricity'] / eer_prog['sqft']
eer_prog['dy_dtemp'] = gamma_temp * eer_prog['electricity'] / eer_prog['temp']
eer_prog['dy_dretrofit'] = eer_prog['electricity']*(np.exp(ln_delta) - 1) / (np.exp(ln_delta)**eer_prog['retrofit'])

# %%
# Bootstrap

n_bootstraps = 1000
bootstrap_results = []
dy_dsqft_bootstrap = []
dy_dtemp_bootstrap = []
dy_dretrofit_bootstrap = []

for i in range(n_bootstraps):
    bootstrap = resample(eer_prog)
    X_boot = sm.add_constant(bootstrap[['retrofit','ln_sqft', 'ln_temp']])
    y_boot = bootstrap['ln_electricity']
    boot_model = sm.OLS(y_boot, X_boot).fit()
    alpha_boot, ln_delta_boot, gamma_sqft_boot, gamma_temp_boot = boot_model.params
    bootstrap_results.append([alpha_boot, ln_delta_boot, gamma_sqft_boot, gamma_temp_boot])
    bootstrap['dy_dsqft'] = gamma_sqft_boot * bootstrap['electricity'] / bootstrap['sqft']
    bootstrap['dy_dtemp'] = gamma_temp_boot * bootstrap['electricity'] / bootstrap['temp']
    bootstrap['dy_dretrofit'] = bootstrap['electricity']*(np.exp(ln_delta_boot) - 1) / (np.exp(ln_delta_boot)**bootstrap['retrofit'])
    dy_dsqft_bootstrap.append(bootstrap['dy_dsqft'].mean())
    dy_dtemp_bootstrap.append(bootstrap['dy_dtemp'].mean())
    dy_dretrofit_bootstrap.append(bootstrap['dy_dretrofit'].mean())

bootstrap_results = np.array(bootstrap_results)
dy_dsqft_bootstrap = np.array(dy_dsqft_bootstrap)
dy_dtemp_bootstrap = np.array(dy_dtemp_bootstrap)
dy_dretrofit_bootstrap = np.array(dy_dretrofit_bootstrap)

# 95% confidence intervals
results_ci = np.percentile(bootstrap_results, [2.5, 97.5], axis=0)
dy_dsqft_ci = np.percentile(dy_dsqft_bootstrap, [2.5, 97.5])
dy_dtemp_ci = np.percentile(dy_dtemp_bootstrap, [2.5, 97.5])
dy_dretrofit_ci = np.percentile(dy_dretrofit_bootstrap, [2.5, 97.5])

# %%
# Output to LaTeX
variables = ['Constant', 'Retrofit', 'Square feet of home', 'Temperature']
ols_coeffs = [alpha, ln_delta, gamma_sqft, gamma_temp]
marginal_effects = ["", eer_prog['dy_dsqft'].mean(), eer_prog['dy_dtemp'].mean(), eer_prog['dy_dretrofit'].mean()]
confidence_intervals_coeff = [f"[{results_ci[0,0]:.3f}, {results_ci[1,0]:.3f}]",
        f"[{results_ci[0,1]:.3f}, {results_ci[1,1]:.3f}]",
        f"[{results_ci[0,2]:.3f}, {results_ci[1,2]:.3f}]",
        f"[{results_ci[0,3]:.3f}, {results_ci[1,3]:.3f}]"
        ]
confidence_intervals_me = ["",
                           f"[{dy_dsqft_ci[0]:.3f}, {dy_dsqft_ci[1]:.3f}]",
        f"[{dy_dtemp_ci[0]:.3f}, {dy_dtemp_ci[1]:.3f}]",
        f"[{dy_dretrofit_ci[0]:.3f}, {dy_dretrofit_ci[1]:.3f}]"
        ]

rows = []
for var, est, marg_eff, ci_coeff, ci_me in zip(variables, ols_coeffs, marginal_effects, confidence_intervals_coeff, confidence_intervals_me):
    rows.append([var, est, marg_eff])
    rows.append(["", ci_coeff, ""])
    rows.append(["", "", ci_me])

results_df = pd.DataFrame(rows, columns=["Variable [ln(x)]", "OLS Estimate", "Average Marginal Effect"])

results_df.to_latex(os.path.join(output_dir, 'bootstrap_results.tex'), index=False)

# %%
# Plot average marginal effects with error bars

dy_dsqft_avg = np.mean(dy_dsqft_bootstrap)
dy_dtemp_avg = np.mean(dy_dtemp_bootstrap)

plt.plot(['sqft'], [dy_dsqft_avg], 'bo', label="Avg. marginal effect of home size", markersize=5)
plt.errorbar(['sqft'], [dy_dsqft_avg], yerr=[[dy_dsqft_avg - dy_dsqft_ci[0]], [dy_dsqft_ci[1] - dy_dsqft_avg]], fmt='o', color='blue', capsize=10)
plt.fill_between(['sqft'], dy_dsqft_ci[0], dy_dsqft_ci[1], color='blue', alpha=0.3)


plt.plot(['temp'], [dy_dtemp_avg], 'ro', label="Avg. marginal effect of temperature", markersize=5)
plt.errorbar(['temp'], [dy_dtemp_avg], yerr=[[dy_dtemp_avg - dy_dtemp_ci[0]], [dy_dtemp_ci[1] - dy_dtemp_avg]], fmt='o', color='red', capsize=10)
plt.fill_between(['temp'], dy_dtemp_ci[0], dy_dtemp_ci[1], color='red', alpha=0.3)

plt.ylabel("Average Marginal Effect")
plt.xticks(['sqft', 'temp'])
plt.xlim((-0.5,2.5))
plt.savefig(os.path.join(output_dir, 'marginal_effects.pdf'))
plt.show()

# %%
