---
paths:
  - "scripts/**/*.do"
  - "scripts/**/*.R"
  - "data/**"
  - "output/**"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** — good enough to save
- **90/100 = Ready for analysis** — clean data or script suitable for downstream use
- **95/100 = Excellence** — aspirational; publication-ready

## Data Cleaning Scripts (.do files)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Script errors out (any `r(error)`) | -100 |
| Critical | `_merge` dropped without inspection or comment | -25 |
| Critical | Raw data modified in place | -25 |
| Critical | `isid` fails on final dataset | -20 |
| Major | Unlabeled variables in output dataset | -5 per variable (max -20) |
| Major | Extended missing not used for known non-applicable values | -10 |
| Major | No cleaning log at end of script | -10 |
| Major | Hardcoded absolute paths | -10 |
| Major | Missing invariant `assert` after critical step | -5 |
| Minor | Long lines (>100 chars, non-mathematical) | -1 per line |
| Minor | Missing `version` statement | -2 |
| Minor | Missing `log using` | -3 |

## R Analysis Scripts (.R)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax / runtime error | -100 |
| Critical | Estimator does not match cited formula | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing `set.seed()` (stochastic code) | -10 |
| Major | SE clustering level not justified | -10 |
| Major | Output not saved (table/figure not exported) | -10 |
| Major | Missing `library()` calls at top | -5 |
| Minor | Long lines (>100 chars, non-mathematical) | -1 per line |
| Minor | No Roxygen doc on exported functions | -2 per function |

## Figures

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | File not created or empty | -100 |
| Major | Axis labels missing or uninformative | -10 |
| Major | Legend missing when needed | -10 |
| Major | Wrong dimensions (not journal-appropriate) | -5 |
| Minor | Grid lines too prominent (distract from data) | -3 |
| Minor | Default ggplot2 theme (not `theme_pub`) | -5 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues explicitly.
- **Score 80–89:** Allow commit with warning. List recommendations.
- **Score ≥ 90:** Commit freely.
- User can override with explicit justification.

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md`.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Tolerance Thresholds (Research Simulations)

Customize for your domain when running Monte Carlo or bootstrap:

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | 1e-6 | Numerical precision |
| Standard errors | 1e-4 | MC variability (tune to B) |
| Coverage rates | ± 0.01 | MC with B ≥ 1000 reps |
| Merge rate | ≥ 90% unless documented | Unexplained loss is a red flag |
