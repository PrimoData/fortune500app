from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pandas as pd


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'

data = pd.read_excel("Fortune500_2020_Final.xlsx")
data.index.name = None


@app.route('/')
def index():
    return render_template('index.html', data=data, data_table=data.to_html(classes='table')) 


if __name__ == "__main__":
    app.run(debug=True)


