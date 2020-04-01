from flask import Flask
from flask import render_template,redirect,request, send_from_directory, send_file, session as fl_session
from flask import session,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Tweet, SentimentReport
import database_setup
from twitter_api import getTweets
from textblob import TextBlob
from datetime import date
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key="somesupersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polite.db'
db = SQLAlchemy(app)

import sql_alchemy_setup as Database
#Connect to Database and create database session
# engine = create_engine('sqlite:///polite.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

@app.route('/')
@app.route('/home')
def home():
    if not session.get('user'):
        return redirect('/login')
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template('register.html')


@app.route('/process_data', methods=['POST'])
def process_data():
    username = request.form.get('username')
    email = request.form.get('email')
    twitterId = request.form.get('twitterId')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    print(email,twitterId,username,password,cpassword)
    if username and email and twitterId and password and cpassword and (password == cpassword):
        user = Database.User(username=username,email=email,twitterid=twitterId,password=password)
        db.session.add(user)
        db.session.commit()
        result = {'status':'successfully registered'}
        return jsonify(result)
    else:
        result = {'status':'failed to registered, contact admin.'}
        return jsonify(result)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = request.form
        if form.get('email'):
            user = Database.User.query.filter_by(email=form.get('email')).first()
            print(user.email, user.password, form)
            if form.get('password') == user.password:
                fl_session['user'] = user.email
                return redirect('/')
    return render_template("login.html")

@app.route("/showtweets", methods=['GET'])
def show():
    if not session.get('user'):
        return redirect('/login')
    return render_template("showtweets.html")

@app.route("/fetchtweets")
def fetch_tweets():
    
    handle = request.args.get("key")
    print(handle)
    tweets = getTweets(handle)
    tweet_text = clean_tweets(tweets)

    addTweets(handle, tweets)

    fl_session['tweets'] = tweet_text
    fl_session['name'] = tweets[0].user.name
    # print(tweet_text)
    
    return jsonify({'data' : tweet_text, 'name' : handle})

@app.route('/getpoldata')
def getPolData():
    if not session.get('user'):
        return redirect('/login')
    return jsonify([fl_session.get('poldata'), fl_session.get('subdata')])

@app.route('/viztweets')
def viz():
    if not session.get('user'):
        return redirect('/login')
    return render_template('visualise.html')

def analyse_sentiment(tweets):
    sentiments = []
    polarity_data = {'positive' : 0, 'negative': 0, 'neutral': 0 }
    subjectivity = []
    for tweet in tweets:
        tb = TextBlob(tweet)
        
        sent = tb.sentiment
        if sent.polarity>0:
            polarity_data['positive']+=1
        elif sent.polarity<0:
            polarity_data['negative']+=1
        elif sent.polarity==0:
            polarity_data['neutral']+=1
        
        subjectivity.append(sent.subjectivity)
        sentiments.append(tb.sentiment)
    fl_session['poldata'] = polarity_data
    fl_session['subdata'] = subjectivity
    generateSentimentReport(subjectivity, polarity_data)
    return sentiments

def generateSentimentReport(subjectivity, polarity):
    avg_subjectivity = sum(subjectivity)/len(subjectivity)
    total = polarity['positive'] + polarity['negative'] + polarity['neutral'] 
    positive = polarity['positive']*100/total
    negative = polarity['negative']*100/total
    neutral = polarity['neutral']*100/total
    tweet_obj = Database.SentimentReport(name = fl_session.get('name'), date = date.today(), subjectivity = avg_subjectivity, 
                positivity = positive, negativity = negative, neutral = neutral)

    db.session.add(tweet_obj)
    db.session.commit()


def clean_tweets(tweets):
    cleaned = []
    for tweet in tweets:
        txt = tweet._json.get('text')
        if txt.startswith("RT"):
                index = txt.find(':')
                txt = txt[index+1:]
        cleaned.append(txt)
    return cleaned

@app.route('/showdb')
def showTweetsinDB():
    if not session.get('user'):
        return redirect('/login')
    return render_template('showdb.html', data = Tweet.query.all())

def addTweets(handle, tweet_details):
    for tweet in tweet_details:
        # print(tweet)
        tweet_date = format_date(tweet._json['created_at'])
        name = tweet._json['user']['name']

        tweet_obj = Database.Tweet(name = name, handle = handle, tweet = tweet._json.get('text'), 
                    tweet_date = tweet_date, analyse_date = date.today())
        db.session.add(tweet_obj)
        db.session.commit()


def format_date(tweet_date):
    months = {'jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9 , 'Oct': 10, 'Nov': 11, 'Dec': 12}

    mon, day, year = tweet_date.split()[1], tweet_date.split()[2], tweet_date.split()[-1]
    return date(int(year), months[mon], int(day))

@app.route('/result')
def result():
    if not session.get('user'):
        return redirect('/login')
    tweets = fl_session.get('tweets')
    sentiments = analyse_sentiment(tweets)
    print(sentiments)
    return render_template('result.html', data = zip(sentiments, tweets))

@app.route('/wordcloud')
def generateWordCloud():
    if not session.get('user'):
        return redirect('/login')
    tweets = ' '.join(fl_session.get('tweets'))
    wordcloud = WordCloud(width=600, height=600).generate(tweets)
    wordcloud.to_file(os.path.join('static/wordcloud', 'cloud.png'))
    return render_template('wordcloud.html')

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if not session.get('user'):
        return redirect('/login')
    return send_file(filename_or_fp=f'static/wordcloud/{filename}')

@app.route('/reportdash')
def reportDashboard():
    if not session.get('user'):
        return redirect('/login')
    return render_template('reportdash.html')

@app.route('/showreport')
def tweetreport():
    if not session.get('user'):
        return redirect('/login')
    data = Database.Tweet.query.all()
    return render_template('tweetreport.html', data = data)

@app.route('/showanareport')
def tweetAnalysisReport():
    if not session.get('user'):
        return redirect('/login')
    data = Database.SentimentReport.query.all()
    return render_template('sentimentreport.html', data = data)

if __name__ == '__main__':
    app.run(debug=True) #change to 'False' while submitting
