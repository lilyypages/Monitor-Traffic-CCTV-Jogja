# Traffic Monitor CCTV Jogja

**Analisis Kepadatan Kendaraan dan Pengunjung Kawasan Malioboro Menggunakan Real-Time CCTV Analytics dengan Big Data Pipeline**

## Deskripsi

Sistem monitoring kepadatan kendaraan dan pengunjung Kawasan Malioboro secara **end-to-end** menggunakan arsitektur **Big Data modern**. Data diambil dari **CCTV YouTube Jogja** secara real-time, diproses dengan **YOLOv8 + ByteTrack** untuk deteksi dan tracking kendaraan, dialirkan melalui **Apache Kafka** ke **PySpark Structured Streaming** untuk stream processing dan **Apache Spark Batch** untuk analisis batch, lalu divisualisasikan di **Grafana** dan **Metabase** dengan alerting via **Telegram/Email**.

## Arsitektur (10 Layer)

```
YouTube CCTV → Stream Extractor → YOLOv8 + ByteTrack → Kafka → Spark Streaming → PostgreSQL + MinIO
                                              ↘ Spark Batch (scheduled by Airflow)
                                                            ↘ ML Pipeline (prediksi kepadatan)
Grafana dashboard + Prometheus/Loki monitoring + Telegram/Email alerting
```

| Layer | Stack |
|-------|-------|
| **Data Source** | CCTV YouTube Jogja (2 camera livestream) |
| **Ingestion** | yt-dlp extract stream URL, Python poller tiap 5 detik |
| **Stream Processing** | YOLOv8 object detection + ByteTrack tracking per frame |
| **Message Queue** | Apache Kafka — 3 topic (traffic-events, traffic-alerts, traffic-aggregated) |
| **Stream Processing (Big Data)** | PySpark Structured Streaming — 5 query (traffic count, density, alerts, aggregations) |
| **Batch Processing** | Apache Spark — 6 analisis (kepadatan per jam/hari, peak hour, tren mingguan, weekday vs weekend, prediksi) |
| **Machine Learning** | K-Means clustering (pola kepadatan) + Time Series Forecasting (prediksi kepadatan 1-6 jam ke depan) |
| **Storage** | PostgreSQL (data warehouse) + MinIO (data lake S3-compatible, raw frame metadata) |
| **Visualization** | Grafana (panel: GeoMap titik kemacetan, timeseries count, piechart distribusi kendaraan, bargauge kepadatan per kamera) + Metabase (dashboard interaktif/ad-hoc) |
| **Monitoring & Alerting** | Prometheus (metrik throughput + alert rules) + Loki (log aggregation) + Telegram alerting (kepadatan tinggi, anomaly detection) |
| **Orchestration** | Apache Airflow — 3 DAG (daily batch summary, weekly ML retrain, pipeline health check tiap 30 menit) |

## Struktur Folder

