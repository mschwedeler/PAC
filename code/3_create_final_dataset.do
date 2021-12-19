
global homedir "D:/Users/mschwede/Dropbox/PAC/"
cd "${homedir}"

*--------------------*
* 1) Pac-to-can data *
*--------------------*
use "output/raw_imported/pac2can.dta", clear

*Add committee (PAC) name
ren pacid cmteid
merge m:1 cycle cmteid using "output/raw_imported/cmte.dta"
drop if _merge == 1 // 1 observation; why?
drop if _merge == 2 // legit
drop _merge

*Add candidate name & party
merge m:1 cycle cid using "output/raw_imported/can.dta"
drop if _merge == 1 // 647 obs; no name or party
drop if _merge == 2 // legit
drop _merge

*Add gvkey
merge m:1 ultorg using "output/name_matched/matched_ultorg.dta"
drop if _merge == 1 // 4 obs, all missing ultorg
drop if _merge == 2 // legit, inherited from dropping == 2 above
drop _merge

*Manually adjust some false negatives
replace fuzz = 100 if ultorg == "Foster Wheeler"
replace fuzz = 100 if ultorg == "HJ Heinz Co"
replace fuzz = 100 if ultorg == "Johnson Controls"
replace fuzz = 100 if ultorg == "Marsh & McLennan"
replace fuzz = 100 if ultorg == "Novo Nordisk"
replace fuzz = 100 if ultorg == "Piper Jaffray"
replace fuzz = 100 if ultorg == "AO Smith Corp"
replace fuzz = 100 if ultorg == "Williams Companies"
replace fuzz = 100 if ultorg == "Flagstar Bank"
replace fuzz = 100 if ultorg == "Waddell & Reed"
replace fuzz = 100 if ultorg == "LyondellBasell Industries"

*Apply cutoff (pretty arbitrary; 100 means perfect match)
keep if fuzz > 95
drop fuzz

*Date
ren date date_str
gen date = date(date_str, "MDY")
format date %td
drop date_str

*Sum by firm-party-quarter
gen dateQ = qofd(date)
format dateQ %tq
collapse (sum) amount_pac2can=amount (count) nofrecipients_pac2can=amount, ///
	by(gvkey party dateQ)

compress
save "output/pac2can_quarterly.dta", replace


*--------------------*
* 2) Pac-to-pac data *
*--------------------*
use "output/raw_imported/pac2pac.dta", clear

/*
I think I am implicitly dismissing a few PAC-to-candidate observations that
are in the PAC-to-PAC data set. Why they are in the PAC-to-PAC data in the
first place is not clear to me.
*/

/*
Attention: There is an additional dimension relative to PAC-to-CAN file
since there can be multiple donors for a given fec committee
*/

*Add gvkey
ren donorcmte donor
merge m:1 donor using "output/name_matched/matched_donor.dta"
drop _merge // perfect match, as it should be

*Manually adjust some false negatives
replace fuzz = 100 if donor == "Foster Wheeler"
replace fuzz = 100 if donor == "HJ Heinz Co"
replace fuzz = 100 if donor == "Johnson Controls"
replace fuzz = 100 if donor == "Marsh & McLennan"
replace fuzz = 100 if donor == "Novo Nordisk"
replace fuzz = 100 if donor == "Piper Jaffray"
replace fuzz = 100 if donor == "AO Smith Corp"
replace fuzz = 100 if donor == "Williams Companies"
replace fuzz = 100 if donor == "Flagstar Bank"
replace fuzz = 100 if donor == "Waddell & Reed"
replace fuzz = 100 if donor == "LyondellBasell Industries"

*Apply cutoff (pretty arbitrary; 100 means perfect match)
keep if fuzz > 95
drop fuzz

*Date
ren date date_str
gen date = date(date_str, "MDY")
format date %td
drop date_str

*Sum by firm-party-quarter
gen dateQ = qofd(date)
format dateQ %tq
collapse (sum) amount_pac2pac=amount (count) nofrecipients_pac2pac=amount, ///
	by(gvkey party dateQ)

compress
save "output/pac2pac_quarterly.dta", replace


*-------------------------------------------------------*
* 3) Collect everything and create additional variables *
*-------------------------------------------------------*
*Merge
use "output/pac2can_quarterly.dta", clear
merge 1:1 gvkey party dateQ using "output/pac2pac_quarterly.dta"
drop _merge

*Party total
sort gvkey dateQ
foreach v of varlist amount_* nofrecipients_* {
	by gvkey dateQ: egen `v'TOTAL = sum(`v')
}

*Keep if party is Democratic or Republican
keep if inlist(party, "D", "R")
replace party = "DEM" if party == "D"
replace party = "REP" if party == "R"

*Reshape wide
reshape wide amount_pac2can amount_pac2pac nofrecipients_pac2can ///
	nofrecipients_pac2pac, i(gvkey dateQ) j(party) string

*Label
foreach a in amount nofrecipients {
	foreach b in pac2can pac2pac {
		foreach c in "DEM" "REP" "TOTAL" {
			if "`c'" == "DEM" {
				local party "democratic party"
			}
			else if "`c'" == "REP" {
				local party "republican party"
			}
			else if "`c'" == "TOTAL" {
				local party "all parties (incl indep)"
			}
			la var `a'_`b'`c' `"Donation `a', `b', `party'"'
		}
	}
}

// OPTIONALLY: Replace missing by zero. Huge assumption though.

*Make gvkey string
tostring gvkey, replace
replace gvkey = "0" + gvkey if length(gvkey) == 5
replace gvkey = "00" + gvkey if length(gvkey) == 6

sort gvkey dateQ
save "output/all_quarterly.dta", replace
