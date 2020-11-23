# import flask, to render a template
from flask import Flask, render_template
# import pymongo to interact with mongoDB
from flask_pymongo import PyMongo
# import scraping to convert from jupyter notebook to python
import scraping

# setup Flask:
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# setup app routes
@app.route("/")
# define the route for the HTML page
def index():
    #find mars collection in mongodb
    mars = mongo.db.mars.find_one()
    #return html template using index.html file
    #tells python to use mars collection in mongodb
    return render_template("index.html", mars=mars)

# set up scraping route: will be the "button" of the web application
@app.route("/scrape")
# function to access the database,
# scrape new data using our scraping.py script,
# update the database, and return a message when successful.
def scrape():
    #assign variable that points to mongodb
    mars = mongo.db.mars
    #scrape new data using our scraping.py script
    mars_data = scraping.scrape_all()
    #update database
    mars.update({}, mars_data, upsert=True)
    #screen_output = mars_data["facts"]
    #return str(screen_output)
    return "Scraping Successful!"


# run the flask
if __name__ == "__main__":
    app.run(debug=True)
