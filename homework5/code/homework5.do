
* Paths
global dt = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework5/"
global in = "$dt/input/"
global out = "$dt/output/" 

* Read data
use "${in}energy_staggered.dta", clear

* convert datetime from string to timestamp
gen double timevar = clock(datetime, "MDYhms")
format timevar %tc
sort timevar
egen hour_count = group(timevar)


* treatment cohort variable
bysort id (timevar): egen cohort = min(timevar) if treatment == 1  // Identify first treatment time
bysort id (cohort): replace cohort = cohort[1] if missing(cohort)
format cohort %tc

egen treatment_cohort = group(cohort)  // Assign each cohort a numeric group
codebook treatment_cohort

*
//ssc install twowayfeweights, replace
twowayfeweights energy treatment_cohort hour_count treatment, type(feTR)

*
eststo hour: reghdfe energy treatment temperature precipitation relativehumidity, absorb(id hour_count) cluster(id)
esttab hour using "${out}hourly_results.tex", replace tex label ///
    se star(* 0.1 ** 0.05 *** 0.01)
	
* Daily date variable
gen day = dofc(timevar) 
format day %td 

* Collapse data to daily level
collapse (mean) temperature relativehumidity precipitation ///
         (sum) energy (max) treatment, ///
		 by(id day)

* Day number
sort day
egen day_count = group(day)

egen first_treat_day=csgvar(treatment), ivar(id) tvar(day)

*
eststo daily: reghdfe energy treatment temperature precipitation relativehumidity, absorb(day id) vce(cluster id)	
esttab daily using "${out}daily_results.tex", ///
varlabels(treatment "Treatment" ///
temperature "Temperature" ///
precipitation "Precipitation" ///
relativehumidity "Relative Humidity" ///
_cons "Constant") replace ///
    se star(* 0.1 ** 0.05 *** 0.01)
	
* Time-to-treatment variable
gen event = day - first_treat_day
* Make dummies for period and omit -1 period
	char event[omit] -1
	xi i.event, pref(_T)
	
* Event study
reghdfe energy  _T* temperature precipitation relativehumidity, absorb(id) vce(cluster id)
estimates store event1
coefplot event1, drop(_cons precipitation relativehumidity temperature) xlabel(1 "-30" 2 "-29" 3 "-28" 4 "-27" 5 "-26" 6 "-25" 7 "-24" 8 "-23" 9 "-22" 10 "-21" 11 "-20" 12 "-19"  13 "-18" 14 "-17" 15 "-16" 16 "-15" 17 "-14" 18 "-13" 19 "-12" 20 "-11" 21 "-10" 22 "-9" 23 "-8" 24 "-7" 25 "-6" 26 "-5" 27 "-4" 28 "-3" 29 "-2" 30 "0" 31 "1" 32 "2" 33 "3" 34 "4" 35 "5" 36 "6" 37 "7" 38 "8" 39 "9" 40 "10" 41 "11" 42 "12" 43 "13" 44 "14" 45 "15" 46 "16" 47 "17" 48 "18" 49 "19" 50 "20" 51 "21" 52 "22" 53 "23" 54 "24" 55 "25" 56 "26" 57 "27" 58 "28" 59 "29" 60 "30" , alternate labsize(*0.7))  vertical xline(29) recast(scatter) xtitle("Hours") ytitle("Energy Consumption") 

graph export "${out}event_study.png", replace

	
///ssc install eventdd, replace
///ssc install matsort, replace
eventdd energy temperature precipitation relativehumidity, hdfe absorb(id) timevar(event) cluster(id) graph_op(ytitle("Daily energy consumption (kWh)", size(3)) xlabel(-30(5)30) xtitle("Days to treatment", size(3)))
graph export "${out}event_study_2.png", replace

//ssc install csdid, replace
//ssc install drdid, replace
csdid energy temperature relativehumidity precipitation, ivar(id) time(day) gvar(treated_day) method(dripw) wboot reps(50)
estat simple
estat event
csdid_plot, ytitle("Daily energy consumption (kWh)", size(3)) xlabel(-30(5)30) xtitle("Days to treatment", size(3)) xline(-.5, lcolor(red))	
graph export "${out}event_study_3.png", replace


















