* Paths
global dt = "/Users/tannishthaghosh/GaTech Dropbox/Tannishtha Ghosh/EE/phdee-TG/homework6/"
global in = "$dt/input/"
global out = "$dt/output/" 

* Read data
import delimited "${in}instrumentalvehicles.csv", clear

* Limited information MLE
ivregress liml price car (mpg = weight), vce(robust)
outreg2 using "${out}IV_LIML.tex", tex(frag) replace

// ssc install weakivtest
// ssc install avar
weakivtest
