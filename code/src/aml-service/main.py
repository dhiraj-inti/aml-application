from datetime import datetime
from flask import Flask, request
import requests

from explanation_service.explanation_core import generate_risk_analysis

app = Flask("aml-service")
port = 5000

@app.route('/', methods=["GET"])
def home():
    return "AML Service is running!"

@app.route('/aml-checks', methods=["POST"])
def aml_checks():
    flag = None
    # Step 1: Receive and parse the request data
    data = request.get_json()
    sender = data.get('sender') # type: ignore
    receiver = data.get('receiver') # type: ignore
    amount = data.get('amount') # type: ignore
    timestamp = data.get('timestamp') # type: ignore

    if not sender or not receiver or not amount or not timestamp:
        return {
            "error": "Missing required fields"
        }
    



    # Step 2: If flagged for explanation, call the explanation service
    # else call the oracle service to add transaction to the blockchain
    try:
        if flag:
            transaction_payload = {
                "sender": sender,
                "receiver": receiver,
                "amount": amount,
                "timestamp": timestamp,
                "fraudulent": True,
                "risk_score": 8  # Example risk score
            }
            response = generate_risk_analysis(transaction_payload)
            message = response
        else:
            response = invoke_add_to_blockchain_service(sender, receiver, amount, timestamp)
            message = "Added to blockchain successfully"
    except Exception as e:
        return {
            "flag": None,
            "message": "Exception occurred: " + str(e)
        }, 500
    
    return {
        "flag": flag,
        "message": message
    }, 200

def is_iso_timestamp(iso_timestamp):
    try:
        # Replace 'Z' with '+00:00' for UTC
        datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def invoke_add_to_blockchain_service(sender, receiver, amount, timestamp):
    # Logic to call the oracle service to add transaction to the blockchain
    if is_iso_timestamp(timestamp):
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        timestamp = int(dt.timestamp())

    response = requests.post("http://localhost:8080/oracle/add-transaction", json={
        "sender":sender,
        "amount":amount,
        "receiver":receiver,
        "timestamp":timestamp
    })
   
    if response.status_code != 200:
        raise Exception("Error calling oracle service")
    return response.text

if __name__ == '__main__':
    app.run(debug=True, port=port)