from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

API_KEY = "TopSecretAPIKey"
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route("/random")
def random_fn():
    cafes = list(Cafe.query.all())
    cafe = choice(cafes)
    # Method of Serialising in JSON
    # return jsonify(id=cafe.id,
    #                name=cafe.name,
    #                map_url=cafe.map_url,
    #                img_url=cafe.img_url,
    #                location=cafe.location,
    #                seats=cafe.seats,
    #                has_toilet=cafe.has_toilet,
    #                has_wifi=cafe.has_wifi,
    #                has_sockets=cafe.has_sockets,
    #                can_take_calls=cafe.can_take_calls,
    #                coffee_price=cafe.coffee_price
    #                )
    # Alternate short method for serialising in JSON
    return jsonify(cafe.to_dict())


@app.route("/all")
def all_cafes():
    cafes = Cafe.query.all()
    cafe_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafe_list
                   )


@app.route("/search")
def search():
    location = request.args.get("location")
    cafes = Cafe.query.filter_by(location=location).all()
    if cafes != []:
        selected_cafes = [cafe.to_dict() for cafe in cafes]
        return jsonify(selected_cafes)
    else:
        return jsonify(error={"Not Found": "Sorry, We don't have a cafe at that location"})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
                    name=request.form.get("name"),
                    map_url=request.form.get("map_url"),
                    img_url=request.form.get("img_url"),
                    location=request.form.get("loc"),
                    has_sockets=bool(request.form.get("sockets")),
                    has_toilet=bool(request.form.get("toilet")),
                    has_wifi=bool(request.form.get("wifi")),
                    can_take_calls=bool(request.form.get("calls")),
                    seats=request.form.get("seats"),
                    coffee_price=request.form.get("coffee_price"),
                    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(success="Successfully added the new cafe")


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe is not None:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(success="Coffee price updated Successfully"), 200
    else:
        return jsonify(error="Sorry, Cafe Id doesn't exist"), 404


# HTTP DELETE - Delete Record
@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    key = request.args.get("api_key")
    if cafe:
        if key == API_KEY:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success="Cafe record deleted Successfully"), 200
        else:
            return jsonify(error="Invalid Api Key"), 400
    else:
        return jsonify(error={"NotFound": "Cafe Id doesn't exists"}), 404


if __name__ == '__main__':
    app.run(debug=True)
