
#import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create instance of Flask app
app = Flask(__name__)

#Use PyMongo to establish Mongo connection
mongo = PyMongo(app,uri='mongodb://localhost:27017/mars_app')

#create route that renders index.html as template
@app.route('/')
def home():
    
    #find one record of data from the mongo database
    red_data = mongo.db.collection.find_one()


    #return template and data
    return render_template('index.html', marsfun = red_data)

#route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape_info()

    #update the mongo database using update and upsert = True
    mongo.db.collection.update({}, mars_data, upsert=True)

    #redirect back to home page
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

