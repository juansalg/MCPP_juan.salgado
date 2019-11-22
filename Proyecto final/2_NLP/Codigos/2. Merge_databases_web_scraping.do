	clear all
	set more off

	
*** Defining paths

	global user "srjc2"
	global bases_path "C:\Users\\$user\OneDrive\Documentos\GitHub\MCPP_juan.salgado\Proyecto final\2_NLP"
	local bases_name "Conteo_variable_final"
	

* ---> Loop over different years and merge databases

local base_num = 1

while `base_num' < 7{

	import excel "$bases_path\\`bases_name'`base_num'.xlsx", firstrow clear
	
	save "$bases_path\\tmp_`bases_name'`base_num'.dta", replace
	
	local base_num = `base_num' + 1
}


local base_num = 1

while `base_num' < 7{

	if `base_num' == 1{
		use "$bases_path\\tmp_`bases_name'`base_num'.dta", clear
	}
	
	else{
		merge 1:1 Link using "$bases_path\\tmp_`bases_name'`base_num'.dta", nogenerate
	}
	
	local base_num = `base_num' + 1
}

drop A
order Link Anio Mes

export excel "$bases_path\\merge_bases.xlsx", firstrow(variables) replace

* ---> Eliminate tmp databases

cd "$bases_path"

local list : dir . files "*tmp*"
foreach f of local list {
erase "`f'"
}
