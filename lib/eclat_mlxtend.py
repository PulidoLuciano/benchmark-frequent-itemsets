import numpy as np
import pandas as pd
from collections import defaultdict
from mlxtend.frequent_patterns import fpcommon as fpc  # same helper module used in apriori and fp_growth

def eclat(df, min_support=0.5, use_colnames=False, max_len=None, verbose=0):
    """
    Get frequent itemsets from a one-hot encoded DataFrame using the Eclat algorithm.

    Parameters
    ----------
    df : pandas DataFrame
        One-hot encoded DataFrame (0/1 or True/False values).

    min_support : float (default: 0.5)
        Minimum support threshold (fraction of transactions).

    use_colnames : bool (default: False)
        If True, return itemsets using column names instead of column indices.

    max_len : int (default: None)
        Maximum length of itemsets. If None, explore all lengths.

    verbose : int (default: 0)
        Verbosity level.

    Returns
    -------
    pandas DataFrame
        Columns ['support', 'itemsets'] where itemsets are frozensets.
    """
    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive number within the interval (0, 1]."
        )

    fpc.valid_input_check(df)

    # Convert df to sparse matrix if possible
    if hasattr(df, "sparse"):
        X = df.sparse.to_coo().tocsc()
        is_sparse = True
    else:
        X = df.values
        is_sparse = False

    n_transactions = X.shape[0]
    minsup_count = np.ceil(min_support * n_transactions)

    # Map index to colname if requested
    colname_map = None
    if use_colnames:
        colname_map = {idx: item for idx, item in enumerate(df.columns)}

    # Build TID lists (transaction ID sets for each item)
    tid_lists = defaultdict(set)
    for tid, row in enumerate(X):
        items = np.where(row.toarray()[0] if is_sparse else row)[0]
        for item in items:
            tid_lists[item].add(tid)

    # Initialize with single items above min_support
    itemsets = []
    single_items = {item: tids for item, tids in tid_lists.items() if len(tids) >= minsup_count}

    def recursive_eclat(prefix, items):
        for i, (item, tids) in enumerate(items.items()):
            support = len(tids) / n_transactions
            new_itemset = prefix + [item]
            itemsets.append((frozenset(new_itemset), support))

            if max_len and len(new_itemset) >= max_len:
                continue

            # Generate new candidate items by intersecting TID lists
            new_items = {}
            for j, (other_item, other_tids) in enumerate(list(items.items())[i+1:]):
                intersected = tids & other_tids
                if len(intersected) >= minsup_count:
                    new_items[other_item] = intersected

            if new_items:
                recursive_eclat(new_itemset, new_items)

    recursive_eclat([], single_items)

    # Build result DataFrame
    res_df = pd.DataFrame(itemsets, columns=["itemsets", "support"])
    if use_colnames and colname_map:
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([colname_map[i] for i in x])
        )

    return res_df[["support", "itemsets"]]
