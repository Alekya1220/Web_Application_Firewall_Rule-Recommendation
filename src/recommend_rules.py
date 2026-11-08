
import pandas as pd
import re
from pathlib import Path

# --------------------------------
# 1. Project paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "block_association_rules.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "recommended_rules.csv"

# --------------------------------
# 2. Recommendation thresholds
# --------------------------------

MIN_SUPPORT = 0.001
MIN_CONFIDENCE = 0.60
MIN_LIFT = 1.0

# --------------------------------
# 3. Load association rules
# --------------------------------

def load_rules():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Run association_mining.py first."
        )

    if INPUT_FILE.stat().st_size == 0:
        return pd.DataFrame()

    df = pd.read_csv(INPUT_FILE)

    print("Association rules loaded:", len(df))

    return df


# --------------------------------
# 4. Convert frozenset text safely
# --------------------------------

def extract_items(value):

    if pd.isna(value):
        return []

    return re.findall(r"""['"]([^'"]+)['"]""", str(value))


# --------------------------------
# 5. Generate recommendations
# --------------------------------

def generate_recommendations(df):

    print("\nGenerating WAF recommendations...")

    if df.empty:
        return pd.DataFrame()

    # Apply recommendation thresholds
    filtered = df[
        (df["support"] >= MIN_SUPPORT) &
        (df["confidence"] >= MIN_CONFIDENCE) &
        (df["lift"] > MIN_LIFT)
    ].copy()

    if filtered.empty:
        print("No rules satisfy the thresholds.")
        return pd.DataFrame()

    filtered = filtered.sort_values(
        by=["confidence", "lift", "support"],
        ascending=False
    ).reset_index(drop=True)

    recommendations = []

    for index, row in filtered.iterrows():

        items = extract_items(row["antecedents"])

        pattern = ", ".join(sorted(items))

        recommendations.append({
            "recommendation_id": index + 1,
            "request_pattern": pattern,
            "suggested_action": "REVIEW_BLOCK_RULE",
            "support": round(row["support"], 4),
            "confidence": round(row["confidence"], 4),
            "lift": round(row["lift"], 4),
            "reason": (
                "This request pattern is associated with "
                "explicitly blocked traffic."
            ),
            "review_status": "PENDING_SECURITY_REVIEW"
        })

    result = pd.DataFrame(recommendations)

    print("Recommendations generated:", len(result))

    return result


# --------------------------------
# 6. Save recommendations
# --------------------------------

def save_recommendations(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nRecommendations saved successfully!")
    print("Location:", OUTPUT_FILE)


# --------------------------------
# 7. Main function
# --------------------------------

def main():

    rules = load_rules()

    if rules.empty:
        print("No association rules available.")
        return

    recommendations = generate_recommendations(rules)

    if recommendations.empty:
        print("No recommendations generated.")
        return

    save_recommendations(recommendations)

    print("\nWAF RULE RECOMMENDATION COMPLETED")


if __name__ == "__main__":
    main()
