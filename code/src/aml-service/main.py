from flask import Flask, request
import requests

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
    # Step 2: If flagged for explanation, call the explanation service
    # else call the oracle service to add transaction to the blockchain
    try:
        if flag:
            message = "<Explanation from explanation service>"
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

def invoke_add_to_blockchain_service(sender, receiver, amount, timestamp):
    # Logic to call the oracle service to add transaction to the blockchain
    response = requests.post("http://localhost:8080/oracle/add-transaction", json={
        "sender":sender,
        "amount":amount,
        "receiver":receiver,
        "timestamp":timestamp
    })
    print(response.status_code, response.text)
    if response.status_code != 200:
        raise Exception("Error calling oracle service")
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=port)