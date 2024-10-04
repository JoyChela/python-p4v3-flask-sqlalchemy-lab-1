# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    # earthquake = Earthquake.query.filter_by(id=id).first()
    earthquake = Earthquake.query.filter_by(id=id).first()

    if not earthquake:
        return make_response(
            jsonify({'message': f"Earthquake {id} not found."}),
            404
        )
    return make_response(
        jsonify(earthquake.to_dict()),
        200
    )
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitude >= the specified value
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Prepare the response data
    quake_data = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        } for quake in quakes
    ]

    response = {
        "count": len(quakes),
        "quakes": quake_data
    }
    
    # Print the response for debugging
    print("Response:", response)
    
    # Return JSON response
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
