# %% 
# Homework 7

# Importing libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.iolib.summary2 as sm_summary
import statsmodels.formula.api as smf
from linearmodels.iv import IVGMM

# %% 
# Setting directories and seed
input_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework7/input'
output_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework7/output'

# %%
# Reading data
carsales = pd.read_csv(os.path.join(input_dir, 'instrumentalvehicles.csv'))

# %%
# RD Scatterplot
cutoff = 225
carsales['length_minus_cutoff'] = carsales['length'] - cutoff

plt.scatter(carsales['length_minus_cutoff'], carsales['mpg'], alpha=0.5, label='Vehicles')
plt.axvline(x=0, color='red', linestyle='--', label='RD Cutoff (225 inches)')
plt.xlabel('Length - Cutoff (inches)')
plt.ylabel('Miles Per Gallon (MPG)')
plt.legend()
plot_path = os.path.join(output_dir, "rd_scatter_plot.png")
plt.savefig(plot_path, dpi=300)
plt.show()

# %%
# Fit RD Models

def fit_plot_rd(data, order, ax):
    data = data.copy()
    data['treatment'] = (data['length'] >= cutoff).astype(int)
    
    # Create polynomial features separately for both sides of the cutoff
    for i in range(1, order + 1):
        data[f'poly_{i}'] = data['length_minus_cutoff'] ** i
    
    # Fit regression model
    X = data[['treatment'] + [f'poly_{i}' for i in range(1, order + 1)]]
    X = sm.add_constant(X)
    y = data['mpg']
    model = sm.OLS(y, X).fit()
    
    # Generate predictions
    x_range = np.linspace(data['length_minus_cutoff'].min(), data['length_minus_cutoff'].max(), 100)
    x_data = pd.DataFrame({'length_minus_cutoff': x_range})
    x_data['treatment'] = (x_data['length_minus_cutoff'] >= 0).astype(int)
    for i in range(1, order + 1):
        x_data[f'poly_{i}'] = x_data['length_minus_cutoff'] ** i
    X_pred = sm.add_constant(x_data[['treatment'] + [f'poly_{i}' for i in range(1, order + 1)]])
    y_pred = model.predict(X_pred)
    
    # Plot scatterplot and fitted line
    ax.scatter(data['length_minus_cutoff'], data['mpg'], alpha=0.5, label='Vehicles')
    ax.plot(x_range, y_pred, color='red', label=f'Order {order} Polynomial')
    ax.axvline(x=0, color='black', linestyle='--', label='RD Cutoff')
    ax.set_xlabel('Length - Cutoff (inches)')
    ax.set_ylabel('Miles Per Gallon (MPG)')
    ax.set_title(f'RD with {order}-Order Polynomial')
    ax.legend()
    
    return model

# Fit models and generate plots
fig, axes = plt.subplots(3, 1, figsize=(6, 18))
orders = [1, 2, 5]
models = []

for i, order in enumerate(orders):
    model = fit_plot_rd(carsales, order, axes[i])
    models.append(model)
    fig.savefig(os.path.join(output_dir, f'rd_plot_order_{order}.png'))

plt.show()

# Create LaTeX table
coef_table = pd.DataFrame()

for i, model in enumerate(models):
    summary = model.summary2().tables[1]  # Extract coefficient table
    coef_table[f'Order {orders[i]}'] = summary.loc['treatment', ['Coef.', 'Std.Err.']]

# Format LaTeX table
coef_table = coef_table.T
coef_table.columns = ['Estimate', 'Standard Error']
latex_table = coef_table.to_latex(float_format="%.3f", index=True, column_format='lcc')

# Save LaTeX table
with open(os.path.join(output_dir, 'rd_estimates.tex'), 'w') as f:
    f.write(latex_table)

# %%
# 2sls using discontinuity as instrument
carsales["treatment"] = (carsales["length"] > cutoff).astype(int)
carsales["length_minus_cutoff_sq"] = carsales["length_minus_cutoff"] ** 2

# First stage: Predicting MPG using RD design
first_stage = smf.ols("mpg ~ treatment + length_minus_cutoff + car", data=carsales).fit()

# Get fitted values (instrumented mpg)
carsales["mpg_hat"] = first_stage.fittedvalues

# Second stage: Estimating price using instrumented MPG
second_stage = smf.ols("price ~ mpg_hat + car", data=carsales).fit()

print(second_stage.params["mpg_hat"])

# %%
