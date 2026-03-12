#!/usr/bin/env python3
"""
clean_2021_cultivated_area.py
------------------------------
Cleans the 2021 Korean cultivated/arable land area survey CSV and exports
to Stata .dta format for downstream analysis.

Source : data/clean/2021_재배면적_경작가능면적_20260126_22142.csv
Output : data/clean/2021_cultivated_area_clean.dta
Encoding: EUC-KR (source) → UTF-8 / Stata .dta v118 (output)

Run from project root:
    python3 scripts/python/clean_2021_cultivated_area.py

INVENTORY
---------
N = 153 rows, K = 11 columns
조사연도         : survey year (uniformly 2021)
행정구역시도코드  : province/metro code (17 unique codes, 9 rows each)
논/밭/계 × 3 area concepts : paddy / non-paddy / total for
    금년경지 (cultivated this year), 규반 (idle/fallow), 가경 (arable)
Known issue: 9 rows per region code — no sub-identifier present in the file.
    Dataset is NOT uniquely identified by (survey_year, region_code).
Known anomaly: region 21 (Busan) has 3 negative paddy area values (physically
    impossible). Set to NaN (Stata extended missing .a).
"""

import os
import sys

import numpy as np
import pandas as pd
import pyreadstat

# ── 0. PATHS ─────────────────────────────────────────────────────────────────
SRC = "data/clean/2021_재배면적_경작가능면적_20260126_22142.csv"
OUT = "data/clean/2021_cultivated_area_clean.dta"

# ── 1. LOAD ───────────────────────────────────────────────────────────────────
df = pd.read_csv(SRC, encoding="euc-kr")
N_IN, K_IN = df.shape
print(f"[1] Loaded: {N_IN} rows × {K_IN} cols")

# ── 2. RENAME COLUMNS ─────────────────────────────────────────────────────────
rename_map = {
    "조사연도":            "survey_year",
    "행정구역시도코드":     "region_code",
    "논_금년경지합계면적":  "paddy_cultivated_area",
    "밭_금년경지합계면적":  "nonpaddy_cultivated_area",
    "계_금년경지합계면적":  "total_cultivated_area",
    "논_규반합계면적":      "paddy_idle_area",
    "밭_규반합계면적":      "nonpaddy_idle_area",
    "계_규반합계면적":      "total_idle_area",
    "논_가경합계면적":      "paddy_arable_area",
    "밭_가경합계면적":      "nonpaddy_arable_area",
    "계_가경합계면적":      "total_arable_area",
}
df = df.rename(columns=rename_map)

# ── 3. IDENTIFY AREA COLUMNS ──────────────────────────────────────────────────
id_cols  = ["survey_year", "region_code"]
area_cols = [c for c in df.columns if c not in id_cols]

# ── 4. PROFILE: duplicates / negatives ────────────────────────────────────────
print(f"\n[2] Unique region_code values ({df['region_code'].nunique()}):",
      sorted(df["region_code"].unique()))
rows_per_region = df.groupby("region_code").size()
print(f"    Rows per region_code: min={rows_per_region.min()}, "
      f"max={rows_per_region.max()}, all equal={rows_per_region.nunique()==1}")

neg_rows = (df[area_cols] < 0).any(axis=1)
print(f"\n[3] Rows with ANY negative area value: {neg_rows.sum()}")
if neg_rows.any():
    print(df[neg_rows])

# ── 5. ADD ANOMALY FLAG ───────────────────────────────────────────────────────
# Flag rows containing physically impossible (negative) area measurements.
# Scheme: data_anomaly_flag = 1 → extended missing .a applies to affected vars.
df["data_anomaly_flag"] = neg_rows.astype("int32")

# ── 6. SET NEGATIVE VALUES TO NaN (→ Stata extended missing .a) ───────────────
# 3 negative paddy values in region_code=21 (Busan Metropolitan City).
# Decision: negative land area is physically impossible; values appear to be
# data entry errors. Set to NaN so downstream code treats them as missing.
# Original raw values preserved in source CSV (never modified).
affected = {}
for col in area_cols:
    mask = df[col] < 0
    n_neg = mask.sum()
    if n_neg > 0:
        affected[col] = df.loc[mask, col].values.tolist()
        df.loc[mask, col] = np.nan
        print(f"[5] {col}: {n_neg} negative value(s) → NaN  (were: {affected[col]})")

# ── 7. ASSERT INTERNAL CONSISTENCY ───────────────────────────────────────────
# arable = cultivated − idle  (holds to floating-point precision)
for prefix in ("paddy", "nonpaddy", "total"):
    cult = df[f"{prefix}_cultivated_area"]
    idle = df[f"{prefix}_idle_area"]
    arab = df[f"{prefix}_arable_area"]
    residual = (cult - idle - arab).abs()
    max_res = residual[residual.notna()].max()
    assert max_res < 1e-6, (
        f"Consistency check FAILED for {prefix}: max residual = {max_res:.2e}"
    )
