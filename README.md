# 🛵 Food Delivery Times Dashboard

An interactive dashboard to analyze factors influencing **food delivery times**. 

Built using **Python, Pandas, Plotly, and Streamlit**.

**Live App:** [Food Delivery Times on Streamlit Cloud]([https://food-delivery-dashboard-xxxx.streamlit.app](https://food-delivery-dashboard-tzy6so9mrptelica2fnfpc.streamlit.app/))

##  Project Background
This project aims to understand the patterns, trends, and key factors that influence food delivery times.
This analysis can be used to help logistics/delivery companies improve **operational efficiency**.

## Business Problem
- What are the main factors that influence food delivery times?
- How do weather conditions, traffic, vehicle type, and courier experience affect delivery performance?
- How can data be used to provide strategic recommendations?

## Dataset
Dataset: **Food_Delivery_Times** 

Key Features:

- Order_ID: Unique identifier for each order.

- Distance_km: The delivery distance in kilometers.

- Weather: Weather conditions during the delivery, including Clear, Rainy, Snowy, Foggy, and Windy.

- Traffic_Level: Traffic conditions categorized as Low, Medium, or High.

- Time_of_Day: The time when the delivery took place, categorized as Morning, Afternoon, Evening, or Night.

- Vehicle_Type: Type of vehicle used for delivery, including Bike, Scooter, and Car.

- Preparation_Time_min: The time required to prepare the order, measured in minutes.

- Courier_Experience_yrs: Experience of the courier in years.

- Delivery_Time_min: The total delivery time in minutes (target variable).

## Data Analysis and Insights
- The distribution of delivery times is predominantly between **40 and 70 minutes**.
- **Distance** has the strongest correlation with delivery time.
- **Bad weather** (snowy, rainy) and **high traffic** increase delivery times.
- **Courier experience** has a small effect, but there is a downward trend with increasing experience.

## Dashboards and Visualizations
- **Delivery time distribution** (histogram)
- **Boxplot** for weather, traffic, time, and vehicle type
- **Scatterplot with trendline** (Distance vs. Delivery Time)
- **Numerical correlation heatmap**

## Recommendation
- Use **p50/p90 (median & 90th percentile)** as a realistic SLA.
- Increase your fleet of vehicles in long-distance and high-traffic areas.
- Anticipate delays due to bad weather with **dynamic ETA adjustment**.
- Optimize order preparation time to avoid delays in delivery.

## Run Locally
Clone this repo:
```bash
git clone https://github.com/username/FOOD-DELIVERY-DASHBOARD.git
cd FOOD-DELIVERY-DASHBOARD
- **Filterable & exportable table**
