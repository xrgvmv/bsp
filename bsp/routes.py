from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    #return "Witaj na mojej stronie Flask!"
    return render_template('index.html')