from lib.eclat_mlxtend import eclat
from scripts.benchmark import run_benchmark


def run_eclat(transactions_df, min_support):
    return eclat(transactions_df, min_support=min_support, use_colnames=True)

def run(transactions_df, min_support):
    print('Ejecutando benchmark...')
    data, output = run_benchmark(func=run_eclat, func_args=[transactions_df, min_support], label="Eclat")
    return data, output
