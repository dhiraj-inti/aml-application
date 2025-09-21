import pandas as pd
import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent")


def prepare_analysis_data(historical_data, transaction):
    """Prepare a forensic risk analysis report based on historical data and new transaction"""
    
    analysis_text = f"""
    FORENSIC CRYPTO TRANSACTION RISK REPORT

    SECTION 1: HISTORICAL TRANSACTION OVERVIEW
    - Data Summary:
    {historical_data.to_string()}
    - Key Patterns: Identify notable trends, anomalies, or outliers in historical activity.

    SECTION 2: NEW TRANSACTION DETAILS
    - Sender: {transaction['sender']}
    - Receiver: {transaction['receiver']}
    - Amount: {transaction['amount']} BTC
    - Timestamp: {transaction['timestamp']}
    - Flagged as fraudulent: {transaction['fraudulent']}
    - Risk score: {transaction['risk_score']}/10

    SECTION 3: FRAUD DETECTION RULES & BENCHMARKS
    1. Mean transaction amount < 750,000 BTC
    2. Average time intervals ≥ 10 hours (36,000 seconds)
    3. Unique senders (recipient perspective) ≤ 7
    4. Unique recipients ≤ 7
    5. Fan-in/fan-out ratio (ratio_in_out) between 0.5 and 1.5
    6. Big TXN sum/small TXN sum ratio: high values indicate risk

    SECTION 4: FORENSIC ANALYSIS REQUEST
    Please provide a detailed forensic report addressing:
    - The specific reasons this transaction was flagged as fraudulent (risk score: {transaction['risk_score']}/10).
    - Which rules or benchmarks were violated, with direct references to the data.
    - Comparative analysis: How does this transaction differ from historical wallet behavior?
    - Breakdown of risk factors and their contribution to the overall score.
    - Actionable recommendations for investigators, including next steps and potential red flags.
    - If applicable, suggest additional data or context that could improve the risk assessment.

    Format your response as a structured forensic report, using bullet points, tables, or numbered lists where appropriate. Be concise, evidence-based, and professional.
    """
    
    return analysis_text

def generate_risk_analysis(transaction_payload):
    try:
        historical_data = pd.read_csv('transaction_history.csv')
        prompt_text = prepare_analysis_data(historical_data, transaction_payload)

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
        print("Error: transaction_history.csv file not found.")
        print("Please ensure the CSV file is in the same directory.")
    except Exception as e:
        print(f"Error: {str(e)}")

# if __name__ == "__main__":
#     generate_risk_analysis()