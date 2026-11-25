import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Food Ordering Trends", page_icon="🍔", layout="wide")
st.title("🍔 Food Ordering Behaviour & Consumer Trends")
st.caption("Explore customer choices, spending patterns, platform preferences and delivery experience.")

@st.cache_data
def load_data(uploaded):
    if uploaded is not None:
        return pd.read_csv(uploaded)
    return pd.read_csv(Path(__file__).parent / "data" / "food_orders_sample.csv")

uploaded = st.sidebar.file_uploader("Upload your own CSV (optional)", type=["csv"])
try:
    raw = load_data(uploaded)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

required = ["order_id","order_date","city","age_group","food_category","platform","order_time",
            "order_amount","payment_method","delivery_minutes","rating","orders_per_month"]
missing = [c for c in required if c not in raw.columns]
if missing:
    st.error("CSV is missing required columns: " + ", ".join(missing))
    st.stop()

data = raw.copy()
data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
for c in ["order_amount","delivery_minutes","rating","orders_per_month"]:
    data[c] = pd.to_numeric(data[c], errors="coerce")
before = len(data)
data = data.drop_duplicates()
for c in ["city","age_group","food_category","platform","order_time","payment_method"]:
    data[c] = data[c].astype("string").str.strip().replace("", pd.NA)
for c in ["order_amount","delivery_minutes","rating","orders_per_month"]:
    data[c] = data[c].fillna(data[c].median())
for c in ["city","age_group","food_category","platform","order_time","payment_method"]:
    data[c] = data[c].fillna("Unknown")
data = data.dropna(subset=["order_date"])

st.sidebar.header("Filters")
cities = sorted(data["city"].dropna().unique())
selected_cities = st.sidebar.multiselect("City", cities, default=cities)
platforms = sorted(data["platform"].dropna().unique())
selected_platforms = st.sidebar.multiselect("Platform", platforms, default=platforms)
categories = sorted(data["food_category"].dropna().unique())
selected_categories = st.sidebar.multiselect("Food category", categories, default=categories)
filtered = data[
    data["city"].isin(selected_cities) &
    data["platform"].isin(selected_platforms) &
    data["food_category"].isin(selected_categories)
]
if filtered.empty:
    st.warning("No records match these filters.")
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total orders", f"{len(filtered):,}")
c2.metric("Average order value", f"₹{filtered.order_amount.mean():,.0f}")
c3.metric("Average rating", f"{filtered.rating.mean():.2f}/5")
c4.metric("Avg. delivery time", f"{filtered.delivery_minutes.mean():.1f} min")

st.subheader("Consumer behaviour")
a,b = st.columns(2)
with a:
    fig = px.bar(filtered["food_category"].value_counts().rename_axis("Food category").reset_index(name="Orders"),
                 x="Food category", y="Orders", title="Most ordered food categories")
    st.plotly_chart(fig, use_container_width=True)
with b:
    p = filtered["platform"].value_counts().rename_axis("Platform").reset_index(name="Orders")
    st.plotly_chart(px.pie(p, names="Platform", values="Orders", title="Platform preference", hole=.35),
                    use_container_width=True)
c,d = st.columns(2)
with c:
    spend = filtered.groupby("age_group", as_index=False)["order_amount"].mean()
    st.plotly_chart(px.bar(spend, x="age_group", y="order_amount", title="Average spend by age group",
                           labels={"order_amount":"Average order value (₹)","age_group":"Age group"}),
                    use_container_width=True)
with d:
    hourly = filtered.groupby("order_time", as_index=False).size().rename(columns={"size":"Orders"})
    order = ["Breakfast","Lunch","Evening","Dinner","Late Night"]
    hourly["order_time"] = pd.Categorical(hourly["order_time"], categories=order, ordered=True)
    hourly = hourly.sort_values("order_time")
    st.plotly_chart(px.bar(hourly, x="order_time", y="Orders", title="Orders by time of day",
                           labels={"order_time":"Time of day"}), use_container_width=True)

st.subheader("Delivery and satisfaction")
e,f = st.columns(2)
with e:
    st.plotly_chart(px.histogram(filtered, x="delivery_minutes", nbins=18,
                                 title="Delivery time distribution", labels={"delivery_minutes":"Minutes"}),
                    use_container_width=True)
with f:
    rating = filtered["rating"].value_counts().sort_index().rename_axis("Rating").reset_index(name="Responses")
    st.plotly_chart(px.bar(rating, x="Rating", y="Responses", title="Customer rating distribution"),
                    use_container_width=True)

st.subheader("Data quality summary")
q1,q2,q3 = st.columns(3)
q1.metric("Rows uploaded", f"{before:,}")
q2.metric("Duplicate rows removed", f"{before-len(raw.drop_duplicates()):,}")
q3.metric("Rows after cleaning", f"{len(data):,}")
st.download_button("Download cleaned data", data.to_csv(index=False).encode("utf-8"),
                   file_name="cleaned_food_orders.csv", mime="text/csv")
st.download_button("Download filtered data", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_food_orders.csv", mime="text/csv")
with st.expander("View filtered records"):
    st.dataframe(filtered, use_container_width=True)

st.info("The included dataset is synthetic sample data for demonstration. Replace it with verified survey or research data before making real-world claims.")
