from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Company Schemas
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    role: str = "user"

class UserCreate(UserBase):
    password: Optional[str] = None

    company_name: str # Helper to create/link company

class User(UserBase):
    id: int
    company_id: int
    class Config:
        from_attributes = True

# Detection Schemas
class DetectionBase(BaseModel):
    image_path: str
    defects: List[dict]
    vehicle_status: str

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
