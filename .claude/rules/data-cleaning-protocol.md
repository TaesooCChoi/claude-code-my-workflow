# Data Cleaning Protocol

**This is the canonical workflow Claude must follow for all data cleaning tasks.**

Cleaning is the highest-stakes step: errors here propagate silently into every downstream analysis. Be slow and systematic.

---

## The Five Phases

```
raw data
  │
  Phase 1: INVENTORY    — understand what you have
  │
  Phase 2: PROFILE      — diagnose quality issues
  │
  Phase 3: CLEAN        — apply documented fixes
  │
  Phase 4: VALIDATE     — verify the cleaned output
  │
  Phase 5: DOCUMENT     — write the cleaning log
  │
clean data
```

---

## Phase 1: Inventory

Before writing a single line of cleaning code, run:

```stata
* In Stata
use "data/raw/[file.dta]", clear
describe
codebook, compact
notes _dta
label list
```

```r
# In R
library(haven)
df <- read_dta("data/raw/file.dta")
skimr::skim(df)
attributes(df)       # variable labels
lapply(df, attr, "label")  # column labels
```

**Deliverable:** A written inventory comment at the top of the cleaning script:
```stata
* INVENTORY:
* N = [obs count], K = [variable count]
* Key identifiers: [list them]
* Time dimension: [year range, wave, etc.]
* Known issues from codebook: [list any flagged values]
```

---

## Phase 2: Profile

Systematically check every variable that will be used:

### Stata profiling checklist:
```stata
* 1. Duplicates on key identifiers
duplicates report id_var
duplicates tag id_var, gen(dup_flag)
tab dup_flag

* 2. Missing rates on all key variables
foreach var of varlist * {
    qui count if missing(`var')
    if r(N) > 0 di "`var': " r(N) " missing (" %4.1f r(N)/_N*100 "%)"
}

* 3. Out-of-range values
sum outcome_var, detail
* Flag implausible values:
tab outcome_var if outcome_var < 0    // check negatives
tab outcome_var if outcome_var > [expected_max]

* 4. Inconsistency checks
assert age >= 0 & age <= 120 if !missing(age)
assert income >= 0 if employed == 1   // income logic
```

**Deliverable:** Note every problem found. Do NOT fix yet — profile completely first.

---

## Phase 3: Clean

Apply fixes in this order:

1. **Identifiers first** — deduplicate or resolve duplicates before anything else
2. **Recode missings** — apply extended missing codes with documentation
3. **Fix values** — recode out-of-range, typos, inconsistencies
4. **Construct variables** — build derived variables from cleaned inputs
5. **Merge** — always last, after all source datasets are individually clean

**Each fix must have a comment explaining WHY:**
```stata
* Negative income recorded as -99 in waves 1-3; confirmed with codebook p.47
replace income = . if income == -99 & wave <= 3

* Duplicate IDs in 2012: two observations per household due to survey re-contact
* Keep the one with more complete data (fewest missings)
egen nmiss = rowmiss(income education health)
bysort id wave: keep if nmiss == min(nmiss)
drop nmiss
```

**Never batch-fix without inspection:**
```stata
* BAD — no inspection:
replace income = 0 if missing(income)

* GOOD — inspect first, then fix with justification:
tab income if missing(income)  // how many? which subgroups?
* Decision: [explain here]
replace income = .a if missing(income) & employed == 0  // not applicable
```

---

## Phase 4: Validate

After cleaning, verify the output satisfies all invariants:

```stata
* 1. Key identifier is unique in the cleaned dataset
isid id_var [year_var]

* 2. No unlabeled variables remain
foreach var of varlist * {
    local lbl : variable label `var'
    if "`lbl'" == "" di "WARNING: `var' has no label"
}

* 3. All expected observations present
count
assert _N == [expected_N_after_cleaning]

* 4. Value ranges make sense
assert income >= 0 | missing(income)
assert age >= 18 & age <= 85 if !missing(age)   // if adult sample

* 5. Merge rates logged
* (Run each merge with -tab _merge- before dropping)

* 6. Cross-tabulations for sanity
tab treated year       // treatment onset makes sense
tab state if missing(income)  // geographic pattern of missings?
```

---

## Phase 5: Document

Every cleaning script ends with a **Cleaning Log** — a block comment recording:

```stata
* ============================================================
* CLEANING LOG
* ============================================================
* Input:  data/raw/[file.dta]   N=[N_raw], K=[K_raw]
* Output: data/clean/[file.dta] N=[N_clean], K=[K_clean]
*
* Key decisions:
* 1. [Decision 1 — what was done and why]
* 2. [Decision 2]
* ...
*
* Data loss:
* - Dropped [N] obs: [reason]
* - Dropped [N] obs: [reason]
*
* Merge rates:
* - [file_A] merge [file_B]: matched=[%], master-only=[%], using-only=[%]
*
* Known issues (unresolved):
* - [Issue 1 — what it is and why it's left as-is]
* ============================================================
```

---

## Definition of "Clean"

A dataset is considered **clean** when ALL of the following hold:

- [ ] Every variable has a `label variable` statement
- [ ] Every categorical variable has `label values`
- [ ] Every constructed variable has a `note` citing the source formula/codebook
- [ ] No unlabeled system missings (`.`) without explanation
- [ ] Extended missings (`.a`, `.b`, `.c`) used consistently with documented scheme
- [ ] Key identifiers are unique (confirmed by `isid`)
- [ ] Merge rates documented (no silent drops)
- [ ] Script runs top-to-bottom without errors in a clean Stata session
- [ ] Cleaning Log block present at end of script

---

## Single Source of Truth for Data

| Layer | Format | Rule |
|-------|--------|------|
| Raw data | `data/raw/*.dta` | **Never modified** — read only |
| Clean data | `data/clean/*.dta` | Output of cleaning `.do` files |
| Analysis data | `data/clean/*.rds` or `.dta` | May be a subset/reshape of clean |
| Figures | `output/figures/` | Derived from R scripts |
| Tables | `output/tables/` | Derived from Stata or R |

No analysis script should load from `data/raw/` directly — always from `data/clean/`.
