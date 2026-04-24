import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_data.csv")

st.title("The Education Gap: Global Children Out of Primary School")
st.markdown(
    "This dashboard explores global trends in primary school age children who are out of school. "
    "It provides insights into how access to education varies across countries and over time, "
    "helping to highlight areas where educational support and policy action may be needed."
)

st.sidebar.header("Filter Data")
country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["Country"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[
    (df["Country"] == country) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]
year_filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

avg_df = year_filtered_df.groupby(
    "Year")["Children_Out_of_School"].mean().reset_index()
st.subheader("Average Children Out of School by Year")

fig = px.line(
    avg_df,
    x="Year",
    y="Children_Out_of_School",
    markers=True,
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Children Out of School",
    xaxis=dict(tickmode='linear'),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
