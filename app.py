from flask import Flask, request, render_template, url_for
from Komoot import Komoot, Forbidden, ServerError

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/route", methods=["GET"])
def get_route():

    route_url = request.args.get("route")
    if route_url == None:
        return render_template('route-error.html')
    
    komoot = Komoot()

    try:
        route = komoot.get_route(route_url)
    except Forbidden as err:
        return render_template('route-error.html', err="Zugriff auf die Route verweigert. Ist die Route privat klicke in der Route auf Teilen und kopiere den Link von dort")
    except ServerError as err:
        return render_template('route-error.html', err=err)
    except Exception as err:
        return render_template('route-error.html', err=err)

    if route == None:
        return render_template('route-error.html', err="Keine Route im Link gefunden")
    


    gpx = komoot.route_to_gpx(route)

    return render_template('route.html', gpx=gpx, name=route.name, creator=route.creator)


with app.test_request_context():
    url_for('static', filename='milligram.min.css')
    url_for('static', filename='normalize.css')
    url_for('static', filename='custom.css')
    url_for('static', filename='pin-icon-end.png')
    url_for('static', filename='pin-icon-start.png')
    url_for('static', filename='pin-icon-wptc.png')
    url_for('static', filename='pin-shadow.png')

