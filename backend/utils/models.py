from sqlalchemy import Column, Integer, String, Float
from database import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    extracted_text = Column(String)
    label = Column(String)
    confidence = Column(Float)
    keywords = Column(String)
    explanation = Column(String)
    crime = Column(String)
    law = Column(String)