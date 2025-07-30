import argparse
import pandas as pd
import importlib
import os
from pathlib import Path

def preprocessing():
    # Cargar el dataset
    retail_df = pd.read_excel(os.path.join(os.path.dirname(__file__), "./data/online_retail_2.xlsx"))

    # Limpiar el dataset
    retail_df = retail_df[retail_df['UnitPrice'] > 0]
    retail_df = retail_df[retail_df['Quantity'] > 0]
    retail_df = retail_df[~retail_df["InvoiceNo"].str.contains("C", na=False)]
    retail_df = retail_df.drop_duplicates()
    retail_df = retail_df[
        ~retail_df['StockCode'].isin(['POST', 'C2', 'DOT', 'M', 'm', 'BANK CHARGES', 'AMAZONFEE', 'S', 'PADS', 'B'])]

    # Crear el dataset para los algoritmos con enteros
    retail_df['Presence'] = 1
    basket = pd.pivot_table(retail_df, index='InvoiceNo', columns='StockCode', values='Presence', aggfunc='max',
                            fill_value=0)

    # Crear el dataset para los algoritmos con booleanos
    retail_df['Presence'] = True
    boolean_basket = pd.pivot_table(retail_df, index='InvoiceNo', columns='StockCode', values='Presence', aggfunc='max',
                                    fill_value=False)

    # Guardar los datasets
    basket.to_csv(os.path.join(os.path.dirname(__file__), "./data/basket.csv"), index=True)
    boolean_basket.to_csv(os.path.join(os.path.dirname(__file__), "./data/boolean_basket.csv"), index=True)

    print('Dataset generados con éxito.')
    print(basket.head())
    print(boolean_basket.head())

def load_dataset(path=os.path.join(os.path.dirname(__file__), "./data/boolean_basket.csv"), max_transactions=None, max_items=None):
    df = pd.read_csv(path)
    df.set_index('InvoiceNo', inplace=True)
    print(f"Dataframe cargado. Tamaño: {df.shape}")

    x, y = df.shape

    if max_transactions:
        x = max_transactions

    if max_items:
        y = max_items

    df = df.iloc[0:x, 0:y]

    print(f"Ejecutando dataframe de tamaño: {df.shape}")

    return df

def read_args():
    parser = argparse.ArgumentParser(description="Benchmark de algoritmos de itemsets frecuentes")
    parser.add_argument("--algorithm", choices=["eclat", "apriori", "fp_growth"], required=True)
    parser.add_argument("--min_support", type=float, required=True)
    parser.add_argument("--max_transactions", type=int)
    parser.add_argument("--max_items", type=int)
    parser.add_argument("--dataset", default=os.path.join(os.path.dirname(__file__), "./data/boolean_basket.csv"))

    return parser.parse_args()

def main():
    try:
        args = read_args()

        if 'preprocess' in args:
            preprocessing()

        transactions_df = load_dataset(args.dataset, args.max_transactions, args.max_items)

        algo_module = importlib.import_module(f"scripts.{args.algorithm}")
        algo_func = getattr(algo_module, "run")

        stats, output = algo_func(transactions_df, args.min_support)

        max_transactions = args.max_transactions if args.max_transactions else transactions_df.shape[0]
        max_items = args.max_items if args.max_items else transactions_df.shape[1]

        is_data_sample = False
        if max_transactions != transactions_df.shape[0] or max_items != transactions_df.shape[1]:
            is_data_sample = True

        max_itemset_len = 4
        itemset_lengths = [len(output[output['itemsets'].apply(lambda x: len(x) == i)]) for i in range(1,max_itemset_len+1)]

        Path("results").mkdir(exist_ok=True)
        with open("results/benchmark.csv", "a") as f:
            f.write(f"{stats['Total_RAM_GB']},{stats['Hostname']},{stats['OS']},{stats['CPU']},"
                    f"{stats['Logical_CPUs']},{stats['Physical_CPUs']},"
                    f"{args.algorithm},{args.min_support},{is_data_sample},{max_transactions},{max_items},"
                    f"{len(output)},"
                    f"{itemset_lengths[0]},{itemset_lengths[1]},{itemset_lengths[2]},{itemset_lengths[3]},"
                    f"{stats['Duration_s']},{stats['User_Time_s']},{stats['Sys_Time_s']},"
                    f"{stats['RSS_Memory_KB']},{stats['Peak_Memory_MB']},{stats['Peak_Tracked_Bytes']}\n")

        output.to_csv(f"results/{args.algorithm}_{args.min_support}_{args.max_transactions}_{args.max_items}.csv", index=False)
    except Exception as ex:
        print(f"Error: {ex}")
        print(f"Por favor revise main()")


if __name__ == "__main__":
    main()
