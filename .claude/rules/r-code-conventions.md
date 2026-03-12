---
paths:
  - "**/*.R"
  - "scripts/R/**"
---

# R Code Standards

**Standard:** Senior applied econometrician quality — rigorous, reproducible, publication-ready.

---

## 1. Reproducibility

- `set.seed()` called ONCE at top (YYYYMMDD format)
- All packages loaded at top via `library()` (not `require()`)
- All paths relative to repository root
- `dir.create(..., recursive = TRUE)` for output directories
- Pin package versions in a comment or `renv.lock` if sharing

## 2. Function Design

- `snake_case` naming, verb-noun pattern
- Roxygen-style documentation
- Default parameters, no magic numbers
- Named return values (lists or tibbles)

## 3. Domain Correctness — Causal Inference

<!-- Field-specific pitfalls for empirical economics -->

### Estimation
- Verify estimator formula matches the cited paper/slide
- Check standard errors: robust? clustered? at what level?
- For DiD: confirm parallel trends assumption is plausible; check pre-trends
- For IV: report first-stage F-stat; check weak instrument (F < 10 is a red flag)
- For RDD: inspect bandwidth selection; plot density (McCrary test)
- For matching: check covariate balance before AND after matching

### Common Pitfalls
| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Singleton fixed effects absorbed silently | Biased SEs | Use `lfe::felm` with `exactDOF = TRUE` or `fixest` |
| Clustering too broadly or narrowly | Wrong inference | Match cluster level to treatment assignment level |
| Extrapolating LATE as ATE | Overstated generalizability | Be explicit about complier population |
| Dropping never-takers before IV | Selection bias | Keep full sample; IV identifies LATE on compliers |
| Forgetting `na.rm = TRUE` in `mean()` | Silent NA propagation | Always explicit |
| Factor variables with wrong reference level | Mis-read coefficients | Use `relevel()` explicitly |

## 4. Visual Identity

```r
# --- Color palette (customize for your project) ---
primary_color  <- "#012169"   # institutional blue (placeholder)
accent_color   <- "#f2a900"   # institutional gold (placeholder)
neutral_gray   <- "#525252"
positive_green <- "#15803d"
negative_red   <- "#b91c1c"
```

### Custom Theme (publication-ready)
```r
theme_pub <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title    = element_text(face = "bold", size = base_size + 2),
      plot.subtitle = element_text(color = neutral_gray),
      axis.title    = element_text(face = "bold"),
      legend.position = "bottom",
      panel.grid.minor = element_blank(),
      strip.text    = element_text(face = "bold")
    )
}
```

### Figure Dimensions (journal articles)
```r
# Single column (~3.5 inches wide for most journals)
ggsave(filepath, width = 3.5, height = 3, units = "in", dpi = 300)

# Full page / two-column figures
ggsave(filepath, width = 7, height = 4.5, units = "in", dpi = 300)

# For working papers / NBER format (no hard constraint)
ggsave(filepath, width = 6.5, height = 4, units = "in", dpi = 300)
```

## 5. RDS Data Pattern

**Heavy computations saved as RDS; analysis loads pre-computed objects.**

```r
saveRDS(result, file.path(out_dir, "descriptive_name.rds"))
result <- readRDS(file.path(out_dir, "descriptive_name.rds"))
```

## 6. Table Output

Use `modelsummary`, `stargazer`, or `kableExtra` consistently:

```r
library(modelsummary)
modelsummary(
  list("OLS" = m1, "IV" = m2, "DiD" = m3),
  stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  vcov = "HC1",     # or cluster-robust
  output = "output/tables/table2_main.tex"
)
```

## 7. Line Length & Mathematical Exceptions

**Standard:** Keep lines <= 100 characters.

**Exception: Mathematical Formulas** — may exceed 100 chars **if and only if:**

1. Breaking the line would harm readability of the math (influence functions, estimator formulas, simulation draws)
2. An inline comment explains the operation:
   ```r
   # ATT via Callaway-Sant'Anna: weighted average of group-time ATTs
   att <- sum(w_gt * att_gt) / sum(w_gt)
   ```
3. The line is in a numerically intensive section (bootstrap loops, GMM, simulation)

## 8. Code Quality Checklist

```
[ ] Packages at top via library()
[ ] set.seed() once at top (YYYYMMDD)
[ ] All paths relative to project root
[ ] Functions documented (Roxygen)
[ ] Estimator matches cited formula
[ ] SEs: clustering level matches treatment assignment
[ ] Figures: theme_pub(), explicit dimensions, dpi = 300
[ ] RDS: every heavy computation saved
[ ] Tables: saved to output/tables/
[ ] Comments explain WHY not WHAT
```
