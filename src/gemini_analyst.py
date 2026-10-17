import os
import json
import time
import pandas as pd

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Configuration
# --------------------------------------------------

KPI_PATH = "outputs/kpi_summary.csv"
REGION_PATH = "outputs/region_analysis.csv"
SOURCE_PATH = "outputs/source_analysis.csv"
INSIGHTS_PATH = "outputs/verified_insights.txt"

JSON_OUTPUT_PATH = "outputs/ai_business_report.json"
MARKDOWN_OUTPUT_PATH = "outputs/ai_business_report.md"


# --------------------------------------------------
# Load API key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Check your .env file."
    )

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Load business data
# --------------------------------------------------

def load_business_data():

    kpis = pd.read_csv(KPI_PATH)
    regions = pd.read_csv(REGION_PATH)
    sources = pd.read_csv(SOURCE_PATH)

    with open(INSIGHTS_PATH, "r", encoding="utf-8") as file:
        verified_insights = file.read()

    return kpis, regions, sources, verified_insights


# --------------------------------------------------
# Convert data into AI prompt
# --------------------------------------------------

def build_prompt(
    kpis,
    regions,
    sources,
    verified_insights
):

    prompt = f"""
You are an AI Business Analyst.

Analyze the supplied sales performance data and produce
a concise, evidence-based executive business report.

IMPORTANT RULES:

1. Use ONLY the supplied data.
2. Do not invent numbers, trends, causes, or facts.
3. Do not claim causation unless the data explicitly supports it.
4. Distinguish observed facts from recommendations.
5. Use exact KPI values from the supplied data.
6. Recommendations must be based on observed evidence.
7. If the data is insufficient to support a conclusion,
   explicitly say so.
8. Do not make unsupported assumptions.
9. Do not replace actual values with variable names or field names.
10. Do not output placeholders such as "total_leads",
    "marketing_roi", "revenue_per_lead", etc.
11. Every KPI must contain its human-readable name AND its actual value.

========================
KPI FORMATTING REQUIREMENTS
========================

For the "key_kpis" section:

- Return each KPI as a complete human-readable statement.
- Include the KPI name and its actual value.
- Never return only a variable name.
- Never return field names such as "total_leads" as the KPI value.
- Counts must use comma separators.
- Revenue, spending, costs, and other monetary values must use INR
  formatting with the ₹ symbol and comma separators.
- Rates must be displayed as percentages with 2 decimal places.
- Marketing ROI must be displayed as a percentage with 2 decimal places.
- Do not change, recalculate, or invent KPI values.
- Always include Lead-to-Customer Rate in the Key Performance Indicators section.

Examples of CORRECT KPI output:

"Total Leads: 16,862"
"Total Demo Calls: 4,266"
"Total Deals Closed: 944"
"Total Revenue: ₹56,155,000"
"Marketing Spend: ₹8,419,500"
"Demo Conversion Rate: 25.30%"
"Win Rate: 22.13%"
"Lead-to-Customer Rate: 5.60%"
"Revenue per Lead: ₹3,330.27"
"Cost per Lead: ₹499.32"
"Customer Acquisition Cost: ₹8,918.96"
"Revenue per Sales Hour: ₹8,282.20"
"Marketing ROI: 566.96%"

IMPORTANT:
The examples above demonstrate formatting only.
Use the actual values from the supplied KPI data.

========================
OVERALL KPI DATA
========================

{kpis.to_string(index=False)}

========================
REGIONAL ANALYSIS
========================

{regions.to_string(index=False)}

========================
LEAD SOURCE ANALYSIS
========================

{sources.to_string(index=False)}

========================
VERIFIED BUSINESS FACTS
========================

{verified_insights}

========================
REQUIRED REPORT
========================

Create the following sections:

1. Executive Summary
   - Provide 3 to 5 concise observations.
   - Use actual numbers where relevant.

2. Key Performance Indicators
   - Include ALL of the following overall KPIs:
     Total Leads
     Total Demo Calls
     Total Deals Closed
     Total Revenue
     Total Marketing Spend
     Demo Conversion Rate
     Win Rate
     Lead-to-Customer Rate
     Revenue per Lead
     Cost per Lead
     Customer Acquisition Cost
     Revenue per Sales Hour
     Marketing ROI

   - Every KPI must contain its human-readable name and actual value.
   - Use the required formatting rules above.
   - Do not output KPI variable names by themselves.
   - Do not omit any KPI from the list above.

3. Positive Trends
   - Identify measurable positive patterns.
   - Support observations with actual data.

4. Risks and Red Flags
   - Identify measurable areas requiring attention.
   - Support observations with actual data.

5. Regional Analysis
   - Explain important differences between regions.
   - Use actual values from the regional analysis.

6. Lead Source Analysis
   - Explain important differences between lead sources.
   - Use actual values from the lead source analysis.

7. Business Recommendations
   - Provide 3 to 5 actionable recommendations.
   - Each recommendation must be linked to observed evidence.
   - Do not present recommendations as established facts.

8. Data Limitations
   - Mention limitations of the supplied dataset.
   - Do not invent limitations that are not reasonably supported
     by the structure of the supplied data.

========================
OUTPUT FORMAT
========================

Return ONLY valid JSON.

Return exactly these top-level fields:

{{
    "executive_summary": [
        "observation 1",
        "observation 2"
    ],

    "key_kpis": [
        "Total Leads: 16,862",
        "Total Revenue: ₹56,155,000",
        "Marketing ROI: 566.96%"
    ],

    "positive_trends": [
        "trend 1",
        "trend 2"
    ],

    "risks_and_red_flags": [
        "risk 1",
        "risk 2"
    ],

    "regional_analysis": [
        "regional observation 1",
        "regional observation 2"
    ],

    "lead_source_analysis": [
        "source observation 1",
        "source observation 2"
    ],

    "recommendations": [
        "recommendation 1",
        "recommendation 2"
    ],

    "data_limitations": [
        "limitation 1",
        "limitation 2"
    ]
}}

Do not add any other top-level fields.
Do not wrap the JSON in Markdown code fences.
"""


    return prompt



