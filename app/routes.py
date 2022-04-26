from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, distance_mil_miles):
        self.id = id
        self.name = name
        self.description = description
        self.distance_mil_miles = distance_mil_miles

planets = [
    Planet(1, "Mercury", "Smallest planet", 30.691),
    Planet(2, "Venus", "Second planet from the sun", 67.605),
    Planet(3, "Earth", "Home to an infestation of humans", 93.446),
    Planet(4, "Mars", "Red planet", 131.48),
    Planet(5, "Jupiter", "Gas giant", 462.37),
    Planet(6, "Saturn", "More rings than Tom Brady", 918.43),
    Planet(7, "Uranus", "Hold the jokes please", 1183.14),
]


planets_bp = Blueprint("planets", __name__, url_prefix="/planets")


@planets_bp.route("", methods=["GET"])
def handle_planets():
    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance_mil_miles": planet.distance_mil_miles
        })
    return jsonify(planets_response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def individual_planet(planet_id):
    try:
        planet_int = int(planet_id)
    except:
        return jsonify("Please enter a valid ID"), 400
    individual_planet = None
    for planet in planets:
        if planet.id == planet_int:
            individual_planet = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance_mil_miles": planet.distance_mil_miles
            }
            return jsonify(individual_planet), 200
    if individual_planet == None:
        return jsonify("That is not a valid planet"), 404
