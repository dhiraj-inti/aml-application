import pandas as pd
import numpy as np


def load_transactions(path):
    df = pd.read_csv(path)
    required = {"sender", "receiver", "amount", "timestamp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input file missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def compute_wallet_metrics(wallet, txs_df, sender, receiver, amount, timestamp):

    MEAN_BTC_THRESHOLD = 47.5
    UNIQUE_SENDERS_MAX = 7
    UNIQUE_RECEIVERS_MAX = 7
    RATIO_MIN = 0.5
    RATIO_MAX = 1.5
    BIG_TXN_BTC_THRESHOLD = 1.0
    INTERVAL_SECONDS_MIN = 720000

    RULES = [
        {"rule": f"Mean transaction amount > {MEAN_BTC_THRESHOLD} BTC", "threshold": MEAN_BTC_THRESHOLD},
        {
            "rule": f"Average time intervals < {INTERVAL_SECONDS_MIN} seconds ({INTERVAL_SECONDS_MIN/3600} hours)",
            "threshold": INTERVAL_SECONDS_MIN,
        },
        {"rule": f"Unique senders > {UNIQUE_SENDERS_MAX}", "threshold": UNIQUE_SENDERS_MAX},
        {"rule": f"Unique receivers > {UNIQUE_RECEIVERS_MAX}", "threshold": UNIQUE_RECEIVERS_MAX},
        {
            "rule": f"Fan-in/fan-out ratio not between {RATIO_MIN} and {RATIO_MAX}",
            "min": RATIO_MIN,
            "max": RATIO_MAX,
        },
        {"rule": f"Big TXN threshold < {BIG_TXN_BTC_THRESHOLD} BTC", "threshold": BIG_TXN_BTC_THRESHOLD},
    ]

    new_tx = {
        "sender": sender,
        "receiver": receiver,
        "amount": float(amount),
        "timestamp": pd.to_datetime(timestamp, utc=True),
    }
    # Get tx histrory

    relevant = txs_df[
        (txs_df["sender"] == wallet) | (txs_df["receiver"] == wallet)
    ].copy()
    relevant = relevant.sort_values("timestamp", ascending=False).head(20)
    # Appending tx
    new_tx_df = pd.DataFrame([new_tx])

    relevant = pd.concat([relevant, new_tx_df], ignore_index=True)
    relevant["timestamp"] = pd.to_datetime(relevant["timestamp"], utc=True)

    relevant = relevant.sort_values("timestamp").reset_index(drop=True)

    mean_tx_btc = relevant["amount"].mean()
    total_time_interval = (
        (relevant["timestamp"].iloc[-1] - relevant["timestamp"].iloc[0]).total_seconds()
        if len(relevant) > 1
        else 0.0
    )

    unique_senders = relevant.loc[relevant["receiver"] == wallet, "sender"].nunique()

    unique_receivers = relevant.loc[relevant["sender"] == wallet, "receiver"].nunique()
    total_input_btc = relevant.loc[relevant["sender"] == wallet, "amount"].sum()
    total_output_btc = relevant.loc[relevant["receiver"] == wallet, "amount"].sum()
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
    }, RULES
