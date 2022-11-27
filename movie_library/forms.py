from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
    PasswordField,
)
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

# flask-wtf protect us from CSRF attacks
class MovieForm(FlaskForm):
    title = StringField("Titoru", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
    year = IntegerField(
        "Year",
        validators=[
            InputRequired(),
            NumberRange(min=1878, message="Please enter a year in the format YYYY"),
        ],
    )
    submit = SubmitField("Add Movie")


# the order of the validators matter from more generic to more specific is recommended

# * the textarea TextAreaField return one long string be default
# * here we want to extend the TextAreaField, we want a textarea where each line is going to be one element of our list
class StringListField(TextAreaField):
    # we are going to modify 2 methods
    def _value(self):  #! this recreates the single string with multiple lines
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:  # [0] is the content of the text area
            #! we converting the content of the textarea into a list of strings splitted into lines
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []
            # https://www.w3schools.com/python/ref_string_strip.asp
            # https://www.w3schools.com/python/ref_string_split.asp


# now we are going to create a ExtendedMovieForm for our MovieForm using our extended TextAreaField
class ExtendedMovieForm(MovieForm):
    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video link")

    submit = SubmitField("Submit")


#! register form with flaskform wtforms
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=4,
                max=20,
                message="Your password must be between 4 and 20 characters long.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo(  # equal to compares this field with another
                "password",  # its a string with the same name as the password variable previously defined
                message="This password did not match the one in the password field",
            ),
        ],
    )
    submit = SubmitField("Register")


#! login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")



