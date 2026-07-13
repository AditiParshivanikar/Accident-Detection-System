# AI-Powered Accident Detection & Alert System

A production-ready traffic monitoring, object tracking, and vehicle collision alert system featuring an enterprise-grade SaaS dashboard UI. 

This application uses **FastAPI (Python)** on the backend to run computer vision pipelines, connecting dynamically to a **React (Vite + Tailwind + AntD + Framer Motion)** frontend via REST APIs and real-time WebSockets.

---

## Key Features

- **Dual YOLO Model Support**: Load lightweight `YOLOv4-Tiny` via OpenCV's C++ DNN wrapper for high-speed CPU inference, or run custom `YOLOv8` PyTorch models.
- **Accident Collision Detection**: Automated intersection geometry algorithms checking axis-aligned bounding box overlaps.
- **Real-Time Video Processing**: Stream MP4/AVI/MOV video uploads frame-by-frame over WebSockets, displaying bounding box overlays, active frame counts, and FPS meters.
- **Live Webcam Monitoring**: Stream webcam capture from browser canvas elements or toggle local USB hardware capture directly from the backend.
- **Twilio SMS Alert Dispatch**: Instant mobile text notifications with a 60-second cooldown protection.
- **High-Fidelity Audio Siren**: Emergency sirens synthesized via browser Web Audio API (no heavy MP3 network loads).
- **Relational History & Analytics**: Log every incident database record locally with SQLite and export logs instantly as standard CSV sheets.

---

## Project Directory Structure

```text
├── backend/
│   ├── uploads/               # Saved video uploads & accident frames
│   ├── database.py            # SQLite session configurations
│   ├── models.py              # SQLAlchemy tables (Settings, History)
│   ├── schemas.py             # Pydantic payloads validation
│   ├── detection.py           # YOLO Model manager & collision algorithms
│   ├── sms.py                 # Twilio SMS utility & cooldown controls
│   └── main.py                # FastAPI endpoints & WebSocket routing
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx  # Overview metrics, charts, & logs
│   │   │   ├── UploadVideo.jsx# Drag-drop uploader, control panels
│   │   │   ├── LiveWebcam.jsx # Client/Server webcam stream views
│   │   │   ├── History.jsx    # Table filters, CSV exporter, image modals
│   │   │   ├── Analytics.jsx  # Recharts graphs
│   │   │   ├── Settings.jsx   # Threshold controls, Twilio setup
│   │   │   └── About.jsx      # Info modules
│   │   ├── App.jsx            # Routing shell, alarm audio loops
│   │   ├── main.jsx           # Mounting index
│   │   └── index.css          # Glassmorphic style layer & themes
│   ├── tailwind.config.js     # Tailwind setup
│   ├── postcss.config.js      # PostCSS configurations
│   ├── vite.config.js         # Vite bundler dev port & proxy routes
│   └── index.html             # HTML mounting core
├── requirements.txt           # Python backend dependencies
├── package.json               # Root scripts concurrently coordinator
├── Dockerfile                 # Multi-stage production container setup
├── vercel.json                # Vercel deployment directives
├── render.yaml                # Render Blueprint setup
└── README.md                  # Manual documentation
```

---

## Local Setup & Run Instruction

### Prerequisites

Make sure you have the following installed:
1. **Python 3.8+**
2. **Node.js v18+** & **NPM**

Ensure you have your weights files in the root folder:
- For YOLOv4-Tiny: `yolov4-tiny.cfg` & `yolov4-tiny.weights` (and `coco.names`)
- For YOLOv8: `best(3).pt` (or it will default download `yolov8n.pt`)

### Running the System Concurrently (Easiest)

From the root directory:

1. **Install Node dependencies**:
   ```bash
   npm run install:all
   ```

2. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Frontend & Backend concurrently**:
   ```bash
   npm run dev
   ```
   This command starts the:
   - FastAPI server at [http://localhost:8000](http://localhost:8000)
   - React UI dashboard at [http://localhost:3000](http://localhost:3000)

### Running Separately

If you prefer to run terminals separately:

**Backend Terminal**:
```bash
uvicorn backend.main:app --reload --port 8000
```

**Frontend Terminal**:
```bash
cd frontend
npm install
npm run dev
```

---

## Production Deployment Guides

### Deploying Frontend on Vercel

The root of this project contains a `vercel.json` configured for Vite.
1. Connect this repo to Vercel.
2. Select **Vite** as the framework.
3. Configure the Root Directory to `frontend`.
4. In Vercel environment variables, set backend routes or keep default local proxies.

### Deploying Fullstack on Render

Render builds from the root `render.yaml` using Docker. It builds both frontend assets and sets up python requirements automatically, mounting the application on port 8000.
1. In Render, select **Blueprints**.
2. Link this repo, and it will deploy automatically.

---

## Backend API Documentation

### REST Routes

| Endpoint | Method | Description |
|---|---|---|
| `/api/settings` | `GET` | Returns active system thresholds & Twilio credentials |
| `/api/settings` | `PUT` | Updates pipeline thresholds and Twilio inputs |
| `/api/settings/test-sms` | `POST` | Triggers a test SMS bypasses rate cooldowns |
| `/api/stats` | `GET` | Aggregates logs to show dashboard counter stats |
| `/api/analytics` | `GET` | Compiles daily trend and vehicle ratio coordinates for charts |
| `/api/history` | `GET` | Returns list of logs. Supports `source` & `accident_only` filters |
| `/api/history/{id}` | `DELETE` | Removes historical database row and snapshot file from disk |
| `/api/upload` | `POST` | Uploads an MP4/AVI/MOV file, checking file integrity |
| `/api/health` | `GET` | Gathers CPU/RAM allocations and GPU hardware statuses |
| `/api/history/download` | `GET` | Generates and downloads the relational log database as a CSV sheet |

### WebSocket Streams

- **Video Processing Stream**: `ws://localhost:8000/api/detection/video/{video_name}`
  - Receives actions: `{"action": "pause"}`, `{"action": "resume"}`, `{"action": "stop"}`.
  - Emits JSON containing base64 JPEG strings and live pipeline metric aggregates.
- **Webcam Processing Stream**: `ws://localhost:8000/api/detection/webcam`
  - Receives base64 frame chunks from client browser canvas elements, or receives `{"action": "start_local"}` to utilize direct USB camera feeds.
