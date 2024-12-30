import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# Title and Sidebar
st.title("Advanced ROI Calculator for Mining Operations")
st.sidebar.header("Input Parameters")

# Input Fields
fleet_size = st.sidebar.number_input("Fleet Size (number of vehicles):", value=50, min_value=1)
fuel_volume = st.sidebar.number_input("Fuel Volume (liters per month):", value=100000, min_value=0)
base_salary = st.sidebar.number_input("Base Salary of Staff (per month in USD):", value=5000, min_value=0)
man_hours_saved = st.sidebar.number_input("Man Hours Saved Per Month (hours):", value=160, min_value=0)
digitization_cost = st.sidebar.number_input("Digitization Cost (USD):", value=20000, min_value=0)
monthly_savings = st.sidebar.number_input("Operational Savings Due to Digitization (USD):", value=5000, min_value=0)
fuel_cost_per_liter = st.sidebar.number_input("Fuel Cost per Liter (USD):", value=1.5, min_value=0.0)
baseline_efficiency = st.sidebar.number_input("Baseline Efficiency (km/l):", value=4.0, min_value=0.0)
improved_efficiency = st.sidebar.number_input("Improved Efficiency (km/l):", value=5.0, min_value=0.0)

# Calculations
if base_salary > 0 and man_hours_saved > 0:
    hourly_rate = base_salary / 160  # Assuming 160 working hours/month
    cost_savings = man_hours_saved * hourly_rate
    fuel_savings = (
        (fuel_volume / baseline_efficiency * fuel_cost_per_liter)
        - (fuel_volume / improved_efficiency * fuel_cost_per_liter)
    )
    total_savings = cost_savings + monthly_savings + fuel_savings
    roi = ((total_savings - digitization_cost) / digitization_cost) * 100
else:
    hourly_rate = cost_savings = fuel_savings = total_savings = roi = 0

# Results Display
st.header("Results")
st.write(f"*Man Hours Saved Per Month:* {man_hours_saved} hours")
st.write(f"*Equivalent Cost Savings:* ${cost_savings:.2f}")
st.write(f"*Fuel Cost Savings:* ${fuel_savings:.2f}")
st.write(f"*Total Savings:* ${total_savings:.2f}")
st.write(f"*ROI on Digitization:* {roi:.2f}%")

# Visualization: Cost Breakdown
st.subheader("Digitization Cost Breakdown")
cost_components = {"Software": 8000, "Hardware": 5000, "Training": 2000, "Implementation": 5000}
fig = px.pie(names=cost_components.keys(), values=cost_components.values(), title="Cost Breakdown")
st.plotly_chart(fig)

# Scenario Comparison
st.subheader("Scenario Comparison")
scenario_data = pd.DataFrame({
    "Scenario": ["Scenario 1", "Scenario 2", "Scenario 3"],
    "Fleet Size": [50, 100, 200],
    "Digitization Cost": [20000, 40000, 60000],
    "ROI (%)": [50, 75, 100]
})
st.table(scenario_data)

# Predictive Analytics
st.subheader("Predictive ROI Based on Fleet Size")
X = np.array([50, 100, 150, 200]).reshape(-1, 1)  # Training fleet sizes
y = np.array([10, 20, 30, 40])  # Corresponding ROI values
model = LinearRegression().fit(X, y)
predicted_roi = model.predict([[fleet_size]])
st.write(f"*Predicted ROI for a fleet size of {fleet_size}:* {predicted_roi[0]:.2f}%")

# Export Results
st.subheader("Export Results")
results_data = {
    "Parameter": ["Fleet Size", "Fuel Volume", "Base Salary", "Man Hours Saved",
                  "Digitization Cost", "Monthly Savings", "Fuel Savings", "ROI (%)"],
    "Value": [fleet_size, fuel_volume, base_salary, man_hours_saved, digitization_cost,
              monthly_savings, fuel_savings, roi]
}
results_df = pd.DataFrame(results_data)
st.download_button(
    label="Download Results as CSV",
    data=results_df.to_csv(index=False),
    file_name="roi_results.csv",
    mime="text/csv"
)

# Help Section
st.sidebar.markdown("---")
if st.sidebar.button("Help"):
    st.markdown("""
    ### How to Use:
    - Adjust input parameters in the sidebar.
    - View detailed results, charts, and scenario comparisons.
    - Export results as a CSV file.
    """)