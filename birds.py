import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3



# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Bird Species Dashboard", layout="wide")

# -------------------- TITLE --------------------
st.title("🐦 Bird Species Observation Insight")

# -------------------- IMAGE --------------------
st.image("https://images.unsplash.com/photo-1501706362039-c6e80948bb0e", use_container_width=True)

st.markdown("### 📊 Analyze bird species data using filters, charts, and SQL queries")

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:

    # Load data
    df = pd.read_csv(uploaded_file)

    # Show dataset
    st.subheader("📄 Dataset Preview")
    st.write(df.head())

    st.write("Columns:", df.columns.tolist())

    # -------------------- SIDEBAR FILTERS --------------------
    st.sidebar.header("🔍 Filters")

    # Species filter
    if "species" in df.columns:
        species = st.sidebar.multiselect(
            "Select Species", df["species"].unique(), default=df["species"].unique()
        )
        df = df[df["species"].isin(species)]

    # Location filter
    if "location" in df.columns:
        location = st.sidebar.multiselect(
            "Select Location", df["location"].unique(), default=df["location"].unique()
        )
        df = df[df["location"].isin(location)]

    # -------------------- KPI METRICS --------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Observations", len(df))

    with col2:
        if "species" in df.columns:
            st.metric("Unique Species", df["species"].nunique())

    with col3:
        if "location" in df.columns:
            st.metric("Locations", df["location"].nunique())

    # -------------------- CHARTS --------------------

    col1, col2 = st.columns(2)

    # Species Count
    if "species" in df.columns:
        with col1:
            st.subheader("📊 Species Distribution")
            fig, ax = plt.subplots()
            df["species"].value_counts().plot(kind="bar", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    # Location Count
    if "location" in df.columns:
        with col2:
            st.subheader("📍 Location Analysis")
            fig, ax = plt.subplots()
            df["location"].value_counts().plot(kind="bar", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    # -------------------- TIME ANALYSIS --------------------
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["month"] = df["date"].dt.month

        st.subheader("📅 Monthly Observations")

        fig, ax = plt.subplots()
        df.groupby("month").size().plot(ax=ax)
        st.pyplot(fig)

    # -------------------- SQL SECTION --------------------
    st.subheader("🧠 Run SQL Queries")

    conn = sqlite3.connect(":memory:")
    df.to_sql("birds", conn, index=False, if_exists="replace")

    query1 = st.text_area("1)Enter SQL Query to View dataset", "SELECT year, COUNT(*) AS total_observations FROM birds GROUP BY year;")

    if st.button("Run Query1"):
        try:
            result = pd.read_sql_query(query1, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query2= st.text_area("2)Enter SQL Query to find Total observations", "SELECT COUNT(*) AS total_records FROM birds ;") 
    if st.button("Run Query2"):
        try:
            result = pd.read_sql_query(query2, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")  

    query3= st.text_area("3)Enter SQL Query to find Unique bird species", "SELECT DISTINCT Common_Name FROM birds;") 
    if st.button("Run Query3"):
        try:
            result = pd.read_sql_query(query3, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}") 

    query4= st.text_area("4)Enter SQL Query to find Total number of species", "SELECT COUNT(DISTINCT Common_Name) AS total_species FROM birds;") 
    if st.button("Run Query4"):
        try:
            result = pd.read_sql_query(query4, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}") 

    query5= st.text_area("5)Enter SQL Query to find Most observed bird species", " SELECT Common_Name, COUNT(*) AS total FROM birds GROUP BY Common_Name ORDER BY total DESC LIMIT 1;") 
    if st.button("Run Query5"):
        try:
            result = pd.read_sql_query(query5, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query6= st.text_area("6)Enter SQL Query to find Top 10 most observed birds", " SELECT Common_Name, COUNT(*) AS total FROM birds GROUP BY Common_Name ORDER BY total DESC LIMIT 1;") 
    if st.button("Run Query6"):
        try:
            result = pd.read_sql_query(query6, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")
                          
    
    query7= st.text_area("7)Enter SQL Query to find Least observed species", "SELECT Common_Name, COUNT(*) AS total FROM birds GROUP BY Common_Name ORDER BY total ASC LIMIT 5;") 
    if st.button("Run Query7"):
        try:
            result = pd.read_sql_query(query7, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query8= st.text_area("8)Enter SQL Query to find Observations per site", "SELECT Site_Name, COUNT(*) AS total FROM birds GROUP BY Site_Name ORDER BY total DESC;") 
    if st.button("Run Query8"):
        try:
            result = pd.read_sql_query(query8, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query9= st.text_area("9)Enter SQL Query to find Observations per plot", "SELECT Plot_Name, COUNT(*) AS total FROM birds GROUP BY Plot_Name;") 
    if st.button("Run Query9"):
        try:
            result = pd.read_sql_query(query9, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query10= st.text_area("10)Enter SQL Query to find Species distribution by location type", "SELECT Location_Type, Common_Name, COUNT(*) AS count FROM birds GROUP BY Location_Type, Common_Name ORDER BY Location_Type;") 
    if st.button("Run Query10"):
        try:
            result = pd.read_sql_query(query10, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query11= st.text_area("11)Enter SQL Query to find Observations per year", "SELECT Year, COUNT(*) AS total FROM birds GROUP BY Year ORDER BY Year;") 
    if st.button("Run Query11"):
        try:
            result = pd.read_sql_query(query11, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query12= st.text_area("12)Enter SQL Query to find Observations per day ", "SELECT Date, COUNT(*) AS total FROM birds GROUP BY Date ORDER BY Date;") 
    if st.button("Run Query12"):
        try:
            result = pd.read_sql_query(query12, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query13= st.text_area("13)Enter SQL Query Peak observation year", "SELECT Year, COUNT(*) AS total FROM birds GROUP BY Year ORDER BY total DESC LIMIT 1;") 
    if st.button("Run Query13"):
        try:
            result = pd.read_sql_query(query13, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    
    query14= st.text_area("14)Enter SQL Query to find Average temperature during observations", "SELECT AVG(Temperature) AS avg_temp FROM birds;") 
    if st.button("Run Query14"):
        try:
            result = pd.read_sql_query(query14, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query15= st.text_area("15)Enter SQL Query to find Bird observations by weather (Sky condition)", "SELECT Sky, COUNT(*) AS total FROM birds GROUP BY Sky;") 
    if st.button("Run Query15"):
        try:
            result = pd.read_sql_query(query15, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query16= st.text_area("16)Enter SQL Query to find Wind impact on observations", "SELECT Wind, COUNT(*) AS total FROM birds GROUP BY Wind;") 
    if st.button("Run Query16"):
        try:
            result = pd.read_sql_query(query16, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query17= st.text_area("17)Enter SQL Query to find Observations per observer", "SELECT Observer, COUNT(*) AS total FROM birds GROUP BY Observer ORDER BY total DESC;") 
    if st.button("Run Query17"):
        try:
            result = pd.read_sql_query(query17, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query18= st.text_area("18)Enter SQL Query to find Flyover vs non-flyover observations", "SELECT Flyover_Observed, COUNT(*) AS total FROM birds GROUP BY Flyover_Observed;") 
    if st.button("Run Query18"):
        try:
            result = pd.read_sql_query(query18, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")
    
    query19= st.text_area("19)Enter SQL Query Birds observed in first 3 minutes", "SELECT Initial_Three_Min_Cnt, COUNT(*) AS total FROM birds GROUP BY Initial_Three_Min_Cnt;") 
    if st.button("Run Query19"):
        try:
            result = pd.read_sql_query(query19, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query20= st.text_area("20)Enter SQL Query to find Birds observed in a specific year", "SELECT * FROM birds WHERE Year = 2020;") 
    if st.button("Run Query20"):
        try:
            result = pd.read_sql_query(query20, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    
    query21= st.text_area("21)Enter SQL Query to find Observations in forest-type locations", "SELECT * FROM birds WHERE Location_Type = 'Forest';") 
    if st.button("Run Query21"):
        try:
            result = pd.read_sql_query(query21, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query22= st.text_area("22)Enter SQL Query to find Species observed in multiple sites", "SELECT Common_Name FROM birds GROUP BY Common_Name HAVING COUNT(DISTINCT Site_Name) > 1") 
    if st.button("Run Query22"):
        try:
            result = pd.read_sql_query(query22, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query23= st.text_area("23)Enter SQL Query to find Rank species by observations", "SELECT Common_Name,COUNT(*) AS total,RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_position FROM birds GROUP BY Common_Name;") 
    if st.button("Run Query23"):
        try:
            result = pd.read_sql_query(query23, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query24= st.text_area("24)Enter SQL Query to find most active observer per year", "SELECT Year, Observer, COUNT(*) AS total FROM birds GROUP BY Year, Observer ORDER BY Year, total DESC;") 
    if st.button("Run Query24"):
        try:
            result = pd.read_sql_query(query24, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query25= st.text_area("25)Enter SQL Query to find missing values", "SELECT * FROM birds WHERE Common_Name IS NULL OR Site_Name IS NULL OR Date IS NULL;") 
    if st.button("Run Query25"):
        try:
            result = pd.read_sql_query(query25, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query26= st.text_area("26)Enter SQL Query to find which species are common in which location","SELECT Location_Type, Common_Name, COUNT(*) AS total FROM birds GROUP BY Location_Type, Common_Name ORDER BY Location_Type, total DESC;") 
    if st.button("Run Query26"):
        try:
            result = pd.read_sql_query(query26, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

           
    query27= st.text_area("27)Enter SQL Query to find which species are common in which location","SELECT Sex, COUNT(*) FROM birds GROUP BY Sex;") 
    if st.button("Run Query27"):
        try:
            result = pd.read_sql_query(query27, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query28= st.text_area("28)Enter SQL Query to find Most active observation time (Start Time)","SELECT Start_Time, COUNT(*) AS activity_count FROM birds GROUP BY Start_Time ORDER BY activity_count DESC;") 
    if st.button("Run Query28"):
        try:
            result = pd.read_sql_query(query28, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    query29= st.text_area("29)Enter SQL Query to How temperature affects bird sightings","SELECT temperature, COUNT(*) AS sightings FROM birds GROUP BY temperature ORDER BY temperature;") 
    if st.button("Run Query29"):
        try:
            result = pd.read_sql_query(query29, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    #query30= st.text_area("30)Enter SQL Query to show species at risk","SELECT * FROM birds WHERE PIF_Watchlist_Status='TRUE';") 
    #if st.button("Run Query30"):
        #try:
            #result = pd.read_sql_query(query30, conn)
            #st.write(result)
        #except Exception as e:
            #st.error(f"Error: {e}")

    query30= st.text_area("30)Enter SQL Query to show Observer analysis","SELECT Observer,COUNT(*) AS observations FROM birds GROUP BY Observer ORDER BY observations DESC;") 
    if st.button("Run Query30"):
        try:
            result = pd.read_sql_query(query30, conn)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

    # -------------------- DOWNLOAD --------------------
    st.subheader("⬇ Download Filtered Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

else:
    st.warning("Please upload a CSV file to start analysis")


# Page config
st.set_page_config(page_title="Bird Species Dashboard", layout="wide")

# Title
st.title("🐦 Bird Species Observation Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Bird_Monitoring_Data_Combined.csv")
    return df

df = load_data()

# Data Cleaning
df = df.dropna(subset=['common_name', 'habitat'])
df['Bird Count'] = df['initial_three_min_cnt']

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Habitat filter
habitat = st.sidebar.multiselect(
    "Select Habitat",
    options=df["habitat"].unique(),
    default=df["habitat"].unique()
)

#Species filter
species = st.sidebar.multiselect(
    "Select Species",
    options=df["common_name"].dropna().unique(),
    default=None
)


# Apply Filters
filtered_df = df[df["habitat"].isin(habitat)]

if species:
    filtered_df = filtered_df[filtered_df["common_name"].isin(species)]

# KPIs
total_birds = int(filtered_df['Bird Count'].sum())
total_species = filtered_df['common_name'].nunique()
total_obs = filtered_df.shape[0]
#col4.metric("Total Locations", filtered_df["site_name"].nunique())
total_locations=filtered_df["site_name"].nunique()

col1, col2, col3, col4= st.columns(4)

col1.metric("Total Birds", total_birds)
col2.metric("Total Species", total_species)
col3.metric("Total Observations", total_obs)
col4.metric("Total Locations", total_locations)

# --- Charts ---

# 1. Species Distribution
st.subheader("Top Bird Species")

top_species = (
    filtered_df.groupby('common_name')['Bird Count']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
sns.barplot(x=top_species.values, y=top_species.index, ax=ax1)
st.pyplot(fig1)

# 2. Habitat Analysis
st.subheader("🌿 Habitat Distribution")

habitat_data = filtered_df.groupby('habitat')['Bird Count'].sum()

fig2, ax2 = plt.subplots()
ax2.pie(habitat_data, labels=habitat_data.index, autopct='%1.1f%%')
st.pyplot(fig2)

# 3. Trend Over Time
st.subheader("Bird Observation Trend")

filtered_df["date"] = pd.to_datetime(filtered_df["date"], errors='coerce')
filtered_df["month"] = filtered_df["date"].dt.month

monthly = filtered_df["month"].value_counts().sort_index()

fig3, ax3 = plt.subplots()
monthly.plot(kind="line", marker='o', ax=ax3)
ax3.set_xlabel("month")
ax3.set_ylabel("Observations")
st.pyplot(fig3)


# 4. Temperature Impact
st.subheader("Temperature vs Bird Count")

temp_trend = filtered_df.groupby('temperature')['Bird Count'].mean()

fig, ax = plt.subplots()
temp_trend.plot(ax=ax)

ax.set_title("Average Bird Count vs Temperature")
st.pyplot(fig)

st.subheader("Bird Sightings Over Time")
df['date'] = pd.to_datetime(df['date'])
trend = df.groupby('date').size()
fig3, ax3 = plt.subplots()
trend.plot(ax=ax3)
st.pyplot(fig3)

st.subheader("Bird Count by Location")
fig4, ax4 = plt.subplots()
df['location_type'].value_counts().plot(kind='bar', ax=ax4)
st.pyplot(fig4)


st.subheader("Temperature Range vs Bird Activity")
df['temp_range'] = pd.cut(df['temperature'], bins=[0,20,25,30,35,40])
fig, ax = plt.subplots()
sns.boxplot(data=df, x='temp_range', y='Bird Count', ax=ax)
st.pyplot(fig)

st.subheader("Humidity vs Bird Count")
fig7, ax7 = plt.subplots()
sns.lineplot(data=df, x='humidity', y='Bird Count', ax=ax7)
st.pyplot(fig7)

# 13. Heatmap
st.subheader("Correlation Heatmap")
fig13, ax13 = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax13)
st.pyplot(fig13)

#get season 
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8]:
        return 'Monsoon'
    else:
        return 'Autumn'

df['season'] = df['date'].dt.month.apply(get_season)

#14. Season Analysis
st.subheader("Bird Count by Season")
fig14, ax14 = plt.subplots()
df.groupby('season')['Bird Count'].sum().plot(kind='bar', ax=ax14)
st.pyplot(fig14)

st.subheader("Weather Condition vs Bird Count")
fig8, ax8 = plt.subplots()
df.groupby('sky')['Bird Count'].sum().plot(kind='bar', ax=ax8)
st.pyplot(fig8)
#fig4, ax4 = plt.subplots()
#sns.scatterplot(data=filtered_df, x='temperature', y='Bird Count', ax=ax4)
#st.pyplot(fig4)
