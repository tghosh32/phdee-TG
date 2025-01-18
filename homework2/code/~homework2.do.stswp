* Homework 2

	clear all
	set more off
	
* Set up your working directories

	local datapath = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/input"	
	local outputpath = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework2/output/" 
	
	cd "`datapath'"

* Download and use plotplainblind scheme

	net install schemepack, from("https://raw.githubusercontent.com/asjadnaqvi/stata-schemepack/main/installation/") replace
	set scheme cblind1, permanently

* Import data	
import delimited "kwh.csv", clear

* Treatment and control groups
gen treatment = (retrofit == 1)

estto summary: estpost su sqft temp electricty


	
	
