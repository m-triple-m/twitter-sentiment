from main import db
db.create_all()

class User(db.Model):
   __tablename__ = 'user'

   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(250), nullable=False)
   email = db.Column(db.String(250),unique=True, nullable=False)
   twitterid = db.Column(db.String(250))
   password = db.Column(db.String(250),nullable=False)


class Tweet(db.Model):
   __tablename__ = 'tweets'

   id = db.Column(db.Integer, primary_key=True)
   handle = db.Column(db.String(20), nullable=False)
   name = db.Column(db.String(50), nullable = False)
   tweet = db.Column(db.String(50), nullable = False)
   tweet_date = db.Column(db.Date, nullable = False)
   analyse_date = db.Column(db.Date, nullable = False)

class SentimentReport(db.Model):
   __tablename__ = 'sentiment_report'

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20), nullable=False)
   date = db.Column(db.Date, nullable = False)
   subjectivity = db.Column(db.Integer, nullable = False)
   positivity = db.Column(db.Integer, nullable = False)
   negativity = db.Column(db.Integer, nullable = False)
   neutral = db.Column(db.Integer, nullable = False)