import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from src.utils.helpers import get_logger

CSV_PATH = "data/logs/traffic.csv"

logger = get_logger()

def load_all_data():
    if not os.path.isfile(CSV_PATH):
        logger.warning("File traffic.csv belum ada")
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def classify_day_column(df):
    if df.empty or "timestamp" not in df.columns:
        return df
    df = df.copy()
    df["day_name"] = df["timestamp"].dt.day_name()
    df["day_type"] = df["day_name"].apply(
        lambda x: "weekend" if x in ["Saturday", "Sunday"] else "weekday"
    )
    df["is_saturday_night"] = (df["day_name"] == "Saturday") & (df["timestamp"].dt.hour >= 18)
    df["is_friday_night"] = (df["day_name"] == "Friday") & (df["timestamp"].dt.hour >= 18)
    return df

def filter_by_period(df, period):
    if df.empty:
        return df
    today = datetime.now()
    if period == "Hari Ini":
        return df[df["timestamp"].dt.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d")]
    elif period == "Kemarin":
        yesterday = today - timedelta(days=1)
        return df[df["timestamp"].dt.strftime("%Y-%m-%d") == yesterday.strftime("%Y-%m-%d")]
    elif period == "Minggu Ini":
        start = today - timedelta(days=today.weekday())
        return df[df["timestamp"] >= start.strftime("%Y-%m-%d")]
    elif period == "Akhir Pekan":
        df = classify_day_column(df)
        return df[df["day_type"] == "weekend"]
    elif period == "Hari Biasa":
        df = classify_day_column(df)
        return df[df["day_type"] == "weekday"]
    return df

def load_today_data():
    return filter_by_period(load_all_data(), "Hari Ini")

def daily_summary(df=None):
    if df is None:
        df = load_today_data()
    if df.empty:
        return {"message": "Belum ada data"}
    total = df["total"].sum()
    avg_per_hour = df.groupby(df["timestamp"].dt.hour)["total"].sum()
    peak_hour = int(avg_per_hour.idxmax()) if not avg_per_hour.empty else 0
    peak_count = int(avg_per_hour.max()) if not avg_per_hour.empty else 0
    return {
        "total_kendaraan": int(total),
        "avg_per_jam": round(df["total"].mean(), 1),
        "peak_hour": f"Jam {peak_hour}:00",
        "peak_count": peak_count,
        "total_baris": len(df)
    }

def hourly_trend(df=None):
    if df is None:
        df = load_today_data()
    if df.empty:
        return {}
    df["hour"] = df["timestamp"].dt.hour
    trend = df.groupby("hour")[["car", "motorcycle", "bus", "truck", "person"]].sum()
    return trend.to_dict(orient="index")

def weekday_vs_weekend_summary():
    df = classify_day_column(load_all_data())
    if df.empty:
        return {}
    groups = df.groupby("day_type").agg(
        total_kendaraan=("total", "sum"),
        avg_per_baris=("total", "mean"),
        total_baris=("total", "count")
    )
    return groups.to_dict(orient="index")

def day_type_hourly_trend():
    df = classify_day_column(load_all_data())
    if df.empty:
        return {}, {}
    df["hour"] = df["timestamp"].dt.hour
    weekday = df[df["day_type"] == "weekday"].groupby("hour")[["car", "motorcycle", "bus", "truck", "person"]].sum()
    weekend = df[df["day_type"] == "weekend"].groupby("hour")[["car", "motorcycle", "bus", "truck", "person"]].sum()
    return weekday.to_dict(orient="index"), weekend.to_dict(orient="index")

def export_summary():
    summary = daily_summary()
    out_path = f"data/logs/summary_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in summary.items():
            w.writerow([k, v])
    logger.info(f"Summary harian tersimpan: {out_path}")
    return out_path
