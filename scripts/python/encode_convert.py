#!/usr/bin/env python3
"""
encode_convert.py
-----------------
Converts the original EUC-KR Korean CSV to UTF-8 so Stata's
`import delimited, encoding(utf-8)` can read it directly.

Run from project root before the Stata cleaning script:
    python3 scripts/python/encode_convert.py

Output: data/temp/2021_cultivated_area_utf8.csv
"""
import os
import pandas as pd

SRC = "data/clean/2021_재배면적_경작가능면적_20260126_22142.csv"
OUT = "data/temp/2021_cultivated_area_utf8.csv"

os.makedirs("data/temp", exist_ok=True)
df = pd.read_csv(SRC, encoding="euc-kr")
df.to_csv(OUT, index=False, encoding="utf-8")
print(f"Converted: {SRC}")
print(f"Output   : {OUT}  ({df.shape[0]} rows × {df.shape[1]} cols)")
