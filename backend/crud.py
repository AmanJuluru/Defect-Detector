from sqlalchemy.orm import Session
import models, schemas

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Check if company exists, else create
    company = get_company_by_name(db, user.company_name)
    if not company:
        company = create_company(db, schemas.CompanyCreate(name=user.company_name))
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=None, 
        role=user.role,
        company_id=company.id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_detection(db: Session, detection: schemas.DetectionCreate, user_id: int):
    db_detection = models.Detection(
        user_id=user_id,
        image_path=detection.image_path,
        defects=detection.defects,
        vehicle_status=detection.vehicle_status
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection

def get_user_detections(db: Session, user_id: int):
    return db.query(models.Detection).filter(models.Detection.user_id == user_id).all()

def get_company_users(db: Session, company_id: int):
    return db.query(models.User).filter(models.User.company_id == company_id).all()

def get_detection(db: Session, detection_id: int):
    return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

def delete_detection(db: Session, detection_id: int):
    db_detection = db.query(models.Detection).filter(models.Detection.id == detection_id).first()
    if db_detection:
        db.delete(db_detection)
        db.commit()
        return True
    return False
