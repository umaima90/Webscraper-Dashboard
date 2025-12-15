import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = [book.h3.a["title"] for book in soup.select(".product_pod")]
prices = [price.text for price in soup.select(".price_color")]

df = pd.DataFrame({"Titles" : titles, "Prices": prices})
# Clean up the Prices column
df["Prices"] = df["Prices"].str.replace("Â£", "")   # remove weird Â£ symbol
df["Prices"] = df["Prices"].str.replace("£", "")    # remove pound sign
df["Prices"] = df["Prices"].astype(float)           # convert to numeric

print(df.head())



import dash 
from dash import dcc, html
import plotly.express as px

fig = px.bar(df, x="Titles", y="Prices", title="Book Prices")
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Books Dashboard"),
    dcc.Graph(figure = fig)
])

if __name__ == "__main__":
    print("Starting dashboard at http://127.0.0.1:8050/")
    app.run(debug=True)