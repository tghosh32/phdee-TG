* Homework 4

	clear all
	set more off
	
if "`c(username)'"== "tannishthaghosh" {                              
		global dt "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG"
		global in "$dt/homework4/input"
		global out "$dt/homework4/output"  
	}
	
* Load data
import delimited "$in/fishbycatch.csv", varnames(1)

* Reshape panel data
reshape long shrimp salmon bycatch, i(firm) j(month)


gen year = 2017 if inrange(month, 1, 24)
replace year = 2018 if !inrange(month, 1, 12)

gen post = (year >= 2018) // Post treatment indicator

gen treated_post = treated * post // Post treatment indicator based on firm assignment

gen time_fe = month // Indicator for each month

* Run OLS with firm and time fixed effects
reg bycatch treated_post shrimp salmon i.firm i.month, vce(cluster firm)
est store ols_fe

* Compute firm-level means
egen mean_bycatch = mean(bycatch), by(firm)
egen mean_treated_post = mean(treated_post), by(firm)
egen mean_shrimp = mean(shrimp), by(firm)
egen mean_salmon = mean(salmon), by(firm)

* Compute within-transformed (demeaned) variables
gen bycatch_within = bycatch - mean_bycatch
gen treated_post_within = treated_post - mean_treated_post
gen shrimp_within = shrimp - mean_shrimp
gen salmon_within = salmon - mean_salmon

* Run OLS on demeaned variables
reg bycatch_within treated_post_within shrimp_within salmon_within i.month, vce(cluster firm)
est store within_transformation

label var treated_post "Treatment x Post"
label var shrimp "Shrimp"
label var salmon "Salmon"
	
label var treated_post_within "Treatment x Post (mean)"
label var shrimp_within "Shrimp (mean)"
label var salmon_within "Salmon (mean)"
	
outreg2 [ols_fe within_transformation] using "$out/reg_output_stata.tex", ///
keep(treated_post shrimp salmon treated_post_within shrimp_within salmon_within) ///
tex(frag) replace label se nocons nonotes ///
ctitle("OLS Fixed Effects", "Within-Transformation")


