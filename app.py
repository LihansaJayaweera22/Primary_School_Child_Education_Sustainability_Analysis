import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_data.csv")

# Title
st.title("The Education Gap: Global Children Out of Primary School")

# Description
st.markdown(
    "This dashboard explores global trends in primary school age children who are out of school. "
    "It provides insights into how access to education varies across countries and over time, "
    "helping to highlight areas where educational support and policy action may be needed."
)

# Sidebar filters
st.sidebar.header("Filter Data")

# Country selection
select_all = st.sidebar.checkbox("Select All Countries", value=False)

if select_all:
    selected_countries = sorted(df["Country"].unique())
    st.sidebar.write("All countries selected")
else:
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        sorted(df["Country"].unique()),
        default=[df["Country"].iloc[0]]
    )

# Year range selection
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

year_filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Average children out of school line chart
st.subheader("Average Children Out of School by Year")

avg_df = filtered_df.groupby(
    "Year")["Children_Out_of_School"].mean().reset_index()

fig = px.line(
    avg_df,
    x="Year",
    y="Children_Out_of_School",
    markers=True
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Children Out of School",
    xaxis=dict(tickmode="linear"),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Trend line by countries
st.subheader("Children Out of School Trends by Country")

if not selected_countries:
    st.warning("Please select at least one country to see the trendlines.")
else:
    fig_trends = px.line(
        filtered_df,
        x="Year",
        y="Children_Out_of_School",
        color="Country",
        markers=True,
    )

    fig_trends.update_layout(
        xaxis_title="Year",
        yaxis_title="Children Out of School",
        xaxis=dict(tickmode="linear"),
        hovermode="closest"
    )

    st.plotly_chart(fig_trends, use_container_width=True)
