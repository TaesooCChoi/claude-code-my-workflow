---
paths:
  - "**/*.do"
  - "scripts/stata/**"
---

# Stata Code Standards

**Standard:** Senior applied econometrician quality — rigorous, reproducible, auditable.

---

## 1. File Structure

Every `.do` file must open with:

```stata
* ============================================================
* Project:  [PROJECT NAME]
* Script:   [filename.do]
* Purpose:  [one-line description]
* Input:    [input dataset(s)]
* Output:   [output dataset(s) and/or tables]
* Author:   [name]
* Created:  [YYYY-MM-DD]
* Modified: [YYYY-MM-DD]
* ============================================================

version 17          // pin Stata version for reproducibility
set more off
clear all
capture log close
log using "logs/[filename].log", replace text
```

---

## 2. Raw Data is Sacred

- **Never modify files in `data/raw/`** — treat as read-only
- Always work on a copy: load from `data/raw/`, save to `data/clean/` or `data/temp/`
- First line that touches data must assert raw data integrity:
  ```stata
  use "data/raw/[file.dta]", clear
  * Verify expected obs count and key variables exist
  assert _N == [expected_N]  // update if known
  ```

---

## 3. Merge Safety (Non-Negotiable)

**Every merge must be followed by:**

```stata
merge 1:1 id using "data/clean/other.dta"
* ALWAYS inspect before dropping:
tab _merge
assert _merge == 3 if [condition]  // document exceptions
drop _merge
```

**Forbidden pattern** — never write without explanation:
```stata
drop if _merge != 3   // NEVER without documented justification
keep if _merge == 3   // NEVER without documented justification
```

**Acceptable pattern** — with explicit documentation:
```stata
* Unmatched from master: [explain why expected, e.g., "treated units only in 2010+"]
* Unmatched from using:  [explain why expected, e.g., "some counties not in CPS"]
keep if inlist(_merge, 1, 3)
drop _merge
```

**Assert merge type before merging:**
```stata
isid id_var          // confirm unique key in master
isid id_var using "data/clean/other.dta"  // confirm unique key in using
merge 1:1 id_var using "data/clean/other.dta"
```

---

## 4. Missing Values

- Distinguish **system missing** (`.`) from **extended missing** (`.a`, `.b`, `.c`)
- Use extended missings to document *why* a value is missing:
  - `.a` = not applicable (e.g., income for non-workers)
  - `.b` = refused / suppressed
  - `.c` = not yet observed (future period)
- Document the scheme at the top of every cleaning script
- **Never** recode extended missing to 0 without a `note` or comment

```stata
* Missing value scheme (document in every cleaning do-file):
* .  = system missing (unknown reason)
* .a = not applicable
* .b = suppressed/confidential
* .c = not collected in this wave
```

---

## 5. Variable Labels and Notes

**Every variable in a cleaned dataset must have:**

1. A `label variable` statement
2. A `label values` statement (for categorical variables)
3. A source note for constructed variables

```stata
label variable income_real "Real household income (2010 USD)"
label define employed_lbl 0 "Not employed" 1 "Employed"
label values employed employed_lbl

note income_real: "Deflated using CPI-U from BLS (series CUUR0000SA0)"
note income_real: "Source: PSID wave 2010-2020, variable V[XXXX]"
```

---

## 6. `preserve` / `restore`

Use `preserve/restore` for temporary transformations — never destructive edits mid-script:

```stata
preserve
  * temporary reshaping or collapse for a check
  collapse (mean) outcome, by(group year)
  list
restore
```

---

## 7. Assertions Throughout

Add `assert` statements at every critical checkpoint:

```stata
* No negative income after cleaning
assert income >= 0 if !missing(income)

* Treatment and control are mutually exclusive
assert treated + control == 1

* Panel is balanced after reshape
bysort id: assert _N == [num_periods]
```

---

## 8. Output Conventions

```stata
* Tables → output/tables/ (use outreg2, estout, or esttab)
esttab using "output/tables/table1_summary.csv", replace

* Figures → output/figures/ (use graph export)
graph export "output/figures/fig1_trends.pdf", replace

* Log every operation that produces output:
di "Saved table1_summary.csv"
```

---

## 9. Forbidden Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `drop if _merge != 3` (without comment) | Silent data loss | Add documented justification |
| `egen x = ... if group==1` | Subtle if-condition bugs | Use `by group: egen x = ...` |
| Hardcoded absolute paths (`/Users/...`) | Breaks on other machines | Use relative paths from root |
| `capture quietly` swallowing errors | Hides real problems | Use `capture` only for known non-fatal errors |
| `replace x = 0 if missing(x)` (without note) | Conflates 0 and missing | Add source note or use extended missing |

---

## 10. Code Quality Checklist

```
[ ] File header present (purpose, inputs, outputs, date)
[ ] version statement pinned
[ ] log using at top
[ ] Raw data loaded from data/raw/ only
[ ] Every merge followed by tab _merge + inspection
[ ] Extended missings used and documented
[ ] All variables labeled (label variable + label values)
[ ] assert statements at key checkpoints
[ ] preserve/restore for temporary transformations
[ ] All paths relative to project root
[ ] Output saved to output/tables/ or output/figures/
[ ] log close at end
```
