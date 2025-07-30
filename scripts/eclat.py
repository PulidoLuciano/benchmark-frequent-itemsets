import pandas as pd
from pyECLAT import ECLAT
from benchmark import run_benchmark
import os
import numpy as np

print('Cargando dataset...')
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/basket.csv"))
df.set_index('InvoiceNo', inplace=True)

print('Transformando dataset...')
transactions = df.apply(lambda row: [item for item, present in row.items() if bool(present)], axis=1).tolist()
max_len = max(len(t) for t in transactions)
structured_df = pd.DataFrame([t + [np.nan] * (max_len - len(t)) for t in transactions]).head(100)

# Función objetivo
def run_eclat():
    eclat = ECLAT(structured_df, verbose=True)
    return eclat.fit(min_support=0.02)

print('Ejecutando benchmark...')
# Ejecutar benchmark
data, output = run_benchmark(run_eclat, label="ECLAT v1")
# Mostrar resultados
df_benchmark = pd.DataFrame([data])
print(df_benchmark.T)
print(output)