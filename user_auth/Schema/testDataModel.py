from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Movies(db.Model):
	movieId = db.Column(db.Integer, primary_key = True)
	rating =  db.Column(db.Integer,nullable = False)
	title = db.Column(db.String(500), nullable = False)
	director = db.Column(db.String(50), nullable = False)

	def __repr__(self):
		return f"Movies('{self.movieId}', '{self.rating}', '{self.title}', '{self.director}')"

class Genre(db.Model):
	genreId = db.Column(db.Integer, primary_key = True)
	genreName = db.Column(db.String(50),nullable = False)

	def __repr__(self):
		return f"Genre('{self.genreId}', '{self.genreName}')"

class MovieHasGenre(db.Model):
	movieHasGenreId = db.Column(db.Integer, primary_key = True)
	genreId = db.Column(db.Integer, db.ForeignKey('genre.genreId'), primary_key = True)
	movieId = db.Column(db.Integer, db.ForeignKey('movies.movieId'), primary_key = True)

	def __repr__(self):
		return f"MovieHasGenre('{self.movieHasGenreId}', '{self.movieId}', '{self.genreId}')"