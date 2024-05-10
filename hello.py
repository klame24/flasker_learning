from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# CREATE A FLASK INSTANCE
app = Flask(__name__)
# ADD DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# SECRET KEY
app.config['SECRET_KEY'] = "password"
# INITIALIZE THE DATABASE
db = SQLAlchemy(app)

#CREATE MODEL
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r' % self.name


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    submit = SubmitField("Submit")



class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/name", methods=['GET', 'POST'])
def create_form():
    name = None
    form = NamerForm()
    # VALIDATE FORM ?
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template('name.html', name=name, form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/users/<name>")
def user(name):
    return render_template('user.html', name=name)


# CREATE CUSTOM ERROR PAGE
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# INVALID URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# CREATE A FORM CLASS





if __name__ == '__main__':
    app.run(debug=True)
