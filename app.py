import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sleep Habits & Screen Time",
    page_icon="🌙",
    layout="wide"
)

DATA_FILE = "bedtime_screentime_sleep_debt.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["blue_light_filter_active"] = df["blue_light_filter_active"].map(
        {1: "On", 0: "Off"}
    ).fillna("Unknown")
    return df

df = load_data()

st.title("Sleep Habits & Late-Night Screen Time")
st.caption(
    "An exploratory dashboard for understanding patterns between bedtime phone use, "
    "sleep duration, and reported sleep debt. Associations shown here do not establish causation."
)

st.sidebar.header("Filter the dataset")
age_min = int(df["age"].min())
age_max = int(df["age"].max())
age_range = st.sidebar.slider(
    "Age range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)
occupations = sorted(df["occupation_type"].dropna().unique().tolist())
selected_occupations = st.sidebar.multiselect(
    "Occupation type",
    options=occupations,
    default=occupations
)
debt_categories = sorted(df["sleep_debt_category"].dropna().unique().tolist())
selected_debt = st.sidebar.multiselect(
    "Sleep debt category",
    options=debt_categories,
    default=debt_categories
)
filter_options = sorted(df["blue_light_filter_active"].dropna().unique().tolist())
selected_filter = st.sidebar.multiselect(
    "Blue-light filter",
    options=filter_options,
    default=filter_options
)

filtered = df[
    df["age"].between(age_range[0], age_range[1])
    & df["occupation_type"].isin(selected_occupations)
    & df["sleep_debt_category"].isin(selected_debt)
    & df["blue_light_filter_active"].isin(selected_filter)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Please broaden your selections.")
    st.stop()

st.subheader("Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records in view", f"{len(filtered):,}")
c2.metric("Average sleep", f"{filtered['total_sleep_hours'].mean():.2f} hours")
c3.metric("Average bedtime phone use", f"{filtered['bedtime_phone_minutes'].mean():.0f} min")
severe_share = filtered["sleep_debt_category"].astype(str).str.contains(
    "Severe", case=False, na=False
).mean() * 100
c4.metric("Severe sleep debt", f"{severe_share:.1f}%")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Bedtime phone use and sleep duration")
    fig_scatter = px.scatter(
        filtered,
        x="bedtime_phone_minutes",
        y="total_sleep_hours",
        color="sleep_debt_category",
        hover_data=["age", "occupation_type", "primary_bedtime_app"],
        labels={
            "bedtime_phone_minutes": "Bedtime phone use (minutes)",
            "total_sleep_hours": "Total sleep (hours)",
            "sleep_debt_category": "Sleep debt category"
        },
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with right:
    st.subheader("Sleep duration by sleep debt category")
    order = (
        filtered.groupby("sleep_debt_category")["total_sleep_hours"]
        .median().sort_values().index.tolist()
    )
    fig_box = px.box(
        filtered,
        x="sleep_debt_category",
        y="total_sleep_hours",
        color="sleep_debt_category",
        category_orders={"sleep_debt_category": order},
        labels={
            "sleep_debt_category": "Sleep debt category",
            "total_sleep_hours": "Total sleep (hours)"
        }
    )
    st.plotly_chart(fig_box, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    st.subheader("Sleep debt category distribution")
    debt_counts = (
        filtered["sleep_debt_category"].value_counts()
        .rename_axis("Sleep debt category").reset_index(name="Records")
    )
    fig_bar = px.bar(
        debt_counts,
        x="Sleep debt category",
        y="Records",
        color="Sleep debt category",
        labels={"Records": "Number of records"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with right2:
    st.subheader("Sleep patterns by bedtime app")
    app_summary = (
        filtered.groupby("primary_bedtime_app", dropna=False)
        .agg(
            Records=("user_id", "count"),
            Avg_phone_minutes=("bedtime_phone_minutes", "mean"),
            Avg_sleep_hours=("total_sleep_hours", "mean"),
            Avg_fatigue=("next_day_fatigue_score", "mean")
        )
        .reset_index()
        .sort_values("Avg_sleep_hours")
    )
    fig_app = px.bar(
        app_summary,
        x="primary_bedtime_app",
        y="Avg_sleep_hours",
        hover_data=["Records", "Avg_phone_minutes", "Avg_fatigue"],
        labels={
            "primary_bedtime_app": "Primary bedtime app",
            "Avg_sleep_hours": "Average sleep (hours)"
        }
    )
    st.plotly_chart(fig_app, use_container_width=True)

with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sleep_data.csv",
        mime="text/csv"
    )

st.caption(
    "Data source: Kaggle dataset by Samartalwar, “Sleep Debt and Screen Time: "
    "Late Night Phone Habits.” This dashboard presents an uploaded dataset snapshot; "
    "it does not update automatically. Results describe patterns in this dataset and "
    "should not be interpreted as medical advice or proof of cause and effect."
)
