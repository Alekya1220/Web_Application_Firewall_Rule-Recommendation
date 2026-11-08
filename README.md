# 🛡️ Web Application Firewall Rule Recommendation Using Association-Rule Mining

## 1. Project Overview

The **Web Application Firewall (WAF) Rule Recommendation System** is a Python-based project that analyzes historical Web Application Firewall logs and identifies frequently occurring request patterns.

The system uses the FP-Growth algorithm and Association-Rule Mining to discover patterns associated with explicitly blocked requests. Based on these patterns, it generates firewall rule recommendations for security engineers to review.

An interactive Streamlit dashboard is developed to display traffic analysis, association rules, recommendations and dataset information through colorful visualizations.

## 2. Objectives

- Analyze historical WAF audit logs.
- Clean and preprocess web request data.
- Identify frequently occurring request patterns.
- Apply FP-Growth for frequent pattern mining.
- Generate association rules using Support, Confidence and Lift.
- Recommend potential firewall rules for security review.
- Display results through an interactive dashboard.

## 3. Dataset

**Dataset:** OWASP ModSecurity 30-Day Audit Log Dataset

**Records used:** 100,000 HTTP transactions.

The dataset contains information about web requests, HTTP methods, endpoints, attack categories, ModSecurity rule information and response status codes.

The action labels used in this project are:

- `block` – The audit log explicitly confirms that the WAF blocked the request.
- `review_required` – The audit log does not explicitly confirm that the request was blocked.

**Note:** `review_required` does not mean that the request was allowed.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| MLxtend | FP-Growth and association rule mining |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive charts and visualizations |
| Matplotlib | Data visualization |
| VS Code | Development environment |

## 5. Project Folder Structure

```text
WAF_Rule_Recommendation/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── owasp_waf_logs_100k.csv
│   └── cleaned_waf_logs.csv
│
├── outputs/
│   ├── frequent_itemsets.csv
│   ├── block_association_rules.csv
│   └── recommended_rules.csv
│
└── src/
    ├── preprocess_logs.py
    ├── association_mining.py
    └── recommend_rules.py
```

## 6. Installation and Setup

### Step 1: Install Python

Install Python 3.10 or above.

### Step 2: Open the project

Open the project folder in Visual Studio Code.

### Step 3: Install dependencies

Open the terminal and execute:

```bash
pip install -r requirements.txt
```

### Step 4: Place the dataset

Place the OWASP dataset inside the `data` folder:

```text
data/owasp_waf_logs_100k.csv
```

## 7. How to Run the Project

Execute the following commands in the VS Code terminal in the given order.

### Step 1: Data Preprocessing

```bash
python src/preprocess_logs.py
```

This program cleans the dataset, removes duplicate and invalid records, standardizes values and saves the cleaned dataset.

Output:

```text
data/cleaned_waf_logs.csv
```

### Step 2: Association Rule Mining

```bash
python src/association_mining.py
```

This program applies the FP-Growth algorithm to identify frequent itemsets and generates association rules related to explicitly blocked requests.

Outputs:

```text
outputs/frequent_itemsets.csv
outputs/block_association_rules.csv
```

### Step 3: Rule Recommendation

```bash
python src/recommend_rules.py
```

This program evaluates and ranks the generated association rules based on support, confidence and lift.

Output:

```text
outputs/recommended_rules.csv
```

### Step 4: Launch the Dashboard

```bash
streamlit run app.py
```

The Streamlit dashboard opens in your web browser.

## 8. Dashboard Modules

The project contains five main dashboard pages.

### 1. Executive Overview
Displays total requests, explicitly blocked requests, review-required requests, attack categories and overall dataset statistics.

### 2. Traffic Analytics
Displays HTTP method analysis, attack categories, WAF actions and HTTP status code distribution.

### 3. Association Mining
Displays frequent itemsets, generated association rules, support, confidence, lift and interactive charts.

### 4. Rule Recommendations
Displays recommended firewall rule patterns, suggested actions, statistical measures and review status. Recommendations can be downloaded as a CSV file.

### 5. Data Explorer
Allows users to search, filter, view and download dataset records. It also displays dataset information and missing-value details.

## 9. Association Rule Measures

The project uses three important measures.

**Support:** Measures how frequently a particular pattern occurs in the dataset.

**Confidence:** Measures how frequently the consequent occurs when the antecedent occurs.

**Lift:** Measures the strength of the association compared with the baseline occurrence of the consequent.

These measures help identify and rank useful association rules.

## 10. Project Results

The current execution produced the following results:

| Parameter | Result |
|---|---:|
| Total dataset records | 100,000 |
| Frequent itemsets | 625 |
| Total raw association rules | 1,539 |
| Rules containing BLOCK consequent | 28 |
| Rules after feature filtering | 28 |
| Final BLOCK association rules | 15 |
| Recommendations generated | 15 |

The results are based on the current dataset and configured mining thresholds.

## 11. Advantages

- Analyzes a large collection of historical WAF logs.
- Identifies frequently occurring request patterns.
- Helps security engineers discover useful traffic relationships.
- Generates recommendations based on association rules.
- Provides an interactive and colorful dashboard.
- Allows users to explore and download analysis results.

## 12. Limitations

- The system works with historical audit logs rather than real-time network traffic.
- The quality of recommendations depends on the available dataset.
- Association does not prove that a request is malicious.
- Recommendations require manual security review.
- The system does not automatically deploy firewall rules.

## 13. Future Enhancements

- Integrate real-time WAF log monitoring.
- Improve attack classification.
- Add more advanced machine learning techniques.
- Provide more detailed security analytics.
- Integrate with firewall management systems after appropriate security validation.

## 14. Conclusion

The Web Application Firewall Rule Recommendation System analyzes historical web application firewall logs using FP-Growth and Association-Rule Mining.

It identifies frequently occurring request patterns associated with explicitly blocked traffic and generates potential firewall rule recommendations.

The Streamlit dashboard provides an easy way to understand the dataset, visualize traffic patterns, explore association rules and review recommendations.

The project helps security engineers make more informed decisions when reviewing and improving firewall configurations.

---

**Project Domain:** Cybersecurity & AI-Driven Threat Detection

**Project Type:** B.Tech Mini Project

**Department:** Artificial Intelligence and Data Science