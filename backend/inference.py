from ultralytics import YOLO
import cv2
import os

# Adjust path if needed.
# Since we are running from root or backend, let's be absolute or relative to project root
# The file is at c:/Users/zeusm/Downloads/project/model/defect_model.pt
MODEL_PATH = "../model/defect_model.pt" 

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Error loading model from {MODEL_PATH}: {e}")
    model = None

COLORS = {
    "dent": (203, 192, 255),
    "scratch": (255, 0, 0),
    "lamp_broken": (0, 255, 255),
    "glass_broken": (128, 0, 128),
    "tire_flat": (0, 0, 255)
}

def predict_image(image_path: str, save_result: bool = True):
    if not model:
        return [], "Model not loaded"
    
    results = model(image_path, conf=0.25)[0]
    
    detections = []
    
    # Pre-calculate detections even if we don't draw, 
    # but we need image dimensions for relative coordinates if we wanted that.
    # For now, we continue to read the image to draw on it if save_result is True, 
    # OR we need it to return result_path.
    
    # If we are live streaming, we might just want to return coordinates.
    # However, existing code relies on drawing.
    
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = model.names[cls_id]
        
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        bbox = [x1, y1, x2, y2]
        
        if save_result:
            # Draw on image
            color = COLORS.get(class_name, (0, 255, 0))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            label = f"{class_name} | {conf:.2f}"
            cv2.putText(img, label, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        detections.append({
            "class": class_name,
            "confidence": conf,
            "bbox": bbox,
            "normalized_bbox": [x1/width, y1/height, x2/width, y2/height] # useful for frontend scaling
        })
        
    result_path = image_path
    if save_result:
        # Save the annotated image
        # We will overwrite the original for now or save as new
        cv2.imwrite(result_path, img)
    
    return detections, result_path
