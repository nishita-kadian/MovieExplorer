import json
import requests
import ast
from movieRecommender import db
from movieRecommender.models import Movie, Genre, Keyword, MovieHasGenre, MovieHasKeyword, Watched
from tqdm import tqdm

# ADD MOVIES TO DB
def addMovie(movieId, title, rating, director, year,  imdbLink, runtime, tagline, language, posterPath, overview, voteCount):
    movieObject = Movie(movieId = movieId, \
                        title = title, \
                        rating = rating, \
                        director = director, \
                        year = year, \
                        revenue = revenue, \
                        imdbLink = imdbLink, \
                        runtime = runtime, \
                        tagline = tagline, \
                        language = language, \
                        posterPath = posterPath, \
                        overview = overview, \
                        voteCount = voteCount)
    ifRowAlready = db.session.query(Movie).filter(Movie.movieId == movieId).count()
    if ifRowAlready == 0:
        db.session.add(movieObject)
        db.session.commit()
        return True
    return False

# ADD GENRE TO DB
def addGenre(genres):
    genresList = list(genres)
    for genre in genresList:
        allGenre.add(genre)
    allGenres = list(allGenre)
    for i, genre in enumerate(allGenres):
        ifRowAlready = db.session.query(Genre).filter(Genre.genreId == i).count()
        genreObject = Genre(genreId=i, genreName=genre)
        if ifRowAlready == 0:
            db.session.add(genreObject)
            db.session.commit()

def addMovieHasKeyword():
    ifMovieRowAlready = db.session.query(Movie).filter(Movie.movieId == movieId).count()
    if ifMovieRowAlready > 0:
        keywordList = list(keywords)
        for keyword in keywordList:
            ifGenreRowAlready = db.session.query(Keyword).filter(Keyword.keywordName == keyword).count()
            if ifGenreRowAlready > 0:
                keywordIdW = db.session.query(Keyword).filter(Keyword.keywordName == keyword).first().keywordId
                if db.session.query(MovieHasKeyword).filter(MovieHasKeyword.keywordId == keywordIdW, MovieHasKeyword.movieHasKeywordId == movieId).count() == 0:
                    movieGenreObject = MovieHasKeyword(movieHasKeywordId=movieId, movieId=movieId, keywordId=keywordIdW)
                    db.session.add(movieGenreObject)
                    db.session.commit()

def addKeyword():
    kwList = list(keywords)
    for keyword in kwList:
        allKw.add(keyword)
    allKws = list(allKw)
    for i, kw in enumerate(allKws):
        ifRowAlready = db.session.query(Keyword).filter(Keyword.keywordId == i).count()
        keywordObject = Keyword(keywordId=i, keywordName=kw)
        if ifRowAlready == 0:
            db.session.add(keywordObject)
            db.session.commit()

def addMovieHasGenre():
    ifMovieRowAlready = db.session.query(Movie).filter(Movie.movieId == movieId).count()
    if ifMovieRowAlready > 0:
        genresList = list(genres)
        for genre in genresList:
            ifGenreRowAlready = db.session.query(Genre).filter(Genre.genreName == genre).count()
            if ifGenreRowAlready > 0:
                genreIdW = db.session.query(Genre).filter(Genre.genreName == genre).first().genreId
                if db.session.query(MovieHasGenre).filter(MovieHasGenre.genreId == genreIdW, MovieHasGenre.movieHasGenreId == movieId).count() == 0:
                    movieGenreObject = MovieHasGenre(movieHasGenreId=movieId, movieId=movieId, genreId=genreIdW)
                    db.session.add(movieGenreObject)
                    db.session.commit()


if __name__ == "__main__":
    with open('linkedData', 'r', encoding='utf-8') as fin:
        data = json.load(fin)
        allGenre = set()
        allKw = set()
        for dataItem in tqdm(data):
            d0Key = list(dataItem.keys())[0]
            try:
                movieId = int(dataItem[d0Key]['movieId'])
                genres = dataItem[d0Key]['genre']
                overview = dataItem[d0Key]['overview']
                posterPath = dataItem[d0Key]['posterPath']
                year = int(dataItem[d0Key]['year'].split("-")[0])
                revenue = int(dataItem[d0Key]['revenue'])
                runtime = float(dataItem[d0Key]['runtime'])
                tagline = dataItem[d0Key]['tagline']
                title = dataItem[d0Key]['title']
                rating = float(dataItem[d0Key]['rating'])
                voteCount = int(dataItem[d0Key]['voteCount'])
                director = dataItem[d0Key]['director']
                keywords = dataItem[d0Key]['keywords']
                imdbLink = dataItem[d0Key]['imdbLink']
                language = dataItem[d0Key]['language']
            except:
                continue
            
            

            # ifMovieRowAlready = db.session.query(Movie).filter(Movie.movieId == movieId).count()
            # if ifMovieRowAlready > 0:
            #     genresList = list(genres)
            #     for genre in genresList:
            #         ifGenreRowAlready = db.session.query(Genre).filter(Genre.genreName == genre).count()
            #         if ifGenreRowAlready > 0:
            #             genreIdW = db.session.query(Genre).filter(Genre.genreName == genre).first().genreId
            #             if db.session.query(MovieHasGenre).filter(MovieHasGenre.genreId == genreIdW, MovieHasGenre.movieHasGenreId == movieId).count() == 0:
            #                 movieGenreObject = MovieHasGenre(movieHasGenreId=movieId, movieId=movieId, genreId=genreIdW)
            #                 db.session.add(movieGenreObject)
            #                 db.session.commit()

            # addMovie(movieId, title, rating, director, year,  imdbLink, runtime, tagline, language, posterPath, overview, voteCount)
        
        #     kwList = list(keywords)
        #     for keyword in kwList:
        #         allKw.add(keyword)
        # allKws = list(allKw)
        # for i, kw in enumerate(allKws):
        #     ifRowAlready = db.session.query(Keyword).filter(Keyword.keywordId == i).count()
        #     keywordObject = Keyword(keywordId=i, keywordName=kw)
        #     if ifRowAlready == 0:
        #         db.session.add(keywordObject)
        #         db.session.commit()

        #     genresList = list(genres)
        #     for genre in genresList:
        #         allGenre.add(genre)
        # allGenres = list(allGenre)
        # for i, genre in enumerate(allGenres):
        #     ifRowAlready = db.session.query(Genre).filter(Genre.genreId == i).count()
        #     genreObject = Genre(genreId=i, genreName=genre)
        #     if ifRowAlready == 0:
        #         db.session.add(genreObject)
        #         db.session.commit()

            
            
            