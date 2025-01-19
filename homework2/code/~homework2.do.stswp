* Homework 2

	clear all
	set more off
	
* Set up your working directories	
	local outputpath = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/output/" 
	
	cd "`outputpath'"

* Download and use plotplainblind scheme

	net install schemepack, from("https://raw.githubusercontent.com/asjadnaqvi/stata-schemepack/main/installation/") replace
	set scheme cblind1, permanently

* Import data	
import delimited "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/input/kwh.csv", clear

* Create balance table
eststo retrofit: quietly estpost summarize electricity sqft temp if retrofit == 1
eststo nonretrofit: quietly estpost summarize electricity sqft temp if retrofit == 0
eststo diff: quietly estpost ttest electricity sqft temp, by(retrofit) unequal
esttab nonretrofit retrofit diff using s_balancetab.tex, tex cells(mean(pattern(1 1 0) fmt(2) label(Mean)) sd(pattern(1 1 0) fmt(2) par label(Std. Dev.)) b(star pattern(0 0 1) fmt(3))) mtitles(Control Treatment Difference) label replace


* Create twoway scatter
twoway (scatter electricity sqft)
graph export s_electricity_by_sqft.pdf, replace

* Run OLS regression
reg electricity sqft retrofit temp, robust
outreg2 using s_ols_results.tex, label 2aster tex(frag) dec(2) replace ctitle("Ordinary least squares")


	
	
	