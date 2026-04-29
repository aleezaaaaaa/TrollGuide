from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    extracted_text = Column(Text)
    label = Column(String)
    confidence = Column(Float)
    keywords = Column(Text)
    explanation = Column(Text)
    crime = Column(String)
    law = Column(String)