from app import db
from app.models.planets import Planet
from flask import Blueprint, jsonify, make_response, request, abort

# class Planet:
#     def __init__(self, id, name, description, distance_mil_miles):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.distance_mil_miles = distance_mil_miles

# planets = [
#     Planet(1, "Mercury", "Smallest planet", 30.691),
#     Planet(2, "Venus", "Second planet from the sun", 67.605),
#     Planet(3, "Earth", "Home to an infestation of humans", 93.446),
#     Planet(4, "Mars", "Red planet", 131.48),
#     Planet(5, "Jupiter", "Gas giant", 462.37),
#     Planet(6, "Saturn", "More rings than Tom Brady", 918.43),
#     Planet(7, "Uranus", "Hold the jokes please", 1183.14),
# ]

def validate_planet(planet_id):
    try:
        planet_int = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(make_response({"message":f"planet {planet_id} not found"}, 404))
    return planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")
@planets_bp.route("", methods=["POST"])
def handle_planets_post():
    request_body = request.get_json()
    new_planet = Planet(planet_name=request_body["planet_name"],
        description=request_body["description"],
        distance_mil_miles=request_body["distance_mil_miles"])

    db.session.add(new_planet)
    db.session.commit()
    return make_response(f"Planet {new_planet.planet_name} successfully created", 201)

@planets_bp.route("", methods=["GET"])
def handle_planets():
    params = request.args
    if "distance_mil_miles" in params and "planet_name" in params:
        distance_mil_miles_value = params["distance_mil_miles"]
        planet_name_value = params["planet_name"]
        planets = Planet.query.filter_by(planet_name=planet_name_value, distance_mil_miles=distance_mil_miles_value)
    elif "distance_mil_miles" in params:
        distance_mil_miles_value = params["distance_mil_miles"]
        planets = Planet.query.filter_by(distance_mil_miles=distance_mil_miles_value)
    elif "planet_name" in params:
        planet_name_value = params["planet_name"]
        planets = Planet.query.filter_by(planet_name=planet_name_value)
    else:
        planets = Planet.query.all()
        
    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "planet_name": planet.planet_name,
            "description": planet.description,
            "distance_mil_miles": planet.distance_mil_miles
        })
    return jsonify(planets_response)
    #something something use abort to refactor? get planet or abort from lesson

@planets_bp.route("/<planet_id>", methods=["GET"])
def individual_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return {
            "id": planet.id,
            "planet_name": planet.planet_name,
            "description": planet.description,
            "distance_mil_miles": planet.distance_mil_miles
        }


#can add 'PATCH' after 'PUT'? 
@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()

    planet.planet_name=request_body["planet_name"]
    planet.description=request_body["description"]
    planet.distance_mil_miles=request_body["distance_mil_miles"]

    db.session.commit()
    return make_response(f"Planet #{planet.id} successfully updated")



@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully deleted")
