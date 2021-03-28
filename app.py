# cd "C:\Users\Owner\AppData\Local\Programs\Python\Python38-32\fortune500app"

# Import Packages
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pandas as pd
from flask_sitemap import Sitemap


# Setup App
app = Flask(__name__)
ext = Sitemap(app=app)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'


# Get Data
## Companies
data = pd.read_excel("Company Data.xlsx", sheet_name="Companies")
data.index.name = None
data = data.fillna("")[["Company","Rank","S&P 500","Website","Diversity Page"]]
data = data.loc[data.Company != ""]

## Report Links
data_links = pd.read_excel("Company Data.xlsx", sheet_name="Reports")
data_links = data_links.loc[(data_links.Company != "") & (data_links.Company.isna() != True)][["Company", "Year", "Status", "EEO Data Report Link"]]
reports_ct = str(len(data_links))
data_links = data_links.pivot(index='Company', columns='Year', values='EEO Data Report Link').fillna("")

## Combine Data
data = data.merge(data_links, left_on='Company', right_index=True)
data.loc[data['Rank'] == '',"Rank"] = 99999
data['Rank'] = data['Rank'].astype('int')
data.loc[data['Rank'] == 99999,"Rank"] = ''

# Calculate Numbers
reports = str(data['Company'].nunique())
sp500 = str((data.value_counts('S&P 500')['Y'] / 500) *100)


# Start App
@app.route('/')
def index():
    return render_template('index.html', 
    						data=data,
                            reports=reports, 
                            sp500=sp500, 
                            reports_ct=reports_ct) 

@ext.register_generator
def index():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'index', {}

    
if __name__ == "__main__":
    app.run(host="0.0.0.0")


