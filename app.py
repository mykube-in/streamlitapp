import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Upwork Earnings Explorer", layout="wide")
st.title("💸 Upwork Earnings Explorer")

st.markdown("""
Upload your Upwork earnings CSV (with columns `client` and `amount`)  
then filter & visualize total spend per client.
""")

@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    # ensure correct types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df.dropna(subset=["client","amount"])

uploaded_file = st.file_uploader("1. Upload earnings.csv", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)

    # client selector
    clients = df["client"].unique().tolist()
    sel = st.multiselect("2. Pick clients to include", options=clients, default=clients)

    # filter & aggregate
    filtered = df[df["client"].isin(sel)]
    agg = filtered.groupby("client", as_index=False)["amount"].sum().sort_values("amount", ascending=False)

    # show table
    st.subheader("Earnings by Client")
    st.dataframe(agg, use_container_width=True)

    # bar chart
    chart = alt.Chart(agg).mark_bar().encode(
        x=alt.X("amount:Q", title="Total Amount (USD)"),
        y=alt.Y("client:N", sort="-x", title="Client"),
        tooltip=["client","amount"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("👉 Upload a CSV to get started!")
