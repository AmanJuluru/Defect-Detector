# 🚗 Car Defect Detection Using YOLO Model

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-13+-000000?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)
![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

**An AI-powered web portal for automobile exterior defect detection using deep learning**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Demo](#-demo) • [Tech Stack](#-tech-stack) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

This project is a **secure web portal** designed for manufacturing inspection teams to detect exterior vehicle defects using state-of-the-art **YOLOv8** deep learning technology. The system enables quality assurance teams to upload vehicle images and receive instant AI-powered defect analysis with visual bounding box annotations.

### 🎯 Key Highlights

- **Real-time Detection**: Sub-second inference time for instant results backed by FastAPI.
- **Interactive Dashboard**: Modern Next.js interface for viewing detection history and statistics.
- **Secure Access**: Robust user authentication and management powered by Firebase.
- **Visual Feedback**: Color-coded bounding boxes for easy defect identification.
- **History Tracking**: Complete audit trail of all uploaded inspections.

---

## ✨ Features

### 🔍 Defect Detection
The pre-trained YOLO model can detect **5 types** of automobile exterior defects:

| Defect Type | Visual Indicator |
|-------------|------------------|
| 🔴 **Dent** | Pink bounding box |
| 🔵 **Scratch** | Blue bounding box |
| 🟡 **Lamp Broken** | Yellow bounding box |
| 🟣 **Glass Broken** | Purple bounding box |
| ⭕ **Tire Flat** | Red bounding box |

### 🛡️ User Management (Firebase)
- Google Sign-In & Email/Password authentication
- Secure session management
- User profile synchronization

### 📊 Dashboard & Analytics
- Real-time inspection statistics
- Visual breakdown of broken vs non-broken vehicles
- Recent inspection activity feed

---

## 🚀 Installation

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Firebase Account & Credentials

### Step 1: Clone the Repository

```bash
git clone https://github.com/AmanJuluru/Defect-Detector.git
cd Defect-Detector
```

### Step 2: Backend Setup

Navigate to the backend directory:
```bash
cd backend
python -m venv .venv
# Activate Virtual Env (Windows)
.venv\Scripts\activate
# Install Dependencies
pip install -r requirements.txt
```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The backend will start at `http://127.0.0.1:8000`

### Step 3: Frontend Setup

Navigate to the frontend directory:
```bash
cd ../frontend
npm install
```

Start the Next.js development server:
```bash
npm run dev
```
The application will be accessible at `http://localhost:3000`

---

## 💻 Usage

### 1. Register/Login
Log in using your secure credentials or Google account.

### 2. Upload 
Navigate to the **Upload** section and:
- Select a vehicle image (JPG, PNG)
- Capture a photo using the **Webcam** feature
- Use WebCam to show LiveFeed for **Real Time Detection**

### 3. View Results
The AI processes the image and displays:
- Annotated image with bounding boxes
- Defect list with confidence scores
- Status: **Broken** / **Non-Broken**

---

## 🎬 Demo

### Detection Flow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Client App     │────▶│  FastAPI API    │────▶│  YOLO Inference │
│  (Next.js)      │     │  (Python)       │     │  (PyTorch)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                       │
┌─────────────────┐     ┌─────────────────┐            ▼
│  Render Results │◀────│  JSON Response  │◀───(Detections)
│  (Dashboard)    │     │  & Annotations  │
└─────────────────┘     └─────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core logic |
| **FastAPI** | High-performance API framework |
| **Firebase Admin** | User authentication & management |

### Machine Learning
| Technology | Purpose |
|------------|---------|
| **Ultralytics YOLOv8** | Object detection model |
| **OpenCV** | Image processing |
| **PyTorch** | Deep learning framework |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 13** | React framework |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Styling & UI components |

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── inference.py            # YOLO model wrapper
│   ├── models.py               # Pydantic models
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── app/                    # Next.js App Router
│   │   ├── dashboard/          # Dashboard pages
│   │   ├── upload/             # Upload interface
│   │   └── login/              # Auth pages
│   └── components/             # Reusable UI components
├── model/
│   └── defect_model.pt         # Pre-trained YOLO weights
└── README.md                   # Project documentation
```

---

## 🔐 Security Features

| Feature | Implementation |
|---------|----------------|
| **Authentication** | Firebase Auth (OAuth2 & JWT) |
| **API Security** | Bearer Token Validation |
| **CORS Policy** | Restricted origin access |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Aman Juluru**

- GitHub: [@AmanJuluru](https://github.com/AmanJuluru)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ for the Automobile Industry

</div>
