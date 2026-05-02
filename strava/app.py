import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Premium Fitness Dashboard", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
body { background-color: #0B1120; color: white; }
.block-container { padding-top: 2rem; }
[data-testid="stMetricValue"] { color: #10B981; }
h1, h2, h3 { color: #E5E7EB; }
.stSidebar { background-color: #020617; }
</style>
""", unsafe_allow_html=True)

st.title("🏃 Premium Fitness Dashboard")

# ---------------- AI FUNCTION ----------------
def generate_insights(df):
    insights = []

    if 'TotalSteps' in df.columns:
        avg_steps = df['TotalSteps'].mean()
        max_steps = df['TotalSteps'].max()

        if avg_steps < 5000:
            insights.append("⚠️ Users are inactive")
        elif avg_steps < 8000:
            insights.append("🙂 Moderate activity")
        else:
            insights.append("🔥 Highly active users")

        insights.append(f"🏆 Peak steps: {int(max_steps)}")

    if 'Calories' in df.columns:
        insights.append(f"🔥 Avg calories: {int(df['Calories'].mean())}")

    return insights

# ---------------- DATABASE ----------------
@st.cache_data
def load_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Atharva#1818",
            database="fitness_analysis"
        )

        df = pd.read_sql("SELECT * FROM fitness_data", conn)

        try:
            sleep_df = pd.read_sql("SELECT * FROM sleepDay_merged", conn)
        except:
            sleep_df = pd.DataFrame()

        try:
            weight_df = pd.read_sql("SELECT * FROM weightloginfo_merged", conn)
        except:
            weight_df = pd.DataFrame()

        conn.close()
        return df, sleep_df, weight_df

    except Exception as e:
        st.error(f"Database Error: {e}")
        return None, None, None


df, sleep_df, weight_df = load_data()

if df is None or df.empty:
    st.stop()

# ---------------- CLEAN DATA ----------------
if 'ActivityDate_New' in df.columns:
    df['ActivityDate_New'] = pd.to_datetime(df['ActivityDate_New'], errors='coerce')

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Dashboard Menu")

page = st.sidebar.radio("Select Page", ["Activity", "Sleep", "Weight"])

users = st.sidebar.multiselect(
    "Select Users",
    df['Id'].dropna().unique(),
    default=df['Id'].dropna().unique()
)

filtered_df = df[df['Id'].isin(users)]

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['ActivityDate_New'].min(), df['ActivityDate_New'].max()]
)

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['ActivityDate_New'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['ActivityDate_New'] <= pd.to_datetime(date_range[1]))
    ]

# ===================== ACTIVITY =====================
if page == "Activity":

    st.header("📈 Activity Dashboard")

    # AI Insights
    st.subheader("🤖 AI Insights")
    insights = generate_insights(filtered_df)
    for i in insights:
        st.success(i)

    # Recommendation
    st.subheader("📈 Recommendation")
    if 'TotalSteps' in filtered_df.columns:
        if filtered_df['TotalSteps'].mean() < 8000:
            st.warning("Increase steps to 8000+")
        else:
            st.success("Great activity level!")

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Steps", int(filtered_df['TotalSteps'].mean()) if 'TotalSteps' in filtered_df else 0)
    col2.metric("Avg Calories", int(filtered_df['Calories'].mean()) if 'Calories' in filtered_df else 0)
    col3.metric("Max Steps", int(filtered_df['TotalSteps'].max()) if 'TotalSteps' in filtered_df else 0)
    col4.metric("Users", filtered_df['Id'].nunique())

    st.markdown("---")

    # Steps Trend
    if 'TotalSteps' in filtered_df.columns:
        fig, ax = plt.subplots()
        sns.lineplot(
            data=filtered_df.sort_values("ActivityDate_New"),
            x="ActivityDate_New",
            y="TotalSteps",
            ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Activity Level
    if 'ActivityLevel' in filtered_df.columns:
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x="ActivityLevel", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ ActivityLevel column not found")

    # Scatter
    if 'TotalSteps' in filtered_df.columns and 'Calories' in filtered_df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x="TotalSteps", y="Calories", ax=ax)
        st.pyplot(fig)

# ===================== SLEEP =====================
elif page == "Sleep":

    st.header("😴 Sleep Dashboard")

    if not sleep_df.empty:

        col1, col2 = st.columns(2)

        if 'TotalMinutesAsleep' in sleep_df.columns:
            col1.metric("Avg Sleep", int(sleep_df['TotalMinutesAsleep'].mean()))

        if 'TotalTimeInBed' in sleep_df.columns:
            eff = sleep_df['TotalMinutesAsleep'].sum() / sleep_df['TotalTimeInBed'].sum()
            col2.metric("Efficiency", round(eff, 2))

        fig, ax = plt.subplots()
        sns.histplot(sleep_df['TotalMinutesAsleep'], bins=20, ax=ax)
        st.pyplot(fig)

# ===================== WEIGHT =====================
elif page == "Weight":

    st.header("⚖️ Weight Dashboard")

    if not weight_df.empty:

        col1, col2 = st.columns(2)

        if 'WeightKg' in weight_df.columns:
            col1.metric("Avg Weight", round(weight_df['WeightKg'].mean(), 2))

        if 'BMI' in weight_df.columns:
            col2.metric("Avg BMI", round(weight_df['BMI'].mean(), 2))

        fig, ax = plt.subplots()
        sns.histplot(weight_df['WeightKg'], bins=10, ax=ax)
        st.pyplot(fig)

# ---------------- DOWNLOAD ----------------
st.sidebar.markdown("---")
st.sidebar.download_button(
    "⬇ Download Data",
    filtered_df.to_csv(index=False),
    file_name="fitness_data.csv"
)