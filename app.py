from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
app=Flask(__name__)
mongo=PyMongo(app,uri="mongodb://localhost:27017/weather_app")

mongo.db.collection.drop()
@app.route("/")
def home():
    mars_info=mongo.db.collection.find_one()
    if not mars_info:
        mars_info = {'hemisphere_image_urls':['','','','']}
    return render_template("index.html", mars = mars_info)

@app.route("/scrape")
def scrape():
    
    mars_data=scrape_mars.scrape()
    mongo.db.collection.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)