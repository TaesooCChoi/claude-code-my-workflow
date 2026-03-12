# CLAUDE.MD -- Empirical Economics Research with Claude Code

<!-- HOW TO USE: Fill in [BRACKETED PLACEHOLDERS] with your project details.
     Keep this file under ~150 lines — Claude loads it every session.
     Full workflow documentation in .claude/rules/ -->

**Project:** [YOUR RESEARCH PROJECT TITLE]
**Institution:** [YOUR INSTITUTION / DEPARTMENT]
**Branch:** main

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — run scripts and confirm output at the end of every task
- **Raw data is sacred** — `data/raw/` is read-only; never modify files there
- **Quality gates** — nothing commits below 80/100
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md                    # This file
├── .claude/                     # Rules, agents, hooks
├── data/
│   ├── raw/                     # Original .dta files — NEVER modify
│   ├── clean/                   # Cleaned datasets (.dta, .rds)
│   └── temp/                    # Intermediate files (gitignored)
├── scripts/
│   ├── stata/                   # .do files (cleaning, construction)
│   └── R/                       # .R files (analysis, figures)
├── output/
│   ├── tables/                  # .tex, .csv regression/summary tables
│   └── figures/                 # .pdf, .png publication figures
├── quality_reports/             # Plans, session logs, merge reports
├── explorations/                # Research sandbox
├── templates/                   # Session log, spec templates
└── master_supporting_docs/      # Papers and existing data docs
```

---

## Commands

```bash
# Run a Stata do-file (batch mode, produces .log)
stata -b do scripts/stata/[file.do]

# Run an R script
Rscript scripts/R/[file.R]

# Quality score (adapt python script as needed)
python scripts/quality_score.py scripts/stata/[file.do]
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | Ready for analysis | Clean data / script ready downstream |
| 95 | Excellence | Aspirational; publication-ready |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/clean-data [file.dta]` | Profile + clean a dataset; output cleaning log |
| `/validate-merge` | Diagnose merge: rates, unmatched obs, duplicates |
| `/audit-cleaning [script.do]` | Score a cleaning script against conventions |
| `/run-analysis [script.R]` | Execute R script, check output, score quality |
| `/make-figure [script.R]` | Create publication-ready figure, score rubric |
| `/review-stata [file.do]` | Stata code quality review |
| `/review-r [file.R]` | R code quality review |
| `/data-quality [dataset]` | Full dataset audit: labels, missings, duplicates |
| `/commit [msg]` | Stage, commit (with quality gate check) |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/review-paper [file]` | Manuscript review |
| `/learn [skill-name]` | Extract discovery into persistent skill |
| `/context-status` | Show session health + context usage |
| `/deep-audit` | Repository-wide consistency audit |

---

## Dataset Registry

<!-- Update as datasets are added to data/raw/ -->

| Dataset | File | N (raw) | Key IDs | Time Period | Status |
|---------|------|---------|---------|-------------|--------|
| [Dataset name] | `data/raw/[file.dta]` | [N] | [id vars] | [years] | raw / cleaning / clean |
