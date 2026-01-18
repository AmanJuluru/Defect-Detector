from flask import Flask, render_template, request, redirect, url_for, session
from ultralytics import YOLO
import os
import cv2

app = Flask(__name__)
app.secret_key = "rtrp_secret_key"

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
MODEL_PATH = "model/defect_model.pt"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)

COLORS = {
    "dent": (203, 192, 255),
    "scratch": (255, 0, 0),
    "lamp_broken": (0, 255, 255),
    "glass_broken": (128, 0, 128),
    "tire_flat": (0, 0, 255)
}

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    result_image = None
    detections = []
    vehicle_status = "Non-Broken"

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            result_path = os.path.join(RESULT_FOLDER, file.filename)
            file.save(image_path)

            results = model(image_path, conf=0.05)[0]
            img = cv2.imread(image_path)

            if len(results.boxes) > 0:
                vehicle_status = "Broken"

            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = COLORS.get(class_name, (0, 255, 0))

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                label = f"{class_name} | {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                detections.append(f"{class_name} ({conf:.2f})")

            cv2.imwrite(result_path, img)
            result_image = result_path

    return render_template(
        "dashboard.html",
        result_image=result_image,
        detections=detections,
        vehicle_status=vehicle_status,
        user=session["user"]
    )

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
