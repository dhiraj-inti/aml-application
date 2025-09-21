from flask import Flask
import requests

app = Flask("aml-service")
port = 5000

@app.route('/', methods=["GET"])
def home():
    return "AML Service is running!"

@app.route('/aml-checks', methods=["POST"])
def aml_checks(request):
    flag = None
    # Step 1: Receive and parse the request data
    data = request.get_json()
    sender, receiver, amount, timestamp = data['sender'], data['receiver'], data['amount'], data["timestamp"]

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
    response = requests.post("http://localhost:8080/add-transaction", json={
        "sender":sender,
        "amount":amount,
        "receiver":receiver,
        "timestamp":timestamp
    })
    if response.status_code != 200:
        raise Exception("Error calling oracle service")
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)