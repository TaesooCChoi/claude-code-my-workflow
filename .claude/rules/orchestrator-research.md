---
paths:
  - "scripts/**/*.do"
  - "scripts/**/*.R"
  - "data/**"
  - "explorations/**"
---

# Research Project Orchestrator (Simplified)

**For Stata data work, R analysis, and figures** — use this simplified loop instead of the full multi-agent orchestrator.

## The Simple Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run code, check outputs
  │         Stata: do-file runs without error, log saved
  │         R: Rscript runs without error, output files created
  │         Figures: PDF/PNG created, correct dimensions
  │         Data: isid passes, no unlabeled vars
  │         If verification fails → fix → re-verify
  │
  Step 3: SCORE — Apply quality-gates rubric
  │
  └── Score >= 80?
        YES → Done (commit when user signals)
        NO  → Fix blocking issues, re-verify, re-score
```

**No 5-round loops. No multi-agent reviews. Just: write, test, done.**

## Verification Checklist

### For Stata (.do files)
- [ ] Do-file runs top-to-bottom without errors in a clean session
- [ ] Log file created and closed
- [ ] No hardcoded absolute paths
- [ ] `isid` passes on key identifier(s)
- [ ] `_merge` inspected and dropped after every merge
- [ ] All variables labeled
- [ ] Output saved to `output/tables/` or `data/clean/`
- [ ] Cleaning Log present at end of script

### For R (.R files)
- [ ] `Rscript scripts/R/filename.R` runs without errors
- [ ] All packages loaded at top via `library()`
- [ ] `set.seed()` once at top if stochastic
- [ ] No hardcoded absolute paths
- [ ] Output files created at expected paths (`output/figures/`, `output/tables/`)
- [ ] Figures: correct dimensions, dpi = 300

### General
- [ ] Output files created with non-zero size
- [ ] Estimates are plausible in magnitude and sign
- [ ] Quality score >= 80
