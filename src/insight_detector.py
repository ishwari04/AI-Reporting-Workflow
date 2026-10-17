import pandas as pd


REGION_PATH = "outputs/region_analysis.csv"
SOURCE_PATH = "outputs/source_analysis.csv"
OUTPUT_PATH = "outputs/verified_insights.txt"

def load_analysis():
    region_df = pd.read_csv(REGION_PATH)
    source_df = pd.read_csv(SOURCE_PATH)

    return region_df, source_df

def analyze_regions(region_df):

    highest_revenue = region_df.loc[
        region_df["Revenue"].idxmax()
    ]

    highest_conversion = region_df.loc[
        region_df["Lead-to-Customer Rate"].idxmax()
    ]

    highest_cac = region_df.loc[
        region_df["Customer Acquisition Cost"].idxmax()
    ]

    highest_roi = region_df.loc[
        region_df["Marketing ROI"].idxmax()
    ]

    return {
        "highest_revenue_region": highest_revenue["Region"],
        "highest_revenue_value": highest_revenue["Revenue"],

        "highest_conversion_region": highest_conversion["Region"],
        "highest_conversion_rate": highest_conversion[
            "Lead-to-Customer Rate"
        ],

        "highest_cac_region": highest_cac["Region"],
        "highest_cac_value": highest_cac[
            "Customer Acquisition Cost"
        ],

        "highest_roi_region": highest_roi["Region"],
        "highest_roi_value": highest_roi["Marketing ROI"]
    }

def analyze_sources(source_df):

    highest_revenue = source_df.loc[
        source_df["Revenue"].idxmax()
    ]

    highest_conversion = source_df.loc[
        source_df["Lead-to-Customer Rate"].idxmax()
    ]

    highest_cac = source_df.loc[
        source_df["Customer Acquisition Cost"].idxmax()
    ]

    highest_roi = source_df.loc[
        source_df["Marketing ROI"].idxmax()
    ]

    lowest_conversion = source_df.loc[
        source_df["Lead-to-Customer Rate"].idxmin()
    ]

    return {
        "highest_revenue_source": highest_revenue["Lead Source"],
        "highest_revenue_value": highest_revenue["Revenue"],

        "highest_conversion_source": highest_conversion[
            "Lead Source"
        ],
        "highest_conversion_rate": highest_conversion[
            "Lead-to-Customer Rate"
        ],

        "highest_cac_source": highest_cac["Lead Source"],
        "highest_cac_value": highest_cac[
            "Customer Acquisition Cost"
        ],

        "highest_roi_source": highest_roi["Lead Source"],
        "highest_roi_value": highest_roi["Marketing ROI"],

        "lowest_conversion_source": lowest_conversion[
            "Lead Source"
        ],
        "lowest_conversion_rate": lowest_conversion[
            "Lead-to-Customer Rate"
        ]
    }

def create_evidence_report(region_facts, source_facts):

    report = f"""
VERIFIED BUSINESS FACTS
=======================

REGION ANALYSIS
---------------

Highest Revenue Region:
{region_facts["highest_revenue_region"]}
Revenue: ₹{region_facts["highest_revenue_value"]:,.0f}

Highest Lead-to-Customer Rate:
{region_facts["highest_conversion_region"]}
Rate: {region_facts["highest_conversion_rate"]:.2%}

Highest Customer Acquisition Cost:
{region_facts["highest_cac_region"]}
CAC: ₹{region_facts["highest_cac_value"]:,.2f}

Highest Marketing ROI:
{region_facts["highest_roi_region"]}
ROI: {region_facts["highest_roi_value"]:.2%}


LEAD SOURCE ANALYSIS
--------------------

Highest Revenue Source:
{source_facts["highest_revenue_source"]}
Revenue: ₹{source_facts["highest_revenue_value"]:,.0f}

Highest Lead-to-Customer Rate:
{source_facts["highest_conversion_source"]}
Rate: {source_facts["highest_conversion_rate"]:.2%}

Highest Customer Acquisition Cost:
{source_facts["highest_cac_source"]}
CAC: ₹{source_facts["highest_cac_value"]:,.2f}

Highest Marketing ROI:
{source_facts["highest_roi_source"]}
ROI: {source_facts["highest_roi_value"]:.2%}

Lowest Lead-to-Customer Rate:
{source_facts["lowest_conversion_source"]}
Rate: {source_facts["lowest_conversion_rate"]:.2%}
"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Verified insights saved to: {OUTPUT_PATH}")


def main():

    region_df, source_df = load_analysis()

    region_facts = analyze_regions(region_df)

    source_facts = analyze_sources(source_df)

    create_evidence_report(
        region_facts,
        source_facts
    )


if __name__ == "__main__":
    main()