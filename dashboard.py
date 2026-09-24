import streamlit as st
import pandas as pd
import requests

import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Sentinel Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #9ca3af;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.status {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background: #123524;
    color: #4ade80;
    font-size: 0.85rem;
    font-weight: 600;
}

.alert-box {
    padding: 15px;
    border-radius: 10px;
    background: #351414;
    border-left: 4px solid #ef4444;
    margin-bottom: 10px;
}

.normal-box {
    padding: 15px;
    border-radius: 10px;
    background: #10291b;
    border-left: 4px solid #22c55e;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)


@st.fragment(run_every="3s")
def dashboard():

    transactions_response = requests.get(
        f"{API_URL}/transactions",
        timeout=5
    )

    stats_response = requests.get(
        f"{API_URL}/stats",
        timeout=5
    )

    transactions_data = transactions_response.json()
    stats_data = stats_response.json()

    df = pd.DataFrame(
        transactions_data["transactions"]
    )

    total = stats_data["total"]
    suspicious = stats_data["suspicious"]
    review = stats_data["review"]
    normal = stats_data["normal"]

    st.markdown(
        '<div class="main-title">🛡️ Sentinel Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Real-time transaction monitoring powered by '
        'Kafka, Isolation Forest and FastAPI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<span class="status">● SYSTEM ONLINE</span>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "TOTAL TRANSACTIONS",
        total
    )

    col2.metric(
        "🚨 SUSPICIOUS",
        suspicious
    )

    col3.metric(
        "⚠️ REVIEW",
        review
    )

    col4.metric(
        "✓ NORMAL",
        normal
    )

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.markdown(
            '<div class="section-title">📈 Risk Activity</div>',
            unsafe_allow_html=True
        )

        if not df.empty:

            chart_data = df[
                ["id", "risk_score"]
            ].set_index("id")

            st.line_chart(
                chart_data,
                height=320
            )

    with right:

        st.markdown(
            '<div class="section-title">🚨 Recent Alerts</div>',
            unsafe_allow_html=True
        )

        if not df.empty:

            alerts = df[
                df["decision"] == "SUSPICIOUS"
            ].head(5)

            if not alerts.empty:

                for _, row in alerts.iterrows():

                    st.markdown(
                        f"""
                        <div class="alert-box">
                        <b>Transaction #{int(row["id"])}</b><br>
                        Amount: ₹{row["amount"]:,.2f}<br>
                        Risk Score: <b>{int(row["risk_score"])}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.markdown(
                    '<div class="normal-box">'
                    '✓ No suspicious transactions detected'
                    '</div>',
                    unsafe_allow_html=True
                )

    st.divider()

    st.markdown(
        '<div class="section-title">💳 Recent Transactions</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        display_df = df.copy()

        display_df["amount"] = display_df[
            "amount"
        ].apply(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["risk_score"] = display_df[
            "risk_score"
        ].astype(int)

        display_df = display_df[
            [
                "id",
                "timestamp",
                "amount",
                "risk_score",
                "decision"
            ]
        ]

        display_df.columns = [
            "Transaction ID",
            "Timestamp",
            "Amount",
            "Risk Score",
            "Decision"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No transactions available.")

    st.caption(
        "🟢 Live monitoring • Automatically refreshed every 3 seconds"
    )


dashboard()