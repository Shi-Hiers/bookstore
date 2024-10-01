from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/services')
def services():
    return render_template('services.html')  # Render the services page

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact page