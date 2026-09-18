
import pandas as pd


DATA_PATH = "data/sales_data.csv"
OUTPUT_PATH = "outputs/kpi_summary.csv"


def load_data():
    """Load sales data from CSV."""
    return pd.read_csv(DATA_PATH)


def calculate_kpis(df):
    """Calculate overall sales KPIs."""

    total_leads = df["Leads Generated"].sum()
    total_demo_calls = df["Demo Calls"].sum()
    total_deals = df["Deals Closed"].sum()
    total_revenue = df["Revenue (INR)"].sum()
    total_marketing_spend = df["Marketing Spend (INR)"].sum()
    total_sales_hours = df["Sales Hours Spent"].sum()

    demo_conversion_rate = total_demo_calls / total_leads
    win_rate = total_deals / total_demo_calls
    lead_to_customer_rate = total_deals / total_leads

    revenue_per_lead = total_revenue / total_leads
    cost_per_lead = total_marketing_spend / total_leads

    customer_acquisition_cost = (
        total_marketing_spend / total_deals
    )

    revenue_per_sales_hour = (
        total_revenue / total_sales_hours
    )

    marketing_roi = (
        total_revenue - total_marketing_spend
    ) / total_marketing_spend

    return {
        "Total Leads": total_leads,
        "Total Demo Calls": total_demo_calls,
        "Total Deals Closed": total_deals,
        "Total Revenue": total_revenue,
        "Total Marketing Spend": total_marketing_spend,
        "Total Sales Hours": total_sales_hours,
        "Demo Conversion Rate": demo_conversion_rate,
        "Win Rate": win_rate,
        "Lead-to-Customer Rate": lead_to_customer_rate,
        "Revenue per Lead": revenue_per_lead,
        "Cost per Lead": cost_per_lead,
        "Customer Acquisition Cost": customer_acquisition_cost,
        "Revenue per Sales Hour": revenue_per_sales_hour,
        "Marketing ROI": marketing_roi
    }


def save_kpis(kpis):
    """Save KPI results to CSV."""

    output_df = pd.DataFrame(
        list(kpis.items()),
        columns=["KPI", "Value"]
    )

    output_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"KPI summary saved to: {OUTPUT_PATH}")


def main():
    """Run the KPI pipeline."""

    df = load_data()

    kpis = calculate_kpis(df)

    save_kpis(kpis)


if __name__ == "__main__":
    main()