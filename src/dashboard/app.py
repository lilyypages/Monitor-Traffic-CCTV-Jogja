import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from src.analytics.traffic_counter import (
    load_all_data, load_today_data, filter_by_period, classify_day_column,
    daily_summary, hourly_trend, weekday_vs_weekend_summary, day_type_hourly_trend
)
from src.config.cameras import CAMERAS

CSV_PATH = "data/logs/traffic.csv"
REFRESH_RATE = 5

st.set_page_config(page_title="Traffic Monitor Jogja", layout="wide")
st.title("Analisis Kepadatan Kendaraan & Pengunjung Malioboro")
st.markdown("**Real-Time CCTV Analytics** — Infrastruktur dan Platform Big Data")

camera_info = CAMERAS["malioboro_01"]
with st.sidebar:
    st.header("Info CCTV")
    st.write(f"**Lokasi:** {camera_info['name']}")
    st.write(f"**Latitude:** {camera_info['lat']}")
    st.write(f"**Longitude:** {camera_info['lon']}")
    st.write(f"**Status:** Aktif")

    st.header("Dataset Info")
    if os.path.isfile(CSV_PATH):
        df_check = pd.read_csv(CSV_PATH)
        st.write(f"Total data: {len(df_check)} baris")
        if not df_check.empty:
            t0 = df_check['timestamp'].iloc[0]
            t1 = df_check['timestamp'].iloc[-1]
            st.write(f"Periode: {t0} s.d. {t1}")
    else:
        st.write("Belum ada data")

    st.header("Filter Waktu")
    period = st.selectbox(
        "Tampilkan Data",
        ["Hari Ini", "Kemarin", "Minggu Ini", "Akhir Pekan", "Hari Biasa", "Hari Biasa vs Akhir Pekan"]
    )

    auto_refresh = st.checkbox("Auto Refresh", value=True)

placeholder_metrics = st.empty()
placeholder_charts = st.empty()
placeholder_hourly = st.empty()

while True:
    if period == "Hari Biasa vs Akhir Pekan":
        df = classify_day_column(load_all_data())
        summary_wd_we = weekday_vs_weekend_summary()
        weekday_trend, weekend_trend = day_type_hourly_trend()
    else:
        df = filter_by_period(load_all_data(), period)
        summary = daily_summary(df)

    with placeholder_metrics.container():
        if period == "Hari Biasa vs Akhir Pekan":
            if summary_wd_we:
                m1, m2, m3, m4 = st.columns(4)
                wd = summary_wd_we.get("weekday", {})
                we = summary_wd_we.get("weekend", {})
                m1.metric("Hari Biasa", wd.get("total_kendaraan", 0), help="Total weekday")
                m2.metric("Akhir Pekan", we.get("total_kendaraan", 0), help="Total weekend")
                delta = (we.get("total_kendaraan", 0) or 0) - (wd.get("total_kendaraan", 0) or 0)
                arrow = "↑" if delta > 0 else "↓"
                m3.metric("Selisih", f"{arrow} {abs(delta)}")
                ratio = ((we.get("avg_per_baris", 0) or 0) / (wd.get("avg_per_baris", 1) or 1) - 1) * 100
                m4.metric("Rata-rata Lebih", f"{ratio:+.0f}%")
            else:
                st.info("Menunggu data untuk perbandingan...")
        else:
            if isinstance(summary, dict) and "message" not in summary:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Kendaraan", summary.get("total_kendaraan", 0))
                m2.metric("Rata-rata per Baris", summary.get("avg_per_jam", 0))
                m3.metric("Peak Hour", summary.get("peak_hour", "-"))
                m4.metric("Peak Count", summary.get("peak_count", 0))
            else:
                st.info("Menunggu data dari stream processing...")

    with placeholder_charts.container():
        if period == "Hari Biasa vs Akhir Pekan":
            if weekday_trend or weekend_trend:
                c1, c2 = st.columns(2)
                with c1:
                    if weekday_trend:
                        wd_df = pd.DataFrame(weekday_trend).T
                        wd_df.index = wd_df.index.astype(str)
                        fig_wd = px.bar(wd_df, barmode="group", title="Trafik per Jam — Hari Biasa")
                        st.plotly_chart(fig_wd, use_container_width=True)
                with c2:
                    if weekend_trend:
                        we_df = pd.DataFrame(weekend_trend).T
                        we_df.index = we_df.index.astype(str)
                        fig_we = px.bar(we_df, barmode="group", title="Trafik per Jam — Akhir Pekan")
                        st.plotly_chart(fig_we, use_container_width=True)
            else:
                st.info("Chart akan tampil setelah ada data")
        else:
            if not df.empty:
                c1, c2 = st.columns(2)
                with c1:
                    df_line = df.copy()
                    df_line["menit"] = df_line["timestamp"].dt.strftime("%H:%M")
                    line_data = df_line.groupby("menit")[["car", "motorcycle", "bus", "truck", "person"]].sum().reset_index()
                    fig_line = px.line(line_data, x="menit", y=["car", "motorcycle", "bus", "truck", "person"],
                        title="Kendaraan per Menit", markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                with c2:
                    total_per_jenis = df[["car", "motorcycle", "bus", "truck", "person"]].sum()
                    fig_pie = px.pie(values=total_per_jenis.values, names=total_per_jenis.index, title="Distribusi Kendaraan")
                    st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Chart akan tampil setelah ada data")

    with placeholder_hourly.container():
        if period != "Hari Biasa vs Akhir Pekan":
            trend = hourly_trend(df)
            if trend:
                hourly_df = pd.DataFrame(trend).T
                fig_hourly = px.bar(hourly_df, barmode="group", title="Trafik per Jam")
                st.plotly_chart(fig_hourly, use_container_width=True)

    if not auto_refresh:
        break
    time.sleep(REFRESH_RATE)
    st.rerun()
