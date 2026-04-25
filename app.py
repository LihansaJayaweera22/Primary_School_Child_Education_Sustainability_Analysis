import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_data.csv")

st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)),
        url("https://images.unsplash.com/photo-1610500796385-3ffc1ae2f046?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("The Education Gap: Global Children Out of Primary School")

# Description
st.markdown("This dashboard explores global trends in primary school age children who are out of school. It provides insights into how access to education varies across countries and over time, helping to highlight areas where educational support and policy action may be needed.")

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
        default=[df["Country"].iloc[0]])

# Year range selection
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max())))

filtered_df = df[(df["Country"].isin(selected_countries)) & (
    df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

year_filtered_df = df[(df["Year"] >= year_range[0]) &
                      (df["Year"] <= year_range[1])]

st.subheader("Key Insights")

col1, col2, col3, col4 = st.columns(4)

countries_count = df["Country"].nunique()
avg_value = int(df["Children_Out_of_School"].mean())

max_country = (df.groupby("Country")["Children_Out_of_School"].mean().idxmax())

latest_year = df["Year"].max()

latest_avg = int(df[df["Year"] == latest_year]
                 ["Children_Out_of_School"].mean())

col1.metric("Countries", countries_count)
col2.metric("Average", f"{avg_value:,}")
col3.metric("Highest Country", max_country)
col4.metric("Latest Year Avg", f"{latest_avg:,}")

# Average children out of school line chart
st.subheader("Average Children Out of School by Year")

avg_df = year_filtered_df.groupby(
    "Year")["Children_Out_of_School"].mean().reset_index()

fig = px.line(
    avg_df,
    x="Year",
    y="Children_Out_of_School",
    markers=True)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Children Out of School",
    xaxis=dict(tickmode="linear"),
    hovermode="x unified")

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
        markers=True,)

    fig_trends.update_layout(
        xaxis_title="Year",
        yaxis_title="Children Out of School",
        xaxis=dict(tickmode="linear"),
        hovermode="closest")

    st.plotly_chart(fig_trends, use_container_width=True)

# Top 10 countries with highest children out of school
st.subheader("Top 10 Countries with Highest Children Out of School")

top10_df = (year_filtered_df.groupby("Country")["Children_Out_of_School"].mean(
).reset_index().sort_values("Children_Out_of_School", ascending=False).head(10))

fig_top10 = px.bar(
    top10_df,
    x="Children_Out_of_School",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Average Children Out of School",
    labels={"Children_Out_of_School": "Average Children Out of School", "Country": "Country"})

fig_top10.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title="Average Children Out of School",
    margin=dict(l=150, r=20, t=60, b=40),)

st.plotly_chart(fig_top10, use_container_width=True)

# World map showing average children out of school
st.subheader("Global Distribution of Children Out of Primary School")

# Aggregating by country
dot_map_df = (year_filtered_df.groupby("Country")[
              "Children_Out_of_School"].mean().reset_index())

# Create a Scatter Geo map
fig_dots = px.scatter_geo(
    dot_map_df,
    locations="Country",
    locationmode="country names",
    size="Children_Out_of_School",
    hover_name="Country",
    template="plotly_dark",
    color_discrete_sequence=["#ff4b4b"])
fig_dots.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        bgcolor="rgb(17, 17, 17)",
        showland=True,
        landcolor="rgb(35, 35, 35)",
        showocean=True,
        oceancolor="rgb(10, 10, 10)"))
st.plotly_chart(fig_dots, use_container_width=True)

# Children out of school distribution histogram
st.subheader("Distribution of Children Out of School")

fig = px.histogram(
    year_filtered_df,
    x="Children_Out_of_School",
    nbins=30,
    labels={"Children_Out_of_School": "Children Out of School",
            "count": "Number of Countries"},
    color_discrete_sequence=["#636EFA"])

fig.update_layout(
    xaxis_title="Children Out of School",
    yaxis_title="Number of Countries",
    bargap=0.1,
    template="plotly_white",
    margin=dict(l=40, r=40, t=80, b=40))

st.plotly_chart(fig, use_container_width=True)

# Top 10 countries with lowest children out of school
st.subheader("Top 10 Countries with Lowest Children Out of School")

low10_df = (year_filtered_df.groupby("Country")["Children_Out_of_School"].mean(
).reset_index().sort_values("Children_Out_of_School", ascending=True).head(10))

fig_low10 = px.bar(
    low10_df,
    x="Children_Out_of_School",
    y="Country",
    orientation="h",
    labels={"Children_Out_of_School": "Average Children Out of School", "Country": "Country"})

fig_low10.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title="Average Children Out of School",
    margin=dict(l=150, r=20, t=60, b=40),)

st.plotly_chart(fig_low10, use_container_width=True)
