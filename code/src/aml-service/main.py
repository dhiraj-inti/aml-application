from flask import Flask

app = Flask("aml-service")
port = 5000

@app.route('/', methods=["GET"])
def home():
    return "AML Service is running!"

@app.route('/aml-checks', methods=["POST"])
def aml_checks():
    flag = None
    # Step 1: Receive and parse the request data

    # Step 2: If flagged for explanation, call the explanation service
    # else call the oracle service to add transaction to the blockchain
    if flag:
        message = "<Explanation from explanation service>"
    else:
        message = "Added to blockchain successfully"

    return {
        "flag": flag,
        "message": "Transaction processed successfully"
    }

if __name__ == '__main__':
    app.run(debug=True)