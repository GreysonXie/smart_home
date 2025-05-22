from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    house_area = Column(Float)

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))
    location = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.user_id"))

class UsageRecord(Base):
    __tablename__ = "usage_records"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
