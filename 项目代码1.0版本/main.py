from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,registry
from sqlalchemy import text
from database import SessionLocal, engine
from models import User, Device, UsageRecord, Base
from schemas import UserCreate, UserResponse, DeviceCreate, DeviceResponse
import matplotlib
matplotlib.use('Agg')  # 设置非交互式后端
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
import uvicorn
# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title='smart home',description='your furniture assistant')

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- 用户接口 ----------------------
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# ---------------------- 设备接口 ----------------------
@app.post("/devices/", response_model=DeviceResponse)
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    try:
        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices/", response_model=list[DeviceResponse])
def get_all_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices

# ---------------------- 数据分析接口 ----------------------
@app.get("/api/device_usage")
def analyze_device_usage(db: Session = Depends(get_db)):
    try:
        # 查询每小时使用次数
        result = db.execute(text("""
            SELECT DATE_TRUNC('hour', start_time) AS hour, COUNT(*) AS usage_count
            FROM usage_records
            GROUP BY DATE_TRUNC('hour', start_time)
            ORDER BY hour
        """))
        data = result.fetchall()

        if not data:
            return {"message": "No data available"}

        # 生成图表
        hours = [row[0].strftime("%H:%M") for row in data]
        counts = [row[1] for row in data]
        plt.figure(figsize=(10, 6))
        plt.bar(hours, counts)
        plt.title("Device Usage by Hour")
        plt.xlabel("Hour of Day")
        plt.ylabel("Usage Count")
        plt.savefig("usage_by_hour.png")
        return FileResponse("usage_by_hour.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 根路径
@app.get("/")
def read_root():
    return {"message": "Welcome to Your Smart Home API! Visit /docs for Swagger UI."}