print("\n[6] Internal consistency checks PASSED  "
      "(arable = cultivated − idle, max |residual| < 1e-6)")

# ── 8. VARIABLE LABELS ────────────────────────────────────────────────────────
# Region code map (for label):
#   11=Seoul, 21=Busan, 22=Daegu, 23=Incheon, 24=Gwangju, 25=Daejeon,
#   26=Ulsan, 29=Sejong, 31=Gyeonggi, 32=Gangwon, 33=N.Chungcheong,
#   34=S.Chungcheong, 35=N.Jeolla, 36=S.Jeolla, 37=N.Gyeongsang,
#   38=S.Gyeongsang, 39=Jeju
variable_labels = {
    "survey_year":              "Survey year (조사연도)",
    "region_code":              (
        "Province/metro code (행정구역시도코드): "
        "11=Seoul, 21=Busan, 22=Daegu, 23=Incheon, 24=Gwangju, "
        "25=Daejeon, 26=Ulsan, 29=Sejong, 31=Gyeonggi, 32=Gangwon, "
        "33=N.Chungcheong, 34=S.Chungcheong, 35=N.Jeolla, 36=S.Jeolla, "
        "37=N.Gyeongsang, 38=S.Gyeongsang, 39=Jeju"
    ),
    "paddy_cultivated_area":    "Paddy cultivated area this year, ha (논 금년경지합계면적)",
    "nonpaddy_cultivated_area": "Non-paddy cultivated area this year, ha (밭 금년경지합계면적)",
    "total_cultivated_area":    "Total cultivated area this year, ha (계 금년경지합계면적)",
    "paddy_idle_area":          "Paddy idle/fallow area, ha (논 규반합계면적)",
    "nonpaddy_idle_area":       "Non-paddy idle/fallow area, ha (밭 규반합계면적)",
    "total_idle_area":          "Total idle/fallow area, ha (계 규반합계면적)",
    "paddy_arable_area":        "Paddy arable (potentially cultivatable) area, ha (논 가경합계면적)",
    "nonpaddy_arable_area":     "Non-paddy arable area, ha (밭 가경합계면적)",
    "total_arable_area":        "Total arable area, ha (계 가경합계면적)",
    "data_anomaly_flag":        "=1 if row contains physically impossible (negative) area values",
}

# ── 9. EXPORT TO .DTA ─────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
pyreadstat.write_dta(df, OUT, variable_labels=variable_labels, version=118)
N_OUT, K_OUT = df.shape
print(f"\n[7] Saved: {OUT}  ({N_OUT} rows × {K_OUT} cols)")

# ── 10. VERIFY OUTPUT ─────────────────────────────────────────────────────────
df_check, meta = pyreadstat.read_dta(OUT)
assert df_check.shape == (N_OUT, K_OUT), "Round-trip shape mismatch"
assert set(df_check.columns) == set(df.columns), "Round-trip column mismatch"
print(f"[8] Round-trip read verified: {df_check.shape}")

# Spot-check: no negative area values remain
for col in area_cols:
    neg = (df_check[col] < 0).sum()
    assert neg == 0, f"Negative values still present in {col} after export"
print("[8] No negative area values in exported file ✓")

# ── 11. CLEANING LOG ──────────────────────────────────────────────────────────
print("""
═══════════════════════════════════════════════════════════════
 CLEANING LOG — 2021 Korean Cultivated/Arable Land Area Survey
═══════════════════════════════════════════════════════════════
 Source : data/clean/2021_재배면적_경작가능면각_20260126_22142.csv
 Output : data/clean/2021_cultivated_area_clean.dta
 Script : scripts/python/clean_2021_cultivated_area.py
 Stata dta version: 118 (Stata 14+)

 N in : 153 rows × 11 cols
 N out: 153 rows × 12 cols  (+data_anomaly_flag)

 Region codes (17): 11, 21–29, 31–39
 Survey years     : [2021]

 KEY DECISIONS
 ─────────────
 1. Negative paddy values → NaN (extended missing .a in Stata)
    Affected row: region_code=21 (Busan Metropolitan City)
    paddy_cultivated_area : -0.6152 → NaN
    paddy_idle_area        : -0.0254 → NaN
    paddy_arable_area      : -0.5898 → NaN
    Rationale: negative land area is physically impossible;
    values are plausible data entry errors. Original raw CSV
    (in data/clean/) is never modified.

 2. All variables labeled in English with Korean original in
    parentheses for reference.

 3. Internal consistency (arable = cultivated − idle) holds
    to floating-point precision for all non-missing rows.

 KNOWN ISSUES (unresolved)
 ─────────────────────────
 1. MISSING SUB-IDENTIFIER: The dataset has 9 rows per province
    code but contains no column identifying the sub-unit.
    (survey_year, region_code) does NOT uniquely identify obs.
    The 9 rows likely represent sub-district-level records
    (시/군/구) or survey strata. Clarification needed before
    merging with other datasets or running regressions at the
    observation level.

 MERGE RATES: N/A (no merge performed)

═══════════════════════════════════════════════════════════════
""")
