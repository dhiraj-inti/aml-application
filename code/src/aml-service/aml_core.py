import pandas as pd
import numpy as np

MEAN_BTC_THRESHOLD = 47.5
UNIQUE_SENDERS_MAX = 7
UNIQUE_RECEIVERS_MAX = 7
RATIO_MIN = 0.5
RATIO_MAX = 1.5
BIG_TXN_BTC_THRESHOLD = 1.0
INTERVAL_SECONDS_MIN = 720000 

RULES = [
    {"rule": "Mean transaction amount < 187.5 BTC", "threshold": MEAN_BTC_THRESHOLD},
    {"rule": "Average time intervals ≥ 36,000 seconds (200 hours)", "threshold": INTERVAL_SECONDS_MIN},
    {"rule": "Unique senders ≤ 7", "threshold": UNIQUE_SENDERS_MAX},
    {"rule": "Unique receivers ≤ 7", "threshold": UNIQUE_RECEIVERS_MAX},
    {"rule": "Fan-in/fan-out ratio between 0.5 and 1.5", "min": RATIO_MIN, "max": RATIO_MAX},
    {"rule": "Big TXN threshold ≥ 1.0 BTC", "threshold": BIG_TXN_BTC_THRESHOLD},
]

def load_transactions(path):
    df = pd.read_csv(path)
    required = {"sender", "receiver", "amount", "timestamp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input file missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df

def compute_wallet_metrics(wallet, txs_df, sender, receiver, amount, timestamp):

    new_tx = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": timestamp,
    }
    # Get tx histrory

    relevant = txs_df[
        (txs_df["sender"] == wallet) | (txs_df["receiver"] == wallet)
    ].copy()
    relevant = relevant.sort_values("timestamp", ascending=False).head(20)
    # Appending tx
    new_tx_df = pd.DataFrame([new_tx])

    print(new_tx_df)
    new_tx_df["timestamp"] = pd.to_datetime(new_tx_df["timestamp"], utc=True)
    relevant = pd.concat([relevant, new_tx_df], ignore_index=True)

    print(relevant)
    relevant = relevant.sort_values("timestamp").reset_index(drop=True)

    print(
        relevant["timestamp"].iloc[0],
        relevant["timestamp"].iloc[19],
        relevant["timestamp"].iloc[-1]
    )

    mean_tx_btc = relevant["amount"].mean()
    total_time_interval = (
        (relevant["timestamp"].iloc[-1] - relevant["timestamp"].iloc[0]).total_seconds()
        if len(relevant) > 1
        else 0.0
    )

    unique_senders = relevant.loc[
        relevant["receiver"] == wallet, "sender"
    ].nunique()

    unique_receivers = relevant.loc[
        relevant["sender"] == wallet, "receiver"
    ].nunique()
    total_input_btc = relevant.loc[
        relevant["sender"] == wallet, "amount"
    ].sum()
    total_output_btc = relevant.loc[
        relevant["receiver"] == wallet, "amount"
    ].sum()
    ratio_in_out = (
        total_input_btc / total_output_btc if total_output_btc != 0 else np.nan
    )
    big_tx = relevant[relevant["amount"] >= BIG_TXN_BTC_THRESHOLD]
    small_tx = relevant[relevant["amount"] < BIG_TXN_BTC_THRESHOLD]
    big_count = len(big_tx)
    small_count = len(small_tx)
    big_sum = big_tx["amount"].sum()
    small_sum = small_tx["amount"].sum()
    ratio_big_small = big_sum / small_sum if small_sum > 0 else np.nan

    fraud_conditions = {
        "mean_btc_above_threshold": mean_tx_btc > MEAN_BTC_THRESHOLD,
        "unique_senders_exceed": unique_senders > UNIQUE_SENDERS_MAX,
        "unique_receivers_exceed": unique_receivers > UNIQUE_RECEIVERS_MAX,
        "interval_below_min": total_time_interval < INTERVAL_SECONDS_MIN,
        "ratio_out_of_range": (
            not (RATIO_MIN <= ratio_in_out <= RATIO_MAX)
            if not np.isnan(ratio_in_out)
            else True
        ),
    }
    fraudulent_flag = int(any(fraud_conditions.values()))

    return {
        "wallet_address": wallet,
        "mean_transaction_amount_btc": float(mean_tx_btc),
        "total_time_interval": float(total_time_interval),
        "unique_senders": int(unique_senders),
        "unique_receivers": int(unique_receivers),
        "total_input_btc": float(total_input_btc),
        "total_output_btc": float(total_output_btc),
        "ratio_in_out": float(ratio_in_out) if not np.isnan(ratio_in_out) else None,
        "big_transactions_count": int(big_count),
        "small_transactions_count": int(small_count),
        "big_txn_sum_small_txn_sum_ratio": (
            float(ratio_big_small) if not np.isnan(ratio_big_small) else None
        ),
        "fraudulent_transaction_flag": int(fraudulent_flag),
        "rules": RULES
    }


if __name__ == "__main__":
    # sender = input("Input address (sender): ")
    # receiver = input("Output address (receiver): ")
    # amount = float(input("Transaction amount (BTC): "))
    # timestamp = input("Transaction timestamp (ISO format): ")
    sender = "11zigLN7gKNKXDipWswH59oivhGKBdCMg"
    receiver = "bc173u6s74ksmz4x34x77j67znavtcw3m7mw49zkgq"
    amount = 44.6
    timestamp = "2017-09-27T18:00:00.000"
    txs_path = "code/src/aml-service/transaction_history.csv"

    txs_df = load_transactions(txs_path)

    wallet = receiver  # or receiver
    metrics = compute_wallet_metrics(wallet, txs_df, sender, receiver, amount, timestamp)
    print(metrics)

    # 2022-09-27T18:00:00.000
    # 11zigLN7gKNKXDipWswH59oivhGKBdCMg
    # bc173u6s74ksmz4x34x77j67znavtcw3m7mw49zkgq
    # 44.6


# {
#     "wallet_address": "11zigLN7gKNKXDipWswH59oivhGKBdCMg",
#     "mean_transaction_amount_btc": 44.6,
#     "total_time_interval": 5094000.0,
#     "unique_senders": 4,
#     "unique_receivers": 5,
#     "total_input_btc": 44.6,
#     "total_output_btc": 0.0,
#     "ratio_in_out": None,
#     "big_transactions_count": 1,
#     "small_transactions_count": 0,
#     "big_txn_sum_small_txn_sum_ratio": None,
#     "fraudulent_transaction_flag": 1,
# }


# {
#     "wallet_address": "bc173u6s74ksmz4x34x77j67znavtcw3m7mw49zkgq",
#     "mean_transaction_amount_btc": 24.517696395238097,
#     "total_time_interval": 163249200.0,
#     "unique_senders": 5,
#     "unique_receivers": 4,
#     "total_input_btc": 249.69171110000002,
#     "total_output_btc": 265.1799132,
#     "ratio_in_out": 0.9415936074753947,
#     "big_transactions_count": 21,
#     "small_transactions_count": 0,
#     "big_txn_sum_small_txn_sum_ratio": None,
#     "fraudulent_transaction_flag": 0,
# }
