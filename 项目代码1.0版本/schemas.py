from pydantic import BaseModel
from datetime import datetime

# 用户模型
class UserCreate(BaseModel):
    name: str
    house_area: float

class UserResponse(UserCreate):
    user_id: int
    class Config:
        from_attributes = True

# 设备模型
class DeviceCreate(BaseModel):
    type: str
    location: str
    user_id: int

class DeviceResponse(DeviceCreate):
    device_id: int
    class Config:
        from_attributes = True
