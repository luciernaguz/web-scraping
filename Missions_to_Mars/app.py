# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# Instance Flask app
app = Flask(__name__)

# Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)


# Route render to index.html
@app.route("/")
def index(): 
    # All the info stores
    mars_info = mongo.db.mars_info.find_one()

    # Return index and info
    return render_template("index.html", mars_info=mars_info)

# Route scrape function
@app.route("/scrape")
def scrape(): 
    # Mars Data & Info
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
