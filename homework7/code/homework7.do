* Paths
global dt = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework7/"
global in = "$dt/input/"
global out = "$dt/output/" 

* Read data
import delimited "${in}instrumentalvehicles.csv", clear

* First stage
rdrobust mpg length, c(225) bwselect(mserd)

* Second stage
gen treatment = (length>=225)
ivregress 2sls price car ( mpg= i.treatment), vce(robust)
outreg2 using "${out}rd_2SLS.tex", label tex(frag) replace

* RD plot
rdplot mpg length, c(225) binselect(qspr) cov(car)
graph export "${out}rdplot_stata.pdf", replace

