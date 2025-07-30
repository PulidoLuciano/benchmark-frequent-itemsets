from mlxtend.frequent_patterns import apriori
from benchmark import run_benchmark
import pandas as pd
import os

print('Cargando dataset...')
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/boolean_basket.csv"))
df.set_index('InvoiceNo', inplace=True)

# Función objetivo
def run_apriori():
    return apriori(df, min_support=0.02, use_colnames=True)

print('Ejecutando benchmark...')
data, output = run_benchmark(run_apriori, label="Apriori v1")

# Mostrar resultados
df_benchmark = pd.DataFrame([data])
print(df_benchmark.T)

