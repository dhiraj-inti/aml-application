from datetime import datetime
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = os.getenv("GEMINI_API_URL","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent")


def prepare_analysis_data(historical_data, transaction, rules):
    """Prepare a forensic risk analysis report using explicit rules and historical reference"""

    rules_text = "\n".join([
        f"{i+1}. {r['rule']} (Thresholds: {', '.join([f'{k}={v}' for k, v in r.items() if k != 'rule'])})"
        for i, r in enumerate(rules)
    ])

    transaction_text = "\n".join([
        f"- {k.replace('_', ' ').capitalize()}: {v}"
        for k, v in transaction.items()
    ])

    analysis_text = f"""
    FORENSIC CRYPTO TRANSACTION RISK REPORT

    SECTION 1: HISTORICAL TRANSACTION REFERENCE
    - Data Source: user_input.csv
    - Summary Table:
    {historical_data.to_string()}
    - Key Patterns: Identify trends, anomalies, or outliers in historical wallet activity.

    SECTION 2: CURRENT TRANSACTION DETAILS
    {transaction_text}

    SECTION 3: APPLIED FRAUD DETECTION RULES
    The following rules are used to assess the current transaction:
    {rules_text}

    SECTION 4: ANALYSIS TASK
    Please provide a structured forensic risk report that includes:
    1. Which specific rules were violated by the current transaction, referencing both the transaction details and historical data and give it in the bulletins format.
    2. Perform a correlation check between the current transaction and historical wallet behavior with the help of the rules.
    3. A breakdown of risk factors. Please present the breakdown as a bulleted list. For each risk factor, include:
        - Risk Factor Name
        - Justification
        - Why this contribution is needed for the overall risk assessment
        End the list with a summary bullet for **Overall Risk Assessment**.
    4. Actionable recommendations for investigators, including next steps and potential red flags.
    5. Suggestions for additional data or context that could improve future risk assessments.


    Format your response as a professional forensic report, using bullet points, tables, or numbered lists where appropriate. Be concise, evidence-based, and reference both the rules and historical data. Take today's date as the analysis date.
    as {datetime.now().date()}.
    """

    return analysis_text


def generate_risk_analysis(RULES, transaction_payload):
    try:
        historical_data = pd.read_csv('explanation_service/user_input.csv')
        prompt_text = prepare_analysis_data(historical_data, transaction_payload, RULES)

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_text
                        }
                    ]
                }
            ]
        }

        print("Generating risk analysis report...\n")
        print("=" * 60)
        print("RISK ANALYSIS REPORT")
        print("=" * 60)

        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Print the model's reply
            print(result['candidates'][0]['content']['parts'][0]['text'])
            report = result['candidates'][0]['content']['parts'][0]['text']
            return report
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print("Error: user_input.csv file not found.")
        print("Please ensure the CSV file is in the same directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

# if __name__ == "__main__":
#     RULES = [
#     {"rule": "Mean transaction amount < 187.5 BTC", "threshold": MEAN_BTC_THRESHOLD},
#     {"rule": "Average time intervals ≥ 36,000 seconds (10 hours)", "threshold": AVG_INTERVAL_SECONDS_MIN},
#     {"rule": "Unique senders ≤ 7", "threshold": UNIQUE_SENDERS_MAX},
#     {"rule": "Unique receivers ≤ 7", "threshold": UNIQUE_RECEIVERS_MAX},
#     {"rule": "Fan-in/fan-out ratio between 0.5 and 1.5", "min": RATIO_MIN, "max": RATIO_MAX},
#     {"rule": "Big TXN threshold ≥ 1.0 BTC", "threshold": BIG_TXN_BTC_THRESHOLD},
# ]
    
    # generate_risk_analysis(RULES, sample_prediction_payload)