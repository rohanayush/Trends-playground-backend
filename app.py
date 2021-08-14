from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import datacompy
from pytrends.request import TrendReq

app = Flask(__name__)
api = Api(app)
CORS(app)
conn=''
@app.route("/")
def hello():
    pytrends = TrendReq(hl='en-US', tz=360)
   
    global conn 
    conn= pytrends
   

    return "connected to google"

@app.route('/suggest', methods=['POST'])
def suggestions():
    a=request.data
    print(a)
    pie= TrendReq(hl='en-US', tz=360)
    keyword=a
    print("\n Recommendation for :",keyword,"\n")
    df = pie.suggestions(keyword)
    return jsonify(df)

@app.route('/data', methods=['POST'])
def getData():
    pytrends = TrendReq(hl='en-US', tz=360)
    b=request.data
    b=b.decode('utf-8')
    print("got from frontend",b)
    # print("array formed",a)
    kw_list = []
    kw_list.append(str(b))
    print("\n\n Kwlist|n\n",kw_list,"\n\n")
    # Can be images, news, youtube or froogle (for Google Shopping results) gprop
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    # df=pytrends.get_historical_interest(kw_list, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
    # df=pytrends.interest_over_time()
    print(df.head(10))
    df1=df.to_json()
    return jsonify(df1)

@app.route('/trending', methods=['POST'])
def trending():
    tr=request.data
    tr=tr.decode('utf-8')

    print("string of tr\n",tr)
    pytrends = TrendReq(hl='en-US', tz=360)
    df=pytrends.trending_searches(pn=tr)
    df1=df.to_json()
    return jsonify(df1)

@app.route('/news', methods=['POST'])
def get_news():

    import requests

    url = "https://google-search3.p.rapidapi.com/api/v1/news/q="
    q=request.data
    q=q.decode('utf-8')
    url=url+str(q)
    headers = {
    'x-rapidapi-key': "b64d452b40mshc4e0459148c0016p11b5eajsn727b13eeebd2",
    'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    # Make the request
    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    # print(response_json)
    return jsonify(response_json)

if __name__ == '__main__':
   app.run(port=5000)
   
   




