import uuid
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    url_for,
)
from movie_library.forms import MovieForm  #! flask-wtf usage
from movie_library.models import Movie  #! @dataclass usage
from dataclasses import asdict  #! to pass a dataclass class as dictionary to mongo

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    return render_template("index.html", title="Movies Watchlist")


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
