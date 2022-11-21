from dataclasses import dataclass, field
from datetime import datetime

# by default python when using dataclass will define a __init__ and __repr__ using the values defined it will allow comparison between objects and things like that

# there is technical reason using el default factory instead of just []
# having default values makes those properties optional the ones with just the definition like _id:str are required


@dataclass
class Movie:
    _id: str
    title: str
    director: str
    year: int
    cast: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    last_watched: datetime = None
    rating: int = 0  # default value
    tags: list[str] = field(default_factory=list)
    description: str = None
    video_link: str = None


# ! let's create a dataclass for the user
@dataclass
class User:
    _id: str
    email: str
    password: str
    movies: list[str] = field(
        default_factory=list
    )  # this track the movies x user watched
