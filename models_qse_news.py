import datetime

from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String


Base = declarative_base()



class QSENews(Base):
    __tablename__ = 'parser_pj_qsenews'
    id = Column(Integer, primary_key=True)
    company_title = Column(String(600))
    news_title = Column(Text, nullable=False)
    news_body = Column(Text, nullable=False)
    news_date = Column(DateTime)
    news_download_attachment_url = Column(Text, nullable=False)
    news_url = Column(Text, nullable=False)
    creat = Column(DateTime, default=datetime.datetime.utcnow)
