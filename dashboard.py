# dashboard.py

# library
import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px

# setup page
st.set_page_config(
    page_title="Food Delivery Times Dashboard",
    page_icon="🛵",
    layout="wide",
)

px.defaults.template = "plotly_white" # Plotly default style

# Load data
@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists("Food_Delivery_Times_CLEAN.csv"):
        df = pd.read_csv("Food_Delivery_Times_CLEAN.csv")
        return df, "CLEAN"
    elif os.path.exists("Food_Delivery_Times.csv"):
        # fallback minimal clean
        df = pd.read_csv("Food_Delivery_Times.csv")
        df.columns = [c.strip() for c in df.columns]
        for c in ["Distance_km", "Courier_Experience_yrs", "Delivery_Time_min"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        # english title case normalization 
        def norm(s): return s.astype(str).str.strip().str.lower()
        maps = {
            "Weather": {"sunny":"Sunny","rainy":"Rainy","snowy":"Snowy","foggy":"Foggy","windy":"Windy"},
            "Traffic_Level": {"low":"Low","medium":"Medium","high":"High"},
            "Time_of_Day": {"morning":"Morning","afternoon":"Afternoon","evening":"Evening","night":"Night"},
            "Vehicle_Type": {"bike":"Bike","scooter":"Scooter","car":"Car"},
        }
        for col, mp in maps.items():
            if col in df.columns:
                df[col] = norm(df[col]).map(mp).fillna(df[col])
        df = df[~df["Delivery_Time_min"].isna()].copy()
        # Simple imputation, that the graphics are error free
        for c in ["Distance_km", "Courier_Experience_yrs"]:
            if c in df.columns and df[c].isna().sum() > 0:
                df[c] = df[c].fillna(df[c].median())
        for c in ["Weather","Traffic_Level","Time_of_Day","Vehicle_Type"]:
            if c in df.columns and df[c].isna().sum() > 0:
                m = df[c].mode(dropna=True)
                if len(m): df[c] = df[c].fillna(m.iloc[0])
        return df, "RAW (auto-clean)"
    else:
        st.error("Put 'Food_Delivery_Times_CLEAN.csv' or 'Food_Delivery_Times.csv' in the same folder.")
        st.stop()

df, src = load_data()

needed = ["Delivery_Time_min","Distance_km","Courier_Experience_yrs",
          "Weather","Traffic_Level","Time_of_Day","Vehicle_Type"]
missing = [c for c in needed if c not in df.columns]
if missing:
    st.error(f"Required fields are missing: {missing}")
    st.stop()

# Color palettes
COLOR_WEATHER = {
    "Sunny":  "#FDB813",  # soft yellow-orange
    "Rainy":  "#4C78A8",  # blue
    "Snowy":  "#9EC1CF",  # light blue
    "Foggy":  "#B8B8B8",  # gray
    "Windy":  "#72B7B2",  # teal
}
COLOR_TRAFFIC = {
    "Low":    "#59A14F",  # green
    "Medium": "#F28E2B",  # orange
    "High":   "#E15759",  # red
}
COLOR_TOD = {
    "Morning":   "#7AA6C2",  # light blue
    "Afternoon": "#86BCB6",  # light teal
    "Evening":   "#C4B7D7",  # violet
    "Night":     "#A1A6B4",  # bluish gray

}
COLOR_VEH = {
    "Bike":    "#8CD17D",  # light green
    "Scooter": "#B6992D",  # gold
    "Car":     "#499894",  # teal
}

def palette_for(column):
    return {
        "Weather": COLOR_WEATHER,
        "Traffic_Level": COLOR_TRAFFIC,
        "Time_of_Day": COLOR_TOD,
        "Vehicle_Type": COLOR_VEH,
    }[column]

# Sidebar filters
st.sidebar.markdown("### Filters")
w_opts  = sorted(df["Weather"].dropna().unique())
t_opts  = sorted(df["Traffic_Level"].dropna().unique())
tod_opts= sorted(df["Time_of_Day"].dropna().unique())
v_opts  = sorted(df["Vehicle_Type"].dropna().unique())

weather_sel = st.sidebar.multiselect("Weather", w_opts, default=w_opts)
traffic_sel = st.sidebar.multiselect("Traffic Level", t_opts, default=t_opts)
tod_sel     = st.sidebar.multiselect("Time of Day", tod_opts, default=tod_opts)
vehicle_sel = st.sidebar.multiselect("Vehicle Type", v_opts, default=v_opts)

dist_min, dist_max = float(df["Distance_km"].min()), float(df["Distance_km"].max())
exp_min, exp_max   = float(df["Courier_Experience_yrs"].min()), float(df["Courier_Experience_yrs"].max())
dist_range = st.sidebar.slider("Distance (km)", min_value=0.0, max_value=float(np.ceil(dist_max)),
                               value=(dist_min, dist_max), step=0.5)
exp_range  = st.sidebar.slider("Courier Experience (yrs)",
                               min_value=0.0, max_value=float(np.ceil(max(exp_max,1)) or 1.0),
                               value=(exp_min, exp_max), step=1.0)

dff = df[
    (df["Weather"].isin(weather_sel)) &
    (df["Traffic_Level"].isin(traffic_sel)) &
    (df["Time_of_Day"].isin(tod_sel)) &
    (df["Vehicle_Type"].isin(vehicle_sel)) &
    (df["Distance_km"].between(dist_range[0], dist_range[1])) &
    (df["Courier_Experience_yrs"].between(exp_range[0], exp_range[1]))
].copy()

st.sidebar.success(f"Rows: {len(dff)}")
if dff.empty:
    st.warning("No data after filter. Loosen the filter.")
    st.stop()

    # Header & KPI
st.markdown("## 🛵 Food Delivery Times")
st.caption("Source: Food_Delivery_Times_CLEAN.csv")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean",   f"{dff['Delivery_Time_min'].mean():.1f} min")
c2.metric("Median", f"{dff['Delivery_Time_min'].median():.1f} min")
c3.metric("p90",    f"{dff['Delivery_Time_min'].quantile(0.9):.1f} min")
c4.metric("Count",  f"{len(dff)}")

st.divider()

# Tabs 
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Distribution", "Boxplot", "Scatter + Trendline", "Correlation", "Table"]
)

