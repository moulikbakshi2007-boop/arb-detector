#database

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()



class Opportunity(Base):

    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    sport = Column(String, nullable=False)
    
    profit_margin = Column(Float, nullable=False)
    arb_sum = Column(Float, nullable=False)
   
    stakes = Column(JSON)
    investment = Column(Float)
    guaranteed_return = Column(Float)
   
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
       
        return {
            "id": self.id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "sport": self.sport,
            "profit_margin": self.profit_margin,
            "arb_sum": self.arb_sum,
            "stakes": self.stakes,
            "investment": self.investment,
            "guaranteed_return": self.guaranteed_return,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None
        }


def create_tables():
   
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def get_db():
 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()