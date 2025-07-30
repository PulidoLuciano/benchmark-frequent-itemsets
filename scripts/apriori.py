from mlxtend.frequent_patterns import apriori
from scripts.benchmark import run_benchmark
import pandas as pd

def run_apriori(transactions_df, min_support):
    return apriori(transactions_df, min_support=min_support, use_colnames=True)

def run(transactions_df, min_support):
    print('Ejecutando benchmark...')
    data, output = run_benchmark(func=run_apriori, func_args=[transactions_df, min_support], label="Apriori")
    return data, output

