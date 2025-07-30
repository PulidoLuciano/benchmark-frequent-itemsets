from mlxtend.frequent_patterns import fpgrowth
from scripts.benchmark import run_benchmark
import pandas as pd

def run_fp_growth(transactions_df, min_support):
    return fpgrowth(transactions_df, min_support=min_support, use_colnames=True)

def run(transactions_df, min_support):
    print('Ejecutando benchmark...')
    data, output = run_benchmark(func=run_fp_growth, func_args=[transactions_df, min_support], label="FP-Growth")
    return data, output
