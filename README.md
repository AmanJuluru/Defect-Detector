# Automobile Defect Detection System

An advanced AI-powered application designed to detect and analyze defects on automobile exteriors automatically. This system leverages computer vision to identify issues like dents, scratches, and other damages, providing a streamlined solution for vehicle inspection.

## Features

- **Real-Time Defect Detection**: Instantly analyzes live camera feeds or uploaded images to detect defects.
- **Interactive Dashboard**: View detection history, statistics, and manage records.
- **User Authentication**: Secure login and registration powered by Firebase.
- **Cross-Platform**: Accessible via web browsers on desktop and mobile.
- **Visual Feedback**: Bounding boxes and confidence scores for identified defects.

## Tech Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI Model**: YOLO (Ultralytics) for object detection
- **Database & Auth**: Firebase

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/project-name.git
   cd project-name
   ```

2. **Backend Setup**
   Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   # source .venv/bin/activate
   pip install -r requirements.txt
   ```
   Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   Navigate to the frontend directory and install dependencies:
   ```bash
   cd ../frontend
   npm install
   ```
   Start the frontend development server:
   ```bash
   npm run dev
   ```

4. **Access the Application**
   Open [http://localhost:3000](http://localhost:3000) with your browser.

## Project Structure

- `/backend`: FastAPI server and YOLO implementation
- `/frontend`: Next.js web application
- `/model`: Trained YOLO weights

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
