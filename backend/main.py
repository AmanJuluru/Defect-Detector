from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import shutil
import os
import secrets

import firebase_admin
from firebase_admin import credentials, auth
from database import engine, Base, get_db
import models, schemas, crud, inference
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Defect Detection API")

# Mount static files to serve images
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Firebase Admin
# Explicitly set the project ID environment variable to satisfy auth requirements
os.environ["GOOGLE_CLOUD_PROJECT"] = "car-defect-detector-4c878"

try:
    firebase_admin.get_app()
except ValueError:
    # Uses GOOGLE_APPLICATION_CREDENTIALS environment variable or default credentials
    # Initialize with Project ID to ensure token verification works
    firebase_admin.initialize_app(options={'projectId': 'car-defect-detector-4c878'})

# CORS setup
origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# API Key from frontend config
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Debug logging
        print(f"Received token: {token[:10]}...") 
        
        # Verify via REST API to avoid needing service account file locally
        import requests
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_WEB_API_KEY}",
            json={"idToken": token}
        )
        
        if response.status_code != 200:
            print(f"Token verification failed: {response.text}")
            raise ValueError(f"Invalid token: {response.text}")
            
        auth_data = response.json()
        if 'users' not in auth_data or not auth_data['users']:
            raise ValueError("No user data found in token response")
            
        user_info = auth_data['users'][0]
        email = user_info.get('email')
        uid = user_info.get('localId')
        
        print(f"Token verified for user: {email}")

        if not email:
            print("No email in token")
            raise HTTPException(status_code=400, detail="Email not found in token")

        # Check if user exists in our DB
        user = crud.get_user_by_email(db, email=email)
        if not user:
            print(f"User {email} not found in DB, auto-registering...")
            # Auto-register user from Firebase token data
            username = email.split('@')[0]
            # Handle collision
            if crud.get_user_by_username(db, username):
                 username = f"{username}_{secrets.token_hex(2)}"
            
            user_data = schemas.UserCreate(
                username=username,
                email=email,
                password=None, # No password stored locally
                company_name="Default Company" # You might want to get this from custom claims or let user update it
            )
            user = crud.create_user(db=db, user=user_data)
            print(f"User registered: {user.email}")
            
        return user
    except Exception as e:
        print(f"Auth error: {e}")
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/users/onboard", response_model=schemas.User)
def onboard_user(
    user_update: schemas.UserCreate, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Update user details that were not set during auto-registration
    # Note: user_update.password is ignored as we use Firebase
    
    # Update company if provided
    company = crud.get_company_by_name(db, user_update.company_name)
    if not company:
        company = crud.create_company(db, schemas.CompanyCreate(name=user_update.company_name))
    
    current_user.company_id = company.id
    current_user.role = user_update.role
    # Update username if desired, though we set a default one
    if user_update.username != current_user.username:
         # Check collision
         if not crud.get_user_by_username(db, user_update.username):
             current_user.username = user_update.username

    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/predict", response_model=schemas.Detection)
async def predict_defect(
    file: UploadFile = File(...), 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save file
    file_extension = file.filename.split(".")[-1]
    filename = f"{secrets.token_hex(8)}.{file_extension}"
    file_path = f"static/uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Inference
    if not inference.model:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    defects, result_path = inference.predict_image(file_path)
    
    # Determine Status
    status = "Broken" if defects else "Non-Broken"

    # Save to DB
    detection_data = schemas.DetectionCreate(
        image_path=result_path,
        defects=defects,
        vehicle_status=status
    )
    
    return crud.create_detection(db=db, detection=detection_data, user_id=current_user.id)

@app.post("/live-predict")
async def live_predict(file: UploadFile = File(...)):
    # Save file temporarily - In a deeper optimization we could read from memory
    # but ultralytics wants a path or PIL image. PIL image from memory is best for speed.
    # For now, keeping it simple: save temp, predict, delete.
    
    file_extension = file.filename.split(".")[-1]
    filename = f"temp_{secrets.token_hex(4)}.{file_extension}"
    file_path = f"static/uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        if not inference.model:
            raise HTTPException(status_code=500, detail="Model not loaded")
            
        # Run inference without drawing/saving result image
        detections, _ = inference.predict_image(file_path, save_result=False)
        
        return {"detections": detections}
    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/user/detections", response_model=List[schemas.Detection])
def read_user_detections(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_detections(db, user_id=current_user.id)

@app.get("/company/users", response_model=List[schemas.User])
def read_company_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_company_users(db, company_id=current_user.company_id)

@app.delete("/detections/{detection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detection(
    detection_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    detection = crud.get_detection(db, detection_id=detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
        
    # Check ownership
    if detection.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this detection")
        
    # Delete file from filesystem
    try:
        if os.path.exists(detection.image_path):
            os.remove(detection.image_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
        # Continue to delete DB record even if file deletion fails
        
    # Delete from DB
    crud.delete_detection(db, detection_id=detection_id)
    return None
