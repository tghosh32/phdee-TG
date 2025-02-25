# %% 
# Homework 6

# Importing libraries
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IVGMM

# %% 
# Setting directories and seed
input_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework6/input'
output_dir = r'/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework6/output'

# %%
# Reading data
carsales = pd.read_csv(os.path.join(input_dir, 'instrumentalvehicles.csv'))

# %%
# OLS
X = sm.add_constant(carsales[['mpg', 'car']])
y = carsales['price']
model = sm.OLS(y, X)
result = model.fit()
print(result.summary())

# %%
# IV by hand
carsales['$weight^2$'] = carsales['weight']**2
instruments = ['weight', '$weight^2$', 'height']
def run_2sls(carsales, instrument):
    results = {}

    for instrument in instruments:
        # First stage: Regression: mpg ~ instrument + car
        X1 = sm.add_constant(carsales[[instrument, 'car']])
        y1 = carsales['mpg']
        first_stage = sm.OLS(y1, X1).fit()
        mpg_hat_col = f"mpg_hat_{instrument}"
        carsales[mpg_hat_col] = first_stage.fittedvalues

        # Second stage: Regression: price ~ mpg_hat + car
        X2 = sm.add_constant(carsales[[mpg_hat_col, 'car']])
        y2 = carsales['price']
        second_stage = sm.OLS(y2, X2).fit()

        # First stage F-statistic
        f_stat = first_stage.f_test(f"{instrument} = 0").fvalue

        # Save results
        results[instrument] = [
            f"{second_stage.params[mpg_hat_col]:.2f}",
            f"({second_stage.bse[mpg_hat_col]:.2f})",
            f"{second_stage.params['car']:.2f}",
            f"({second_stage.bse['car']:.2f})",
            f"{f_stat:.2f}",
            ""
        ]

        row_names = ["$\\hat{mpg}$", "", "$Car$", "", "$F$-stat", ""]

        # Create results DataFrame
        results_df = pd.DataFrame(results, index=row_names)
        latex_table = results_df.to_latex(index=True, escape=False)
        output_path = os.path.join(output_dir, "IV_byhand.tex")
        with open(output_path, "w") as f:
            f.write(latex_table)

        print(f"LaTeX table saved to {output_path}")
   

run_2sls(carsales, instruments)

# %%
# IV GMM
iv_gmm_model = IVGMM.from_formula('price ~ 1 + car + [mpg ~ weight]', data=carsales).fit()
results = [
    f"{iv_gmm_model.params['car']:.2f}",
    f"({iv_gmm_model.std_errors['car']:.2f})",
    f"{iv_gmm_model.params['mpg']:.2f}",
    f"({iv_gmm_model.std_errors['mpg']:.2f})",
    ""
]

results_df = pd.DataFrame(results, index=["$Car$", "", "$Mpg$", "", ""])
results_df.columns = ["Weight"]
latex_table = results_df.to_latex(index=True, escape=False)
output_path = os.path.join(output_dir, "IV_GMM.tex")
with open(output_path, "w") as f:
    f.write(latex_table)


# %%
