---
paths:
  - "scripts/**/*.do"
  - "scripts/**/*.R"
  - "data/**"
  - "output/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

---

## For Stata Do-Files

1. Run the do-file in a clean session: `stata -b do scripts/stata/[file.do]` (batch mode)
2. Check the log: scan for `r(error)`, `r(198)`, or any error exit
3. Confirm output files exist with non-zero size:
   - `data/clean/[output.dta]` if data cleaning
   - `output/tables/[table.csv]` if producing tables
4. Run the final invariant checks:
   - `isid [key_vars]` — dataset uniqueness
   - `tab _merge` check documented
5. Spot-check key variables: `sum income age, detail` — are ranges sensible?
6. Report: N obs in, N obs out, merge rates

## For R Scripts

1. Run: `Rscript scripts/R/[file.R]`
2. Confirm exit code 0 (no errors)
3. Confirm output files created at expected paths
4. Spot-check estimates for reasonable magnitude and sign
5. Open one figure to verify visual quality (not blank, correct axis labels)

## For Figures (both Stata and R)

1. File created at `output/figures/[name.pdf]` or `.png`
2. Non-zero file size
3. Read the file to confirm it is a valid image (not an empty/corrupt render)
4. Check: axis labels present, legend readable, no clipping

## For Merged/Joined Datasets

1. `tab _merge` was documented in the script (not silently dropped)
2. Match rate is reasonable (document if < 90%)
3. `isid` passes on final output
4. N-obs change from merge is explained in the cleaning log

## Common Pitfalls

- **Silent Stata errors:** `quietly` can swallow errors — always check the log
- **R warnings ≠ success:** Check for `NA` values in key output columns
- **Phantom output:** File exists from a previous run; check modification timestamp
- **`_merge` never inspected:** Failure to tab _merge before dropping is a blocking issue

## Verification Checklist

```
[ ] Script ran without errors (checked log or exit code)
[ ] Output files exist and are non-empty
[ ] Key identifier uniqueness confirmed (isid)
[ ] Merge rates documented
[ ] Estimates / ranges are plausible
[ ] Figures: saved, non-blank, labels readable
[ ] Reported results summary to user
```
