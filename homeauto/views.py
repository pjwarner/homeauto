from homeauto import app
from flask import redirect, render_template, request, url_for

@app.route('/')
def index():
        return render_template('index.jade')
