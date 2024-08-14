import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.tools as tls
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import altair as alt
import streamlit_shadcn_ui as ui
import os
import mysql.connector


st.set_page_config(page_title="ADVERTISING CHANNEL ANALYSIS", page_icon="", layout="wide")

# Initialize connection
conn = st.connection('mysql', type='sql')

# Function to fetch data from the database
def view_all_data():
    query = 'SELECT * FROM dashboard_analytics.combined_data;'
    data = conn.query(query, ttl=600)  # Cached for 10 minutes
    return data


data = view_all_data()
df = pd.DataFrame(data, columns=['Campaign_ID', 'Date_Time', 'Platform_Type', 'Impressions', 'Clicks', 'Conversions', 'Tracked_Ads', 'Cost', 'Revenue', 'Average_Frequency', 'Audience_Reach', 'Unique_Reach', 'On_Target_Impressions', 'Audience_Efficiency_Rate', 'Percentage_On_Target'])

# Display caption in the sidebar
st.sidebar.caption("Advertising campaigns analytics")

# Sidebar filters
st.sidebar.header("Please Filter")
campaignID = st.sidebar.multiselect(
    "Select Campaign ID",
    options=df["Campaign_ID"].unique(),
    default=df["Campaign_ID"].unique(),
)
platformType = st.sidebar.multiselect(
    "Select Platform",
    options=df["Platform_Type"].unique(),
    default=df["Platform_Type"].unique(),
)
date_range = st.sidebar.selectbox("Date Range", ["Daily", "Weekly", "Monthly"])

def Home():
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])

    if date_range == "Daily":
        filtered_df = df[(df["Date_Time"].dt.date == df["Date_Time"].dt.date.max()) &
                         (df["Campaign_ID"].isin(campaignID)) &
                         (df["Platform_Type"].isin(platformType))]
    elif date_range == "Weekly":
        filtered_df = df[(df["Date_Time"].dt.isocalendar().week == df["Date_Time"].dt.isocalendar().week.max()) &
                         (df["Campaign_ID"].isin(campaignID)) &
                         (df["Platform_Type"].isin(platformType))]
    elif date_range == "Monthly":
        filtered_df = df[(df["Date_Time"].dt.month == df["Date_Time"].dt.month.max()) &
                         (df["Campaign_ID"].isin(campaignID)) &
                         (df["Platform_Type"].isin(platformType))]
    
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', filtered_df.columns, default=[])
        st.write(filtered_df[showData])

    # Calculate the metrics
    audience_size = 10000
    # Calculate the Audience Reach as a percentage
    filtered_df['Audience Reach %'] = (filtered_df['Audience_Reach'] / audience_size) * 100

    # Display the updated DataFrame
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.info("Audience Reach %")
        st.metric(label="", value=f"{filtered_df['Audience Reach %'].iloc[0]:.2f}%", delta=f"{filtered_df['Audience Reach %'].mean():.2f}%")
    with col2:
        st.info("Avg Frequency") 
        st.metric(label="", value=f"{filtered_df['Average_Frequency'].iloc[0]:.2f}%", delta=f"{filtered_df['Average_Frequency'].mean():.2f}%")
    with col3:
        st.info("Audience Eff. Rate")
        st.metric(label="", value=f"{filtered_df['Audience_Efficiency_Rate'].iloc[0]:.2f}%", delta=f"{filtered_df['Audience_Efficiency_Rate'].mean():.2f}%")
    with col4:
        st.info("% On Target")
        st.metric(label="", value=f"{filtered_df['Percentage_On_Target'].iloc[0] * 100:.2f}%", delta=f"{filtered_df['Percentage_On_Target'].mean():.2f}%")
    with col5:
        st.info("Tracked Ads")   
        tracked_ads = filtered_df["Tracked_Ads"].iloc[0]
        if tracked_ads >= 1000000000:
            tracked_ads_formatted = f"{tracked_ads/1000000000:.2f}B"
        elif tracked_ads >= 1000000:
            tracked_ads_formatted = f"{tracked_ads/1000000:.2f}M"
        elif tracked_ads >= 1000:
            tracked_ads_formatted = f"{tracked_ads/1000:.2f}K"
        else:
            tracked_ads_formatted = str(int(tracked_ads))
        st.metric(label="", value=tracked_ads_formatted)
    def get_chart_audience_by_platform(use_container_width: bool, filtered_df):
        # Calculate the Audience Reach by Platform
        platform_reach = filtered_df.groupby('Platform_Type')['Audience_Reach'].sum().reset_index()
        total_reach = platform_reach['Audience_Reach'].sum()
        platform_reach['Audience_Percentage'] = (platform_reach['Audience_Reach'] / total_reach) * 100

        # Create the Altair chart
        chart = alt.Chart(platform_reach).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Audience_Percentage", type="quantitative"),
            color=alt.Color(field="Platform_Type", type="nominal"),
            
        )

        return chart, platform_reach

    with st.container():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("% On Target")
            chart, platform_reach = get_chart_audience_by_platform(use_container_width=True, filtered_df=filtered_df)
            st.altair_chart(chart, theme="streamlit", use_container_width=True)

        with col2:
            st.subheader("Progression")
            for _, row in platform_reach.iterrows():
                col2_1, col2_2 = st.columns(2)
                with col2_1:
                    st.write(f"{row['Platform_Type']}: {row['Audience_Percentage']:.2f}%")
                with col2_2:
                    st.progress(row['Audience_Percentage'] / 100)

    # Add your code for the second column here
    platform_data = filtered_df['Platform_Type'].unique()
    st.subheader("Audience Efficiency Rate")
    st.write(":large_blue_circle: Audience Efficiency Rate")
    # Create a grid layout for the donut charts
    cols = st.columns(5)
       
# Create the donut charts
    for i, platform in enumerate(platform_data):
        with cols[i]:
            value = filtered_df.loc[filtered_df['Platform_Type'] == platform, 'Audience_Efficiency_Rate'].iloc[0] * 100
            fig, ax = plt.subplots(figsize=(3, 3))
            colors = sns.color_palette("pastel", 2)
            ax.pie([value, 100 - value], colors=colors, startangle=90, autopct='%1.1f%%', pctdistance=0.85)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            ax.add_artist(centre_circle)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is circular.
            ax.set_title(platform, fontsize=10)
            st.pyplot(fig)

# Call the Home function
Home()



