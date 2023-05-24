from flask import Flask, jsonify, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from random import choice

load_dotenv()


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


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
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def random():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    print(cafes)
    random_cafe = choice(cafes)
    return jsonify(
        cafe = random_cafe.to_dict()
    )
    # return render_template('index.html')

@app.route('/all')
def all():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(
        cafes = [cafe.to_dict() for cafe in cafes]
    )

@app.route('/search')
def search():
    query_location = request.args.get('loc')
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)).scalars().all()
    if cafes:
        return jsonify(
            cafes = [cafe.to_dict() for cafe in cafes]
        )
    else:
        return jsonify(
            error={"Not Found": "Sorry, we don't have a cafe at that location."}
        ), 404



# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True, port=9000)
