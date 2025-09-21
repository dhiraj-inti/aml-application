
import argparse
import pandas as pd
import numpy as np


MEAN_BTC_THRESHOLD = 187.5  
AVG_INTERVAL_SECONDS_MIN = 10 * 3600  
UNIQUE_SENDERS_MAX = 7
UNIQUE_RECEIVERS_MAX = 7
RATIO_MIN = 0.5
RATIO_MAX = 1.5
BIG_TXN_BTC_THRESHOLD = 1.0 


def load_transactions(path):
    df = pd.read_csv(path)
    required = {"input_address", "output_address", "transaction_value_btc", "timestamp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input file missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def compute_wallet_metrics_for_wallet(wallet, txs_df, n_last=20):
    related = txs_df[
        (txs_df["input_address"] == wallet) | (txs_df["output_address"] == wallet)
    ].copy()
    if related.empty:
        return None

    related = related.sort_values("timestamp", ascending=False).head(n_last)
    related = related.sort_values("timestamp").reset_index(drop=True)

    mean_tx_btc = related["transaction_value_btc"].mean()

    if len(related) > 1:
        intervals = related["timestamp"].diff().dropna().dt.total_seconds()
        avg_interval_seconds = intervals.mean()
    else:
        avg_interval_seconds = 0.0

    unique_senders = related["input_address"].nunique()
    unique_receivers = related["output_address"].nunique()

    total_input_btc = related.loc[
        related["input_address"] == wallet, "transaction_value_btc"
    ].sum()
    total_output_btc = related.loc[
        related["output_address"] == wallet, "transaction_value_btc"
    ].sum()
    ratio_in_out = (
        total_input_btc / total_output_btc if total_output_btc != 0 else np.nan
    )

    # Big / small txns
    big_tx = related[related["transaction_value_btc"] >= BIG_TXN_BTC_THRESHOLD]
    small_tx = related[related["transaction_value_btc"] < BIG_TXN_BTC_THRESHOLD]
    big_count = len(big_tx)
    small_count = len(small_tx)
    big_sum = big_tx["transaction_value_btc"].sum()
    small_sum = small_tx["transaction_value_btc"].sum()
    ratio_big_small = big_sum / small_sum if small_sum > 0 else np.nan

    fraud_conditions = {
        "mean_btc_above_threshold": mean_tx_btc > MEAN_BTC_THRESHOLD,
        "avg_interval_below_10hrs": avg_interval_seconds < AVG_INTERVAL_SECONDS_MIN,
        "unique_senders_exceed": unique_senders > UNIQUE_SENDERS_MAX,
        "unique_receivers_exceed": unique_receivers > UNIQUE_RECEIVERS_MAX,
        "ratio_out_of_range": (
            not (RATIO_MIN <= ratio_in_out <= RATIO_MAX)
            if not np.isnan(ratio_in_out)
            else True
        ),
    }
    fraudulent_flag = int(any(fraud_conditions.values()))

    return {
        "wallet_address": wallet,
        "mean_transaction_amount_btc": mean_tx_btc,
        "average_time_interval_seconds": avg_interval_seconds,
        "unique_senders": unique_senders,
        "unique_receivers": unique_receivers,
        "total_input_btc": total_input_btc,
        "total_output_btc": total_output_btc,
        "ratio_in_out": ratio_in_out,
        "big_transactions_count": big_count,
        "small_transactions_count": small_count,
        "big_txn_sum_small_txn_sum_ratio": ratio_big_small,
        "fraudulent_transaction_flag": fraudulent_flag,
    }


def derive_wallet_metrics(txs_csv_path, out_csv_path, n_last=20):
    txs = load_transactions(txs_csv_path)
    wallets = pd.Index(
        txs["input_address"].tolist() + txs["output_address"].tolist()
    ).unique()
    metrics_list = []
    for w in wallets:
        m = compute_wallet_metrics_for_wallet(w, txs, n_last=n_last)
        if m:
            metrics_list.append(m)
    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv(out_csv_path, index=False)
    return metrics_df


def parse_args():
    p = argparse.ArgumentParser(
        description="Derive wallet metrics from transaction CSV (BTC only)"
    )
    p.add_argument("--txs", required=True, help="Path to transactions CSV")
    p.add_argument("--out", required=True, help="Path to output metrics CSV")
    p.add_argument(
        "--n_last",
        required=False,
        default=20,
        type=int,
        help="Number of last transactions per wallet (default 20)",
    )
    return p.parse_args()


if __name__ == "__main__":
    input_path = "hsdf.csv"
    output_path = "wallet_metrics.csv"
    print("Computing wallet metrics (BTC only)...")
    metrics = derive_wallet_metrics(input_path, output_path)
    print(f"Done. Wrote {len(metrics)} wallets to {output_path}")
