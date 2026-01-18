from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    users = relationship("User", back_populates="company")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)

    role = Column(String, default="user") # 'admin' or 'user'
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    company = relationship("Company", back_populates="users")
    detections = relationship("Detection", back_populates="user")

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)
    defects = Column(JSON) # Stores list of {class, conf, bbox}
    vehicle_status = Column(String) # Broken / Non-Broken
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="detections")