```
.
├── main.py                          # Entry point stream processing (YOLO + ByteTrack)
├── docker-compose.yml               # 19 container orchestration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── README.md                        # Dokumentasi
│
├── models/
│   └── yolov8n.pt                   # Model YOLOv8 nano
│
├── data/
│   └── logs/
│       ├── traffic.csv              # Data deteksi real-time
│       ├── app.log                  # Log aplikasi
│       └── error.log                # Log error
│
├── src/
│   ├── ingestion/                   # Data ingestion layer
│   │   ├── youtube_stream.py        # Ambil URL stream YouTube via yt-dlp
│   │   └── poller.py                # Kafka producer untuk stream data
│   │
│   ├── processing/                  # Stream processing layer
│   │   ├── detection/
│   │   │   └── vehicle_detection.py # Deteksi kendaraan YOLOv8
│   │   └── tracking/
│   │       └── vehicle_tracking.py  # ByteTrack tracking
│   │
│   ├── kafka/                       # Message queue layer
│   │   ├── producer.py              # Kafka producer
│   │   └── consumer.py              # Kafka consumer
│   │
│   ├── spark/                       # Big data processing layer
│   │   ├── streaming/               # PySpark Structured Streaming
│   │   │   ├── traffic_count_query.py
│   │   │   ├── density_query.py
│   │   │   ├── alert_query.py
│   │   │   └── aggregation_query.py
│   │   └── batch/                   # Apache Spark Batch
│   │       ├── hourly_density.py
│   │       ├── peak_hour_analysis.py
│   │       ├── weekly_trend.py
│   │       ├── weekday_weekend.py
│   │       └── prediction_input.py
│   │
│   ├── ml/                          # Machine learning layer
│   │   ├── clustering.py            # K-Means pola kepadatan
│   │   ├── forecasting.py           # Time Series prediksi 1-6 jam
│   │   └── train.py                 # Pipeline training
│   │
│   ├── storage/                     # Storage layer
│   │   ├── logger.py                # Simpan ke CSV + PostgreSQL
│   │   └── minio_client.py          # Client MinIO S3-compatible
│   │
│   ├── airflow/
│   │   └── dags/                    # Airflow orchestration
│   │       ├── daily_batch.py       # Batch processing harian
│   │       ├── weekly_ml_retrain.py # Retrain ML mingguan
│   │       └── pipeline_health_check.py  # Health check tiap 30 menit
│   │
│   ├── dashboard/                   # Visualization layer
│   │   ├── app.py                   # Streamlit dashboard
│   │   ├── grafana/dashboards/
│   │   │   └── traffic-monitor.json # Grafana dashboard config
│   │   └── metabase/
│   │       └── setup.py             # Metabase setup
│   │
│   ├── monitoring/                  # Monitoring layer
│   │   ├── prometheus/
│   │   │   ├── prometheus.yml       # Prometheus config
│   │   │   └── alert_rules.yml      # Alert rules
│   │   └── loki/
│   │       └── loki-config.yml      # Loki config
│   │
│   ├── alerting/                    # Alerting layer
│   │   ├── telegram_bot.py          # Telegram notifier
│   │   └── email_notifier.py        # Email notifier
│   │
│   ├── security/                    # Security layer
│   │   ├── rbac.py                  # Role-based access control
│   │   └── credential_manager.py    # Credential management
│   │
│   ├── governance/                  # Governance layer
│   │   ├── data_lineage.py          # Data lineage tracker
│   │   └── audit_logger.py          # Audit logging ke PostgreSQL
│   │
│   ├── config/
│   │   ├── cameras.py               # Konfigurasi kamera CCTV
│   │   └── settings.py              # Global configuration
│   │
│   ├── multi_camera/
│   │   └── camera_manager.py        # Manajemen multi-kamera
│   │
│   ├── analytics/
│   │   └── traffic_counter.py       # Batch processing harian (legacy)
│   │
│   └── utils/
│       └── helpers.py               # Logging & utility
│
├── tests/                           # Unit testing
│   ├── conftest.py                  # Test fixtures
│   ├── test_detection.py
│   ├── test_alerting.py
│   └── test_governance.py
│
├── docker/                          # Dockerfiles per service
│   ├── app/Dockerfile
│   ├── spark/Dockerfile
│   ├── airflow/Dockerfile
│   └── kafka/Dockerfile
│
└── scripts/                         # Setup scripts
    ├── init_kafka_topics.sh
    ├── init_minio_buckets.sh
    └── setup.sh
```

## Tech Stack

| Kategori | Teknologi |
|----------|-----------|
| **Computer Vision** | YOLOv8, ByteTrack (supervision), OpenCV |
| **Stream Extraction** | yt-dlp |
| **Message Queue** | Apache Kafka (3 topic, 3 partition) |
| **Stream Processing** | PySpark Structured Streaming |
| **Batch Processing** | Apache Spark |
| **Machine Learning** | scikit-learn (K-Means), Prophet/Statsmodels (Time Series) |
| **Database** | PostgreSQL (data warehouse), MinIO (data lake S3) |
| **Visualization** | Grafana (13+ panel), Metabase (ad-hoc), Streamlit (real-time) |
| **Monitoring** | Prometheus, Loki |
| **Alerting** | Telegram Bot, SMTP Email |
| **Orchestration** | Apache Airflow (CeleryExecutor) |
| **Container** | Docker Compose — 19 container |
| **Python** | 3.11+ |

## Container (19 Services)

| # | Container | Port | Healthcheck |
|---|-----------|------|-------------|
| 1 | traffic-zookeeper | 2181 | ✅ |
| 2 | traffic-kafka | 9092 | ✅ |
| 3 | traffic-postgres | 5432 | ✅ |
| 4 | traffic-minio | 9000, 9001 | ✅ |
| 5 | traffic-spark-master | 8080, 7077 | ✅ |
| 6 | traffic-spark-worker-1 | 8081 | ✅ |
| 7 | traffic-spark-worker-2 | 8082 | ✅ |
| 8 | traffic-grafana | 3000 | ✅ |
| 9 | traffic-metabase | 3001 | ✅ |
| 10 | traffic-prometheus | 9090 | ✅ |
| 11 | traffic-loki | 3100 | ✅ |
| 12 | traffic-airflow-db | — | ✅ |
| 13 | traffic-airflow-redis | — | ✅ |
| 14 | traffic-airflow-webserver | 8085 | ✅ |
| 15 | traffic-airflow-scheduler | — | ✅ |
| 16 | traffic-airflow-worker | — | ✅ |
| 17 | traffic-app | — | ✅ |
| 18 | traffic-kafka-producer | — | ✅ |
| 19 | traffic-alerting | — | ✅ |

