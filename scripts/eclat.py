import pandas as pd # type: ignore
from scripts.benchmark import run_benchmark
import numpy as np # type: ignore
from collections import defaultdict

def build_tid_lists(transactions):
    tid_lists = defaultdict(set)
    n_transactions = len(transactions)
    for tid, items in enumerate(transactions):
        for item in items:
            tid_lists[item].add(tid)
    return tid_lists, n_transactions

def generate_itemsets(antecedent, tid_lists, min_support, n_transactions):
    itemsets = []
    while tid_lists:
        item = tid_lists.popitem()
        support = len(item[1]) / n_transactions
        if support < min_support:
            continue
        itemsets.append((antecedent + [item[0]], support))
        new_tid_lists = defaultdict(set)
        for k in tid_lists.keys():
            new_tid_lists[k] = tid_lists[k] & item[1]
        itemsets = itemsets + generate_itemsets(antecedent + [item[0]], new_tid_lists, min_support, n_transactions)
    return itemsets

def eclat(transactions, min_support=0.2):
    tid_lists, n_transactions = build_tid_lists(transactions)
    return generate_itemsets([], tid_lists, min_support, n_transactions)


def run_eclat(transactions, min_support):
    return eclat(transactions, min_support=min_support)

def run(transactions_df, min_support):
    print('Transformando dataset...')
    transactions = transactions_df.apply(lambda row: [item for item, present in row.items() if bool(present)], axis=1).tolist()
    print('Ejecutando benchmark...')
    data, output = run_benchmark(func=run_eclat, func_args=[transactions, min_support], label="ECLAT")
    print('Convirtiendo resultados a dataframe...')
    df_results = pd.DataFrame(columns=['support', 'itemsets'])
    for itemsets, support in output:
        df_results = pd.concat([df_results, pd.DataFrame({'support': [support], 'itemsets': [frozenset(itemsets)]})], ignore_index=True)
    return data, df_results