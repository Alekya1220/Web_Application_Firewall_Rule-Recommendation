
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="WAF Rule Recommendation System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

LOG_FILE = DATA_DIR / "cleaned_waf_logs.csv"
ITEMSET_FILE = OUTPUT_DIR / "frequent_itemsets.csv"
RULE_FILE = OUTPUT_DIR / "block_association_rules.csv"
RECOMMENDATION_FILE = OUTPUT_DIR / "recommended_rules.csv"

# =====================================================
# 3. COLOR PALETTE
# =====================================================

CHART_COLORS = [
    "#A78BFA",
    "#06B6D4",
    "#EC4899",
    "#F59E0B",
    "#22C55E",
    "#3B82F6",
    "#F97316",
    "#E879F9",
    "#14B8A6",
    "#EF4444"
]

# =====================================================
# 4. CUSTOM COLORFUL CSS
# =====================================================

st.markdown("""
<style>

/* Main background */

.stApp {
    background: linear-gradient(
        135deg,
        #0f0c29,
        #17153b,
        #242052,
        #30245c
    );

    color: #ffffff;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #24104f,
        #172554,
        #0f172a
    );
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

/* Main headings */

h1 {
    color: #c4b5fd !important;
    font-weight: 800 !important;
}

h2 {
    color: #67e8f9 !important;
}

h3 {
    color: #f0abfc !important;
}

/* Paragraphs */

p, label {
    color: #e2e8f0;
}

/* KPI cards */

.metric-card {
    background: linear-gradient(
        135deg,
        #7c3aed,
        #4f46e5,
        #0891b2
    );

    padding: 23px 12px;
    border-radius: 16px;
    border: 1px solid #818cf8;
    text-align: center;

    box-shadow: 0 5px 20px rgba(0,0,0,0.3);

    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(139,92,246,0.35);
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #ffffff;
}

.metric-label {
    font-size: 14px;
    color: #e0f2fe;
    margin-top: 5px;
}

/* Streamlit metric cards */

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #312e81,
        #6d28d9
    );

    padding: 16px;
    border-radius: 14px;
    border: 1px solid #818cf8;
}

/* Buttons */

.stButton button,
.stDownloadButton button {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #2563eb,
        #0891b2
    );

    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    padding: 8px 18px;
}

.stButton button:hover,
.stDownloadButton button:hover {
    border: 1px solid #c4b5fd;
    color: white;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #6366f1;
    border-radius: 10px;
}

/* Input fields */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e1b4b;
    color: white;
}

/* Divider */

hr {
    border-color: #6366f1;
}

/* Information boxes */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */

.footer {
    text-align: center;
    color: #a5b4fc;
    padding: 15px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 5. PLOTLY CHART THEME
# =====================================================

def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            color="#F8FAFC",
            size=13
        ),

        title_font=dict(
            color="#C4B5FD",
            size=20
        ),

        legend_title_font=dict(
            color="#67E8F9"
        ),

        margin=dict(
            l=20,
            r=20,
            t=65,
            b=30
        ),

        hoverlabel=dict(
            bgcolor="#312E81",
            font_color="white"
        )
    )

    return fig


# =====================================================
# 6. LOAD DATASETS
# =====================================================

@st.cache_data
def load_csv(path):

    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path)

    return pd.DataFrame()


logs = load_csv(LOG_FILE)
itemsets = load_csv(ITEMSET_FILE)
rules = load_csv(RULE_FILE)
recommendations = load_csv(RECOMMENDATION_FILE)


# =====================================================
# 7. DASHBOARD HEADER
# =====================================================

st.title("🛡️ WAF Rule Recommendation System")

st.markdown(
    """
    <p style="
        color:#67e8f9;
        font-size:17px;
        font-weight:500;
    ">
        Association-Rule Mining Based Web Application
        Firewall Analysis
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 8. CHECK DATASET
# =====================================================

if logs.empty:

    st.error(
        "Cleaned dataset not found. "
        "Please run the preprocessing program first."
    )

    st.stop()


# =====================================================
# 9. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown(
    """
    <h1 style="color:#c4b5fd;">🛡️ WAF Security</h1>
    <p style="color:#67e8f9;">
        Analytics Dashboard
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Traffic Analytics",
        "Association Mining",
        "Rule Recommendations",
        "Data Explorer"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### 📊 Dataset Information")

st.sidebar.info(
    "Dataset: OWASP ModSecurity\n\n"
    "Source Records: 100,000"
)

st.sidebar.markdown(
    """
    ### ⚙️ Technology Stack

    - Python
    - Pandas
    - FP-Growth
    - Association Rules
    - Streamlit
    - Plotly
    """
)


# =====================================================
# 10. REUSABLE KPI CARD
# =====================================================


def metric_card(label, value):

    html = f"""
<div class="metric-card">
    <div class="metric-value">{value}</div>
    <div class="metric-label">{label}</div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)



