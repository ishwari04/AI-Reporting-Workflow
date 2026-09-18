import pandas as pd

DATA_PATH = "data/sales_data.csv"

df = pd.read_csv(DATA_PATH)

def analyze_by_region(df):
    region_analysis = df.groupby("Region").agg(
        Leads=("Leads Generated", "sum"),
        Demo_Calls=("Demo Calls", "sum"),
        Deals=("Deals Closed", "sum"),
        Revenue=("Revenue (INR)", "sum"),
        Marketing_Spend=("Marketing Spend (INR)", "sum"),
        Sales_Hours=("Sales Hours Spent", "sum")
    ).reset_index()

    region_analysis["Demo Conversion Rate"] = (
        region_analysis["Demo_Calls"]
        / region_analysis["Leads"]
    )

    region_analysis["Win Rate"] = (
        region_analysis["Deals"]
        / region_analysis["Demo_Calls"]
    )

    region_analysis["Lead-to-Customer Rate"] = (
        region_analysis["Deals"]
        / region_analysis["Leads"]
    )

    region_analysis["Revenue per Lead"] = (
        region_analysis["Revenue"]
        / region_analysis["Leads"]
    )

    region_analysis["Cost per Lead"] = (
        region_analysis["Marketing_Spend"]
        / region_analysis["Leads"]
    )

    region_analysis["Customer Acquisition Cost"] = (
        region_analysis["Marketing_Spend"]
        / region_analysis["Deals"]
    )

    region_analysis["Marketing ROI"] = (
        region_analysis["Revenue"]
        - region_analysis["Marketing_Spend"]
    ) / region_analysis["Marketing_Spend"]

    return region_analysis

def analyze_by_lead_source(df):
    source_analysis = df.groupby("Lead Source").agg(
        Leads=("Leads Generated", "sum"),
        Demo_Calls=("Demo Calls", "sum"),
        Deals=("Deals Closed", "sum"),
        Revenue=("Revenue (INR)", "sum"),
        Marketing_Spend=("Marketing Spend (INR)", "sum"),
        Sales_Hours=("Sales Hours Spent", "sum")
    ).reset_index()

    source_analysis["Demo Conversion Rate"] = (
        source_analysis["Demo_Calls"]
        / source_analysis["Leads"]
    )

    source_analysis["Win Rate"] = (
        source_analysis["Deals"]
        / source_analysis["Demo_Calls"]
    )

    source_analysis["Lead-to-Customer Rate"] = (
        source_analysis["Deals"]
        / source_analysis["Leads"]
    )

    source_analysis["Revenue per Lead"] = (
        source_analysis["Revenue"]
        / source_analysis["Leads"]
    )

    source_analysis["Cost per Lead"] = (
        source_analysis["Marketing_Spend"]
        / source_analysis["Leads"]
    )

    source_analysis["Customer Acquisition Cost"] = (
        source_analysis["Marketing_Spend"]
        / source_analysis["Deals"]
    )

    source_analysis["Marketing ROI"] = (
        source_analysis["Revenue"]
        - source_analysis["Marketing_Spend"]
    ) / source_analysis["Marketing_Spend"]

    return source_analysis

def main():

    region_analysis = analyze_by_region(df)

    source_analysis = analyze_by_lead_source(df)

    region_analysis.to_csv(
        "outputs/region_analysis.csv",
        index=False
    )

    source_analysis.to_csv(
        "outputs/source_analysis.csv",
        index=False
    )

    print("Region analysis saved.")
    print("Lead source analysis saved.")


if __name__ == "__main__":
    main()