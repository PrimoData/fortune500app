# cd "C:\Users\Owner\AppData\Local\Programs\Python\Python38-32\fortune500app"

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pandas as pd


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'

data = pd.read_excel("Fortune500_2020_Final.xlsx")
data.index.name = None

reports = str((1 - data['Diversity Report Title'].value_counts(normalize=True)['N'])*100) + '%'
leaders = str((1 - data['Diversity Leader'].value_counts(normalize=True)['N'])*100) + '%'
pages = str((1 - data['Landing Page'].value_counts(normalize=True)['N'])*100) + '%'

@app.route('/')
def index():
    return render_template('index.html', data=data, data_table=data.to_html(classes='table'),
                            reports=reports, leaders=leaders, pages=pages) 


if __name__ == "__main__":
    app.run(host="0.0.0.0")


