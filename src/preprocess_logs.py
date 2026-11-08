
import pandas as pd
from pathlib import Path

# --------------------------------
# 1. Set project paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "owasp_waf_logs_100k.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_waf_logs.csv"

# --------------------------------
# 2. Load dataset
# --------------------------------

def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print("\nOriginal Dataset Loaded")
    print("Total records:", len(df))
    print("Total columns:", len(df.columns))

    return df


# --------------------------------
# 3. Clean dataset
# --------------------------------

def clean_data(df):

    print("\nStarting Data Cleaning...")

    # Standardize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    # Required columns
    required_columns = [
        "request_id",
        "method",
        "endpoint",
        "attack_type",
        "rule_triggered",
        "action",
        "status_code"
    ]

    # Check required columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Remove exact duplicate records
    before_duplicates = len(df)

    df = df.drop_duplicates().copy()

    duplicates_removed = before_duplicates - len(df)

    # Remove records missing essential information
    before_missing = len(df)

    df = df.dropna(
        subset=[
            "request_id",
            "method",
            "endpoint",
            "action"
        ]
    ).copy()

    missing_removed = before_missing - len(df)

    # Clean text columns
    text_columns = [
        "method",
        "endpoint",
        "attack_type",
        "rule_triggered",
        "action"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # Replace empty attack types
    df["attack_type"] = df["attack_type"].replace(
        "", "untagged"
    )

    # Replace empty rule values
    df["rule_triggered"] = df["rule_triggered"].replace(
        "", "unknown"
    )

    # Keep only known action labels
    valid_actions = ["block", "review_required"]

    before_actions = len(df)

    df = df[
        df["action"].isin(valid_actions)
    ].copy()

    invalid_actions_removed = before_actions - len(df)

    # Convert status code to numeric
    df["status_code"] = pd.to_numeric(
        df["status_code"],
        errors="coerce"
    )

    # Remove invalid HTTP status codes
    before_status = len(df)

    df = df[
        df["status_code"].between(100, 599)
    ].copy()

    invalid_status_removed = before_status - len(df)

    df["status_code"] = df["status_code"].astype(int)

    # Reset index
    df = df.reset_index(drop=True)

    # --------------------------------
    # 4. Display cleaning report
    # --------------------------------

    print("\nDATA CLEANING REPORT")
    print("-----------------------------")

    print("Duplicate records removed:", duplicates_removed)
    print("Missing essential records removed:", missing_removed)
    print("Invalid action records removed:", invalid_actions_removed)
    print("Invalid status records removed:", invalid_status_removed)

    print("\nFinal records:", len(df))

    print("\nAction Distribution:")
    print(df["action"].value_counts())

    return df


# --------------------------------
# 5. Save cleaned dataset
# --------------------------------

def save_data(df):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCleaned dataset saved successfully!")
    print("File location:", OUTPUT_FILE)


# --------------------------------
# 6. Main function
# --------------------------------

def main():

    df = load_data()

    cleaned_df = clean_data(df)

    save_data(cleaned_df)


if __name__ == "__main__":
    main()
