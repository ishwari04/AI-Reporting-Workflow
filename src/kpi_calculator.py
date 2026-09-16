import pandas as pd

DATA_PATH = "data/sales_data.csv"

df = pd.read_csv(DATA_PATH)

print(df.head())

# Step 1: Calculate total leads
total_leads = df["Leads Generated"].sum()

# Step 2: Calculate total demo calls
total_demo_calls = df["Demo Calls"].sum()

# Step 3: Calculate Demo Conversion Rate
demo_conversion_rate = total_demo_calls / total_leads

print(f"Total Leads: {total_leads}")
print(f"Total Demo Calls: {total_demo_calls}")
print(f"Demo Conversion Rate: {demo_conversion_rate:.2%}")

# Step 4: Calculate total deals
total_deals = df["Deals Closed"].sum()

# Step 5: Calculate Win Rate
win_rate = total_deals / total_demo_calls

print(f"Total Deals Closed: {total_deals}")
print(f"Win Rate: {win_rate:.2%}")

# Step 6: Calculate total revenue
total_revenue = df["Revenue (INR)"].sum()

# Step 7: Calculate Revenue per Lead
revenue_per_lead = total_revenue / total_leads

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Revenue per Lead: ₹{revenue_per_lead:,.2f}")

# Step 8: Calculate total marketing spend
total_marketing_spend = df["Marketing Spend (INR)"].sum()

# Step 9: Calculate Cost per Lead
cost_per_lead = total_marketing_spend / total_leads

print(f"Total Marketing Spend: ₹{total_marketing_spend:,.2f}")
print(f"Cost per Lead: ₹{cost_per_lead:,.2f}")

# Step 10: Calculate Customer Acquisition Cost (CAC)
customer_acquisition_cost = total_marketing_spend / total_deals

print(f"Customer Acquisition Cost: ₹{customer_acquisition_cost:,.2f}")

# Step 11: Calculate total sales hours
total_sales_hours = df["Sales Hours Spent"].sum()

# Step 12: Calculate Revenue per Sales Hour
revenue_per_sales_hour = total_revenue / total_sales_hours

print(f"Total Sales Hours: {total_sales_hours:,.1f}")
print(f"Revenue per Sales Hour: ₹{revenue_per_sales_hour:,.2f}")

# Step 13: Calculate Marketing ROI
marketing_roi = (
    total_revenue - total_marketing_spend
) / total_marketing_spend

print(f"Marketing ROI: {marketing_roi:.2%}")

# Step 14: Create KPI summary

kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Leads",
        "Total Demo Calls",
        "Total Deals Closed",
        "Total Revenue",
        "Total Marketing Spend",
        "Total Sales Hours",
        "Demo Conversion Rate",
        "Win Rate",
        "Revenue per Lead",
        "Cost per Lead",
        "Customer Acquisition Cost",
        "Revenue per Sales Hour",
        "Marketing ROI"
    ],
    "Value": [
        total_leads,
        total_demo_calls,
        total_deals,
        total_revenue,
        total_marketing_spend,
        total_sales_hours,
        demo_conversion_rate,
        win_rate,
        revenue_per_lead,
        cost_per_lead,
        customer_acquisition_cost,
        revenue_per_sales_hour,
        marketing_roi
    ]
})

# Step 15: Save KPI summary
output_path = "outputs/kpi_summary.csv"

kpi_summary.to_csv(output_path, index=False)

print(f"\nKPI summary saved to: {output_path}")