# 1 Distribution
with tab1:
    left, right = st.columns([2,1])
    with left:
        fig = px.histogram(
            dff, x="Delivery_Time_min", nbins=30, opacity=0.95,
            color_discrete_sequence=["#4C78A8"]  # soft blue
        )
        fig.update_layout(
            title="Distribution of Delivery_Time_min",
            xaxis_title="Delivery Time (minutes)", yaxis_title="Count",
            bargap=0.05, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("**Brief Interpretation**")
        st.write(
            "- Most deliveries are around 40–70 minutes.\n"
            "- The right tail shows the fraction of deliveries >90 minutes.\n"
            "- Use p50/p90 in KPIs for realistic SLAs (Service Level Agreement)."
        )

# 2 Boxplot by Category
with tab2:
    cat = st.selectbox("Select a category:", ["Weather","Traffic_Level","Time_of_Day","Vehicle_Type"])
    palette = palette_for(cat)
    # make sure the legend order is stable
    category_order = sorted(dff[cat].dropna().unique())
    fig2 = px.box(
        dff, x=cat, y="Delivery_Time_min", color=cat,
        category_orders={cat: category_order},
        color_discrete_map=palette
    )
    fig2.update_layout(
        title=f"Delivery Time vs {cat}",
        xaxis_title=cat, yaxis_title="Delivery Time (minutes)",
        legend_title=cat
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3 Scatter + Trendline
with tab3:
    left, right = st.columns([3,2])
    with left:
        xopt = st.selectbox("X axis:", ["Distance_km","Courier_Experience_yrs"], index=0)
        color_by = st.selectbox("Color by (optional):", [None,"Weather","Traffic_Level","Time_of_Day","Vehicle_Type"], index=0)
        if color_by:
            cmap = palette_for(color_by)
            fig3 = px.scatter(
                dff, x=xopt, y="Delivery_Time_min",
                opacity=0.6, trendline="ols",
                color=color_by, color_discrete_map=cmap
            )
        else:
            fig3 = px.scatter(
                dff, x=xopt, y="Delivery_Time_min",
                opacity=0.6, trendline="ols",
                color_discrete_sequence=["#E15759"]  # soft red
            )
        fig3.update_layout(
            title=f"Delivery Time vs {xopt}",
            xaxis_title=xopt, yaxis_title="Delivery Time (minutes)"
        )
        st.plotly_chart(fig3, use_container_width=True)
    with right:
        st.markdown("**Tips for Reading Scatter**")
        if xopt == "Distance_km":
            st.write("- Upward trend line → further distance = longer time (main driver).")
        else:
            st.write("- The trend line tends to be flat/slightly downward → courier experience has little influence.")
        

# 4 Correlation Heatmap
with tab4:
    use_cols = ["Distance_km","Courier_Experience_yrs","Delivery_Time_min"]
    corr = dff[use_cols].corr()
    # safe diverging palette (blue-white-red) for clear contrast
    fig4 = px.imshow(
        corr, text_auto=True, zmin=-1, zmax=1,
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    fig4.update_layout(title="Numerical Correlation Heatmap")
    st.plotly_chart(fig4, use_container_width=True)

# 5 Table
with tab5:
    st.markdown("**Filtered data (top 200 rows for preview)**")
    st.dataframe(dff.head(200), use_container_width=True)
    st.download_button(
        "Download filtered CSV",
        data=dff.to_csv(index=False).encode("utf-8"),
        file_name="filtered_food_delivery_times.csv",
        mime="text/csv"
    )

