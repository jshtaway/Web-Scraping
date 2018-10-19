import pandas as pd
import datetime as dt
import scrape_mars
import pymongo
from bson.json_util import loads


from flask import (
    Flask,
    render_template,
    jsonify,
    redirect)

conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.space_db

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route('/')
#merged scrape and home
def home():
    mars_data = db.mars.find().sort("_id", -1).limit(1)[0]
    # mars_data = db.collection.find().limit(1).sort({$natural:-1})
    with open('templates/table.html','w+') as f:
        f.write(mars_data['mars_facts'])
    # print(mars_data['mars_facts'])
    return render_template('index2.html', mars=mars_data)
    # except: 
    #     print('scraping data')
    #     return redirect("http://localhost:5000/scrape", code=302)

@app.route('/scrape')
def scrape():
    scrapedata = scrape_mars.scrape()
    data = {
        "news": scrapedata["news"],
        "space_images": scrapedata["space_images"],
        "featured_image_url": scrapedata["mars_weather"],
        "mars_facts": scrapedata["mars_facts"],
        "mars_hemispheres": scrapedata["mars_hemispheres"],
    }
    print('space_images: ',data['space_images'])
    collection = db.mars
    # Insert data into database
    collection.update(
        data,
        data,
        upsert=True)
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
