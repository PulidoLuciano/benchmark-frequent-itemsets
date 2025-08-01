import pandas as pd

def measure_sparsity(df):
    """
    Mide el factor de dispersion de un dataset transaccional en one-hot encoding.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    # Convert booleans to integers if necessary
    data = df.astype(int)
    data.drop("InvoiceNo", axis=1, inplace=True)

    # Ensure only 0/1 values
    if not ((data.values >= 0).all() and (data.values <= 1).all()):
        raise ValueError("Dataset must be one-hot encoded (0/1 or True/False only).")

    n_transactions, n_items = data.shape
    total_cells = n_transactions * n_items

    if total_cells == 0:
        raise ValueError("Dataset is empty.")

    density = data.values.sum() / total_cells
    sparsity = 1 - density

    return {
        "denisdad": round(density, 6),
        "dispersion": round(sparsity, 6),
        "avg_items_por_transaccion": round(data.sum(axis=1).mean(), 4),
        "items_unicos": n_items,
        "transacciones": n_transactions,
    }


# Example usage:
if __name__ == "__main__":
    # Example one-hot dataset
    df = pd.read_csv("../data/boolean_basket.csv")

    result = measure_sparsity(df)
    print("Dataset Sparsity Metrics:")
    for k, v in result.items():
        print(f"{k}: {v}")