## Fitur Non-Fungsional

- **Docker Compose** — 19 container, semua terdefinisi dengan healthcheck, network isolasi (`traffic-network`)
- **Security** — RBAC simulation (admin/analyst/viewer/operator), credential manager, env-based secrets
- **Governance** — Data lineage tracker + audit logging ke PostgreSQL
- **Fault tolerance** — Kafka replication, Spark checkpointing, retry exponential backoff
- **Unit tests** — 30 test (26 pass), coverage di detection, alerting, governance

## Dataset

**CCTV YouTube Jogja (2 sumber):**

| Camera | URL | Koordinat |
|--------|-----|-----------|
| Malioboro - Plaza | `https://www.youtube.com/watch?v=q7ZX2tSFEDg` | -7.792, 110.365 |
| Malioboro - Utara Inna | `https://www.youtube.com/live/ozAEmr_r5Pg` | -7.791, 110.366 |

**Output data per 10 detik:**
```csv
timestamp,camera_id,car,motorcycle,bus,truck,person,total,fps
2025-01-01 10:00:05,malioboro_01,12,45,2,1,33,93,28.5
```

**Struktur Database PostgreSQL:**
```sql
CREATE TABLE traffic_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    camera_id TEXT,
    car INT,
    motorcycle INT,
    bus INT,
    truck INT,
    person INT,
    total INT,
    fps FLOAT
);
```

## Output Utama

- Dashboard real-time kepadatan di **Grafana** (localhost:3000)
- Dashboard interaktif/ad-hoc di **Metabase** (localhost:3001)
- Dashboard real-time di **Streamlit** (localhost:8501)
- Notifikasi **Telegram** + **Email** untuk kepadatan tinggi ( threshold)
- Prediksi kepadatan 1-6 jam ke depan via ML
- Data historis di **PostgreSQL** + raw metadata di **MinIO**
- DAG **Airflow** untuk automation (daily batch, weekly ML retrain, health check)

## Cara Install

### Prerequisites
- Python 3.11+
- Git
- Docker & Docker Compose

### Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd Monitor-Traffic-CCTV-Jogja

# 2. Setup environment
cp .env.example .env
# Edit .env sesuai konfigurasi (Telegram token, SMTP, dll.)

# 3. Jalankan semua container
docker-compose up -d
# 19 container akan running

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Setup Kafka topics
scripts/init_kafka_topics.sh
```

### Menjalankan Stream Processing

```bash
python main.py
```
- Deteksi kendaraan + tracking real-time dari CCTV YouTube
- Tekan `q` untuk berhenti
- Data otomatis tersimpan ke CSV & PostgreSQL

### Dashboard

```bash
# Streamlit dashboard
streamlit run src/dashboard/app.py
# Buka http://localhost:8501

# Grafana dashboard
# Buka http://localhost:3000 (admin/admin)

# Metabase dashboard
# Buka http://localhost:3001
```

## Status Fitur

| Fitur | Status |
|-------|--------|
| Real-time stream YouTube | ✅ |
| Deteksi kendaraan YOLOv8 | ✅ |
| Object tracking ByteTrack | ✅ |
| Counting kendaraan unik | ✅ |
| Simpan ke CSV + PostgreSQL | ✅ |
| Dashboard Streamlit | ✅ |
| Grafana dashboard | 📌 Stub |
| Metabase dashboard | 📌 Stub |
| Kafka integration | 📌 Stub |
| Spark Streaming | 📌 Stub |
| Spark Batch | 📌 Stub |
| ML Pipeline (K-Means + Forecasting) | 📌 Stub |
| Airflow DAGs | 📌 Stub |
| Prometheus + Loki monitoring | 📌 Stub |
| Telegram + Email alerting | 📌 Stub |
| RBAC Security | 📌 Stub |
| Data Lineage & Audit | 📌 Stub |

## Mata Kuliah

**Infrastruktur dan Platform Big Data** — Semester 4
**Tema:** Analisis Kepadatan Kendaraan dan Pengunjung Kawasan Malioboro Menggunakan Real-Time CCTV Analytics dengan Big Data Pipeline
