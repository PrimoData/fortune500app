# cd "C:\Users\Owner\AppData\Local\Programs\Python\Python38-32\fortune500app"

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pandas as pd
from flask_sitemap import Sitemap



app = Flask(__name__)
ext = Sitemap(app=app)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'

data = pd.read_excel("Fortune500_2020_Final.xlsx")
data['Rank'] = data['Rank'].fillna(99999).astype("int").astype("str").replace("99999","n/a")
data.index.name = None
detailed_data = pd.read_excel("static/eeo_cleaned.xlsx")

reports = str(int(data['EEO Data Report'].value_counts().sum() - data['EEO Data Report'].value_counts()['N']))
fortune500 = str(int(data.loc[(data['Rank'] != 'n/a') & (data["EEO Data Report"] != 'N'),"EEO Data Report"].value_counts().sum())/500*100)[0:3]
employees = str("{:,}".format(detailed_data["count"].sum()))

@app.route('/')
def index():
    return render_template('index.html', data=data, data_table=data.to_html(classes='table'),
                            reports=reports, fortune500=fortune500, employees=employees) 

@ext.register_generator
def index():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'index', {}

    
if __name__ == "__main__":
    app.run(host="0.0.0.0")


