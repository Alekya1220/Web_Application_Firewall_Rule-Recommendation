
import pandas as pd
from pathlib import Path
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

# --------------------------------
# 1. Project paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned_waf_logs.csv"

OUTPUT_DIR = BASE_DIR / "outputs"

ITEMSETS_FILE = OUTPUT_DIR / "frequent_itemsets.csv"
RULES_FILE = OUTPUT_DIR / "block_association_rules.csv"

# --------------------------------
# 2. Mining parameters
# --------------------------------

MIN_SUPPORT = 0.001
MIN_CONFIDENCE = 0.60

# --------------------------------
# 3. Load cleaned dataset
# --------------------------------

def load_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run preprocessing first."
        )

    df = pd.read_csv(INPUT_FILE)

    print("Cleaned dataset loaded:", len(df), "records")

    return df


# --------------------------------
# 4. Prepare transactions
# --------------------------------

def prepare_transactions(df):

    print("\nPreparing transactions...")

    required_columns = [
        "method",
        "endpoint",
        "attack_type",
        "action"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    transactions = []

    for row in df[required_columns].itertuples(
        index=False,
        name=None
    ):

        method, endpoint, attack_type, action = row

        items = [
            "method=" + str(method),
            "endpoint=" + str(endpoint),
            "attack_type=" + str(attack_type),
            "action=" + str(action)
        ]

        transactions.append(items)

    print("Transactions prepared:", len(transactions))

    return transactions


# --------------------------------
# 5. Convert transactions to matrix
# --------------------------------

def encode_transactions(transactions):

    print("\nEncoding transactions...")

    encoder = TransactionEncoder()

    encoded_array = encoder.fit(
        transactions
    ).transform(
        transactions,
        sparse=True
    )

    encoded_df = pd.DataFrame.sparse.from_spmatrix(
        encoded_array,
        columns=encoder.columns_
    )

    print("Encoded columns:", len(encoded_df.columns))

    return encoded_df


# --------------------------------
# 6. Apply FP-Growth
# --------------------------------

def mine_frequent_itemsets(encoded_df):

    print("\nApplying FP-Growth algorithm...")

    frequent_itemsets = fpgrowth(
        encoded_df,
        min_support=MIN_SUPPORT,
        use_colnames=True,
        max_len=4
    )

    frequent_itemsets["length"] = (
        frequent_itemsets["itemsets"].apply(len)
    )

    print("Frequent itemsets found:", len(frequent_itemsets))

    return frequent_itemsets


# --------------------------------
# 7. Generate association rules
# --------------------------------

def generate_rules(frequent_itemsets):

    print("\nGenerating association rules...")

    if frequent_itemsets.empty:
        print("No frequent itemsets found.")
        return pd.DataFrame()

    # Generate all possible association rules
    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=0.10
    )

    print("\nRULE GENERATION REPORT")
    print("-----------------------------")
    print("Total raw rules:", len(rules))

    if rules.empty:
        print("No association rules generated.")
        return rules

    # Display the actual item names
    print("\nAvailable consequents:")

    print(
        rules["consequents"]
        .astype(str)
        .value_counts()
        .head(15)
    )

    # Check for the BLOCK outcome
    block_rules = rules[
        rules["consequents"].apply(
            lambda items: "action=block" in items
        )
    ].copy()

    print("\nRules containing action=block:", len(block_rules))

    if block_rules.empty:
        print("\nNo BLOCK consequent found.")
        print("Please check the transaction labels.")
        return block_rules

    # Keep only rules with request features as antecedents
    allowed_features = [
        "method=",
        "endpoint=",
        "attack_type="
    ]

    block_rules = block_rules[
        block_rules["antecedents"].apply(
            lambda items: (
                len(items) > 0 and
                all(
                    any(
                        str(item).startswith(prefix)
                        for prefix in allowed_features
                    )
                    for item in items
                )
            )
        )
    ].copy()

    print(
        "Rules after feature filtering:",
        len(block_rules)
    )

    # Apply final thresholds
    block_rules = block_rules[
        (block_rules["confidence"] >= 0.60) &
        (block_rules["lift"] > 1.0)
    ].copy()

    block_rules = block_rules.sort_values(
        by=["confidence", "lift", "support"],
        ascending=False
    )

    print(
        "Final BLOCK association rules:",
        len(block_rules)
    )

    return block_rules

# --------------------------------
# 8. Save results
# --------------------------------

def save_results(frequent_itemsets, rules):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    frequent_itemsets.to_csv(
        ITEMSETS_FILE,
        index=False
    )

    if not rules.empty:

        rules.to_csv(
            RULES_FILE,
            index=False
        )

    else:

        pd.DataFrame().to_csv(
            RULES_FILE,
            index=False
        )

    print("\nResults saved successfully!")

    print("Frequent itemsets:", ITEMSETS_FILE)
    print("Association rules:", RULES_FILE)


# --------------------------------
# 9. Main function
# --------------------------------

def main():

    df = load_data()

    transactions = prepare_transactions(df)

    encoded_df = encode_transactions(transactions)

    frequent_itemsets = mine_frequent_itemsets(
        encoded_df
    )

    rules = generate_rules(frequent_itemsets)

    save_results(frequent_itemsets, rules)

    print("\nASSOCIATION MINING COMPLETED")


if __name__ == "__main__":
    main()
