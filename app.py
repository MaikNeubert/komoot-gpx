from flask import Flask, request, render_template, url_for
from Komoot import Komoot

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/route", methods=["GET"])
def get_route():

    route_url = request.args.get("route")
    if route_url == None:
        return render_template('route-error.html')
    
    kahoot = Komoot()
    route = kahoot.get_route(route_url)
    gpx = kahoot.route_to_gpx(route)

    return render_template('route.html', gpx=gpx)


with app.test_request_context():
    url_for('static', filename='milligram.min.css')
    url_for('static', filename='normalize.css')
    url_for('static', filename='custom.css')
