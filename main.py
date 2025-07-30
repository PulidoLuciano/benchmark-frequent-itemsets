import argparse
import pandas as pd
import importlib
import os
from pathlib import Path

def load_dataset(path=os.path.join(os.path.dirname(__file__), "./data/boolean_basket.csv"), max_transactions=None, max_items=None):
    df = pd.read_csv(path)
    df.set_index('InvoiceNo', inplace=True)
    
    if max_transactions:
        df = df.head(max_transactions)

    if max_items:
        transactions = [[item for item in trans if hash(item) % 1000 < max_items] for trans in transactions]

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
    args = read_args()

    transactions_df = load_dataset(args.dataset, args.max_transactions, args.max_items)

    algo_module = importlib.import_module(f"scripts.{args.algorithm}")
    algo_func = getattr(algo_module, "run")

    stats, output = algo_func(transactions_df, args.min_support)

    Path("results").mkdir(exist_ok=True)
    with open("results/benchmark.csv", "a") as f:
        f.write(f"{stats['Total_RAM_GB']},{stats['Hostname']},{stats['OS']},{stats['CPU']},{stats['Logical_CPUs']},{stats['Physical_CPUs']},{args.algorithm},{args.min_support},{args.max_transactions},{args.max_items},{stats['Duration_s']},{stats['User_Time_s']},{stats['Sys_Time_s']},{stats['RSS_Memory_KB']},{stats['Peak_Memory_MB']},{stats['Peak_Tracked_Bytes']}\n")
    
    output.to_csv(f"results/{args.algorithm}_{args.min_support}_{args.max_transactions}_{args.max_items}.csv", index=False)

if __name__ == "__main__":
    main()
