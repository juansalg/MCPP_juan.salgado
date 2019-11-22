	clear all
	set more off

	
*** Defining paths

	global user "srjc2"
	global bases_path "C:\Users\\$user\OneDrive\Documentos\GitHub\MCPP_juan.salgado\Proyecto final\0_Base_consolidada\Bases crimen"

	

* ---> Clean each database

* Homicidios

use "$bases_path\homic_consolidado.dta", clear

keep if cod_DANE == 11001

g Año = year(Fecha)

drop Fecha

bysort Año cod_DANE: egen total_homicidios = total(Cantidad)

drop Cantidad

duplicates drop

export excel "$bases_path\homicidios.xlsx", firstrow(variables) replace


* Hurto

use "$bases_path\hurto_pers_consolidado.dta", clear

keep if codmpio == 11001

g Año = year(date)

drop date base_name

bysort Año codmpio: egen total_hurtos = total(Total_hurto_personas)

drop Total_hurto_personas

duplicates drop

export excel "$bases_path\hurto.xlsx", firstrow(variables) replace
