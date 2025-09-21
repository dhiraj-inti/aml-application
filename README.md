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

### 1. Client App (React) *(To be added)*

**Setup Steps:**
1. Clone the repository.
2. Navigate to the client app directory (once available).
3. Install dependencies:
    ```bash
    npm install
    ```
4. Start the development server:
    ```bash
    npm start
    ```
5. Access the app at `http://localhost:3000`.

---

### 2. AML Service (Flask)

**Directory:** `code/aml-service`

**Setup Steps:**
1. Navigate to the AML Service directory:
    ```bash
    cd code/aml-service
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

**Directory:** `code/oracle-service`

**Setup Steps:**
1. Navigate to the Oracle Service directory:
    ```bash
    cd code/oracle-service
    ```
2. Install dependencies:
    ```bash
    npm install
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

---

## Notes

- Ensure all services are running before submitting transactions from the client app.
- The blockchain contract and schema are located in `code/aml-contract` for advanced integrations.
- Environment variables can be configured in the `.env` files within each service directory.

---

## License

This project is for educational and demonstration purposes.