# =====================================================
# PAGE 1: EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.header("📊 Executive Overview")

    total = len(logs)

    blocked = (
        logs["action"].eq("block").sum()
        if "action" in logs.columns else 0
    )

    review = (
        logs["action"].eq("review_required").sum()
        if "action" in logs.columns else 0
    )

    attack_types = (
        logs["attack_type"].nunique()
        if "attack_type" in logs.columns else 0
    )

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Total Requests",
            f"{total:,}"
        )

    with col2:
        metric_card(
            "Explicitly Blocked",
            f"{blocked:,}"
        )

    with col3:
        metric_card(
            "Review Required",
            f"{review:,}"
        )

    with col4:
        metric_card(
            "Attack Categories",
            attack_types
        )

    st.divider()

    # CHARTS

    left, right = st.columns(2)

    with left:

        st.subheader("🛡️ WAF Action Distribution")

        action_data = (
            logs["action"]
            .value_counts()
            .reset_index()
        )

        action_data.columns = [
            "Action",
            "Count"
        ]

        fig = px.pie(
            action_data,
            names="Action",
            values="Count",
            hole=0.55,
            title="Request Action Distribution",
            color_discrete_sequence=CHART_COLORS
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(
                line=dict(
                    color="#17153b",
                    width=3
                )
            )
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🌐 HTTP Status Codes")

        status_data = (
            logs["status_code"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        status_data.columns = [
            "Status Code",
            "Count"
        ]

        fig = px.bar(
            status_data,
            x="Status Code",
            y="Count",
            color="Count",
            color_continuous_scale=[
                "#312e81",
                "#7c3aed",
                "#06b6d4",
                "#22c55e"
            ],
            title="Top HTTP Status Codes"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("📌 Dataset Summary")

    st.write(
        "This dashboard analyzes OWASP ModSecurity "
        "audit logs to identify recurring request patterns "
        "associated with explicitly blocked traffic."
    )

    st.warning(
        "Review Required records are not confirmed ALLOW "
        "requests. They are kept separate from explicitly "
        "blocked requests."
    )


# =====================================================
# PAGE 2: TRAFFIC ANALYTICS
# =====================================================

elif page == "Traffic Analytics":

    st.header("📈 Traffic Analytics")

    left, right = st.columns(2)

    # HTTP METHOD CHART

    with left:

        st.subheader("🌐 HTTP Method Analysis")

        method_data = (
            logs["method"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        method_data.columns = [
            "Method",
            "Count"
        ]

        fig = px.bar(
            method_data,
            x="Method",
            y="Count",
            color="Method",
            color_discrete_sequence=CHART_COLORS,
            title="Requests by HTTP Method"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ATTACK CATEGORY CHART

    with right:

        st.subheader("🚨 Attack Category Analysis")

        attack_data = (
            logs["attack_type"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        attack_data.columns = [
            "Attack Type",
            "Count"
        ]

        fig = px.bar(
            attack_data,
            x="Count",
            y="Attack Type",
            orientation="h",
            color="Attack Type",
            color_discrete_sequence=CHART_COLORS,
            title="Top Attack Categories"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ACTION VS ATTACK CHART

    st.subheader("🔍 Attack Category vs WAF Action")

    action_attack = (
        logs.groupby(
            ["attack_type", "action"]
        )
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        action_attack,
        x="attack_type",
        y="Count",
        color="action",
        barmode="group",
        color_discrete_sequence=[
            "#F43F5E",
            "#06B6D4"
        ],
        title="WAF Action by Attack Category"
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # STATUS CODE DISTRIBUTION

    st.subheader("📊 Status Code Distribution")

    status_data = (
        logs["status_code"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status Code",
        "Count"
    ]

    fig = px.bar(
        status_data,
        x="Status Code",
        y="Count",
        color="Count",
        color_continuous_scale="Plasma",
        title="HTTP Response Status Distribution"
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# PAGE 3: ASSOCIATION MINING
# =====================================================

elif page == "Association Mining":

    st.header("🔗 Association Rule Mining")

    st.write(
        "Discover request patterns associated with "
        "explicitly blocked traffic using FP-Growth "
        "and Association Rule Mining."
    )

    col1, col2 = st.columns(2)

    with col1:

        metric_card(
            "Frequent Itemsets",
            f"{len(itemsets):,}"
        )

    with col2:

        metric_card(
            "BLOCK Association Rules",
            f"{len(rules):,}"
        )

    st.divider()

    st.subheader("📋 Association Rules")

    if not rules.empty:

        display_columns = [
            col for col in [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
            if col in rules.columns
        ]

        st.dataframe(
            rules[display_columns],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Association Rules",
            data=rules.to_csv(index=False).encode("utf-8"),
            file_name="block_association_rules.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No association rules are available."
        )

    st.divider()

    # TOP RULES

    st.subheader("🏆 Top 10 Rules by Confidence")

    if not rules.empty:

        top_rules = rules.nlargest(
            min(10, len(rules)),
            "confidence"
        ).copy()

        top_rules["rule"] = (
            top_rules["antecedents"].astype(str)
            + " → "
            + top_rules["consequents"].astype(str)
        )

        fig = px.bar(
            top_rules,
            x="confidence",
            y="rule",
            orientation="h",
            color="confidence",
            color_continuous_scale="Turbo",
            title="Association Rule Confidence"
        )

        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # SUPPORT VS CONFIDENCE

        st.subheader("📊 Support vs Confidence")

        fig = px.scatter(
            rules,
            x="support",
            y="confidence",
            size="lift",
            color="lift",
            color_continuous_scale="Plasma",
            hover_data=["antecedents", "consequents"],
            title="Association Rule Performance"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# PAGE 4: RULE RECOMMENDATIONS
# =====================================================

elif page == "Rule Recommendations":

    st.header("🛡️ WAF Rule Recommendations")

    if recommendations.empty:

        st.warning(
            "Recommendations file is not available. "
            "Run recommend_rules.py first."
        )

    else:

        total_recommendations = len(
            recommendations
        )

        st.metric(
            "Total Recommendations",
            f"{total_recommendations:,}"
        )

        st.divider()

        st.subheader("🔎 Filter Recommendations")

        filtered = recommendations.copy()

        if "review_status" in filtered.columns:

            status_options = [
                "All"
            ] + sorted(
                filtered["review_status"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_status = st.selectbox(
                "Select Review Status",
                status_options
            )

            if selected_status != "All":

                filtered = filtered[
                    filtered["review_status"]
                    == selected_status
                ]

        st.write(
            f"Displaying {len(filtered):,} recommendations"
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # DOWNLOAD

        st.download_button(
            "⬇️ Download Recommendations",
            data=filtered.to_csv(
                index=False
            ).encode("utf-8"),

            file_name="recommended_rules.csv",

            mime="text/csv"
        )

        # TOP RECOMMENDATIONS

        if "confidence" in filtered.columns:

            st.subheader(
                "🏆 Top Recommendations by Confidence"
            )

            top_recommendations = filtered.nlargest(
                min(10, len(filtered)),
                "confidence"
            ).copy()

            if not top_recommendations.empty:

                fig = px.bar(
                    top_recommendations,
                    x="confidence",
                    y="recommendation_id",
                    orientation="h",
                    color="confidence",
                    color_continuous_scale="Turbo",
                    title="Recommendation Confidence"
                )

                fig = style_chart(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        st.info(
            "Recommendations are suggestions for security "
            "engineers. Human review is required before "
            "changing firewall configurations."
        )


# =====================================================
# PAGE 5: DATA EXPLORER
# =====================================================

elif page == "Data Explorer":

    st.header("📂 Dataset Explorer")

    st.write(
        "Explore, search and download the cleaned "
        "OWASP ModSecurity dataset."
    )

    st.metric(
        "Total Dataset Records",
        f"{len(logs):,}"
    )

    st.divider()

    # SEARCH

    st.subheader("🔍 Search Dataset")

    search_column = st.selectbox(
        "Choose Search Column",
        [
            "attack_type",
            "method",
            "endpoint",
            "action"
        ]
    )

    search_text = st.text_input(
        "Enter search value"
    )

    filtered_logs = logs.copy()

    if search_text and search_column in logs.columns:

        filtered_logs = logs[
            logs[search_column]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.write(
        f"Matching records: {len(filtered_logs):,}"
    )

    # DATA TABLE

    st.dataframe(
        filtered_logs.head(1000),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "The table displays up to 1,000 matching records."
    )

    # DOWNLOAD

    st.download_button(
        "⬇️ Download Filtered Dataset",

        data=filtered_logs.to_csv(
            index=False
        ).encode("utf-8"),

        file_name="filtered_waf_logs.csv",

        mime="text/csv"
    )

    st.divider()

    # DATASET INFORMATION

    st.subheader("📊 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Number of Records:**", len(logs))

        st.write("**Number of Columns:**", len(logs.columns))

    with col2:

        st.write(
            "**Unique HTTP Methods:**",
            logs["method"].nunique()
        )

        st.write(
            "**Unique Attack Categories:**",
            logs["attack_type"].nunique()
        )

    st.subheader("Missing Values")

    missing_data = (
        logs.isnull()
        .sum()
        .reset_index()
    )

    missing_data.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 11. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #312e81, #6d28d9, #0891b2);
        border-radius: 12px;
        color: white;
    ">
        <h4 style="color:white;">
            🛡️ Web Application Firewall Rule Recommendation
        </h4>
        <p>Using Association-Rule Mining</p>
        <p>Artificial Intelligence & Data Science</p>
    </div>
    """,
    unsafe_allow_html=True
)
