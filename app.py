import plotly.express as px
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Survey Explorer", layout="wide")
st.title("Student Survey Explorer")
uploaded = st.sidebar.file_uploader("Survey CSV (optional)", type=["csv"])
df = pd.read_csv(uploaded) if uploaded is None else pd.read_csv("survey.csv")

st.caption(f"{len(df)} responses loaded")
tab1, tab2, tab3 = st.tabs(["Overview", "Compare", "Data"])
numeric_ok = pd.api.types.is_numeric_dtype(df["satisfaction"])
if not numeric_ok: st.error("satisfaction must be a number column."); st.stop()
a, b = st.columns(2); a.metric("Responses", len(df)); b.metric("Average satisfaction", f"{df['satisfaction'].mean():.2f}")
st.bar_chart(df.value_counts("satisfaction").sort_values())

group = st.radio("Compare by", ["faculty", "year_of_study"], horizontal=True)
summary = df.groupby(group)["satisfaction"].mean()
fig = px.bar(x=group, y="satisfaction", data=summary)
fig.show()

st.plotly_chart(px.scatter(df, x="study_hours", y="satisfaction", color=group))
query = st.text_input("Search faculty")

shown = df[df["faculty"].str.contains(query, case=False, na=False)]
st.dataframe(shown, hide_index=True); st.caption(f"{len(shown)} matching responses")
st.download_button("Download matches", shown.to_csv(index=False), "matches.csv", "text/csv")
