
* Paths
global dt = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework8"
global in = "$dt/input/"
global out = "$dt/output/" 

* Read data
use "${in}recycling_hw.dta", clear

* Recycling rate for NYC vs Controls
bysort year: egen avg_rr_nyc = mean(recyclingrate) if nyc == 1
bysort year: egen avg_rr_control = mean(recyclingrate) if nyc == 0

twoway connected avg_rr_nyc avg_rr_control year, legend(label(1 "NYC") label(2 "Controls")) ///
		ytitle("Recycling Rate") ///
        xtitle("Year") ///
		xline(2002 2004) ///
		legend(order(1 "NYC" 2 "Controls") ring(0) pos(1))
		
graph export "${out}parallel_trends.png", replace

* TWFE
preserve

keep if year >= 1997 & year <= 2004

xtset id year

gen post_pause = year >= 2002
gen treated = nyc
gen treatment = post_pause * treated

reghdfe recyclingrate treatment, absorb(id year) vce(cluster id)

* Synthetic DID

// ssc install sdid
sdid recyclingrate id year treatment, vce(bootstrap) seed(1000) graph 
graph export "${out}sdid.png", replace

restore

* Event Study

xtset id year

gen l = year
replace l = . if year == 2001

gen treatment = 0
replace treatment = 1 if l>=2002 & nyc==1

eststo reg1: reg recyclingrate treatment incomepercapita nonwhite i.id i.year, vce(cluster id)
eststo reg2: xtreg recyclingrate treatment incomepercapita nonwhite i.year ,fe vce(cluster id)
eststo reg3: reghdfe recyclingrate treatment incomepercapita nonwhite, absorb(id year) vce(cluster id)

coefplot (reg1 reg2 reg3), ///
vertical keep (recyclingrate treatment incomepercapita nonwhite) aseq swapnames coeflabels(reg1 = "reg" reg2 = "xtreg" reg3 = "reghdfe") ytitle(Coefficient) 
graph export "${out}event_study.png", replace

* Synthetic Control
tsset id year

replace id =0 if nyc == 1
collapse nyc nj ma recyclingrate fips collegedegree2000 incomepercapita munipop2000 democratvoteshare2000 democratvoteshare2004 nonwhite, by(year id)

/// net install synth_runner, from("https://raw.githubusercontent.com/bquistorff/synth_runner/master")
synth_runner recyclingrate incomepercapita nonwhite munipop2000, trunit(0) trperiod(2002) gen_vars

single_treatment_graphs, do_color(green) treated_name("NYC") donors_name("All Other Regions") raw_options(xtitle("Year") ytitle("Recycling Rate")) effects_options(xtitle("Year") ytitle("Change in Recycling Rate"))
graph export "${out}5a.png", name(raw) replace

effect_graphs, treated_name("NYC") tc_options(xtitle("Year") ytitle("Recycling Rate")) effect_options(xtitle("Year") ytitle("Change in Recycling Rate")) 
graph export "${out}5b.png", replace
graph export "${out}5d.png", name("effect") replace


pval_graphs
graph export "${out}5c.png", name("pvals") replace































































		
		