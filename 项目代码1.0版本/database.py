from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # 加载环境变量

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:213108@localhost:5432/smart_home")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
