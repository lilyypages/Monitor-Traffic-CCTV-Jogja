# Traffic Monitor CCTV Jogja

**Analisis Kepadatan Kendaraan dan Pengunjung Kawasan Malioboro Menggunakan Real-Time CCTV Analytics**

## Deskripsi

Sistem real-time traffic monitoring berbasis Computer Vision dan Big Data pipeline. Menggunakan CCTV YouTube Jogja sebagai sumber data, YOLOv8 untuk deteksi objek, ByteTrack untuk tracking, dan Streamlit untuk dashboard visualisasi.

## Arsitektur Sistem

```
[Data Source] → [Stream Processing] → [Storage] → [Analytics] → [Dashboard]
     │                  │                   │             │             │
  YouTube           YOLOv8 +             CSV /        Batch          Streamlit
  CCTV Jogja        ByteTrack           PostgreSQL   Harian         + Plotly
```

### Pipeline:
1. **Data Source** — CCTV YouTube Jogja livestream
2. **Ingestion** — yt-dlp mengambil URL stream
3. **Stream Processing** — YOLOv8 deteksi + ByteTrack tracking per frame
4. **Storage** — Data disimpan ke CSV (fallback) dan PostgreSQL
5. **Batch Processing** — Rekap harian: total kendaraan, peak hour, rata-rata per jam
6. **Dashboard** — Streamlit dashboard real-time dengan grafik interaktif

## Tech Stack

- **Python 3.11+**
- **YOLOv8** — Object detection (ultralytics)
- **ByteTrack** — Object tracking (supervision)
- **OpenCV** — Image processing & visualization
- **yt-dlp** — YouTube stream extraction
- **Streamlit** — Dashboard web
- **Plotly** — Grafik interaktif
- **Pandas** — Data analysis
- **PostgreSQL** — Database (opsional, fallback ke CSV)
- **Docker** — Containerized PostgreSQL deployment

## Struktur Folder

```
.
├── main.py                     # Entry point stream processing
├── requirements.txt            # Python dependencies
├── README.md                   # Dokumentasi
├── models/
│   └── yolov8n.pt              # Model YOLOv8 nano
├── data/
│   └── logs/
│       ├── traffic.csv         # Data deteksi real-time
│       ├── app.log             # Log aplikasi
│       ├── error.log           # Log error
│       └── summary_YYYYMMDD.csv # Summary harian
└── src/
    ├── config/
    │   └── cameras.py          # Konfigurasi kamera CCTV
    ├── stream/
    │   └── youtube_stream.py   # Ambil URL stream YouTube
    ├── detection/
    │   └── vehicle_detection.py # Deteksi kendaraan YOLOv8
    ├── tracking/
    │   └── vehicle_tracking.py  # ByteTrack tracking
    ├── storage/
    │   └── logger.py           # Simpan ke CSV + PostgreSQL
    ├── analytics/
    │   └── traffic_counter.py  # Batch processing harian
    ├── dashboard/
    │   └── app.py              # Streamlit dashboard
    ├── multi_camera/
    │   └── camera_manager.py   # Manajemen multi-kamera
    └── utils/
        └── helpers.py          # Logging & utility
```

##  Cara Install

### Prerequisites
- Python 3.11+
- Git
- (Opsional) Docker & Docker Compose untuk PostgreSQL

### Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd Monitor-Traffic-CCTV-Jogja

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup PostgreSQL (pilih salah satu)
```

#### PostgreSQL via Docker (recommended)
```bash
docker-compose up -d
```
Container `traffic-postgres` akan jalan di `localhost:5432`, database `traffic_db` auto dibuat.

### 1. Stream Processing (deteksi & tracking real-time)
```bash
python main.py
```
- Tekan `q` untuk berhenti
- Data otomatis tersimpan ke CSV & PostgreSQL setiap 10 detik
- Log muncul di terminal dan `data/logs/app.log`

### 2. Dashboard Streamlit
```bash
streamlit run src/dashboard/app.py
```
- Buka browser di `http://localhost:8501`
- Lihat grafik real-time kendaraan per menit
- Distribusi kendaraan, traffic per jam

### 3. Batch Processing (rekap harian)
```python
from src.analytics.traffic_counter import daily_summary, export_summary

summary = daily_summary()
print(summary)

export_summary()
# -> data/logs/summary_20250101.csv
```

## Output Data

### Format CSV (`data/logs/traffic.csv`)
```csv
timestamp,camera_id,car,motorcycle,bus,truck,person,total,fps
2025-01-01 10:00:05,malioboro_01,12,45,2,1,33,93,28.5
```

### Struktur Database PostgreSQL
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

## Fitur

| Fitur | Status |
|-------|--------|
| Real-time stream YouTube | ✅ |
| Deteksi kendaraan YOLOv8 | ✅ |
| Object tracking ByteTrack | ✅ |
| Counting kendaraan unik | ✅ |
| Simpan ke CSV | ✅ |
| Simpan ke PostgreSQL | ✅ |
| Dashboard Streamlit | ✅ |
| Grafik per menit (Plotly) | ✅ |
| Distribusi kendaraan (Pie) | ✅ |
| Traffic per jam (Bar) | ✅ |
| Batch summary harian | ✅ |
| Multi-camera support | ✅ |
| Logging & Monitoring | ✅ |
| FPS monitoring | ✅ |


**Mata Kuliah:** Infrastruktur dan Platform Big Data  
**Tema:** Analisis Kepadatan Kendaraan dan Pengunjung Kawasan Malioboro  

