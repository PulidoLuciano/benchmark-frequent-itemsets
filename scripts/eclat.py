import pandas as pd # type: ignore
from benchmark import run_benchmark
import os
import numpy as np # type: ignore
from collections import defaultdict

def build_tid_lists(transactions):
    """
    Construye los TID-lists (ítem -> transacciones donde aparece).
    """
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
    """
    Corre el algoritmo ECLAT y retorna itemsets frecuentes con su soporte.
    """
    tid_lists, n_transactions = build_tid_lists(transactions)
    return generate_itemsets([], tid_lists, min_support, n_transactions)


print('Cargando dataset...')
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/boolean_basket.csv"))
df.set_index('InvoiceNo', inplace=True)

print('Transformando dataset...')
transactions = df.apply(lambda row: [item for item, present in row.items() if bool(present)], axis=1).tolist()

# Función objetivo
def run_eclat():
    return eclat(transactions, min_support=0.025)

print('Ejecutando benchmark...')
# Ejecutar benchmark
data, output = run_benchmark(run_eclat, label="ECLAT v1")
# Mostrar resultados
df_benchmark = pd.DataFrame([data])
print(df_benchmark.T)
print(sorted(output))