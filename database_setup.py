import sys

#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, types

#for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

#for configuration
from sqlalchemy import create_engine

#create declarative_base instance
Base = declarative_base()


#classes
class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   username = Column(String(250), nullable=False)
   email = Column(String(250),unique=True, nullable=False)
   twitterid = Column(String(250))
   password = Column(String(250),nullable=False)


class Tweet(Base):
   __tablename__ = 'tweets'

   id = Column(Integer, primary_key=True)
   handle = Column(String(20), nullable=False)
   name = Column(String(50), nullable = False)
   tweet = Column(String(50), nullable = False)
   tweet_date = Column(types.Date, nullable = False)
   analyse_date = Column(types.Date, nullable = False)

class SentimentReport(Base):
   __tablename__ = 'sentiment_report'

   id = Column(Integer, primary_key=True)
   name = Column(String(20), nullable=False)
   date = Column(types.Date, nullable = False)
   subjectivity = Column(Integer, nullable = False)
   positivity = Column(Integer, nullable = False)
   negativity = Column(Integer, nullable = False)
   neutral = Column(Integer, nullable = False)

#creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///polite.db')

Base.metadata.create_all(engine)