# --------------------------------------------------
# Generate AI report
# --------------------------------------------------

def generate_report(prompt):

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    max_retries = 4

    for model in models:

        print(f"Trying model: {model}")

        for attempt in range(max_retries):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json"
                    }
                )

                print(
                    f"Successfully generated report using {model}"
                )

                return response.text

            except Exception as error:

                error_message = str(error)

                if "503" not in error_message:
                    raise

                if attempt == max_retries - 1:

                    print(
                        f"{model} unavailable after "
                        f"{max_retries} attempts."
                    )

                    break

                wait_time = 2 ** attempt

                print(
                    f"{model} temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    raise RuntimeError(
        "All Gemini models are temporarily unavailable. "
        "Please try again later."
    )
    
# --------------------------------------------------
# Save JSON report
# --------------------------------------------------

def save_json_report(report_text):

    report = json.loads(report_text)

    with open(
        JSON_OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    return report


# --------------------------------------------------
# Convert JSON report to Markdown
# --------------------------------------------------

def create_markdown_report(report):

    markdown = f"""# AI Business Analysis Report

## Executive Summary

"""

    for item in report["executive_summary"]:
        markdown += f"- {item}\n"

    markdown += "\n## Key Performance Indicators\n\n"

    for item in report["key_kpis"]:
        markdown += f"- {item}\n"

    markdown += "\n## Positive Trends\n\n"

    for item in report["positive_trends"]:
        markdown += f"- {item}\n"

    markdown += "\n## Risks and Red Flags\n\n"

    for item in report["risks_and_red_flags"]:
        markdown += f"- {item}\n"

    markdown += "\n## Regional Analysis\n\n"

    for item in report["regional_analysis"]:
        markdown += f"- {item}\n"

    markdown += "\n## Lead Source Analysis\n\n"

    for item in report["lead_source_analysis"]:
        markdown += f"- {item}\n"

    markdown += "\n## Business Recommendations\n\n"

    for item in report["recommendations"]:
        markdown += f"- {item}\n"

    markdown += "\n## Data Limitations\n\n"

    for item in report["data_limitations"]:
        markdown += f"- {item}\n"

    with open(
        MARKDOWN_OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(markdown)


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():

    print("Loading business data...")

    kpis, regions, sources, verified_insights = (
        load_business_data()
    )

    print("Building AI analysis prompt...")

    prompt = build_prompt(
        kpis,
        regions,
        sources,
        verified_insights
    )

    print("Generating Gemini analysis...")

    report_text = generate_report(prompt)

    print("Saving AI report...")

    report = save_json_report(report_text)

    create_markdown_report(report)

    print("\nAI Business Report generated successfully.")

    print(f"JSON: {JSON_OUTPUT_PATH}")
    print(f"Markdown: {MARKDOWN_OUTPUT_PATH}")


# --------------------------------------------------
# Run pipeline
# --------------------------------------------------

if __name__ == "__main__":
    main()