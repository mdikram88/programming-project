from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_DATABASE_API_KEY = "8520a0181e6d92385eb73f4d0bb87a4c"
MOVIE_DATABASE_BASE_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "api_key": MOVIE_DATABASE_API_KEY
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()
Bootstrap(app)


class Movie(db.Model):
    __tablename__ = "Movie"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(255))
    img_url = db.Column(db.String(255), nullable=False)

    def __init__(self, title, year, description, img_url, rating=0, ranking=0, review=None):
        self.title = title
        self.year = year
        self.description = description
        self.rating = rating
        self.ranking = ranking
        self.review = review
        self.img_url = img_url

# db.create_all()


# --------------------------Creating WTF Forms------------------------
class EditRating(FlaskForm):
    new_rating = StringField("Your Rating out of 10 eg: 7.3", validators=[DataRequired()],
                             render_kw={"placeholder": "Rating"})
    new_review = StringField("Your Review", validators=[DataRequired()],
                             render_kw={"placeholder": "Review"})
    submit = SubmitField("Update")


class AddMovie(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")



@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating).all()
    # print(movies)
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    db.session.commit()

    return render_template("index.html", movies=movies[::-1])


@app.route("/edit/<title>", methods=["GET", "POST"])
def edit_info(title):
    record = Movie.query.filter_by(title=title).first()
    form = EditRating()
    if form.validate_on_submit():
        record.rating = float(form.new_rating.data)
        record.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=record)


@app.route("/delete/<title>")
def delete_movie(title):
    record = Movie.query.filter_by(title=title).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovie()
    if form.validate_on_submit():
        movie_title = form.title.data
        params = {
            "api_key": MOVIE_DATABASE_API_KEY,
            "query": movie_title
        }
        response = requests.get(url=MOVIE_DATABASE_BASE_URL, params=params).json()["results"]
        return render_template('select.html', movies=response)
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    title = request.args.get("title")
    year = request.args.get("date").split("-")[0]
    path = request.args.get("path")
    description = request.args.get("description")
    try:
        new_movie = Movie(
            title=title,
            year=int(year),
            img_url=f"{MOVIE_DB_IMAGE_URL}{path}",
            description=description)
        db.session.add(new_movie)
        db.session.commit()
    except:
        print("Error")
        return redirect(url_for('home'))
    return redirect(url_for('edit_info', title=new_movie.title))


if __name__ == '__main__':
    app.run(debug=True)
