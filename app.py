from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mryvrlnjhojjlc:eb93d9a9d6f41a1688c9913b24ca4571ba4a2b76b20e7f9359da25581a9452fc@ec2-3-216-129-140.compute-1.amazonaws.com:5432/d7t9dt29mkm053"


db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    character_class = db.Column(db.String(), nullable=False)
    hitpoints = db.Column(db.Integer, nullable=False)

    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.hitpoints = 100

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "character_class", "hitpoints")

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)       

@app.route("/character/add", methods=["POST"])
def add_character():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    name = post_data.get("name")
    character_class = post_data.get("character_class")   

    record =  Character(name, character_class)
    db.session.add(record)
    db.session.commit()

    return jsonify("character Created")

@app.route("/character/get", methods=["GET"])
def get_all_characters():
    all_characters = db.session.query(Character).all()
    return jsonify(characters_schema.dump(all_characters)) 

@app.route("/character/get/<id>", methods=["GET"])   
def get_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()   
    return jsonify(character_schema.dump(character))

@app.route("/character/delete/<id>", methods=["DELETE"])  
def delete_character_by_id(id):
    character = db.session.query(Character).filter(Character.id == id).first()
    db.session.delete(character)
    db.session.commit()
    return jsonify("Character Deleted")


@app.route("character/update/<id>", methods=["put"])
def update_character_by_id(id):
    if content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    put_data = request.get_json()
    name = put_data.get("name")
    character_class = put_data.get("character_class")
    hitpoints = put_data.get("hitpoints") 

    character = db.session.query(Character).filter(Character.id == id).first()
    if name is not None:
        character.name = name 
    if character_class is not None:    
        character.character_class = character_class
    if hitpoints is not None:    
        character.hitpoints = hitpoints

    return jsonify("Character Updated")    





if __name__ == "__main__":
    app.run(debug=True)