
#import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

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
    mars_data = scrape_mars2.scrape_all()
    print(f'mars_data={mars_data}')
    print()
    mars = mongo.db.mars

    #update the mongo database using update and upsert = True
    #mongo.db.collection.update_one({}, mars_data, upsert=True)
    mars.update_many({},{"$set": mars_data}, upsert=True)

    #redirect back to home page
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)

