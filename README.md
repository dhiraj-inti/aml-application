# AML Application

This repository contains a modular Anti-Money Laundering (AML) application designed to analyze and process financial transactions using a combination of client, service, and blockchain components.

## Application Flow

1. **Client App (React)**
    - Users submit a transaction and upload a CSV file containing transaction history.
    - CSV format: `sender, receiver, amount, timestamp`
    - The client forwards this data to the AML Service.

2. **AML Service (Flask)**
    - Receives transaction data from the client.
    - Determines if the transaction is flagged for suspicious activity.
    - If flagged, invokes the Explanation Service to generate a forensic report explaining the reason.
    - If not flagged, forwards the transaction to the Oracle Service for blockchain storage.

3. **Oracle Service (Express)**
    - Receives non-flagged transactions from the AML Service.
    - Uses Cosmos SDK to store the transaction on the blockchain.

---

## Setup Instructions

### 1. Client App (React)

**Directory:** `code/src/frontend`

**Setup Steps:**
1. Clone the repository.
2. Navigate to the client app directory (frontend).
3. Install dependencies:
    ```bash
    npm install
    ```
4. Start the development server:
    ```bash
    npm run dev
    ```
5. Access the app at `http://localhost:3000`.

---

### 2. AML Service (Flask)

**Directory:** `code/src/aml-service`

**Setup Steps:**
1. Navigate to the AML Service directory:
    ```bash
    cd code/src/aml-service
    ```
2. Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the Flask server:
    ```bash
    python main.py
    ```
5. The service will be available at `http://localhost:5000`.

**Files:**
- `aml_core.py`: Core AML logic.
- `main.py`: Flask entry point.
- `explanation_service/explanation_core.py`: Forensic explanation logic.
- `explanation_service/transaction_history.csv`: Sample transaction history.

---

### 3. Oracle Service (Express)

**Directory:** `code/src/oracle-service`

**Setup Steps:**
1. Navigate to the Oracle Service directory:
    ```bash
    cd code/src/oracle-service
    ```
2. Install dependencies:
    ```bash
    npm install
    npm install -g @cosmwasm/ts-codegen@1.6.0
    ```
3. Start the Express server:
    ```bash
    npx ts-node src\app.ts
    ```
4. The service will be available at `http://localhost:8080` (or as configured).

**Files:**
- `src/app.ts`: Main Express app.
- `src/controller.ts`: Handles transaction logic.
- `src/routes.ts`: API routes.
- `src/sdk/Oracle.client.ts`: Cosmos SDK integration.


### 4. AML Contract (Rust)

**Directory:** `code/src/aml-contract`

**Setup Steps:**
1. Navigate to the Oracle Service directory:
    ```bash
    cd code/src/oracle-service
    ```
2. Compile the smart contract:


    ```bash
    set RUSTFLAGS=-C link-arg=-s
    cargo wasm
    ```
    Confirm `aml_contract.wasm` is listed
    ```bash
    dir target\wasm32-unknown-unknown\release\aml_contract.wasm
    ```
    Optimize WASM
    ```bash
    wasm-opt -Os --signext-lowering .\target/wasm32-unknown-unknown/release/aml_contract.wasm -o ./target/wasm32-unknown-unknown/release/aml_contract_opt.wasm
    ```
    Validate aml_contract_opt.wasm
    ```bash
    cosmwasm-check ./target/wasm32-unknown-unknown/release/aml_contract_opt.wasm
    ```
3. Deploy the smart contract by doing a right click on 'aml_contract_opt.wasm' and clicking on 'Upload contract'
4. Note down the code_id given by Cosmy Wasmy and use 'Initialise' section of the extension to instantiate the contract with following payload:
    ```json
    {
        "oracle_pubkey": "AjrX9BclyF9K8drtbJ+0+FBbGsS4Pg+UjPiYfBT7nRh2",
        "oracle_key_type": "secp256k1"
    }
    ```

---

## Notes

- Ensure all services are running before submitting transactions from the client app.
- The blockchain contract and schema are located in `code/src/aml-contract` for advanced integrations.
- Environment variables can be configured in the `.env` files within each service directory.

---

## License

This project is for educational and demonstration purposes.
