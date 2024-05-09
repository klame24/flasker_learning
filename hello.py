from flask import Flask, render_template


# CREATE A FLASK INSTANCE

app = Flask(__name__)


@app.route("/")
def index():
    text = "This is bold text"
    favourite_pizza = ["Pepperoni", "Cheese", "Mashrooms", 41]
    return render_template('index.html', text=text, favourite_pizza=favourite_pizza)


@app.route("/users/<name>")
def user(name):
    return render_template('user.html', name=name)

#CREATE CUSTOM ERROR PAGE

#INVALID URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
