from mlxtend.frequent_patterns import apriori
from scripts.benchmark import run_benchmark
import pandas as pd
import os
from multiprocessing import Manager, Process

print('Cargando dataset...')
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/boolean_basket.csv"))
df.set_index('InvoiceNo', inplace=True)


TOTAL_TRANSACTIONS = len(df)
MIN_SUPPORT = 0.01

def run_apriori_chunk(chunk, shared_counts, lock):
    """Run apriori on a chunk and update global shared counts."""
    local_transactions = len(chunk)
    # Set min_support=0 to avoid losing candidates
    result = apriori(chunk, min_support=1e-6, use_colnames=True) # o usar 1e-6

    for _, row in result.iterrows():
        itemset = frozenset(row["itemsets"])
        count = round(row["support"] * local_transactions)  # Use round instead of int to avoid truncation
        with lock:
            shared_counts[itemset] = shared_counts.get(itemset, 0) + count


def run_apriori_multiprocess(workers=4):
    """Split dataset, run apriori in parallel, and recalculate support."""
    manager = Manager()
    shared_counts = manager.dict()
    lock = manager.Lock()

    chunks = [df.iloc[i::workers] for i in range(workers)]
    processes = []

    # Launch processes
    for chunk in chunks:
        p = Process(target=run_apriori_chunk, args=(chunk, shared_counts, lock))
        processes.append(p)
        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    results = pd.DataFrame([
        {"itemsets": k, "count": v, "support": v / TOTAL_TRANSACTIONS}
        for k, v in shared_counts.items()
    ])

    # Ensure we have the correct columns even if empty
    if results.empty:
        results = pd.DataFrame(columns=["itemsets", "count", "support"])
    else:
        results = results[results["support"] >= MIN_SUPPORT].reset_index(drop=True)

    return results[["itemsets", "support"]]


# Función objetivo
def run_apriori_single_process():
    return apriori(df, min_support=0.04, use_colnames=True)

print('Ejecutando benchmark...')
results = run_apriori_multiprocess(workers=8)  # Get results DataFrame
# results = run_apriori_single_process()
data, output = run_benchmark(lambda: run_apriori_multiprocess(workers=8), label="Apriori v1 Multiprocessing")
# data, output = run_benchmark(run_apriori_single_process, label="Apriori v1")

# Mostrar resultados del benchmark
df_benchmark = pd.DataFrame([data])
print(df_benchmark.T)

# Guardar resultados de itemsets en CSV
output_csv_path = os.path.join(os.path.dirname(__file__), "../results/apriori_results_01_multi.csv")
results.to_csv(output_csv_path, index=False)
print(f"Resultados de Apriori guardados en: {output_csv_path}")

