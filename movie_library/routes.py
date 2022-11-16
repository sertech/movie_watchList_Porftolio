import uuid
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    url_for,
    abort,
)
from movie_library.forms import MovieForm  #! flask-wtf usage
from movie_library.models import Movie  #! @dataclass usage
from dataclasses import asdict  #! to pass a dataclass class as dictionary to mongo

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    movie_data = current_app.db.movie.find({})  # ({}) means get all the data
    # with list comprehension we will create a object of type movie for each the of elements in movie_data
    movies = [Movie(**movie) for movie in movie_data]
    return render_template("index.html", title="Movies Watchlist", movies_data=movies)


@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    # 1) create a movieForm object
    form = MovieForm()

    if form.validate_on_submit():  # this also runs the form validation
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )

        # * current_app is the current app that is dealing with the request
        current_app.db.movie.insert_one(asdict(movie))

        return redirect(
            url_for(".index")
        )  # . (dot) means the index root of the current blueprint other blueprints may have their own index's

    return render_template(
        "new_movie.html", title="Movies Watchlist - Add Movie", form=form
    )


@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie_data = current_app.db.movie.find_one({"_id": _id})
    if not movie_data:
        abort(404)
    movie = Movie(**movie_data)
    return render_template("movie_details.html", movie=movie)


# for this there are two solutions
# 1) @pages.get("/movie/<string:_id>/rate/<int:rating>") /movie/bless2540/rate/4
# 2) the other is to receive it as query parameter /movie/<string:_id>/rate?rating=4
@pages.get("/movie/<string:_id>/rate")
def rate_movie(_id):
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one(
        {"_id": _id}, {"$set": {"rating": rating}}
    )  # we use _id to find the record and $set :{what to change}
    return redirect(url_for(".movie", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    #! passed variables from the templates that are not parameters are query values
    print(request.args.get("query_test"))

    # all endpoints have to return something
    return redirect(request.args.get("current_page"))
